from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import Client, Provider


def test_client_model_persists_with_provider_ownership():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        provider = Provider(id="provider-a", name="Provider A", timezone="UTC")
        session.add(provider)
        session.flush()

        client = Client(
            provider_id=provider.id,
            name="Morgan Lee",
            email="morgan@example.com",
            phone="+1-555-0100",
            timezone="America/New_York",
            service_type="consultation",
            goals=["Improve sleep"],
        )
        session.add(client)
        session.commit()

        saved_client = session.scalar(select(Client).where(Client.id == client.id))
        assert saved_client is not None
        assert saved_client.id
        assert saved_client.provider_id == provider.id
        assert saved_client.name == "Morgan Lee"
        assert saved_client.goals == ["Improve sleep"]
        assert saved_client.status == "active"

    engine.dispose()