"""Auth & User REST routes — Clerk JWT → internal JWT."""

from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.core.security import create_access_token, get_current_user
from app.models import InviteCode, User, UserRole
from app.schemas import TokenRequest, TokenResponse, UserProfileResponse
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
    try:
        email: str
        clerk_id: str | None = None
        name: str | None = None

        if settings.clerk_configured or settings.clerk_secret_key:
            claims = await verify_clerk_token(body.clerk_token)
            email, clerk_id, name = await extract_clerk_identity(claims)
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
            if settings.require_invite_code:
                code = (body.invite_code or "").strip()
                if not code:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="An invite code is required to sign up",
                    )
                invite_result = await db.execute(select(InviteCode).where(InviteCode.code == code))
                invite = invite_result.scalar_one_or_none()
                if not invite or invite.uses_count >= invite.max_uses:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid or fully-used invite code",
                    )
                invite.uses_count += 1

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
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("auth_database_error")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable — check DATABASE_URL and migrations on Render",
        ) from exc
    except Exception as exc:
        logger.exception("clerk_token_exchange_failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        ) from exc


@users_router.get("/me", response_model=UserProfileResponse)
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role.value,
        quotas={"pipelines_per_day": 50, "tokens_per_month": 1_000_000},
    )



# Platform connect/status now lives under /oauth (see api/routes/oauth.py) — that flow
# generates a real CSRF state + PKCE pair server-side, which this old endpoint never did,
# and never returns raw access tokens to the client.
