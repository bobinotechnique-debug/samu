from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base


class AuditFields:
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.utcnow
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)


class User(Base, AuditFields):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    memberships: Mapped[list[Membership]] = relationship("Membership", back_populates="user")
    tokens: Mapped[list[AuthToken]] = relationship("AuthToken", back_populates="user")


class Organization(Base, AuditFields):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    memberships: Mapped[list[Membership]] = relationship("Membership", back_populates="organization")


class Membership(Base, AuditFields):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("user_id", "org_id", name="uq_membership_user_org"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member")

    user: Mapped[User] = relationship("User", back_populates="memberships")
    organization: Mapped[Organization] = relationship("Organization", back_populates="memberships")


class AuthToken(Base, AuditFields):
    __tablename__ = "auth_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    default_org_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped[User] = relationship("User", back_populates="tokens")
    default_org: Mapped[Organization | None] = relationship("Organization")
