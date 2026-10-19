from sqlalchemy.orm import Session

from app.models import Client
from app.repositories import ClientRepository
from app.schemas import ClientCreate, ClientUpdate


def create_client(
    session: Session, provider_id: str, payload: ClientCreate
) -> Client | None:
    return ClientRepository(session).create(
        provider_id, payload.model_dump(mode="json")
    )


def list_clients(session: Session, provider_id: str) -> list[Client]:
    return ClientRepository(session).list_for_provider(provider_id)


def get_client(session: Session, provider_id: str, client_id: str) -> Client | None:
    return ClientRepository(session).get(provider_id, client_id)


def update_client(
    session: Session, provider_id: str, client_id: str, payload: ClientUpdate
) -> Client | None:
    return ClientRepository(session).update(
        provider_id, client_id, payload.model_dump(exclude_unset=True)
    )