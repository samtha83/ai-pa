from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Provider
from app.repositories import (
    ClientRepository,
    ProviderPreferencesRepository,
    ProviderRepository,
)


@pytest.fixture
def repository_session() -> Generator[Session, None, None]:
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
        yield session
    engine.dispose()


def test_provider_repository_reads_and_updates_only_requested_provider(
    repository_session: Session,
):
    repository = ProviderRepository(repository_session)

    updated = repository.update_profile(
        "provider-a", {"name": "Updated Provider A", "tone": "warm"}
    )

    assert updated is not None
    assert updated.name == "Updated Provider A"
    assert updated.tone == "warm"
    assert repository.get_profile("provider-b").name == "Provider B"
    assert repository.get_profile("missing-provider") is None
    assert repository.update_profile("missing-provider", {"name": "Missing"}) is None


def test_provider_repository_creates_and_retrieves_provider(
    repository_session: Session,
):
    repository = ProviderRepository(repository_session)

    created = repository.create(
        "provider-c",
        {
            "name": "Provider C",
            "business_name": "Provider C Practice",
            "timezone": "America/Chicago",
        },
    )

    assert created.id == "provider-c"
    assert created.name == "Provider C"
    assert created.business_name == "Provider C Practice"
    assert created.timezone == "America/Chicago"
    assert repository.get_profile("provider-c") == created


def test_provider_repository_validates_all_fields_before_mutating(
    repository_session: Session,
):
    repository = ProviderRepository(repository_session)

    with pytest.raises(ValueError, match="Unsupported provider profile field"):
        repository.update_profile(
            "provider-a", {"name": "Should not persist", "unsupported": "value"}
        )

    repository_session.commit()
    assert repository.get_profile("provider-a").name == "Provider A"


def test_preferences_repository_creates_defaults_and_scopes_updates(
    repository_session: Session,
):
    repository = ProviderPreferencesRepository(repository_session)

    preferences = repository.get_or_create("provider-a")

    assert preferences is not None
    assert preferences.session_duration == 50
    assert preferences.buffer_time == 10
    assert repository.get_or_create("provider-a").provider_id == "provider-a"

    updated = repository.update("provider-a", {"session_duration": 45})
    assert updated is not None
    assert updated.session_duration == 45

    other_preferences = repository.get_or_create("provider-b")
    assert other_preferences is not None
    assert other_preferences.session_duration == 50
    assert repository.get_or_create("missing-provider") is None
    assert repository.update("missing-provider", {"session_duration": 30}) is None


def test_preferences_repository_validates_all_fields_before_mutating(
    repository_session: Session,
):
    repository = ProviderPreferencesRepository(repository_session)
    preferences = repository.get_or_create("provider-a")
    assert preferences is not None

    with pytest.raises(ValueError, match="Unsupported provider preference field"):
        repository.update(
            "provider-a", {"session_duration": 45, "unsupported": "value"}
        )

    repository_session.commit()
    assert repository.get_or_create("provider-a").session_duration == 50


def test_client_repository_crud_is_scoped_to_provider(repository_session: Session):
    repository = ClientRepository(repository_session)

    client = repository.create("provider-a", {"name": "Client A"})

    assert client is not None
    assert client.provider_id == "provider-a"
    assert repository.list_for_provider("provider-a") == [client]
    assert repository.list_for_provider("provider-b") == []
    assert repository.get("provider-a", client.id) == client
    assert repository.get("provider-b", client.id) is None

    updated = repository.update("provider-a", client.id, {"name": "Updated Client A"})
    assert updated is not None
    assert updated.name == "Updated Client A"
    assert repository.update("provider-b", client.id, {"name": "Unauthorized"}) is None
    assert repository.get("provider-a", client.id).name == "Updated Client A"
    assert repository.create("missing-provider", {"name": "Orphan"}) is None


def test_client_repository_validates_all_fields_before_mutating(
    repository_session: Session,
):
    repository = ClientRepository(repository_session)
    client = repository.create("provider-a", {"name": "Client A"})
    assert client is not None

    with pytest.raises(ValueError, match="Unsupported client field"):
        repository.update(
            "provider-a",
            client.id,
            {"name": "Should not persist", "unsupported": "value"},
        )

    repository_session.commit()
    assert repository.get("provider-a", client.id).name == "Client A"
