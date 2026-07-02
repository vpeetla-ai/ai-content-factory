"""FastAPI middleware — propagate request_id and trace_id into agent runs."""

from __future__ import annotations

import logging
import time
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .context import bind_trace_context, clear_trace_context

logger = logging.getLogger("vpeetla_observability")


class TraceRequestMiddleware(BaseHTTPMiddleware):
  """Attach X-Request-Id / X-Trace-Id and bind structured log context per HTTP request."""

  def __init__(self, app, *, service_name: str = "api") -> None:
    super().__init__(app)
    self.service_name = service_name

  async def dispatch(self, request: Request, call_next: Callable) -> Response:
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    trace_id = request.headers.get("x-trace-id") or request_id
    bind_trace_context(
      request_id=request_id,
      trace_id=trace_id,
      root_trace_id=trace_id,
      service=self.service_name,
      http_method=request.method,
      http_path=request.url.path,
    )
    started = time.monotonic()
    try:
      import structlog

      structlog.get_logger("http").info(
        "request_started",
        request_id=request_id,
        trace_id=trace_id,
        method=request.method,
        path=request.url.path,
      )
    except Exception:
      logger.info("request_started %s %s", request.method, request.url.path)

    try:
      response = await call_next(request)
    except Exception as exc:
      try:
        import structlog

        structlog.get_logger("http").exception(
          "request_failed",
          request_id=request_id,
          trace_id=trace_id,
          error=str(exc),
        )
      except Exception:
        logger.exception("request_failed")
      clear_trace_context()
      raise

    duration_ms = int((time.monotonic() - started) * 1000)
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Trace-Id"] = trace_id
    try:
      import structlog

      structlog.get_logger("http").info(
        "request_completed",
        request_id=request_id,
        trace_id=trace_id,
        status_code=response.status_code,
        duration_ms=duration_ms,
      )
    except Exception:
      logger.info("request_completed status=%s duration_ms=%s", response.status_code, duration_ms)
    clear_trace_context()
    return response
