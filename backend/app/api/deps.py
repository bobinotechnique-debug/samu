from collections.abc import Generator

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import ForbiddenError
from app.core.feature_flags import FeatureFlagService, get_cached_feature_flag_service
from app.core.db.session import db_session
from app.core.security.auth import PrincipalContext, resolve_principal


def get_app_settings() -> Settings:
    return get_settings()


def get_db_session(_: Settings = Depends(get_app_settings)) -> Generator[Session, None, None]:
    with db_session() as session:
        yield session


def get_principal_context(
    session: Session = Depends(get_db_session),
    authorization: str | None = Header(default=None),
    org_header: str | None = Header(default=None, alias="X-Org-ID"),
) -> PrincipalContext:
    return resolve_principal(session=session, authorization=authorization, requested_org_id=org_header)


def require_permission(permission: str):
    def dependency(principal: PrincipalContext = Depends(get_principal_context)) -> PrincipalContext:
        if permission not in principal.permissions:
            raise ForbiddenError(f"Missing permission: {permission}")
        return principal

    return dependency


def get_current_auth_context(principal: PrincipalContext = Depends(get_principal_context)) -> PrincipalContext:
    return principal


def get_feature_flag_service(settings: Settings = Depends(get_app_settings)) -> FeatureFlagService:
    return get_cached_feature_flag_service(settings.environment)
