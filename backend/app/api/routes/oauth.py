"""OAuth callback routes for platform token storage."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services.oauth_tokens import exchange_linkedin_code, exchange_x_code

router = APIRouter(prefix="/oauth", tags=["OAuth"])


@router.get("/linkedin/callback")
async def linkedin_callback(
    code: Annotated[str, Query(...)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    settings = get_settings()
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/linkedin/callback"
    try:
        token_payload = await exchange_linkedin_code(code, redirect_uri)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    tokens = dict(user.platform_tokens or {})
    tokens["linkedin"] = {
        "access_token": token_payload.get("access_token"),
        "expires_in": token_payload.get("expires_in"),
    }
    user.platform_tokens = tokens
    await db.flush()
    return {"platform": "linkedin", "status": "connected"}


@router.get("/x/callback")
async def x_callback(
    code: Annotated[str, Query(...)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    settings = get_settings()
    redirect_uri = f"{settings.api_base_url.rstrip('/')}/oauth/x/callback"
    try:
        token_payload = await exchange_x_code(code, redirect_uri)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    tokens = dict(user.platform_tokens or {})
    tokens["x"] = {
        "access_token": token_payload.get("access_token"),
        "token_type": token_payload.get("token_type"),
        "expires_in": token_payload.get("expires_in"),
    }
    user.platform_tokens = tokens
    await db.flush()
    return {"platform": "x", "status": "connected"}


@router.get("/status/{user_id}")
async def oauth_status(user_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    tokens = user.platform_tokens or {}
    return {"connected": list(tokens.keys())}
