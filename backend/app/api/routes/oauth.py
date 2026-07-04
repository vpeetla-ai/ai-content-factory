"""OAuth connect (authorize redirect) and callback routes for platform token storage."""

from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.redis import get_redis
from app.core.redis_keys import OAUTH_STATE
from app.core.security import get_current_user
from app.models import User
from app.services.oauth_tokens import (
    build_linkedin_authorize_url,
    build_x_authorize_url,
    exchange_linkedin_code,
    exchange_x_code,
    fetch_linkedin_person_id,
    generate_pkce_pair,
)
import secrets

router = APIRouter(prefix="/oauth", tags=["OAuth"])

OAUTH_STATE_TTL_SECONDS = 600


async def _store_oauth_state(user_id: str, platform: str, code_verifier: str | None) -> str:
    state = secrets.token_urlsafe(32)
    redis = get_redis()
    payload = {"user_id": user_id, "platform": platform}
    if code_verifier:
        payload["code_verifier"] = code_verifier
    await redis.set(OAUTH_STATE.format(state=state), json.dumps(payload), ex=OAUTH_STATE_TTL_SECONDS)
    return state


async def _consume_oauth_state(state: str, platform: str) -> dict:
    redis = get_redis()
    key = OAUTH_STATE.format(state=state)
    raw = await redis.get(key)
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OAuth state")
    await redis.delete(key)
    payload = json.loads(raw)
    if payload.get("platform") != platform:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OAuth state platform mismatch")
    return payload


@router.get("/linkedin/authorize")
async def linkedin_authorize(user: Annotated[User, Depends(get_current_user)]):
    settings = get_settings()
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/linkedin/callback"
    state = await _store_oauth_state(str(user.id), "linkedin", code_verifier=None)
    try:
        authorize_url = build_linkedin_authorize_url(redirect_uri, state)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return {"authorize_url": authorize_url}


@router.get("/x/authorize")
async def x_authorize(user: Annotated[User, Depends(get_current_user)]):
    settings = get_settings()
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/x/callback"
    code_verifier, code_challenge = generate_pkce_pair()
    state = await _store_oauth_state(str(user.id), "x", code_verifier=code_verifier)
    try:
        authorize_url = build_x_authorize_url(redirect_uri, state, code_challenge)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return {"authorize_url": authorize_url}


@router.get("/linkedin/callback")
async def linkedin_callback(
    code: Annotated[str, Query(...)],
    state: Annotated[str, Query(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    settings = get_settings()
    state_data = await _consume_oauth_state(state, "linkedin")
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/linkedin/callback"
    try:
        token_payload = await exchange_linkedin_code(code, redirect_uri)
        person_id = await fetch_linkedin_person_id(token_payload["access_token"])
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    result = await db.execute(select(User).where(User.id == state_data["user_id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    tokens = dict(user.platform_tokens or {})
    tokens["linkedin"] = {
        "access_token": token_payload.get("access_token"),
        "expires_in": token_payload.get("expires_in"),
        "person_id": person_id,
    }
    user.platform_tokens = tokens
    await db.flush()
    return RedirectResponse(url=f"{settings.frontend_url.rstrip('/')}/?connected=linkedin")


@router.get("/x/callback")
async def x_callback(
    code: Annotated[str, Query(...)],
    state: Annotated[str, Query(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    settings = get_settings()
    state_data = await _consume_oauth_state(state, "x")
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/x/callback"
    try:
        token_payload = await exchange_x_code(code, redirect_uri, state_data["code_verifier"])
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    result = await db.execute(select(User).where(User.id == state_data["user_id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    tokens = dict(user.platform_tokens or {})
    tokens["x"] = {
        "access_token": token_payload.get("access_token"),
        "token_type": token_payload.get("token_type"),
        "expires_in": token_payload.get("expires_in"),
    }
    user.platform_tokens = tokens
    await db.flush()
    return RedirectResponse(url=f"{settings.frontend_url.rstrip('/')}/?connected=x")


@router.get("/status")
async def oauth_status(user: Annotated[User, Depends(get_current_user)]):
    tokens = user.platform_tokens or {}
    return {"connected": list(tokens.keys())}
