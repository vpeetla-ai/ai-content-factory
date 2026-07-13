"""LLM gateway plane wiring (no live gateway required)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents.llm import call_llm, llm_gateway_enabled
from app.core.config import get_settings


def test_llm_gateway_disabled_by_default(monkeypatch):
    monkeypatch.delenv("LLM_GATEWAY_URL", raising=False)
    get_settings.cache_clear()
    assert llm_gateway_enabled() is False
    get_settings.cache_clear()


def test_llm_gateway_enabled_when_url_set(monkeypatch):
    monkeypatch.setenv("LLM_GATEWAY_URL", "http://127.0.0.1:8100/v1")
    get_settings.cache_clear()
    assert llm_gateway_enabled() is True
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_call_llm_routes_through_gateway(monkeypatch):
    monkeypatch.setenv("LLM_GATEWAY_URL", "http://127.0.0.1:8100/v1")
    monkeypatch.setenv("LLM_GATEWAY_TENANT_ID", "acf-test")
    monkeypatch.setenv("MOCK_LLM", "false")
    get_settings.cache_clear()

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"brief":"gw"}'))]
    mock_response.usage = MagicMock(prompt_tokens=1, completion_tokens=2)

    with patch("agents.llm.acompletion", new=AsyncMock(return_value=mock_response)) as mock_ac:
        with patch("agents.llm.use_mock_llm", return_value=False):
            content = await call_llm("research", "sys", "Topic: gateway")

    assert "gw" in content or content
    kwargs = mock_ac.await_args.kwargs
    assert kwargs["api_base"] == "http://127.0.0.1:8100/v1"
    assert kwargs["extra_headers"]["X-Tenant-Id"] == "acf-test"
    assert kwargs["model"].startswith("openai/")

    get_settings.cache_clear()
    monkeypatch.setenv("MOCK_LLM", "true")
