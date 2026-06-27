"""Redis pub/sub + event log for live SSE streaming."""

import json
from collections.abc import AsyncGenerator

from app.core.redis import get_redis

EVENT_CHANNEL = "pipeline:events:{run_id}"
EVENT_LOG = "pipeline:eventlog:{run_id}"
EVENT_LOG_TTL = 86400


async def publish_pipeline_event(run_id: str, event: str, data: dict) -> None:
    redis = get_redis()
    payload = json.dumps({"event": event, "data": data})
    channel = EVENT_CHANNEL.format(run_id=run_id)
    log_key = EVENT_LOG.format(run_id=run_id)
    await redis.publish(channel, payload)
    await redis.rpush(log_key, payload)
    await redis.expire(log_key, EVENT_LOG_TTL)


async def replay_events(run_id: str) -> list[dict]:
    redis = get_redis()
    log_key = EVENT_LOG.format(run_id=run_id)
    raw = await redis.lrange(log_key, 0, -1)
    return [json.loads(item) for item in raw]


async def subscribe_pipeline_events(run_id: str) -> AsyncGenerator[dict, None]:
    """Yield events from log replay, then live pub/sub."""
    for item in await replay_events(run_id):
        yield item

    redis = get_redis()
    pubsub = redis.pubsub()
    channel = EVENT_CHANNEL.format(run_id=run_id)
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            yield json.loads(message["data"])
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.aclose()
