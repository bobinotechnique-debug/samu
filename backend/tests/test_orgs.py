from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from app.domain.models import AuthToken, Membership, Organization, User

pytestmark = pytest.mark.skip(reason="Business endpoints are disabled during Phase 2 bootstrap skeleton.")


REQUEST_ID = "test-request"


def _create_user(session: Session, email: str, actor_id=None) -> User:
    user = User(
        email=email,
        display_name=email.split("@")[0],
        is_active=True,
        created_by=actor_id,
        updated_by=actor_id,
        request_id=REQUEST_ID,
    )
    session.add(user)
    session.flush()
    return user


def _create_org(session: Session, name: str, actor_id) -> Organization:
    organization = Organization(name=name, is_active=True, created_by=actor_id, updated_by=actor_id, request_id=REQUEST_ID)
    session.add(organization)
    session.flush()
    return organization


def _add_membership(session: Session, user: User, organization: Organization, role: str, actor_id) -> Membership:
    membership = Membership(
        user_id=user.id,
        org_id=organization.id,
        role=role,
        created_by=actor_id,
        updated_by=actor_id,
        request_id=REQUEST_ID,
    )
    session.add(membership)
    session.flush()
    return membership


def _issue_token(session: Session, user: User, default_org_id=None, actor_id=None, token_value: str | None = None) -> str:
    value = token_value or f"token-{uuid4()}"
    token = AuthToken(
        token=value,
        user_id=user.id,
        default_org_id=default_org_id,
        is_active=True,
        created_by=actor_id,
        updated_by=actor_id,
        request_id=REQUEST_ID,
    )
    session.add(token)
    session.flush()
    return value


def test_auth_required(client: TestClient):
    response = client.get("/api/v1/orgs")
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "unauthorized"


def test_org_context_required(client: TestClient, session_factory: sessionmaker[Session]):
    with session_factory() as session:
        user = _create_user(session, "user1@example.com")
        _issue_token(session, user, default_org_id=None, actor_id=user.id, token_value="token-no-org")
        session.commit()

    headers = {"Authorization": "Bearer token-no-org"}
    response = client.get("/api/v1/orgs", headers=headers)
    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "validation_error"


def test_rbac_forbidden(client: TestClient, session_factory: sessionmaker[Session]):
    with session_factory() as session:
        actor = _create_user(session, "owner@example.com")
        org = _create_org(session, "Org One", actor_id=actor.id)
        _add_membership(session, actor, org, role="member", actor_id=actor.id)
        invitee = _create_user(session, "invitee@example.com", actor_id=actor.id)
        token_value = _issue_token(session, actor, default_org_id=org.id, actor_id=actor.id, token_value="member-token")
        org_id = str(org.id)
        invitee_id = str(invitee.id)
        session.commit()

    headers = {"Authorization": f"Bearer {token_value}"}
    response = client.post(
        f"/api/v1/orgs/{org_id}/memberships",
        headers=headers,
        json={"user_id": invitee_id},
    )
    assert response.status_code == 403
    payload = response.json()
    assert payload["error"]["code"] == "forbidden"


def test_list_orgs_scoped(client: TestClient, session_factory: sessionmaker[Session]):
    with session_factory() as session:
        actor = _create_user(session, "scoped@example.com")
        org_one = _create_org(session, "Org One", actor_id=actor.id)
        _add_membership(session, actor, org_one, role="owner", actor_id=actor.id)
        other_org = _create_org(session, "Other Org", actor_id=actor.id)
        token_value = _issue_token(session, actor, default_org_id=org_one.id, actor_id=actor.id, token_value="scoped-token")
        org_one_id = str(org_one.id)
        other_org_id = str(other_org.id)
        session.commit()

    headers = {"Authorization": f"Bearer {token_value}"}
    response = client.get("/api/v1/orgs", headers=headers)
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == org_one_id
    assert payload[0]["role"] == "owner"
    assert all(item["id"] != other_org_id for item in payload)


def test_memberships_scoped(client: TestClient, session_factory: sessionmaker[Session]):
    with session_factory() as session:
        actor = _create_user(session, "actor@example.com")
        org_one = _create_org(session, "Org One", actor_id=actor.id)
        _add_membership(session, actor, org_one, role="owner", actor_id=actor.id)
        org_two = _create_org(session, "Org Two", actor_id=actor.id)
        outsider = _create_user(session, "outsider@example.com", actor_id=actor.id)
        _add_membership(session, outsider, org_two, role="member", actor_id=actor.id)
        token_value = _issue_token(session, actor, default_org_id=org_one.id, actor_id=actor.id, token_value="owner-token")
        org_two_id = str(org_two.id)
        session.commit()

    headers = {"Authorization": f"Bearer {token_value}", "X-Org-ID": org_two_id}
    response = client.get(f"/api/v1/orgs/{org_two_id}/memberships", headers=headers)
    assert response.status_code == 403
    payload = response.json()
    assert payload["error"]["code"] == "forbidden"


def test_error_model_shape_for_not_found(client: TestClient, session_factory: sessionmaker[Session]):
    missing_org_id = str(uuid4())
    with session_factory() as session:
        actor = _create_user(session, "notfound@example.com")
        token_value = _issue_token(session, actor, default_org_id=None, actor_id=actor.id, token_value="nf-token")
        session.commit()

    headers = {"Authorization": f"Bearer {token_value}", "X-Org-ID": missing_org_id}
    response = client.get(f"/api/v1/orgs/{missing_org_id}/memberships", headers=headers)
    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "not_found"
    assert payload["error"]["details"]["id"] == missing_org_id
