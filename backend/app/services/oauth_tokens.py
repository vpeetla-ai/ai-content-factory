"""OAuth token exchange for social publish platforms."""

from __future__ import annotations

import base64
import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


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


async def exchange_x_code(code: str, redirect_uri: str) -> dict[str, Any]:
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
                "code_verifier": "challenge",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {basic}",
            },
        )
        response.raise_for_status()
        return response.json()
