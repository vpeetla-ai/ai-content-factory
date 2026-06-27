"""Rate limiter — Redis sliding window per user."""

import time

from fastapi import HTTPException, status

from app.core.redis import get_redis
from app.core.redis_keys import RATELIMIT

REQUESTS_PER_MINUTE = 60


async def check_rate_limit(user_id: str) -> None:
    redis = get_redis()
    minute = int(time.time() // 60)
    key = RATELIMIT.format(user_id=user_id, minute=minute)
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 60)
    if count > REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
