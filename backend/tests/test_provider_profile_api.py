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


@pytest.fixture
def provider_profile_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(
            [
                Provider(id="profile-provider-a", name="Provider A", timezone="UTC"),
                Provider(id="profile-provider-b", name="Provider B", timezone="UTC"),
            ]
        )
        session.commit()

    def override_db_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_current_provider] = lambda: {
        "provider_id": "profile-provider-a"
    }
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_provider_profile_api_reads_and_updates_current_provider(
    provider_profile_client: TestClient,
):
    response = provider_profile_client.get("/api/v1/providers/me")
    assert response.status_code == 200
    assert response.json()["name"] == "Provider A"

    response = provider_profile_client.patch(
        "/api/v1/providers/me",
        json={
            "name": "Updated Provider",
            "business_name": "Updated Practice",
            "timezone": "America/Chicago",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Provider"
    assert response.json()["business_name"] == "Updated Practice"
    assert response.json()["timezone"] == "America/Chicago"

    app.dependency_overrides[get_current_provider] = lambda: {
        "provider_id": "profile-provider-b"
    }
    other_provider = provider_profile_client.get("/api/v1/providers/me")
    assert other_provider.json()["name"] == "Provider B"


def test_provider_profile_api_rejects_invalid_updates(
    provider_profile_client: TestClient,
):
    response = provider_profile_client.patch(
        "/api/v1/providers/me", json={"timezone": "Mars/Olympus"}
    )
    assert response.status_code == 422

    response = provider_profile_client.patch(
        "/api/v1/providers/me", json={"name": None}
    )
    assert response.status_code == 422
