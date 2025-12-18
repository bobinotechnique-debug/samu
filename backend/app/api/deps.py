from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.db.session import db_session
from app.core.security.auth import AuthContext, get_auth_context


def get_app_settings() -> Settings:
    return get_settings()


def get_db_session(_: Settings = Depends(get_app_settings)) -> Generator[Session, None, None]:
    with db_session() as session:
        yield session


def get_current_auth_context(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
    return auth
