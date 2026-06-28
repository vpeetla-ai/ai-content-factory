"""Auth & User REST routes — Clerk JWT → internal JWT."""

from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.core.security import create_access_token, get_current_user
from app.models import User, UserRole
from app.schemas import PlatformConnectRequest, TokenRequest, TokenResponse, UserProfileResponse
from app.services.clerk_auth import extract_clerk_identity, verify_clerk_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
users_router = APIRouter(prefix="/users", tags=["Users"])
logger = get_logger(__name__)


@auth_router.post("/token", response_model=TokenResponse)
async def exchange_token(
    body: TokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Exchange Clerk session JWT → internal API JWT."""
    settings = get_settings()
    email: str
    clerk_id: str | None = None
    name: str | None = None

    if settings.clerk_configured:
        try:
            claims = await verify_clerk_token(body.clerk_token)
            email, clerk_id, name = extract_clerk_identity(claims)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    elif settings.allow_dev_auth and settings.is_development:
        email = body.clerk_token if "@" in body.clerk_token else f"{body.clerk_token}@dev.local"
        name = email.split("@")[0]
        logger.info("dev_auth_bypass", email=email)
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Clerk authentication is required but not configured",
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            id=uuid4(),
            email=email,
            name=name or email.split("@")[0],
            clerk_id=clerk_id,
            role=UserRole.editor,
        )
        db.add(user)
        await db.flush()
    elif clerk_id and not user.clerk_id:
        user.clerk_id = clerk_id
        if name:
            user.name = name

    token = create_access_token(user.id, user.email, user.role.value)
    return TokenResponse(access_token=token, expires_in=settings.jwt_expire_minutes * 60)


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
    settings = get_settings()
    platform = body.platform.value
    oauth_urls = {
        "linkedin": f"https://www.linkedin.com/oauth/v2/authorization?client_id={settings.linkedin_client_id}&redirect_uri={settings.frontend_url}/oauth/linkedin&response_type=code&scope=w_member_social",
        "x": f"https://twitter.com/i/oauth2/authorize?client_id={settings.x_api_key}&redirect_uri={settings.frontend_url}/oauth/x&response_type=code&scope=tweet.read+tweet.write",
    }
    oauth_url = oauth_urls.get(platform, f"{settings.frontend_url}/settings/platforms?connect={platform}")
    return {"platform": platform, "oauth_url": oauth_url, "status": "pending"}


@users_router.get("/platforms")
async def list_platforms(user: Annotated[User, Depends(get_current_user)]):
    tokens = user.platform_tokens or {}
    return {"connected": list(tokens.keys()), "platforms": tokens}
