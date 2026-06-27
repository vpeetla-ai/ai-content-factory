"""Shared LangGraph checkpointer + compiled graph (Redis-backed)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langgraph.checkpoint.redis.aio import AsyncRedisSaver
    from langgraph.graph.state import CompiledStateGraph

_checkpointer: AsyncRedisSaver | None = None
_graph: CompiledStateGraph | None = None
_checkpointer_cm = None


async def init_graph(redis_url: str, *, ttl_seconds: int = 86400) -> None:
    """Initialize Redis checkpointer and compile graph once at app startup."""
    global _checkpointer, _graph, _checkpointer_cm

    from langgraph.checkpoint.redis.aio import AsyncRedisSaver

    from agents.graph import build_graph

    _checkpointer_cm = AsyncRedisSaver.from_conn_string(
        redis_url,
        ttl={"default_ttl": ttl_seconds},
    )
    _checkpointer = await _checkpointer_cm.__aenter__()
    await _checkpointer.asetup()
    _graph = build_graph(checkpointer=_checkpointer)


async def shutdown_graph() -> None:
    global _checkpointer, _graph, _checkpointer_cm
    if _checkpointer_cm is not None:
        await _checkpointer_cm.__aexit__(None, None, None)
    _checkpointer = None
    _graph = None
    _checkpointer_cm = None


def get_graph() -> "CompiledStateGraph":
    if _graph is None:
        raise RuntimeError("LangGraph not initialized — call init_graph() in app lifespan")
    return _graph


def get_checkpointer() -> "AsyncRedisSaver":
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized")
    return _checkpointer
