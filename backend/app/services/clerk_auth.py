"""Clerk JWT verification for production auth."""

from __future__ import annotations

import time
from typing import Any

import httpx
from jose import JWTError, jwk, jwt

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_jwks_cache: dict[str, Any] = {"url": None, "keys": None, "fetched_at": 0.0}
_JWKS_TTL_SECONDS = 3600


def _resolve_jwks_url(token: str) -> str:
    """Always derive JWKS from token issuer so dev/prod keys cannot mismatch."""
    try:
        claims = jwt.get_unverified_claims(token)
        issuer = claims.get("iss", "").rstrip("/")
        if issuer:
            return f"{issuer}/.well-known/jwks.json"
    except JWTError:
        pass

    settings = get_settings()
    if settings.clerk_jwks_url:
        return settings.clerk_jwks_url.rstrip("/")

    raise ValueError("CLERK_JWKS_URL is not configured and could not be derived from token issuer")


async def _fetch_jwks(jwks_url: str) -> dict:
    now = time.time()
    if (
        _jwks_cache["keys"]
        and _jwks_cache["url"] == jwks_url
        and (now - _jwks_cache["fetched_at"]) < _JWKS_TTL_SECONDS
    ):
        return _jwks_cache["keys"]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(jwks_url)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        logger.error("clerk_jwks_fetch_failed", url=jwks_url, error=str(exc))
        raise ValueError(f"Failed to fetch Clerk JWKS: {exc}") from exc

    _jwks_cache["keys"] = data
    _jwks_cache["url"] = jwks_url
    _jwks_cache["fetched_at"] = now
    return data


def _get_signing_key(jwks: dict, kid: str | None) -> Any:
    for key in jwks.get("keys", []):
        if kid is None or key.get("kid") == kid:
            return jwk.construct(key)
    return None


async def _fetch_clerk_user(clerk_user_id: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.clerk_secret_key:
        raise ValueError("CLERK_SECRET_KEY is not configured")

    url = f"https://api.clerk.com/v1/users/{clerk_user_id}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                url,
                headers={"Authorization": f"Bearer {settings.clerk_secret_key}"},
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        logger.error("clerk_user_fetch_failed", user_id=clerk_user_id, error=str(exc))
        raise ValueError("Failed to fetch Clerk user profile") from exc


async def verify_clerk_token(token: str) -> dict[str, Any]:
    """Verify Clerk session JWT and return claims."""
    settings = get_settings()
    if not settings.clerk_secret_key:
        raise ValueError("Clerk is not configured")

    jwks_url = _resolve_jwks_url(token)
    jwks = await _fetch_jwks(jwks_url)

    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise ValueError("Invalid Clerk token header") from exc

    signing_key = _get_signing_key(jwks, header.get("kid"))
    if not signing_key:
        raise ValueError("Unable to find matching JWKS key")

    try:
        claims = jwt.decode(
            token,
            signing_key,
            algorithms=[header.get("alg", "RS256")],
            options={"verify_aud": False, "leeway": 120},
        )
        return claims
    except JWTError as exc:
        err = str(exc)
        logger.warning("clerk_jwt_invalid", error=err)
        if "expired" in err.lower():
            raise ValueError("Clerk token expired — please retry") from exc
        raise ValueError(f"Invalid Clerk token: {err}") from exc


async def extract_clerk_identity(claims: dict[str, Any]) -> tuple[str, str | None, str | None]:
    """Return (email, clerk_id, name) from Clerk JWT claims + Clerk API fallback."""
    clerk_id = claims.get("sub")
    email = claims.get("email")

    if not email:
        emails = claims.get("email_addresses") or []
        if emails and isinstance(emails[0], dict):
            email = emails[0].get("email_address")

    name = claims.get("name") or claims.get("first_name")

    if clerk_id and not email:
        try:
            user = await _fetch_clerk_user(clerk_id)
            addresses = user.get("email_addresses") or []
            primary_id = user.get("primary_email_address_id")
            for addr in addresses:
                if addr.get("id") == primary_id or addr.get("email_address"):
                    email = addr.get("email_address")
                    break
            if not name:
                name = " ".join(
                    p for p in [user.get("first_name"), user.get("last_name")] if p
                ).strip() or None
        except ValueError:
            logger.warning("clerk_user_profile_unavailable", clerk_id=clerk_id)

    if not email and clerk_id:
        email = f"{clerk_id}@clerk.user"

    if not email:
        raise ValueError("Clerk token missing email claim")

    if not name:
        name = email.split("@")[0]

    return email, clerk_id, name
