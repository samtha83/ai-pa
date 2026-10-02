from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_name: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    tone: Mapped[str | None] = mapped_column(String(80))
    modality: Mapped[str | None] = mapped_column(String(100))
    service_type: Mapped[str | None] = mapped_column(String(100))
    template_settings: Mapped[dict[str, object] | None] = mapped_column(JSON)
    boundaries: Mapped[dict[str, object] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    sessions: Mapped[list["DemoSession"]] = relationship(back_populates="provider")
    preferences: Mapped["ProviderPreferences | None"] = relationship(
        back_populates="provider", cascade="all, delete-orphan", uselist=False
    )


class ProviderPreferences(Base):
    __tablename__ = "provider_preferences"

    provider_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("providers.id", ondelete="CASCADE"), primary_key=True
    )
    working_hours: Mapped[dict[str, dict[str, str]]] = mapped_column(JSON, nullable=False)
    session_duration: Mapped[int] = mapped_column(nullable=False, default=50)
    buffer_time: Mapped[int] = mapped_column(nullable=False, default=10)
    blackout_dates: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    max_sessions_per_day: Mapped[int] = mapped_column(nullable=False, default=8)
    summary_template: Mapped[str] = mapped_column(
        String(80), nullable=False, default="standard"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    provider: Mapped[Provider] = relationship(back_populates="preferences")


class DemoSession(Base):
    __tablename__ = "demo_sessions"
    __table_args__ = (
        Index("ix_demo_sessions_provider_id", "provider_id"),
        Index("ix_demo_sessions_expires_at", "expires_at"),
    )

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    provider_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("providers.id", ondelete="CASCADE"), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    provider: Mapped[Provider] = relationship(back_populates="sessions")