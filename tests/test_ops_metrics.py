"""Tests for public ops metrics endpoint."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_ops_metrics_returns_aggregate_shape():
    fake = {
        "service": "ai-content-factory",
        "total_runs": 3,
        "success_rate_pct": 100.0,
        "p95_latency_ms": 12,
        "active_entities": 1,
        "slo": {"target_uptime_pct": 99.5, "pipeline_success_target_pct": 95.0},
        "extra": {},
    }
    with patch("app.api.routes.ops.collect_ops_metrics", new=AsyncMock(return_value=fake)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/ops/metrics")

    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "ai-content-factory"
    assert "total_runs" in data
    assert "success_rate_pct" in data
    assert "slo" in data
    assert data["slo"]["pipeline_success_target_pct"] == 95.0
    assert "llm_gateway" in data["extra"]
    assert data["extra"]["llm_gateway"]["plane"] == "aegis-llm-gateway"
    assert "enterprise_rag" in data["extra"]
    assert "compose" in data["extra"]["enterprise_rag"]
    assert data["extra"]["schedule"]["mutation"] == "env_only"
    assert data["extra"]["schedule"]["timezone"] == "UTC"
