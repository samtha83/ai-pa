from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.auth.dependencies import get_current_provider
from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models import Provider
from app.schemas import ProviderPreferencesUpdate


@pytest.fixture
def preferences_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Provider(id="preferences-provider", name="Preference Provider"))
        session.commit()

    def override_db_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_current_provider] = lambda: {
        "provider_id": "preferences-provider"
    }
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_preferences_api_creates_defaults_and_persists_provider_update(
    preferences_client: TestClient,
):
    client = preferences_client

    defaults_response = client.get("/api/v1/providers/me/preferences")
    assert defaults_response.status_code == 200
    defaults = defaults_response.json()
    assert defaults["provider_id"] == "preferences-provider"
    assert defaults["session_duration"] == 50
    assert defaults["buffer_time"] == 10
    assert defaults["max_sessions_per_day"] == 8
    assert defaults["summary_template"] == "standard"
    assert defaults["working_hours"]["monday"] == {
        "start": "09:00:00",
        "end": "17:00:00",
    }

    payload = {
        "working_hours": {"tuesday": {"start": "10:00", "end": "16:30"}},
        "session_duration": 45,
        "buffer_time": 15,
        "blackout_dates": ["2026-12-25"],
        "max_sessions_per_day": 6,
        "summary_template": "concise",
    }
    update_response = client.put("/api/v1/providers/me/preferences", json=payload)
    assert update_response.status_code == 200
    assert update_response.json()["working_hours"]["tuesday"] == {
        "start": "10:00:00",
        "end": "16:30:00",
    }
    assert update_response.json()["blackout_dates"] == ["2026-12-25"]

    read_response = client.get("/api/v1/providers/me/preferences")
    assert read_response.json()["session_duration"] == 45
    assert read_response.json()["summary_template"] == "concise"

def test_preferences_api_rejects_invalid_schedule_and_values(
    preferences_client: TestClient,
):
    response = preferences_client.put(
        "/api/v1/providers/me/preferences",
        json={
            "working_hours": {"monday": {"start": "17:00", "end": "09:00"}},
            "session_duration": 5,
            "buffer_time": -1,
            "blackout_dates": ["not-a-date"],
            "max_sessions_per_day": 0,
            "summary_template": "unknown",
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"

    request_with_provider_override = preferences_client.put(
        "/api/v1/providers/me/preferences",
        json={
            "provider_id": "some-other-provider",
            "working_hours": {},
            "session_duration": 50,
            "buffer_time": 10,
            "blackout_dates": [],
            "max_sessions_per_day": 8,
            "summary_template": "standard",
        },
    )
    assert request_with_provider_override.status_code == 422


def test_preferences_api_rejects_offset_aware_working_hours(
    preferences_client: TestClient,
):
    response = preferences_client.put(
        "/api/v1/providers/me/preferences",
        json={
            "working_hours": {"monday": {"start": "09:00+01:00", "end": "17:00"}},
            "session_duration": 50,
            "buffer_time": 10,
            "blackout_dates": [],
            "max_sessions_per_day": 8,
            "summary_template": "standard",
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_preferences_api_requires_authentication():
    response = TestClient(app).get("/api/v1/providers/me/preferences")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_preferences_update_schema_rejects_duplicate_blackout_dates():
    with pytest.raises(ValueError, match="Blackout dates must be unique"):
        ProviderPreferencesUpdate(
            working_hours={"monday": {"start": "09:00", "end": "17:00"}},
            session_duration=50,
            buffer_time=10,
            blackout_dates=["2026-12-25", "2026-12-25"],
            max_sessions_per_day=8,
            summary_template="standard",
        )


def test_preferences_update_schema_requires_a_working_day():
    with pytest.raises(ValueError, match="At least one working-hours day"):
        ProviderPreferencesUpdate(
            working_hours={},
            session_duration=50,
            buffer_time=10,
            blackout_dates=[],
            max_sessions_per_day=8,
            summary_template="standard",
        )