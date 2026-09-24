from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app


def test_health_endpoint_returns_ok():
    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "ai-pa-backend"
    assert "version" in payload


def test_unknown_route_returns_structured_error():
    client = TestClient(app)
    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "not_found"
    assert "message" in payload["error"]
    assert "correlation_id" in payload["error"]


def test_readiness_returns_database_status():
    response = TestClient(app).get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}


def test_readiness_reports_database_failure(monkeypatch):
    def unavailable_database():
        raise OperationalError("SELECT 1", {}, Exception("database unavailable"))

    monkeypatch.setattr("app.api.v1.health.check_database_connection", unavailable_database)

    response = TestClient(app).get("/api/v1/ready")

    assert response.status_code == 503
    assert response.json()["error"]["message"] == "Database is not ready."
