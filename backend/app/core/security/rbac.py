from app.core.errors import ForbiddenError
from app.core.security.auth import AuthContext


class Permission:
    ORG_READ = "org:read"
    ORG_WRITE = "org:write"
    PROJECT_READ = "project:read"
    PROJECT_WRITE = "project:write"


def enforce_permission(context: AuthContext, permission: str) -> None:
    if context.scopes is not None and permission not in context.scopes:
        raise ForbiddenError("Permission denied")
