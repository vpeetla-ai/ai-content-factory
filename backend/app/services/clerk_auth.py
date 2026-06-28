"""Clerk JWT verification for production auth."""

from __future__ import annotations

import time
from typing import Any

import httpx
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_jwks_cache: dict[str, Any] = {"keys": None, "fetched_at": 0.0}
_JWKS_TTL_SECONDS = 3600


async def _fetch_jwks() -> dict:
    settings = get_settings()
    now = time.time()
    if _jwks_cache["keys"] and (now - _jwks_cache["fetched_at"]) < _JWKS_TTL_SECONDS:
        return _jwks_cache["keys"]

    if not settings.clerk_jwks_url:
        raise ValueError("CLERK_JWKS_URL is not configured")

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(settings.clerk_jwks_url)
        resp.raise_for_status()
        data = resp.json()

    _jwks_cache["keys"] = data
    _jwks_cache["fetched_at"] = now
    return data


def _get_signing_key(jwks: dict, kid: str | None) -> dict | None:
    for key in jwks.get("keys", []):
        if kid is None or key.get("kid") == kid:
            return key
    return None


async def verify_clerk_token(token: str) -> dict[str, Any]:
    """Verify Clerk session JWT and return claims."""
    settings = get_settings()
    if not settings.clerk_configured:
        raise ValueError("Clerk is not configured")

    jwks = await _fetch_jwks()
    header = jwt.get_unverified_header(token)
    signing_key = _get_signing_key(jwks, header.get("kid"))
    if not signing_key:
        raise ValueError("Unable to find matching JWKS key")

    try:
        claims = jwt.decode(
            token,
            signing_key,
            algorithms=[header.get("alg", "RS256")],
            options={"verify_aud": False},
        )
        return claims
    except JWTError as exc:
        logger.warning("clerk_jwt_invalid", error=str(exc))
        raise ValueError("Invalid Clerk token") from exc


def extract_clerk_identity(claims: dict[str, Any]) -> tuple[str, str | None, str | None]:
    """Return (email, clerk_id, name) from Clerk JWT claims."""
    clerk_id = claims.get("sub")
    email = (
        claims.get("email")
        or claims.get("primary_email_address")
        or (claims.get("email_addresses") or [{}])[0].get("email_address")
    )
    name = claims.get("name") or claims.get("first_name") or (email.split("@")[0] if email else "user")
    if not email and clerk_id:
        email = f"{clerk_id}@clerk.user"
    if not email:
        raise ValueError("Clerk token missing email claim")
    return email, clerk_id, name
