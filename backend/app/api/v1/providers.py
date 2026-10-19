from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_provider
from app.db.session import get_db_session
from app.schemas import ProviderProfileRead, ProviderProfileUpdate
from app.services import get_provider_profile, update_provider_profile


router = APIRouter()


@router.get("/providers/me", response_model=ProviderProfileRead)
def read_provider_profile(
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ProviderProfileRead:
    profile = get_provider_profile(session, current_provider["provider_id"])
    if profile is None:
        raise HTTPException(status_code=404, detail="Provider not found.")
    return ProviderProfileRead.model_validate(profile)


@router.patch("/providers/me", response_model=ProviderProfileRead)
def write_provider_profile(
    payload: ProviderProfileUpdate,
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ProviderProfileRead:
    profile = update_provider_profile(
        session, current_provider["provider_id"], payload
    )
    if profile is None:
        raise HTTPException(status_code=404, detail="Provider not found.")
    return ProviderProfileRead.model_validate(profile)
