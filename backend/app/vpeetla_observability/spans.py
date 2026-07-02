"""Span context managers — system, trace, and node levels."""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Any, Iterator

from .context import bind_trace_context
from .recorder import SpanEvent, get_recorder

logger = logging.getLogger("vpeetla_observability")


def _log_span_event(event: str, level: str, name: str, **fields: Any) -> None:
    payload = {"span_level": level, "span_name": name, **fields}
    try:
        import structlog

        structlog.get_logger("vpeetla_observability").info(event, **payload)
    except Exception:
        logger.info("%s %s", event, payload)


@contextmanager
def system_span(name: str, **metadata: Any) -> Iterator[None]:
    with _span("system", name, metadata) as _:
        yield


@contextmanager
def trace_span(name: str, **metadata: Any) -> Iterator[None]:
    with _span("trace", name, metadata) as _:
        yield


@contextmanager
def node_span(name: str, **metadata: Any) -> Iterator[None]:
    with _span("node", name, metadata) as _:
        yield


@contextmanager
def eval_score(name: str, value: float | int | bool | str, **metadata: Any) -> Iterator[None]:
    recorder = get_recorder()
    _log_span_event("eval_recorded", "trace", f"eval.{name}", value=value, **metadata)
    if recorder is not None:
        recorder.record_eval(name, value, **metadata)
    try:
        from .export import score_langfuse

        score_langfuse(name=name, value=value, comment=str(metadata) if metadata else None)
    except Exception:
        pass
    yield


@contextmanager
def _span(level: str, name: str, metadata: dict[str, Any]) -> Iterator[None]:
    started = time.monotonic()
    wall = time.time()
    bind_trace_context(span_level=level, span_name=name)
    _log_span_event("span_start", level, name, **metadata)
    langfuse_obs = None
    recorder = get_recorder()
    try:
        from .export import start_langfuse_span

        langfuse_obs = start_langfuse_span(name, level=level, metadata=metadata)
        if langfuse_obs is not None:
            langfuse_obs.__enter__()
    except Exception:
        langfuse_obs = None

    status = "ok"
    error: str | None = None
    try:
        yield
    except Exception as exc:
        status = "error"
        error = str(exc)
        raise
    finally:
        duration_ms = int((time.monotonic() - started) * 1000)
        end_meta = {**metadata, "duration_ms": duration_ms}
        if error:
            end_meta["error"] = error
        _log_span_event("span_end", level, name, status=status, **end_meta)
        if recorder is not None:
            recorder.events.append(
                SpanEvent(
                    level=level,  # type: ignore[arg-type]
                    name=name,
                    started_at=wall,
                    duration_ms=duration_ms,
                    status=status,
                    metadata=end_meta,
                )
            )
        if langfuse_obs is not None:
            try:
                langfuse_obs.__exit__(None, None, None)
            except Exception:
                pass
