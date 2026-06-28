"""Shared LangGraph checkpointer + compiled graph (Redis-backed)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langgraph.checkpoint.redis.aio import AsyncRedisSaver
    from langgraph.graph.state import CompiledStateGraph

logger = logging.getLogger(__name__)

_checkpointer: AsyncRedisSaver | None = None
_graph: CompiledStateGraph | None = None
_checkpointer_cm = None
_using_memory = False


def force_memory_graph() -> None:
    """Fallback when Redis checkpointer is unavailable (e.g. Upstash without RediSearch)."""
    global _checkpointer, _graph, _checkpointer_cm, _using_memory
    from langgraph.checkpoint.memory import MemorySaver

    from agents.graph import build_graph

    _checkpointer = None
    _checkpointer_cm = None
    _graph = build_graph(checkpointer=MemorySaver())
    _using_memory = True
    logger.warning("LangGraph using MemorySaver fallback")


async def init_graph(redis_url: str, *, ttl_seconds: int = 86400) -> None:
    """Initialize Redis checkpointer and compile graph once at app startup."""
    global _checkpointer, _graph, _checkpointer_cm, _using_memory

    from agents.graph import build_graph

    try:
        from langgraph.checkpoint.redis.aio import AsyncRedisSaver

        _checkpointer_cm = AsyncRedisSaver.from_conn_string(
            redis_url,
            ttl={"default_ttl": ttl_seconds},
        )
        _checkpointer = await _checkpointer_cm.__aenter__()
        await _checkpointer.asetup()
        _graph = build_graph(checkpointer=_checkpointer)
        _using_memory = False
        logger.info("LangGraph initialized with Redis checkpointer")
    except Exception as exc:
        from langgraph.checkpoint.memory import MemorySaver

        logger.warning(
            "Redis Stack checkpointer unavailable (%s) — falling back to MemorySaver",
            exc,
        )
        _checkpointer = None
        _checkpointer_cm = None
        _graph = build_graph(checkpointer=MemorySaver())
        _using_memory = True


async def shutdown_graph() -> None:
    global _checkpointer, _graph, _checkpointer_cm, _using_memory
    if _checkpointer_cm is not None:
        await _checkpointer_cm.__aexit__(None, None, None)
    _checkpointer = None
    _graph = None
    _checkpointer_cm = None
    _using_memory = False


def get_graph() -> "CompiledStateGraph":
    if _graph is None:
        raise RuntimeError("LangGraph not initialized — call init_graph() in app lifespan")
    return _graph


def get_checkpointer() -> "AsyncRedisSaver":
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized")
    return _checkpointer


def is_memory_checkpointer() -> bool:
    return _using_memory
