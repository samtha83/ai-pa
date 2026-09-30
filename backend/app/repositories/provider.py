from collections.abc import Mapping

from sqlalchemy.orm import Session

from app.models import Provider


class ProviderRepository:
    _PROFILE_FIELDS = {
        "name",
        "business_name",
        "timezone",
        "tone",
        "modality",
        "service_type",
        "template_settings",
        "boundaries",
    }

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_profile(self, provider_id: str) -> Provider | None:
        return self.session.get(Provider, provider_id)

    def update_profile(
        self, provider_id: str, values: Mapping[str, object]
    ) -> Provider | None:
        provider = self.get_profile(provider_id)
        if provider is None:
            return None

        for field, value in values.items():
            if field not in self._PROFILE_FIELDS:
                raise ValueError(f"Unsupported provider profile field: {field}")
            setattr(provider, field, value)

        if values:
            self.session.commit()
            self.session.refresh(provider)
        return provider