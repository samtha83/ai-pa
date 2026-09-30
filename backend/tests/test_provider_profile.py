import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Provider
from app.schemas import ProviderProfileRead, ProviderProfileUpdate
from app.services import get_provider_profile, update_provider_profile


def test_provider_profile_update_persists_only_for_requested_provider():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(
            [
                Provider(id="provider-a", name="Provider A", timezone="UTC"),
                Provider(id="provider-b", name="Provider B", timezone="UTC"),
            ]
        )
        session.commit()

        updated = update_provider_profile(
            session,
            "provider-a",
            ProviderProfileUpdate(
                name="Provider A Updated",
                timezone="America/New_York",
                tone="warm and concise",
                modality="in-person",
                service_type="consultation",
                template_settings={"summary": "brief"},
                boundaries={"after_hours": False},
            ),
        )

        assert updated is not None
        assert updated.name == "Provider A Updated"
        assert updated.timezone == "America/New_York"
        assert updated.template_settings == {"summary": "brief"}
        assert get_provider_profile(session, "provider-b").name == "Provider B"
        assert get_provider_profile(session, "missing-provider") is None

        response = ProviderProfileRead.model_validate(updated)
        assert response.id == "provider-a"
        assert response.boundaries == {"after_hours": False}

    engine.dispose()


def test_provider_profile_schema_rejects_invalid_values():
    with pytest.raises(ValidationError):
        ProviderProfileUpdate(timezone="Mars/Olympus")

    with pytest.raises(ValidationError):
        ProviderProfileUpdate(name="   ")

    with pytest.raises(ValidationError):
        ProviderProfileUpdate(name=None)

    with pytest.raises(ValidationError):
        ProviderProfileUpdate(real_person_ssn="not-accepted")