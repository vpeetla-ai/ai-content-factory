"""Trace-linked observability — logs, spans, and eval scores on one execution path."""

from .context import (
    bind_trace_context,
    clear_trace_context,
    get_agent_name,
    get_request_id,
    get_root_trace_id,
    get_run_id,
    get_trace_id,
    set_run_context,
)
from .export import export_trace_summary
from .recorder import SpanEvent, TraceRecorder, get_recorder, set_recorder
from .spans import eval_score, node_span, system_span, trace_span

__all__ = [
    "SpanEvent",
    "TraceRecorder",
    "bind_trace_context",
    "clear_trace_context",
    "eval_score",
    "export_trace_summary",
    "get_agent_name",
    "get_recorder",
    "get_request_id",
    "get_root_trace_id",
    "get_run_id",
    "get_trace_id",
    "node_span",
    "set_recorder",
    "set_run_context",
    "system_span",
    "trace_span",
]
