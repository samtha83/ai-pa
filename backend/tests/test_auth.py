from fastapi.testclient import TestClient

from app.db.seed import ensure_demo_provider
from app.main import app


def test_demo_auth_login_me_and_logout_flow():
    ensure_demo_provider()
    client = TestClient(app)

    login_response = client.post(
        "/api/v1/auth/login",
        json={"provider_id": "demo-provider"},
    )

    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["provider_id"] == "demo-provider"
    assert payload["provider"]["name"] == "Demo Provider"

    me_response = client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["provider_id"] == "demo-provider"

    protected_response = client.get("/api/v1/auth/protected")
    assert protected_response.status_code == 200
    assert protected_response.json()["provider_id"] == "demo-provider"

    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["status"] == "logged_out"

    unauthenticated_me = client.get("/api/v1/auth/me")
    assert unauthenticated_me.status_code == 401


def test_demo_auth_requires_valid_session():
    ensure_demo_provider()
    client = TestClient(app)

    response = client.get("/api/v1/auth/protected")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"
