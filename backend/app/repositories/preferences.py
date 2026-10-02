from collections.abc import Mapping

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Provider, ProviderPreferences


DEFAULT_WORKING_HOURS = {
    day: {"start": "09:00:00", "end": "17:00:00"}
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday")
}


class ProviderPreferencesRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_or_create(self, provider_id: str) -> ProviderPreferences | None:
        provider = self.session.get(Provider, provider_id)
        if provider is None:
            return None

        preferences = self.session.scalar(
            select(ProviderPreferences).where(
                ProviderPreferences.provider_id == provider_id
            )
        )
        if preferences is None:
            preferences = ProviderPreferences(
                provider_id=provider_id,
                working_hours=DEFAULT_WORKING_HOURS,
                session_duration=50,
                buffer_time=10,
                blackout_dates=[],
                max_sessions_per_day=8,
                summary_template="standard",
            )
            self.session.add(preferences)
            self.session.commit()
            self.session.refresh(preferences)
        return preferences

    def update(
        self, provider_id: str, values: Mapping[str, object]
    ) -> ProviderPreferences | None:
        preferences = self.get_or_create(provider_id)
        if preferences is None:
            return None

        for field, value in values.items():
            if field not in {
                "working_hours",
                "session_duration",
                "buffer_time",
                "blackout_dates",
                "max_sessions_per_day",
                "summary_template",
            }:
                raise ValueError(f"Unsupported provider preference field: {field}")
            setattr(preferences, field, value)

        self.session.commit()
        self.session.refresh(preferences)
        return preferences