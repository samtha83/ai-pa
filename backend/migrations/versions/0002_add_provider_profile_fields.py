"""add provider profile fields

Revision ID: 0002_provider_profile
Revises: 0001_provider_sessions
Create Date: 2026-09-29
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0002_provider_profile"
down_revision: str | None = "0001_provider_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("providers", sa.Column("tone", sa.String(length=80), nullable=True))
    op.add_column("providers", sa.Column("modality", sa.String(length=100), nullable=True))
    op.add_column("providers", sa.Column("service_type", sa.String(length=100), nullable=True))
    op.add_column("providers", sa.Column("template_settings", sa.JSON(), nullable=True))
    op.add_column("providers", sa.Column("boundaries", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("providers", "boundaries")
    op.drop_column("providers", "template_settings")
    op.drop_column("providers", "service_type")
    op.drop_column("providers", "modality")
    op.drop_column("providers", "tone")