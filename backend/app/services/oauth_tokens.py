"""OAuth token exchange for social publish platforms."""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

LINKEDIN_AUTHORIZE_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_SCOPE = "openid profile w_member_social"
X_AUTHORIZE_URL = "https://twitter.com/i/oauth2/authorize"
X_SCOPE = "tweet.write tweet.read users.read offline.access"


def generate_pkce_pair() -> tuple[str, str]:
    """Return (code_verifier, code_challenge) for the S256 PKCE method."""
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def build_linkedin_authorize_url(redirect_uri: str, state: str) -> str:
    settings = get_settings()
    if not settings.linkedin_client_id:
        raise ValueError("LinkedIn OAuth is not configured")
    params = {
        "response_type": "code",
        "client_id": settings.linkedin_client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": LINKEDIN_SCOPE,
    }
    return f"{LINKEDIN_AUTHORIZE_URL}?{httpx.QueryParams(params)}"


def build_x_authorize_url(redirect_uri: str, state: str, code_challenge: str) -> str:
    settings = get_settings()
    if not settings.x_api_key:
        raise ValueError("X OAuth is not configured")
    params = {
        "response_type": "code",
        "client_id": settings.x_api_key,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": X_SCOPE,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{X_AUTHORIZE_URL}?{httpx.QueryParams(params)}"


async def exchange_linkedin_code(code: str, redirect_uri: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.linkedin_client_id or not settings.linkedin_client_secret:
        raise ValueError("LinkedIn OAuth is not configured")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": settings.linkedin_client_id,
                "client_secret": settings.linkedin_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()


async def fetch_linkedin_person_id(access_token: str) -> str:
    """Resolve the LinkedIn person URN id via the OIDC userinfo endpoint."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        payload = response.json()
        person_id = payload.get("sub")
        if not person_id:
            raise ValueError("LinkedIn userinfo response missing 'sub' claim")
        return person_id


async def exchange_x_code(code: str, redirect_uri: str, code_verifier: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.x_api_key or not settings.x_api_secret:
        raise ValueError("X OAuth is not configured")

    basic = base64.b64encode(f"{settings.x_api_key}:{settings.x_api_secret}".encode()).decode()
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.twitter.com/2/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {basic}",
            },
        )
        response.raise_for_status()
        return response.json()
