"""Tests for R2 media cards + LinkedIn/X native image attach (fail-soft)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models import Platform
from app.services.media_assets import materialize_media_assets
from app.services.media_cards import card_object_key, render_prompt_card_png, render_prompt_card_svg
from app.services.publisher import LinkedInAdapter, XAdapter
from tests.test_publisher_adapters import make_draft


def test_render_prompt_card_svg_contains_topic():
    raw = render_prompt_card_svg(topic="Gateway governance", prompt="Navy control plane diagram", index=0)
    assert b"Gateway governance" in raw
    assert b"image/svg" not in raw  # body is svg xml
    assert raw.startswith(b"<?xml")


def test_render_prompt_card_png_is_png():
    raw = render_prompt_card_png(topic="Gateway governance", prompt="Navy control plane diagram", index=0)
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(raw) > 500


def test_card_object_key_defaults_to_png():
    key = card_object_key("run-abc", "hello world", 1)
    assert key.startswith("runs/")
    assert "card-1-" in key
    assert key.endswith(".png")


@pytest.mark.asyncio
async def test_materialize_skips_when_r2_unset():
    with patch("app.services.media_assets.r2_configured", return_value=False):
        assets = await materialize_media_assets(
            run_id="r1", topic="t", prompts=["a", "b"]
        )
    assert assets == []


@pytest.mark.asyncio
async def test_materialize_uploads_png_when_configured():
    fake = MagicMock()
    fake.key = "runs/r1/card-0-abc.png"
    fake.public_url = "https://cdn.example/runs/r1/card-0-abc.png"
    fake.content_type = "image/png"
    upload = AsyncMock(return_value=fake)
    with patch("app.services.media_assets.r2_configured", return_value=True):
        with patch("app.services.media_assets.upload_bytes", new=upload):
            assets = await materialize_media_assets(
                run_id="r1", topic="Topic", prompts=["Prompt one"]
            )
    assert len(assets) == 1
    assert assets[0]["url"].startswith("https://cdn.example/")
    assert assets[0]["content_type"] == "image/png"
    assert upload.await_args.kwargs.get("content_type") == "image/png"
    assert str(upload.await_args.args[0]).endswith(".png")


@pytest.mark.asyncio
async def test_linkedin_mock_path_without_token():
    draft = make_draft(Platform.linkedin, content="Hello team")
    result = await LinkedInAdapter().publish(
        draft, {"_media_urls": ["https://cdn.example/card.png"]}
    )
    assert result["external_post_id"].startswith("li_mock_")


@pytest.mark.asyncio
async def test_linkedin_native_image_attach():
    draft = make_draft(Platform.linkedin, content="Hello team")
    png = b"\x89PNG\r\n\x1a\n" + b"fake"
    client = MagicMock()
    get_resp = MagicMock(status_code=200, content=png)
    register_resp = MagicMock(status_code=200)
    register_resp.json = lambda: {
        "value": {
            "asset": "urn:li:digitalmediaAsset:ABC",
            "uploadMechanism": {
                "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest": {
                    "uploadUrl": "https://upload.linkedin.example/put"
                }
            },
        }
    }
    put_resp = MagicMock(status_code=201)
    ugc_resp = MagicMock(status_code=201)
    ugc_resp.json = lambda: {"id": "urn:li:share:1"}

    async def _post(url, **kwargs):
        if "registerUpload" in str(url):
            return register_resp
        return ugc_resp

    client.get = AsyncMock(return_value=get_resp)
    client.post = AsyncMock(side_effect=_post)
    client.put = AsyncMock(return_value=put_resp)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = client
        result = await LinkedInAdapter().publish(
            draft,
            {
                "access_token": "tok",
                "person_id": "abc",
                "_media_urls": ["https://cdn.example/card.png"],
            },
        )

    assert result.get("media_attached") is True
    ugc_json = None
    for call in client.post.await_args_list:
        if "ugcPosts" in str(call.args[0]):
            ugc_json = call.kwargs["json"]
    assert ugc_json is not None
    share = ugc_json["specificContent"]["com.linkedin.ugc.ShareContent"]
    assert share["shareMediaCategory"] == "IMAGE"
    assert "https://cdn.example/card.png" not in share["shareCommentary"]["text"]


@pytest.mark.asyncio
async def test_linkedin_failsoft_url_when_fetch_fails():
    draft = make_draft(Platform.linkedin, content="Hello team")
    client = MagicMock()
    get_resp = MagicMock(status_code=404, content=b"")
    ugc_resp = MagicMock(status_code=201)
    ugc_resp.json = lambda: {"id": "urn:li:share:1"}
    client.get = AsyncMock(return_value=get_resp)
    client.post = AsyncMock(return_value=ugc_resp)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = client
        await LinkedInAdapter().publish(
            draft,
            {
                "access_token": "tok",
                "person_id": "abc",
                "_media_urls": ["https://cdn.example/card.png"],
            },
        )
    sent = client.post.await_args.kwargs["json"]
    text = sent["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
    assert "https://cdn.example/card.png" in text
    assert sent["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] == "NONE"


@pytest.mark.asyncio
async def test_x_native_media_attach():
    draft = make_draft(Platform.x, content="Hello X")
    png = b"\x89PNG\r\n\x1a\n" + b"fake"
    client = MagicMock()
    get_resp = MagicMock(status_code=200, content=png)
    upload_resp = MagicMock(status_code=200)
    upload_resp.json = lambda: {"media_id_string": "999"}
    tweet_resp = MagicMock(status_code=201)
    tweet_resp.json = lambda: {"data": {"id": "42"}}
    client.get = AsyncMock(return_value=get_resp)
    client.post = AsyncMock(side_effect=[upload_resp, tweet_resp])

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = client
        result = await XAdapter().publish(
            draft,
            {"access_token": "tok", "_media_urls": ["https://cdn.example/c.png"]},
        )
    assert result.get("media_attached") is True
    tweet_json = client.post.await_args_list[-1].kwargs["json"]
    assert tweet_json["media"]["media_ids"] == ["999"]
    assert "https://cdn.example/c.png" not in tweet_json["text"]


@pytest.mark.asyncio
async def test_x_failsoft_url_when_upload_fails():
    draft = make_draft(Platform.x, content="x" * 270)
    png = b"\x89PNG\r\n\x1a\n" + b"fake"
    client = MagicMock()
    get_resp = MagicMock(status_code=200, content=png)
    upload_resp = MagicMock(status_code=403)
    upload_resp.text = "forbidden"
    tweet_resp = MagicMock(status_code=201)
    tweet_resp.json = lambda: {"data": {"id": "42"}}
    client.get = AsyncMock(return_value=get_resp)
    client.post = AsyncMock(side_effect=[upload_resp, tweet_resp])

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = client
        await XAdapter().publish(
            draft,
            {"access_token": "tok", "_media_urls": ["https://cdn.example/c.png"]},
        )
    text = client.post.await_args_list[-1].kwargs["json"]["text"]
    assert "https://cdn.example/c.png" in text
    assert len(text) <= 280
