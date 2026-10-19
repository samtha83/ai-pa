from collections.abc import Mapping

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Client, Provider


class ClientRepository:
    _CLIENT_FIELDS = {
        "name",
        "email",
        "phone",
        "timezone",
        "service_type",
        "goals",
        "status",
    }

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, provider_id: str, values: Mapping[str, object]) -> Client | None:
        if self.session.get(Provider, provider_id) is None:
            return None

        client = Client(provider_id=provider_id, **values)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def list_for_provider(self, provider_id: str) -> list[Client]:
        statement = (
            select(Client)
            .where(Client.provider_id == provider_id)
            .order_by(Client.created_at, Client.id)
        )
        return list(self.session.scalars(statement))

    def get(self, provider_id: str, client_id: str) -> Client | None:
        statement = select(Client).where(
            Client.provider_id == provider_id,
            Client.id == client_id,
        )
        return self.session.scalar(statement)

    def update(
        self, provider_id: str, client_id: str, values: Mapping[str, object]
    ) -> Client | None:
        client = self.get(provider_id, client_id)
        if client is None:
            return None

        for field, value in values.items():
            if field not in self._CLIENT_FIELDS:
                raise ValueError(f"Unsupported client field: {field}")
            setattr(client, field, value)

        if values:
            self.session.commit()
            self.session.refresh(client)
        return client