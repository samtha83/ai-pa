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
from app.models import Client, Provider


@pytest.fixture
def clients_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(
            [
                Provider(id="client-provider-a", name="Provider A"),
                Provider(id="client-provider-b", name="Provider B"),
            ]
        )
        session.commit()
        session.add(
            Client(
                id="client-b-private",
                provider_id="client-provider-b",
                name="Private Client",
            )
        )
        session.commit()

    def override_db_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_current_provider] = lambda: {
        "provider_id": "client-provider-a"
    }
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_client_api_creates_lists_reads_and_updates_own_clients(
    clients_client: TestClient,
):
    response = clients_client.post(
        "/api/v1/clients",
        json={
            "name": "Morgan Lee",
            "email": "morgan@example.com",
            "timezone": "America/New_York",
            "service_type": "consultation",
            "goals": ["Improve sleep"],
        },
    )
    assert response.status_code == 201
    created = response.json()
    assert created["provider_id"] == "client-provider-a"
    assert created["name"] == "Morgan Lee"
    assert created["goals"] == ["Improve sleep"]

    client_id = created["id"]
    assert clients_client.get("/api/v1/clients").json()[0]["id"] == client_id
    assert clients_client.get(f"/api/v1/clients/{client_id}").status_code == 200

    update_response = clients_client.patch(
        f"/api/v1/clients/{client_id}", json={"status": "inactive"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "inactive"


def test_client_api_rejects_invalid_payload_and_provider_override(
    clients_client: TestClient,
):
    blank_name = clients_client.post("/api/v1/clients", json={"name": "   "})
    assert blank_name.status_code == 422

    provider_override = clients_client.post(
        "/api/v1/clients",
        json={"name": "Morgan Lee", "provider_id": "client-provider-b"},
    )
    assert provider_override.status_code == 422


def test_client_api_rejects_null_status_update(clients_client: TestClient):
    created = clients_client.post(
        "/api/v1/clients", json={"name": "Morgan Lee"}
    ).json()

    response = clients_client.patch(
        f"/api/v1/clients/{created['id']}", json={"status": None}
    )

    assert response.status_code == 422
    assert (
        clients_client.get(f"/api/v1/clients/{created['id']}").json()["status"]
        == "active"
    )


def test_client_api_hides_other_providers_clients(clients_client: TestClient):
    response = clients_client.get("/api/v1/clients/client-b-private")
    assert response.status_code == 404
    assert clients_client.get("/api/v1/clients").json() == []
    assert (
        clients_client.get("/api/v1/clients?provider_id=client-provider-b").json()
        == []
    )

    update_response = clients_client.patch(
        "/api/v1/clients/client-b-private",
        json={"name": "Unauthorized Update"},
    )
    assert update_response.status_code == 404

    app.dependency_overrides[get_current_provider] = lambda: {
        "provider_id": "client-provider-b"
    }
    private_client = clients_client.get("/api/v1/clients/client-b-private")
    assert private_client.status_code == 200
    assert private_client.json()["name"] == "Private Client"


def test_client_api_requires_authentication():
    response = TestClient(app).get("/api/v1/clients")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"