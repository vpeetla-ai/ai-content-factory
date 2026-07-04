"""Tests for platform publish adapters — real LinkedIn/X calls vs. not-supported fallback."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models import ContentDraft, Platform
from app.services.publisher import (
    ADAPTERS,
    InstagramAdapter,
    LinkedInAdapter,
    MediumAdapter,
    SubstackAdapter,
    XAdapter,
)


def make_draft(platform: Platform, content: str = "Hello world") -> ContentDraft:
    return ContentDraft(
        id=uuid.uuid4(),
        run_id=uuid.uuid4(),
        platform=platform,
        draft_content=content,
        edited_content=None,
    )


@pytest.mark.asyncio
async def test_linkedin_adapter_mocks_when_no_access_token():
    draft = make_draft(Platform.linkedin)
    result = await LinkedInAdapter().publish(draft, {})
    assert result["external_post_id"].startswith("li_mock_")


@pytest.mark.asyncio
async def test_linkedin_adapter_errors_when_person_id_missing():
    draft = make_draft(Platform.linkedin)
    result = await LinkedInAdapter().publish(draft, {"access_token": "tok"})
    assert result["external_post_id"].startswith("li_error_")


@pytest.mark.asyncio
async def test_linkedin_adapter_uses_real_person_urn():
    draft = make_draft(Platform.linkedin)
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json = lambda: {"id": "urn:li:share:123"}

    with patch("httpx.AsyncClient") as mock_client:
        mock_post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = mock_post
        result = await LinkedInAdapter().publish(draft, {"access_token": "tok", "person_id": "abc123"})

    sent_json = mock_post.call_args.kwargs["json"]
    assert sent_json["author"] == "urn:li:person:abc123"
    assert result["external_post_id"] == "urn:li:share:123"


@pytest.mark.asyncio
async def test_linkedin_adapter_handles_api_error():
    draft = make_draft(Platform.linkedin)
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "invalid token"

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        result = await LinkedInAdapter().publish(draft, {"access_token": "tok", "person_id": "abc123"})

    assert result["external_post_id"].startswith("li_error_")


@pytest.mark.asyncio
async def test_x_adapter_mocks_when_no_access_token():
    draft = make_draft(Platform.x)
    result = await XAdapter().publish(draft, {})
    assert result["external_post_id"].startswith("x_mock_")


@pytest.mark.asyncio
async def test_x_adapter_real_publish():
    draft = make_draft(Platform.x)
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json = lambda: {"data": {"id": "999"}}

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        result = await XAdapter().publish(draft, {"access_token": "tok"})

    assert result["external_post_id"] == "999"


@pytest.mark.parametrize("adapter_cls,platform", [
    (MediumAdapter, Platform.medium),
    (SubstackAdapter, Platform.substack),
    (InstagramAdapter, Platform.instagram),
])
@pytest.mark.asyncio
async def test_not_supported_adapters_return_draft_for_copy(adapter_cls, platform):
    draft = make_draft(platform, content="Copy me")
    result = await adapter_cls().publish(draft, {"access_token": "tok"})
    assert result["not_supported"] is True
    assert result["draft_content"] == "Copy me"
    assert result["external_post_id"] == ""


def test_adapter_registry_covers_all_five_platforms():
    assert set(ADAPTERS.keys()) == {"linkedin", "x", "medium", "substack", "instagram"}
