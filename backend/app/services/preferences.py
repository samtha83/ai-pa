from sqlalchemy.orm import Session

from app.models import ProviderPreferences
from app.repositories import ProviderPreferencesRepository
from app.schemas import ProviderPreferencesUpdate


def get_provider_preferences(
    session: Session, provider_id: str
) -> ProviderPreferences | None:
    return ProviderPreferencesRepository(session).get_or_create(provider_id)


def update_provider_preferences(
    session: Session,
    provider_id: str,
    preferences: ProviderPreferencesUpdate,
) -> ProviderPreferences | None:
    values = preferences.model_dump(mode="json")
    return ProviderPreferencesRepository(session).update(provider_id, values)