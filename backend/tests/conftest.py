import os
import sys
import uuid
from collections.abc import Callable, Generator
from importlib import reload
from pathlib import Path

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
TEST_REDIS_URL = "redis://localhost:6379/0"


def _configure_environment() -> None:
    os.environ["SAMU_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["SAMU_REDIS_URL"] = TEST_REDIS_URL
    os.environ["SAMU_TESTING"] = "true"
    os.environ["SAMU_ENVIRONMENT"] = "ci"


_configure_environment()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

import app.core.config as config
from app.api.context import attach_principal, get_request_context
from app.api.deps import get_current_auth_context, get_principal_context
from app.core.db.base import Base
from app.core.db.session import get_engine, get_session_factory, reset_engine_cache
from app.core.ids import OrgId, UserId
from app.core.security.auth import PrincipalContext
from app.main import create_app


def _reset_state() -> None:
    _configure_environment()
    reset_engine_cache()
    config.get_settings.cache_clear()
    reload(config)


def _prepare_schema() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def app() -> FastAPI:
    _reset_state()
    _prepare_schema()
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def session_factory(app: FastAPI) -> sessionmaker[Session]:  # noqa: ARG001
    return get_session_factory()


@pytest.fixture
def db_session(session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def fake_auth_context(app: FastAPI) -> Callable[..., PrincipalContext]:
    def _parse_uuid(value: str | uuid.UUID | None) -> uuid.UUID:
        if value is None:
            return uuid.uuid4()
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))

    overrides = app.dependency_overrides

    def _create_principal(
        user_id: str | uuid.UUID | None = None,
        org_id: str | uuid.UUID | None = None,
        roles: list[str] | None = None,
        permissions: set[str] | None = None,
        token_id: str | None = None,
    ) -> PrincipalContext:
        user_uuid = _parse_uuid(user_id)
        org_uuid = _parse_uuid(org_id)
        principal = PrincipalContext(
            user_id=UserId(user_uuid),
            org_id=OrgId(org_uuid),
            roles=roles or ["owner"],
            permissions=permissions
            or {"org:read", "org:write", "membership:read", "membership:write"},
            token_id=token_id or "test-token",
        )

        request_context = get_request_context()
        attach_principal(
            request_context,
            actor_id=str(principal.user_id),
            org_id=str(principal.org_id),
            token_id=principal.token_id,
        )

        overrides[get_principal_context] = lambda: principal
        overrides[get_current_auth_context] = lambda: principal
        return principal

    yield _create_principal
    overrides.pop(get_principal_context, None)
    overrides.pop(get_current_auth_context, None)
