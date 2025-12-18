from datetime import datetime
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.context import get_request_context
from app.api.deps import get_db_session, require_permission
from app.core.errors import ForbiddenError, NotFoundError, ValidationError
from app.core.security.auth import PrincipalContext
from app.domain.models import Membership, Organization, User

router = APIRouter()


class OrgSummary(BaseModel):
    id: str
    name: str
    is_active: bool
    role: str


class OrgDetail(OrgSummary):
    created_at: datetime
    created_by: str | None
    updated_at: datetime | None = None
    updated_by: str | None = None
    request_id: str | None = None


class CreateOrgRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class MembershipSummary(BaseModel):
    id: str
    user_id: str
    org_id: str
    role: str
    created_at: datetime
    created_by: str | None


class CreateMembershipRequest(BaseModel):
    user_id: str
    role: str = Field(default="member", min_length=1, max_length=50)


def _apply_audit_fields(record, principal: PrincipalContext) -> None:
    context = get_request_context()
    record.created_by = principal.user_id
    record.updated_by = principal.user_id
    record.request_id = context.request_id


def _ensure_same_org(path_org_id: str, principal: PrincipalContext) -> None:
    if str(principal.org_id) != path_org_id:
        raise ForbiddenError("Organization context mismatch")


@router.get("/me", response_model=OrgDetail)
def get_active_org(
    principal: PrincipalContext = Depends(require_permission("org:read")),
    session: Session = Depends(get_db_session),
) -> OrgDetail:
    organization: Organization | None = session.get(Organization, principal.org_id)
    if not organization:
        raise NotFoundError("organization", str(principal.org_id))
    membership: Membership | None = session.scalar(
        select(Membership).where(Membership.org_id == principal.org_id, Membership.user_id == principal.user_id)
    )
    role = membership.role if membership else "member"
    return OrgDetail(
        id=str(organization.id),
        name=organization.name,
        is_active=organization.is_active,
        role=role,
        created_at=organization.created_at,
        created_by=str(organization.created_by) if organization.created_by else None,
        updated_at=organization.updated_at,
        updated_by=str(organization.updated_by) if organization.updated_by else None,
        request_id=organization.request_id,
    )


@router.get("/", response_model=list[OrgSummary])
def list_orgs(
    principal: PrincipalContext = Depends(require_permission("org:read")),
    session: Session = Depends(get_db_session),
) -> list[OrgSummary]:
    memberships = session.scalars(select(Membership).where(Membership.user_id == principal.user_id)).all()
    if not memberships:
        return []

    org_ids = [membership.org_id for membership in memberships]
    organizations = session.scalars(select(Organization).where(Organization.id.in_(org_ids))).all()
    org_by_id = {org.id: org for org in organizations}
    summaries: list[OrgSummary] = []
    for membership in memberships:
        organization = org_by_id.get(membership.org_id)
        if organization:
            summaries.append(
                OrgSummary(
                    id=str(organization.id),
                    name=organization.name,
                    is_active=organization.is_active,
                    role=membership.role,
                )
            )
    return summaries


@router.post("/", response_model=OrgDetail, status_code=201)
def create_org(
    payload: CreateOrgRequest,
    principal: PrincipalContext = Depends(require_permission("org:write")),
    session: Session = Depends(get_db_session),
) -> OrgDetail:
    organization = Organization(name=payload.name, is_active=True)
    _apply_audit_fields(organization, principal)
    session.add(organization)
    session.flush()

    membership = Membership(user_id=principal.user_id, org_id=organization.id, role="owner")
    _apply_audit_fields(membership, principal)
    session.add(membership)
    session.commit()
    session.refresh(organization)
    session.refresh(membership)

    return OrgDetail(
        id=str(organization.id),
        name=organization.name,
        is_active=organization.is_active,
        role=membership.role,
        created_at=organization.created_at,
        created_by=str(organization.created_by) if organization.created_by else None,
        updated_at=organization.updated_at,
        updated_by=str(organization.updated_by) if organization.updated_by else None,
        request_id=organization.request_id,
    )


@router.get("/{org_id}/memberships", response_model=list[MembershipSummary])
def list_memberships(
    org_id: str,
    principal: PrincipalContext = Depends(require_permission("membership:read")),
    session: Session = Depends(get_db_session),
) -> list[MembershipSummary]:
    _ensure_same_org(org_id, principal)
    organization = session.get(Organization, principal.org_id)
    if not organization:
        raise NotFoundError("organization", org_id)
    memberships = session.scalars(select(Membership).where(Membership.org_id == organization.id)).all()
    return [
        MembershipSummary(
            id=str(membership.id),
            user_id=str(membership.user_id),
            org_id=str(membership.org_id),
            role=membership.role,
            created_at=membership.created_at,
            created_by=str(membership.created_by) if membership.created_by else None,
        )
        for membership in memberships
    ]


@router.post("/{org_id}/memberships", response_model=MembershipSummary, status_code=201)
def add_membership(
    org_id: str,
    payload: CreateMembershipRequest,
    principal: PrincipalContext = Depends(require_permission("membership:write")),
    session: Session = Depends(get_db_session),
) -> MembershipSummary:
    _ensure_same_org(org_id, principal)
    organization = session.get(Organization, principal.org_id)
    if not organization:
        raise NotFoundError("organization", org_id)

    try:
        user_uuid = uuid.UUID(payload.user_id)
    except ValueError as exc:
        raise ValidationError("Invalid user identifier", details={"user_id": payload.user_id}) from exc

    user: User | None = session.get(User, user_uuid)
    if not user:
        raise NotFoundError("user", payload.user_id)
    existing = session.scalar(
        select(Membership).where(Membership.org_id == organization.id, Membership.user_id == user_uuid)
    )
    if existing:
        raise ValidationError("User is already a member of this organization")

    membership = Membership(user_id=user_uuid, org_id=organization.id, role=payload.role)
    _apply_audit_fields(membership, principal)
    session.add(membership)
    session.commit()
    session.refresh(membership)

    return MembershipSummary(
        id=str(membership.id),
        user_id=str(membership.user_id),
        org_id=str(membership.org_id),
        role=membership.role,
        created_at=membership.created_at,
        created_by=str(membership.created_by) if membership.created_by else None,
    )
