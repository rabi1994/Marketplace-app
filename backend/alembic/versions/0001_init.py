"""init schema

Revision ID: 0001
Revises:
Create Date: 2025-12-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from backend.domain.entities import LeadStatus, PlanType

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("phone", sa.String()),
        sa.Column("phone_verified", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name_i18n", postgresql.JSONB(), nullable=False),
    )
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name_i18n", postgresql.JSONB(), nullable=False),
    )
    op.create_table(
        "areas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("cities.id")),
        sa.Column("name_i18n", postgresql.JSONB(), nullable=False),
    )
    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("bio_i18n", postgresql.JSONB(), nullable=False),
        sa.Column("avatar_url", sa.String()),
        sa.Column("verified", sa.Boolean(), default=False),
        sa.Column("languages", postgresql.ARRAY(sa.String())),
        sa.Column("category_ids", postgresql.ARRAY(sa.Integer())),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("cities.id")),
        sa.Column("area_ids", postgresql.ARRAY(sa.Integer())),
        sa.Column("pricing_hint", sa.String()),
        sa.Column("availability", sa.String()),
        sa.Column("whatsapp", sa.String()),
        sa.Column("phone", sa.String()),
        sa.Column("rating", sa.Float(), default=0.0),
        sa.Column("rating_count", sa.Integer(), default=0),
    )
    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id")),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("cities.id")),
        sa.Column("area_ids", postgresql.ARRAY(sa.Integer())),
        sa.Column("description", sa.Text()),
        sa.Column("preferred_time", sa.String()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "lead_deliveries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("lead_id", sa.Integer(), sa.ForeignKey("leads.id")),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id")),
        sa.Column("status", sa.Enum(LeadStatus)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("lead_delivery_id", sa.Integer(), sa.ForeignKey("lead_deliveries.id")),
        sa.Column("rating", sa.Integer()),
        sa.Column("comment", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "plans",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String()),
        sa.Column("plan_type", sa.Enum(PlanType)),
        sa.Column("monthly_credits", sa.Integer()),
        sa.Column("price", sa.Float()),
        sa.Column("features", postgresql.ARRAY(sa.String())),
    )
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id")),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("plans.id")),
        sa.Column("credits", sa.Integer()),
        sa.Column("active", sa.Boolean(), default=True),
        sa.Column("expires_at", sa.DateTime()),
    )
    op.create_table(
        "contact_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id")),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("lead_id", sa.Integer(), sa.ForeignKey("leads.id"), nullable=True),
        sa.Column("token", sa.String(), unique=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("contact_events")
    op.drop_table("subscriptions")
    op.drop_table("plans")
    op.drop_table("reviews")
    op.drop_table("lead_deliveries")
    op.drop_table("leads")
    op.drop_table("providers")
    op.drop_table("areas")
    op.drop_table("cities")
    op.drop_table("categories")
    op.drop_table("users")
