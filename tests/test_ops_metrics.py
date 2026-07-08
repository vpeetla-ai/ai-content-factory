"""Tests for public ops metrics endpoint."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_ops_metrics_returns_aggregate_shape():
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
