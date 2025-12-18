from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Header, HTTPException, status

from app.core.errors import UnauthorizedError
from app.core.ids import OrgId, UserId, parse_uuid


@dataclass
class AuthContext:
    subject_id: UserId
    org_id: OrgId
    roles: list[str]
    token_id: Optional[str] = None
    scopes: list[str] | None = None


class AuthTokenParser:
    @staticmethod
    def parse_header(authorization: str | None) -> AuthContext:
        if not authorization:
            raise UnauthorizedError("Missing Authorization header")
        try:
            scheme, token = authorization.split(" ", 1)
        except ValueError as exc:
            raise UnauthorizedError("Invalid Authorization header") from exc
        if scheme.lower() != "bearer":
            raise UnauthorizedError("Unsupported auth scheme")
        parts = token.split(":")
        if len(parts) < 2:
            raise UnauthorizedError("Invalid token payload")
        org_part, subject_part = parts[0], parts[1]
        org_id = OrgId(parse_uuid(org_part))
        subject_id = UserId(parse_uuid(subject_part))
        scopes = parts[2].split(",") if len(parts) > 2 and parts[2] else []
        token_id = parts[3] if len(parts) > 3 else None
        return AuthContext(subject_id=subject_id, org_id=org_id, roles=[], token_id=token_id, scopes=scopes)


def get_auth_context(authorization: str | None = Header(default=None)) -> AuthContext:
    try:
        return AuthTokenParser.parse_header(authorization)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message, headers={"WWW-Authenticate": "Bearer"})
