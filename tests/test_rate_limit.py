"""Tests for the per-user Redis sliding-window rate limiter."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.core.rate_limit import check_rate_limit


class FakeRedis:
    def __init__(self):
        self.counts: dict[str, int] = {}

    async def incr(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]

    async def expire(self, key, seconds):
        pass


@pytest.mark.asyncio
async def test_allows_requests_under_limit():
    fake_redis = FakeRedis()
    with patch("app.core.rate_limit.get_redis", return_value=fake_redis):
        for _ in range(60):
            await check_rate_limit("user-1")


@pytest.mark.asyncio
async def test_blocks_requests_over_limit():
    fake_redis = FakeRedis()
    with patch("app.core.rate_limit.get_redis", return_value=fake_redis):
        for _ in range(60):
            await check_rate_limit("user-1")
        with pytest.raises(HTTPException) as exc_info:
            await check_rate_limit("user-1")

    assert exc_info.value.status_code == 429


@pytest.mark.asyncio
async def test_limits_are_per_user():
    fake_redis = FakeRedis()
    with patch("app.core.rate_limit.get_redis", return_value=fake_redis):
        for _ in range(60):
            await check_rate_limit("user-1")
        # a different user should not be affected by user-1's usage
        await check_rate_limit("user-2")
