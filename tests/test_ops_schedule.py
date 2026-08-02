"""Tests for schedule surface (no DB required)."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_ops_schedule_returns_cron_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/ops/schedule")

    assert response.status_code == 200
    data = response.json()
    assert "enabled" in data
    assert "cron" in data
    assert "platforms" in data
    assert data["mutation"] == "env_only"
    assert data["timezone"] == "UTC"
