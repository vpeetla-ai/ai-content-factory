"""Unit tests for optional Enterprise RAG compose helper."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agents.nodes.research import _fetch_enterprise_rag


@pytest.mark.asyncio
async def test_enterprise_rag_disabled_returns_empty():
    with patch("agents.nodes.research.get_settings") as mock_settings:
        mock_settings.return_value.enterprise_rag_api_url = ""
        parts, meta = await _fetch_enterprise_rag("topic")
    assert parts == []
    assert meta["configured"] is False
    assert meta["used"] is False


@pytest.mark.asyncio
async def test_enterprise_rag_parses_answer_and_citations():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = lambda: {
        "answer": "Governed agents need a gateway.",
        "citations": [{"text": "ADR-007", "page": 2}],
    }

    settings = MagicMock()
    settings.enterprise_rag_api_url = "https://erag.example"
    settings.enterprise_rag_api_key = "k"
    settings.enterprise_rag_timeout_s = 5.0

    with patch("agents.nodes.research.get_settings", return_value=settings):
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )
            parts, meta = await _fetch_enterprise_rag("gateway")

    assert any("Governed agents" in p for p in parts)
    assert any("ADR-007" in p for p in parts)
    assert any("p.2" in p for p in parts)
    assert meta["configured"] is True
    assert meta["used"] is True
    assert meta["cite_count"] == 1
