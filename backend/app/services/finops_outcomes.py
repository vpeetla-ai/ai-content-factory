"""Record pipeline outcomes to agent-finops (ADR-029)."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def record_pipeline_outcome(
    *,
    workflow_id: str,
    status: str,
    total_cost_usd: float = 0.0,
    hitl_was_required: bool = False,
    hitl_approved: bool = True,
) -> dict[str, Any] | None:
    settings = get_settings()
    base = (settings.agentfinops_url or "").strip()
    if not base:
        return None
    done = status == "done"
    payload = {
        "workflow_id": workflow_id,
        "tenant_id": settings.llm_gateway_tenant_id or "ai-content-factory",
        "eval_pass": done,
        "policy_deny": False,
        "hitl_required": hitl_was_required,
        "hitl_approved": hitl_approved if hitl_was_required else True,
        "budget_ok": True,
        "total_cost_usd": float(total_cost_usd or 0),
    }
    headers = {"Content-Type": "application/json"}
    if settings.agentfinops_api_key:
        headers["X-API-Key"] = settings.agentfinops_api_key
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(f"{base.rstrip('/')}/v1/outcomes", json=payload, headers=headers)
            r.raise_for_status()
            return r.json()
    except Exception as exc:  # noqa: BLE001
        logger.warning("finops_outcome_record_failed: %s", exc)
        return {"error": str(exc), "payload": payload}
