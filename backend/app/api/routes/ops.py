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
    metrics["extra"] = extra
    return metrics
