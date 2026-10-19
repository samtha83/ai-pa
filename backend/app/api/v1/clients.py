from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_provider
from app.db.session import get_db_session
from app.schemas import ClientCreate, ClientRead, ClientUpdate
from app.services import create_client, get_client, list_clients, update_client


router = APIRouter()


@router.get("/clients", response_model=list[ClientRead])
def read_clients(
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> list[ClientRead]:
    clients = list_clients(session, current_provider["provider_id"])
    return [ClientRead.model_validate(client) for client in clients]


@router.post(
    "/clients", response_model=ClientRead, status_code=status.HTTP_201_CREATED
)
def create_client_record(
    payload: ClientCreate,
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ClientRead:
    client = create_client(session, current_provider["provider_id"], payload)
    if client is None:
        raise HTTPException(status_code=404, detail="Provider not found.")
    return ClientRead.model_validate(client)


@router.get("/clients/{client_id}", response_model=ClientRead)
def read_client(
    client_id: str,
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ClientRead:
    client = get_client(session, current_provider["provider_id"], client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found.")
    return ClientRead.model_validate(client)


@router.patch("/clients/{client_id}", response_model=ClientRead)
def update_client_record(
    client_id: str,
    payload: ClientUpdate,
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ClientRead:
    client = update_client(
        session, current_provider["provider_id"], client_id, payload
    )
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found.")
    return ClientRead.model_validate(client)