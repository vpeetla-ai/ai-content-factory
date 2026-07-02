"""Execution context — run_id, trace_id, request_id propagated across HTTP → graph → LLM."""

from __future__ import annotations

import contextvars
from typing import Any

run_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("run_id", default=None)
trace_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
root_trace_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("root_trace_id", default=None)
request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)
agent_name_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("agent_name", default=None)
service_name_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("service_name", default=None)


def set_run_context(
    run_id: str | None,
    *,
    agent_name: str | None = None,
    trace_id: str | None = None,
) -> None:
    if run_id is not None:
        run_id_var.set(run_id)
    if agent_name is not None:
        agent_name_var.set(agent_name)
    if trace_id is not None:
        trace_id_var.set(trace_id)
        if root_trace_id_var.get() is None:
            root_trace_id_var.set(trace_id)


def get_run_id() -> str | None:
    return run_id_var.get()


def get_trace_id() -> str | None:
    return trace_id_var.get() or run_id_var.get()


def get_root_trace_id() -> str | None:
    return root_trace_id_var.get() or get_trace_id()


def get_request_id() -> str | None:
    return request_id_var.get()


def get_agent_name() -> str | None:
    return agent_name_var.get()


def bind_trace_context(
    *,
    run_id: str | None = None,
    trace_id: str | None = None,
    root_trace_id: str | None = None,
    request_id: str | None = None,
    service: str | None = None,
    **extra: Any,
) -> None:
    """Bind IDs to contextvars and structlog (when installed)."""
    if run_id is not None:
        run_id_var.set(run_id)
    if trace_id is not None:
        trace_id_var.set(trace_id)
    if root_trace_id is not None:
        root_trace_id_var.set(root_trace_id)
    elif trace_id is not None and root_trace_id_var.get() is None:
        root_trace_id_var.set(trace_id)
    if request_id is not None:
        request_id_var.set(request_id)
    if service is not None:
        service_name_var.set(service)

    payload = {
        k: v
        for k, v in {
            "run_id": run_id or run_id_var.get(),
            "trace_id": trace_id or trace_id_var.get(),
            "root_trace_id": root_trace_id_var.get(),
            "request_id": request_id or request_id_var.get(),
            "service": service or service_name_var.get(),
            **extra,
        }.items()
        if v is not None
    }
    if not payload:
        return
    try:
        import structlog

        structlog.contextvars.bind_contextvars(**payload)
    except Exception:
        pass


def clear_trace_context() -> None:
    for var in (
        run_id_var,
        trace_id_var,
        root_trace_id_var,
        request_id_var,
        agent_name_var,
        service_name_var,
    ):
        var.set(None)
    try:
        import structlog

        structlog.contextvars.clear_contextvars()
    except Exception:
        pass
