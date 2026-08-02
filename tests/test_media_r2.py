"""Tests for R2 media cards (fail-soft when unset)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.media_assets import materialize_media_assets
from app.services.media_cards import card_object_key, render_prompt_card_svg
from app.services.publisher import LinkedInAdapter, XAdapter
from tests.test_publisher_adapters import make_draft
from app.models import Platform


def test_render_prompt_card_svg_contains_topic():
    raw = render_prompt_card_svg(topic="Gateway governance", prompt="Navy control plane diagram", index=0)
    assert b"Gateway governance" in raw
    assert b"image/svg" not in raw  # body is svg xml
    assert raw.startswith(b"<?xml")


def test_card_object_key_stable_slug():
    key = card_object_key("run-abc", "hello world", 1)
    assert key.startswith("runs/")
    assert "card-1-" in key
    assert key.endswith(".svg")


@pytest.mark.asyncio
async def test_materialize_skips_when_r2_unset():
    with patch("app.services.media_assets.r2_configured", return_value=False):
        assets = await materialize_media_assets(
            run_id="r1", topic="t", prompts=["a", "b"]
        )
    assert assets == []


@pytest.mark.asyncio
async def test_materialize_uploads_when_configured():
    fake = MagicMock()
    fake.key = "runs/r1/card-0-abc.svg"
    fake.public_url = "https://cdn.example/runs/r1/card-0-abc.svg"
    fake.content_type = "image/svg+xml"
    with patch("app.services.media_assets.r2_configured", return_value=True):
        with patch("app.services.media_assets.upload_bytes", new=AsyncMock(return_value=fake)):
            assets = await materialize_media_assets(
                run_id="r1", topic="Topic", prompts=["Prompt one"]
            )
    assert len(assets) == 1
    assert assets[0]["url"].startswith("https://cdn.example/")


@pytest.mark.asyncio
async def test_linkedin_appends_media_url():
    draft = make_draft(Platform.linkedin, content="Hello team")
    result = await LinkedInAdapter().publish(
        draft, {"_media_urls": ["https://cdn.example/card.svg"]}
    )
    # mock path without token still returns mock id; assert via content path by patching
    assert result["external_post_id"].startswith("li_mock_")


@pytest.mark.asyncio
async def test_linkedin_includes_media_in_api_payload():
    draft = make_draft(Platform.linkedin, content="Hello team")
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json = lambda: {"id": "urn:li:share:1"}
    with patch("httpx.AsyncClient") as mock_client:
        mock_post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = mock_post
        await LinkedInAdapter().publish(
            draft,
            {
                "access_token": "tok",
                "person_id": "abc",
                "_media_urls": ["https://cdn.example/card.svg"],
            },
        )
    sent = mock_post.call_args.kwargs["json"]
    text = sent["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
    assert "https://cdn.example/card.svg" in text


@pytest.mark.asyncio
async def test_x_truncates_with_media_url():
    draft = make_draft(Platform.x, content="x" * 270)
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json = lambda: {"data": {"id": "42"}}
    with patch("httpx.AsyncClient") as mock_client:
        mock_post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = mock_post
        await XAdapter().publish(
            draft,
            {"access_token": "tok", "_media_urls": ["https://cdn.example/c.svg"]},
        )
    text = mock_post.call_args.kwargs["json"]["text"]
    assert "https://cdn.example/c.svg" in text
    assert len(text) <= 280
