import pytest
from pydantic import ValidationError

from app.schemas import ClientCreate, ClientRead, ClientUpdate


def test_client_create_schema_normalizes_and_defaults_fields():
    client = ClientCreate(name="  Morgan Lee  ", goals=["  Improve sleep  "])

    assert client.name == "Morgan Lee"
    assert client.goals == ["Improve sleep"]
    assert client.timezone == "UTC"
    assert client.status == "active"


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   "},
        {"name": "Morgan", "timezone": "Mars/Olympus"},
        {"name": "Morgan", "provider_id": "provider-b"},
        {"name": "Morgan", "status": "pending"},
    ],
)
def test_client_create_schema_rejects_invalid_values(payload: dict[str, object]):
    with pytest.raises(ValidationError):
        ClientCreate(**payload)


def test_client_update_schema_rejects_blank_required_values():
    with pytest.raises(ValidationError):
        ClientUpdate(name="   ")

    with pytest.raises(ValidationError):
        ClientUpdate(timezone="Mars/Olympus")

    with pytest.raises(ValidationError):
        ClientUpdate(status=None)


def test_client_read_schema_exposes_persisted_record():
    from datetime import datetime, timezone

    client = ClientRead(
        id="client-1",
        provider_id="provider-a",
        name="Morgan Lee",
        email=None,
        phone=None,
        timezone="UTC",
        service_type=None,
        goals=[],
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    assert client.provider_id == "provider-a"