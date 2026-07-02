"""In-process trace recorder — diagnostic events linked to eval scores."""

from __future__ import annotations

import contextvars
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

SpanLevel = Literal["system", "trace", "node"]

recorder_var: contextvars.ContextVar[TraceRecorder | None] = contextvars.ContextVar(
    "trace_recorder", default=None
)


@dataclass
class SpanEvent:
    level: SpanLevel
    name: str
    started_at: float
    duration_ms: int = 0
    status: str = "ok"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceRecorder:
    """Collects span events and eval scores for one workflow run."""

    trace_id: str
    run_id: str
    service: str = "agent-service"
    events: list[SpanEvent] = field(default_factory=list)
    eval_scores: dict[str, float | int | bool | str] = field(default_factory=dict)
    _langfuse_trace: Any | None = field(default=None, repr=False)

    @classmethod
    def create(cls, *, run_id: str | None = None, trace_id: str | None = None, service: str = "agent-service") -> TraceRecorder:
        rid = run_id or str(uuid.uuid4())
        tid = trace_id or rid
        return cls(trace_id=tid, run_id=rid, service=service)

    def ensure_langfuse_root(self, name: str, *, metadata: dict[str, Any] | None = None) -> None:
        if self._langfuse_trace is not None:
            return
        try:
            from .export import get_langfuse_client

            client = get_langfuse_client()
            if client is None:
                return
            self._langfuse_trace = client.trace(
                id=self.trace_id,
                name=name,
                session_id=self.run_id,
                metadata={"run_id": self.run_id, "service": self.service, **(metadata or {})},
            )
        except Exception:
            self._langfuse_trace = None

    def record_eval(self, name: str, value: float | int | bool | str, **metadata: Any) -> None:
        self.eval_scores[name] = value
        self.events.append(
            SpanEvent(
                level="trace",
                name=f"eval.{name}",
                started_at=time.time(),
                duration_ms=0,
                metadata={"value": value, **metadata},
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "service": self.service,
            "eval_scores": self.eval_scores,
            "events": [
                {
                    "level": e.level,
                    "name": e.name,
                    "duration_ms": e.duration_ms,
                    "status": e.status,
                    "metadata": e.metadata,
                }
                for e in self.events
            ],
        }


def set_recorder(recorder: TraceRecorder | None) -> None:
    recorder_var.set(recorder)


def get_recorder() -> TraceRecorder | None:
    return recorder_var.get()
