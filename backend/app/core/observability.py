"""Production observability bootstrap — Sentry, LangSmith, Langfuse, OpenTelemetry."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from app.core.config import get_settings
from app.core.logging import get_logger

if TYPE_CHECKING:
    from langfuse import Langfuse

logger = get_logger(__name__)

_langfuse_client: Langfuse | None = None
_initialized = False


def init_observability() -> None:
    """Call once at application startup."""
    global _initialized, _langfuse_client
    if _initialized:
        return
    _initialized = True

    settings = get_settings()
    _init_sentry(settings)
    _init_langsmith(settings)
    _langfuse_client = _init_langfuse(settings)
    _init_opentelemetry(settings)

    logger.info(
        "observability_initialized",
        app_env=settings.app_env,
        langsmith=settings.langsmith_enabled,
        langfuse=settings.langfuse_configured,
        sentry=bool(settings.sentry_dsn),
    )


def _init_sentry(settings) -> None:
    if not settings.sentry_dsn:
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.app_env,
            traces_sample_rate=settings.sentry_traces_sample_rate,
            integrations=[FastApiIntegration(), SqlalchemyIntegration()],
            send_default_pii=False,
        )
    except Exception as exc:
        logger.warning("sentry_init_failed", error=str(exc))


def _init_langsmith(settings) -> None:
    if not settings.langsmith_enabled:
        return
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_TRACING"] = "true"


def _init_langfuse(settings) -> Langfuse | None:
    if not settings.langfuse_configured:
        return None
    try:
        from langfuse import Langfuse

        client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
            environment=settings.app_env,
        )
        return client
    except Exception as exc:
        logger.warning("langfuse_init_failed", error=str(exc))
        return None


def _init_opentelemetry(settings) -> None:
    if not settings.otel_exporter_otlp_endpoint:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        resource = Resource.create({"service.name": settings.app_name, "deployment.environment": settings.app_env})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint))
        )
        trace.set_tracer_provider(provider)
    except Exception as exc:
        logger.warning("otel_init_failed", error=str(exc))


def get_langfuse() -> Langfuse | None:
    return _langfuse_client


def flush_observability() -> None:
    if _langfuse_client is not None:
        try:
            _langfuse_client.flush()
        except Exception:
            pass
