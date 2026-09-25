from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_provider
from app.auth.service import (
    SESSION_COOKIE_NAME,
    create_provider_session,
    get_provider_identity,
    revoke_session,
    resolve_provider_from_session,
)
from app.db.seed import DEMO_PROVIDER_ID, ensure_demo_provider

router = APIRouter()


class LoginRequest(BaseModel):
    provider_id: str = Field(default=DEMO_PROVIDER_ID, min_length=1)


@router.post("/auth/login")
def login(payload: LoginRequest, response: Response) -> dict[str, object]:
    ensure_demo_provider()
    token = create_provider_session(payload.provider_id)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )

    provider = get_provider_identity(payload.provider_id)
    return {
        "provider_id": payload.provider_id,
        "provider": provider,
        "status": "logged_in",
    }


@router.post("/auth/logout")
def logout(request: Request, response: Response) -> dict[str, str]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    revoke_session(token)
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return {"status": "logged_out"}


@router.get("/auth/me")
def me(request: Request) -> dict[str, object]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    provider_id = resolve_provider_from_session(token)
    if provider_id is None:
        raise HTTPException(status_code=401, detail="Authentication required.")

    provider = get_provider_identity(provider_id)
    return {"provider_id": provider_id, "provider": provider}


@router.get("/auth/protected")
def protected(request: Request) -> dict[str, str]:
    current_provider = get_current_provider(request)
    return {"provider_id": current_provider["provider_id"]}
