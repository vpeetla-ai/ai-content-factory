"""Auth & User REST routes — /api/v1/auth, /api/v1/users"""

from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.models import User, UserRole
from app.schemas import PlatformConnectRequest, TokenRequest, TokenResponse, UserProfileResponse

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/users", tags=["Users"])


@auth_router.post("/token", response_model=TokenResponse)
async def exchange_token(
    body: TokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Exchange Clerk token → JWT.

    Dev mode: accepts any token string as email identifier.
    Production: verify Clerk JWT via clerk_secret_key.
    """
    email = body.clerk_token if "@" in body.clerk_token else f"{body.clerk_token}@dev.local"

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(id=uuid4(), email=email, name=email.split("@")[0], role=UserRole.editor)
        db.add(user)
        await db.flush()

    token = create_access_token(user.id, user.email, user.role.value)
    return TokenResponse(access_token=token, expires_in=3600)


@users_router.get("/me", response_model=UserProfileResponse)
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role.value,
        quotas={"pipelines_per_day": 50, "tokens_per_month": 1_000_000},
    )


@users_router.post("/platforms/connect")
async def connect_platform(
    body: PlatformConnectRequest,
    user: Annotated[User, Depends(get_current_user)],
):
  """Initiate OAuth2 flow for social platform."""
  return {
      "platform": body.platform.value,
      "oauth_url": f"https://oauth.example.com/{body.platform.value}?user={user.id}",
      "status": "pending",
  }


@users_router.get("/platforms")
async def list_platforms(user: Annotated[User, Depends(get_current_user)]):
    tokens = user.platform_tokens or {}
    return {"connected": list(tokens.keys()), "platforms": tokens}
