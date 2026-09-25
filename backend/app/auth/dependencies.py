from fastapi import HTTPException, Request

from app.auth.service import SESSION_COOKIE_NAME, resolve_provider_from_session


def get_current_provider(request: Request) -> dict[str, str]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    provider_id = resolve_provider_from_session(token)
    if provider_id is None:
        raise HTTPException(status_code=401, detail="Authentication required.")

    return {"provider_id": provider_id}
