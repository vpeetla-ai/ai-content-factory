"""Langfuse export — root trace, nested spans, eval scores."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator

_langfuse_client: Any | None = None


def get_langfuse_client() -> Any | None:
    global _langfuse_client
    if _langfuse_client is not None:
        return _langfuse_client
    public = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    secret = os.environ.get("LANGFUSE_SECRET_KEY", "")
    if not public or not secret:
        return None
    enabled = os.environ.get("LANGFUSE_ENABLED", "true").lower() not in {"0", "false", "no"}
    if not enabled:
        return None
    try:
        from langfuse import Langfuse

        _langfuse_client = Langfuse(
            public_key=public,
            secret_key=secret,
            host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            environment=os.environ.get("APP_ENV", os.environ.get("ENVIRONMENT", "development")),
        )
        return _langfuse_client
    except Exception:
        return None


def configure_langfuse(client: Any | None) -> None:
    global _langfuse_client
    _langfuse_client = client


@contextmanager
def start_langfuse_span(name: str, *, level: str = "node", metadata: dict[str, Any] | None = None) -> Iterator[Any]:
    client = get_langfuse_client()
    if client is None:
        yield None
        return
    try:
        from .context import get_root_trace_id

        trace_id = get_root_trace_id()
        with client.start_as_current_observation(
            as_type="span",
            name=f"{level}.{name}",
            input=metadata or {},
            trace_context={"trace_id": trace_id} if trace_id else None,
        ) as observation:
            yield observation
    except Exception:
        yield None


def score_langfuse(*, name: str, value: float | int | bool | str, comment: str | None = None) -> None:
    client = get_langfuse_client()
    if client is None:
        return
    try:
        from .context import get_root_trace_id

        trace_id = get_root_trace_id()
        if not trace_id:
            return
        numeric = float(value) if isinstance(value, bool) else value
        if isinstance(value, bool):
            numeric = 1.0 if value else 0.0
        client.score(trace_id=trace_id, name=name, value=numeric, comment=comment)
    except Exception:
        pass


def export_trace_summary(recorder: Any, *, trace_name: str = "workflow.run") -> dict[str, Any]:
    """Flush eval scores and span summary to Langfuse."""
    status: dict[str, Any] = {"langfuse": False, "events": len(recorder.events), "eval_scores": recorder.eval_scores}
    recorder.ensure_langfuse_root(trace_name, metadata={"eval_count": len(recorder.eval_scores)})
    for name, value in recorder.eval_scores.items():
        score_langfuse(name=name, value=value)
    client = get_langfuse_client()
    if client is not None:
        try:
            client.flush()
            status["langfuse"] = True
        except Exception:
            pass
    return status
