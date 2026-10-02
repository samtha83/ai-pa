from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_provider
from app.db.session import get_db_session
from app.schemas import ProviderPreferencesRead, ProviderPreferencesUpdate
from app.services import get_provider_preferences, update_provider_preferences


router = APIRouter()


@router.get("/providers/me/preferences", response_model=ProviderPreferencesRead)
def read_preferences(
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ProviderPreferencesRead:
    preferences = get_provider_preferences(session, current_provider["provider_id"])
    if preferences is None:
        raise HTTPException(status_code=404, detail="Provider not found.")
    return ProviderPreferencesRead.model_validate(preferences)


@router.put("/providers/me/preferences", response_model=ProviderPreferencesRead)
def write_preferences(
    payload: ProviderPreferencesUpdate,
    current_provider: dict[str, str] = Depends(get_current_provider),
    session: Session = Depends(get_db_session),
) -> ProviderPreferencesRead:
    preferences = update_provider_preferences(
        session, current_provider["provider_id"], payload
    )
    if preferences is None:
        raise HTTPException(status_code=404, detail="Provider not found.")
    return ProviderPreferencesRead.model_validate(preferences)