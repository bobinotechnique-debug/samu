import os
from importlib import reload

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
TEST_REDIS_URL = "redis://localhost:6379/0"


def _configure_environment() -> None:
    os.environ["SAMU_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["SAMU_REDIS_URL"] = TEST_REDIS_URL
    os.environ["SAMU_TESTING"] = "true"
    os.environ["SAMU_ENVIRONMENT"] = "ci"


_configure_environment()

import pytest
from fastapi.testclient import TestClient

import app.core.config as config
from app.core.db.base import Base
from app.core.db.session import get_engine, get_session_factory, reset_engine_cache
from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    _configure_environment()
    reset_engine_cache()
    config.get_settings.cache_clear()
    reload(config)
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app = create_app()
    return TestClient(app)


@pytest.fixture
def session_factory(client: TestClient):  # noqa: ARG001
    return get_session_factory()
