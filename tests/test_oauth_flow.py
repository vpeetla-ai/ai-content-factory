"""Tests for OAuth connect flow — PKCE, authorize URLs, token exchange, and state storage."""

from __future__ import annotations

import base64
import hashlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.oauth_tokens import (
    build_linkedin_authorize_url,
    build_x_authorize_url,
    exchange_x_code,
    fetch_linkedin_person_id,
    generate_pkce_pair,
)


def test_generate_pkce_pair_challenge_matches_verifier():
    verifier, challenge = generate_pkce_pair()
    expected = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    assert challenge == expected
    assert verifier != challenge


def test_build_linkedin_authorize_url_contains_scope_and_state():
    with patch("app.services.oauth_tokens.get_settings") as mock_settings:
        mock_settings.return_value.linkedin_client_id = "client-123"
        url = build_linkedin_authorize_url("https://api.example/oauth/linkedin/callback", "state-abc")

    assert "client_id=client-123" in url
    assert "state=state-abc" in url
    assert "w_member_social" in url


def test_build_x_authorize_url_contains_code_challenge():
    with patch("app.services.oauth_tokens.get_settings") as mock_settings:
        mock_settings.return_value.x_api_key = "x-client-1"
        url = build_x_authorize_url("https://api.example/oauth/x/callback", "state-xyz", "chal-1")

    assert "code_challenge=chal-1" in url
    assert "code_challenge_method=S256" in url
    assert "state=state-xyz" in url


@pytest.mark.asyncio
async def test_exchange_x_code_sends_provided_code_verifier():
    mock_response = MagicMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: {"access_token": "tok", "token_type": "bearer", "expires_in": 3600}

    with patch("app.services.oauth_tokens.get_settings") as mock_settings:
        mock_settings.return_value.x_api_key = "k"
        mock_settings.return_value.x_api_secret = "s"
        with patch("httpx.AsyncClient") as mock_client:
            mock_post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.post = mock_post
            await exchange_x_code("code-1", "https://api.example/oauth/x/callback", "real-verifier")

    sent_data = mock_post.call_args.kwargs["data"]
    assert sent_data["code_verifier"] == "real-verifier"


@pytest.mark.asyncio
async def test_fetch_linkedin_person_id_returns_sub_claim():
    mock_response = MagicMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: {"sub": "abc123"}

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        person_id = await fetch_linkedin_person_id("tok")

    assert person_id == "abc123"


@pytest.mark.asyncio
async def test_fetch_linkedin_person_id_raises_when_sub_missing():
    mock_response = MagicMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: {}

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        with pytest.raises(ValueError, match="sub"):
            await fetch_linkedin_person_id("tok")


class FakeRedis:
    def __init__(self):
        self.store: dict[str, str] = {}

    async def set(self, key, value, ex=None):
        self.store[key] = value

    async def get(self, key):
        return self.store.get(key)

    async def delete(self, key):
        self.store.pop(key, None)


@pytest.mark.asyncio
async def test_oauth_state_roundtrip_and_single_use():
    from app.api.routes.oauth import _consume_oauth_state, _store_oauth_state

    fake_redis = FakeRedis()
    with patch("app.api.routes.oauth.get_redis", return_value=fake_redis):
        state = await _store_oauth_state("user-1", "x", code_verifier="verifier-1")
        payload = await _consume_oauth_state(state, "x")
        assert payload["user_id"] == "user-1"
        assert payload["code_verifier"] == "verifier-1"

        # state is single-use — a second consume must fail
        with pytest.raises(Exception):
            await _consume_oauth_state(state, "x")


@pytest.mark.asyncio
async def test_oauth_state_platform_mismatch_rejected():
    from fastapi import HTTPException

    from app.api.routes.oauth import _consume_oauth_state, _store_oauth_state

    fake_redis = FakeRedis()
    with patch("app.api.routes.oauth.get_redis", return_value=fake_redis):
        state = await _store_oauth_state("user-1", "linkedin", code_verifier=None)
        with pytest.raises(HTTPException):
            await _consume_oauth_state(state, "x")
