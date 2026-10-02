"""add provider preferences

Revision ID: 0003_provider_preferences
Revises: 0002_provider_profile
Create Date: 2026-10-01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0003_provider_preferences"
down_revision: str | None = "0002_provider_profile"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "provider_preferences",
        sa.Column("provider_id", sa.String(length=64), nullable=False),
        sa.Column("working_hours", sa.JSON(), nullable=False),
        sa.Column("session_duration", sa.Integer(), nullable=False),
        sa.Column("buffer_time", sa.Integer(), nullable=False),
        sa.Column("blackout_dates", sa.JSON(), nullable=False),
        sa.Column("max_sessions_per_day", sa.Integer(), nullable=False),
        sa.Column("summary_template", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("provider_id"),
    )


def downgrade() -> None:
    op.drop_table("provider_preferences")