"""Public ops metrics — anonymized aggregates for portfolio / SLO dashboard."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.services.ops_metrics import collect_ops_metrics

router = APIRouter(prefix="/ops", tags=["Operations"])


@router.get("/metrics")
async def ops_metrics(db: Annotated[AsyncSession, Depends(get_db)]):
    """Anonymized pipeline metrics — no PII, safe for public landing page."""
    metrics = await collect_ops_metrics(db)
    settings = get_settings()
    gateway_on = bool((settings.llm_gateway_url or "").strip())
    extra = dict(metrics.get("extra") or {})
    extra["llm_gateway"] = {
        "enabled": gateway_on,
        "url_configured": gateway_on,
        "tenant_id": settings.llm_gateway_tenant_id if gateway_on else None,
        "plane": "aegis-llm-gateway",
    }
    extra["enterprise_rag"] = {
        "configured": bool((settings.enterprise_rag_api_url or "").strip()),
        "compose": "research_node",
        "fail_soft": True,
    }
    extra["r2_media"] = {
        "configured": bool(
            settings.r2_account_id
            and settings.r2_access_key_id
            and settings.r2_secret_access_key
            and settings.r2_public_url
        ),
    }
    extra["schedule"] = {
        "enabled": settings.cron_pipeline_enabled,
        "cron": settings.cron_schedule,
        "timezone": "UTC",
        "mutation": "env_only",
    }
    metrics["extra"] = extra
    return metrics


@router.get("/schedule")
async def ops_schedule():
    """Product-facing view of the cron schedule (env-configured today).

    Month-3 depth: expose schedule as a first-class surface instead of
    ops-only env vars. Mutations remain env/dashboard until HITL calendar UI.
    """
    settings = get_settings()
    return {
        "enabled": settings.cron_pipeline_enabled,
        "cron": settings.cron_schedule,
        "topic": settings.cron_topic,
        "platforms": settings.cron_platform_list(),
        "timezone": "UTC",
        "mutation": "env_only",
        "note": "Enable via CRON_PIPELINE_ENABLED; gateway authorizes schedule_pipeline.",
    }


@router.get("/observability/status")
async def observability_status():
    """Compose-plane honesty for ACF — publish path vs LLM/RAG planes."""
    settings = get_settings()
    gateway_on = bool((settings.llm_gateway_url or "").strip())
    return {
        "source_of_truth": (
            "ACF Postgres pipeline/trace tables for content runs; "
            "AegisAI authorizes publish side effects when wired"
        ),
        "exporters": [
            {
                "name": "OpsMetrics",
                "state": "live",
                "detail": "GET /api/v1/ops/metrics — anonymized aggregates + compose planes",
            },
            {
                "name": "Langfuse",
                "state": "configured" if settings.langfuse_configured else "unconfigured",
                "detail": "Optional trace export — not the publish/HITL ledger",
            },
        ],
        "planes": {
            "llm_gateway": {
                "enabled": gateway_on,
                "plane": "aegis-llm-gateway",
            },
            "enterprise_rag": {
                "configured": bool((settings.enterprise_rag_api_url or "").strip()),
                "compose": "research_node",
                "fail_soft": True,
            },
            "aegisai_gateway": {
                "configured": bool(settings.aegisai_api_base_url),
                "plane": "publish_side_effects",
            },
            "langfuse": {"configured": settings.langfuse_configured},
            "langsmith": {"enabled": settings.langsmith_enabled},
            "schedule": {
                "enabled": settings.cron_pipeline_enabled,
                "mutation": "env_only",
            },
            "production_strict": settings.production_strict,
            "mock_llm": settings.mock_llm,
        },
        "recommendation": (
            "Unauthenticated golden path stops at /health for ACF. "
            "Live publish requires Clerk + gateway/HITL — Medium/Substack/IG stay copy-draft."
        ),
    }
