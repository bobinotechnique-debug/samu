"""initial auth and organization tables"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
    )

    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
    )

    op.create_table(
        "memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="member"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.UniqueConstraint("user_id", "org_id", name="uq_membership_user_org"),
    )

    op.create_table(
        "auth_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("default_org_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("organizations.id"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.UniqueConstraint("token", name="uq_auth_token_value"),
    )


def downgrade() -> None:
    op.drop_table("auth_tokens")
    op.drop_table("memberships")
    op.drop_table("organizations")
    op.drop_table("users")
