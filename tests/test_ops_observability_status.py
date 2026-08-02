"""Tests for public ACF observability status compose planes."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_ops_observability_status_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/ops/observability/status")

    assert response.status_code == 200
    data = response.json()
    assert "source_of_truth" in data
    assert "exporters" in data
    assert "planes" in data
    assert "recommendation" in data
    planes = data["planes"]
    assert planes["llm_gateway"]["plane"] == "aegis-llm-gateway"
    assert planes["enterprise_rag"]["compose"] == "research_node"
    assert planes["aegisai_gateway"]["plane"] == "publish_side_effects"
    assert planes["schedule"]["mutation"] == "env_only"
    names = {e["name"] for e in data["exporters"]}
    assert "OpsMetrics" in names
    assert "Langfuse" in names
