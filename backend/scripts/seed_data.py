import os
from typing import Iterable

from sqlalchemy import select

from app.core.config import get_settings
from app.core.db.base import Base
from app.core.db.session import get_engine, get_session_factory
from app.domain.models import AuthToken, Membership, Organization, User


DEV_TOKEN_ENV = "SAMU_DEV_TOKEN"
DEFAULT_TOKEN_VALUE = "dev-token"
REQUEST_ID = "seed-script"


def _ensure_user(session, email: str, display_name: str) -> User:
    existing = session.scalar(select(User).where(User.email == email))
    if existing:
        return existing
    user = User(email=email, display_name=display_name, is_active=True, request_id=REQUEST_ID)
    session.add(user)
    session.flush()
    user.created_by = user.id
    user.updated_by = user.id
    return user


def _ensure_org(session, name: str, actor_id) -> Organization:
    existing = session.scalar(select(Organization).where(Organization.name == name))
    if existing:
        return existing
    organization = Organization(name=name, is_active=True, created_by=actor_id, updated_by=actor_id, request_id=REQUEST_ID)
    session.add(organization)
    session.flush()
    return organization


def _ensure_membership(session, user: User, organization: Organization, role: str) -> Membership:
    membership = session.scalar(
        select(Membership).where(Membership.user_id == user.id, Membership.org_id == organization.id)
    )
    if membership:
        return membership
    membership = Membership(
        user_id=user.id,
        org_id=organization.id,
        role=role,
        created_by=user.id,
        updated_by=user.id,
        request_id=REQUEST_ID,
    )
    session.add(membership)
    session.flush()
    return membership


def _ensure_token(session, user: User, org: Organization, token_value: str) -> AuthToken:
    existing = session.scalar(select(AuthToken).where(AuthToken.token == token_value))
    if existing:
        return existing
    token = AuthToken(
        token=token_value,
        user_id=user.id,
        default_org_id=org.id,
        is_active=True,
        created_by=user.id,
        updated_by=user.id,
        request_id=REQUEST_ID,
    )
    session.add(token)
    session.flush()
    return token


def seed_local() -> None:
    settings = get_settings()
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    session_factory = get_session_factory()
    token_value = os.getenv(DEV_TOKEN_ENV, DEFAULT_TOKEN_VALUE)

    with session_factory() as session:
        user = _ensure_user(session, "dev@samu.local", "Dev User")
        primary_org = _ensure_org(session, "Acme Delivery", actor_id=user.id)
        backup_org = _ensure_org(session, "Beacon Ops", actor_id=user.id)
        _ensure_membership(session, user, primary_org, role="owner")
        _ensure_membership(session, user, backup_org, role="member")
        _ensure_token(session, user, primary_org, token_value)
        session.commit()

    print("Seed complete.")
    print(f"Environment: {settings.environment}")
    print(f"User: dev@samu.local")
    print(f"Token: {token_value}")
    print(f"Organizations: {['Acme Delivery', 'Beacon Ops']}")


if __name__ == "__main__":
    seed_local()
