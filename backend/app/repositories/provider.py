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

    def create(self, provider_id: str, values: Mapping[str, object]) -> Provider:
        unsupported_fields = values.keys() - self._PROFILE_FIELDS
        if unsupported_fields:
            field = next(iter(unsupported_fields))
            raise ValueError(f"Unsupported provider profile field: {field}")

        provider = Provider(id=provider_id, **values)
        self.session.add(provider)
        self.session.commit()
        self.session.refresh(provider)
        return provider

    def update_profile(
        self, provider_id: str, values: Mapping[str, object]
    ) -> Provider | None:
        provider = self.get_profile(provider_id)
        if provider is None:
            return None

        unsupported_fields = values.keys() - self._PROFILE_FIELDS
        if unsupported_fields:
            field = next(iter(unsupported_fields))
            raise ValueError(f"Unsupported provider profile field: {field}")

        for field, value in values.items():
            setattr(provider, field, value)

        if values:
            self.session.commit()
            self.session.refresh(provider)
        return provider