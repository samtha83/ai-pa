import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.seed import DEMO_PROVIDER_ID, ensure_demo_provider
from app.db.session import get_session_factory
from app.models import DemoSession

SESSION_COOKIE_NAME = "ai_pa_session"
SESSION_TTL = timedelta(hours=8)


def create_provider_session(provider_id: str = DEMO_PROVIDER_ID) -> str:
    ensure_demo_provider()
    session_factory = get_session_factory()
    session_token = uuid.uuid4().hex
    expires_at = datetime.now(timezone.utc) + SESSION_TTL

    with session_factory() as session:
        session.add(
            DemoSession(
                id=session_token,
                provider_id=provider_id,
                expires_at=expires_at,
            )
        )
        session.commit()

    return session_token


def revoke_session(token: str | None) -> None:
    if not token:
        return

    with get_session_factory()() as session:
        db_session = session.scalar(select(DemoSession).where(DemoSession.id == token))
        if db_session is not None and db_session.revoked_at is None:
            db_session.revoked_at = datetime.now(timezone.utc)
            session.commit()


def resolve_provider_from_session(token: str | None) -> str | None:
    if not token:
        return None

    now = datetime.now(timezone.utc)
    with get_session_factory()() as session:
        db_session = session.scalar(
            select(DemoSession).where(
                DemoSession.id == token,
                DemoSession.revoked_at.is_(None),
                DemoSession.expires_at > now,
            )
        )
        if db_session is None:
            return None
        return db_session.provider_id


def get_provider_identity(provider_id: str) -> dict[str, str]:
    provider = ensure_demo_provider()
    return {
        "id": provider.id,
        "name": provider.name,
        "business_name": provider.business_name or "Demo Provider",
    }
