from sqlalchemy.orm import Session

from app.models import Provider
from app.repositories import ProviderRepository
from app.schemas import ProviderProfileUpdate


def get_provider_profile(session: Session, provider_id: str) -> Provider | None:
    return ProviderRepository(session).get_profile(provider_id)


def update_provider_profile(
    session: Session, provider_id: str, profile: ProviderProfileUpdate
) -> Provider | None:
    return ProviderRepository(session).update_profile(
        provider_id, profile.model_dump(exclude_unset=True)
    )