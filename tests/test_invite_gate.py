"""Tests for invite-code gated signup on the Clerk -> internal JWT exchange."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.api.routes.auth import exchange_token
from app.models import InviteCode
from app.schemas import TokenRequest


def make_settings(require_invite_code: bool):
    settings = MagicMock()
    settings.clerk_configured = False
    settings.clerk_secret_key = ""
    settings.allow_dev_auth = True
    settings.is_development = True
    settings.require_invite_code = require_invite_code
    settings.jwt_expire_minutes = 60
    return settings


def make_db(existing_user=None, invite_code_row=None):
    db = MagicMock()

    async def execute(query):
        result = MagicMock()
        # First execute() call in the route looks up the User by email.
        # If an invite lookup is needed it happens on a later call.
        if not hasattr(execute, "_calls"):
            execute._calls = 0
        execute._calls += 1
        if execute._calls == 1:
            result.scalar_one_or_none = MagicMock(return_value=existing_user)
        else:
            result.scalar_one_or_none = MagicMock(return_value=invite_code_row)
        return result

    db.execute = execute
    db.add = MagicMock()
    db.flush = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_signup_blocked_without_invite_code_when_required():
    settings = make_settings(require_invite_code=True)
    db = make_db(existing_user=None, invite_code_row=None)
    body = TokenRequest(clerk_token="newuser@dev.local", invite_code=None)

    with patch("app.api.routes.auth.get_settings", return_value=settings):
        with pytest.raises(HTTPException) as exc_info:
            await exchange_token(body, db)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_signup_blocked_with_invalid_invite_code():
    settings = make_settings(require_invite_code=True)
    db = make_db(existing_user=None, invite_code_row=None)
    body = TokenRequest(clerk_token="newuser@dev.local", invite_code="bogus")

    with patch("app.api.routes.auth.get_settings", return_value=settings):
        with pytest.raises(HTTPException) as exc_info:
            await exchange_token(body, db)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_signup_allowed_with_valid_unused_invite_code():
    settings = make_settings(require_invite_code=True)
    invite = InviteCode(code="good-code", max_uses=1, uses_count=0)
    db = make_db(existing_user=None, invite_code_row=invite)
    body = TokenRequest(clerk_token="newuser@dev.local", invite_code="good-code")

    with patch("app.api.routes.auth.get_settings", return_value=settings):
        with patch("app.api.routes.auth.create_access_token", return_value="jwt-token"):
            response = await exchange_token(body, db)

    assert response.access_token == "jwt-token"
    assert invite.uses_count == 1


@pytest.mark.asyncio
async def test_signup_blocked_when_invite_code_fully_used():
    settings = make_settings(require_invite_code=True)
    invite = InviteCode(code="used-up", max_uses=1, uses_count=1)
    db = make_db(existing_user=None, invite_code_row=invite)
    body = TokenRequest(clerk_token="newuser@dev.local", invite_code="used-up")

    with patch("app.api.routes.auth.get_settings", return_value=settings):
        with pytest.raises(HTTPException) as exc_info:
            await exchange_token(body, db)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_signup_not_gated_when_invite_code_not_required():
    settings = make_settings(require_invite_code=False)
    db = make_db(existing_user=None, invite_code_row=None)
    body = TokenRequest(clerk_token="newuser@dev.local", invite_code=None)

    with patch("app.api.routes.auth.get_settings", return_value=settings):
        with patch("app.api.routes.auth.create_access_token", return_value="jwt-token"):
            response = await exchange_token(body, db)

    assert response.access_token == "jwt-token"
