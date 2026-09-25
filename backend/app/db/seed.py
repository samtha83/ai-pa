from datetime import datetime, timezone

from sqlalchemy import select

from app.db.session import get_session_factory
from app.models import Provider

DEMO_PROVIDER_ID = "demo-provider"
DEMO_PROVIDER_NAME = "Demo Provider"


def ensure_demo_provider() -> Provider:
    session_factory = get_session_factory()
    with session_factory() as session:
        provider = session.scalar(select(Provider).where(Provider.id == DEMO_PROVIDER_ID))
        if provider is None:
            provider = Provider(
                id=DEMO_PROVIDER_ID,
                name=DEMO_PROVIDER_NAME,
                business_name="Local development provider",
                timezone="UTC",
            )
            session.add(provider)
            session.commit()
            session.refresh(provider)

        return provider


def get_demo_provider() -> Provider:
    return ensure_demo_provider()
