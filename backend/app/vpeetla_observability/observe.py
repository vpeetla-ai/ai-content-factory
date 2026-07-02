"""LangGraph node decorator — trace-linked spans + structured logs."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, TypeVar

from .context import bind_trace_context, set_run_context
from .spans import node_span

F = TypeVar("F", bound=Callable[..., Any])


def observe_node(name: str | None = None) -> Callable[[F], F]:
    """Wrap a LangGraph node with node-level span and run context binding."""

    def decorator(fn: F) -> F:
        node_name = name or fn.__name__.replace("_agent", "").replace("_node", "")

        @functools.wraps(fn)
        async def async_wrapper(state: dict, *args: Any, **kwargs: Any) -> dict:
            run_id = str(state.get("run_id") or state.get("thread_id") or "")
            trace_id = str(state.get("trace_id") or run_id)
            set_run_context(run_id or None, agent_name=node_name, trace_id=trace_id or None)
            bind_trace_context(run_id=run_id or None, trace_id=trace_id or None, node=node_name)
            input_meta = {
                "run_id": run_id,
                "status_in": state.get("status"),
                "has_error": bool(state.get("error")),
            }
            with node_span(node_name, **{k: v for k, v in input_meta.items() if v}):
                result = await fn(state, *args, **kwargs)
            if isinstance(result, dict) and result.get("error"):
                bind_trace_context(node_error=result.get("error"))
            return result

        @functools.wraps(fn)
        def sync_wrapper(state: dict, *args: Any, **kwargs: Any) -> dict:
            raise TypeError(f"{node_name} must be async for observe_node")

        if inspect.iscoroutinefunction(fn):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator
