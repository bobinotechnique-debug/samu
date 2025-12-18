from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.context import attach_principal, get_request_context
from app.core.errors import ForbiddenError, NotFoundError, UnauthorizedError, ValidationError
from app.core.ids import OrgId, UserId, parse_uuid
from app.domain.models import AuthToken, Membership, Organization, User


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "owner": {"org:read", "org:write", "membership:read", "membership:write"},
    "admin": {"org:read", "org:write", "membership:read", "membership:write"},
    "member": {"org:read", "membership:read"},
}


@dataclass
class PrincipalContext:
    user_id: UserId
    org_id: OrgId
    roles: list[str]
    permissions: set[str]
    token_id: str | None = None


def _parse_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise UnauthorizedError("Missing Authorization header")
    try:
        scheme, token = authorization.split(" ", 1)
    except ValueError as exc:
        raise UnauthorizedError("Invalid Authorization header") from exc
    if scheme.lower() != "bearer":
        raise UnauthorizedError("Unsupported auth scheme")
    if not token:
        raise UnauthorizedError("Missing token")
    return token


def _map_roles_to_permissions(roles: Iterable[str]) -> set[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, set()))
    return permissions


def resolve_principal(session: Session, authorization: str | None, requested_org_id: str | None) -> PrincipalContext:
    token_value = _parse_bearer_token(authorization)
    token = session.scalar(select(AuthToken).where(AuthToken.token == token_value, AuthToken.is_active.is_(True)))
    if not token:
        raise UnauthorizedError("Invalid or inactive token")

    user: User | None = session.get(User, token.user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("User is not active")

    org_identifier = requested_org_id or (str(token.default_org_id) if token.default_org_id else None)
    if not org_identifier:
        raise ValidationError("Organization context is required", details={"field": "X-Org-ID"})
    try:
        org_uuid = parse_uuid(org_identifier)
    except ValueError as exc:
        raise ValidationError("Invalid organization identifier", details={"org_id": org_identifier}) from exc

    organization: Organization | None = session.get(Organization, org_uuid)
    if not organization:
        raise NotFoundError("organization", org_identifier)
    if not organization.is_active:
        raise ForbiddenError("Organization is not active")

    membership: Membership | None = session.scalar(
        select(Membership).where(Membership.org_id == organization.id, Membership.user_id == user.id)
    )
    if not membership:
        raise ForbiddenError("User is not a member of this organization")

    roles = [membership.role]
    permissions = _map_roles_to_permissions(roles)
    principal = PrincipalContext(
        user_id=UserId(user.id),
        org_id=OrgId(organization.id),
        roles=roles,
        permissions=permissions,
        token_id=str(token.id),
    )

    request_context = get_request_context()
    attach_principal(
        request_context,
        actor_id=str(user.id),
        org_id=str(organization.id),
        token_id=str(token.id),
    )
    return principal
