"""AegisAI governance gateway — authorize publish side effects."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

PUBLISH_TOOLS = {
    "linkedin": "publish.linkedin",
    "x": "publish.x",
    "medium": "publish.medium",
    "substack": "publish.substack",
    "instagram": "publish.instagram",
}


@dataclass(frozen=True)
class GatewayAuthz:
    allowed: bool
    requires_approval: bool
    blocked: bool
    decision: str
    reason: str
    case_id: str | None = None
    raw: dict[str, Any] | None = None


def gateway_enabled() -> bool:
    settings = get_settings()
    return bool(settings.aegisai_api_base_url and settings.aegisai_gateway_enabled)


async def authorize_tool(
    *,
    tool_name: str,
    action_type: str,
    target_system: str,
    case_id: str | None = None,
    customer_impact: bool = True,
) -> GatewayAuthz:
    settings = get_settings()
    if not gateway_enabled():
        return GatewayAuthz(
            allowed=True,
            requires_approval=False,
            blocked=False,
            decision="allow",
            reason="gateway_disabled",
        )

    payload = {
        "tenant_id": settings.aegisai_tenant_id,
        "agent_id": settings.aegisai_agent_id,
        "principal_id": settings.aegisai_principal_id,
        "tool_name": tool_name,
        "action_type": action_type,
        "target_system": target_system,
        "amount_usd": 0.0,
        "data_classification": "public",
        "reversible": False,
        "customer_impact": customer_impact,
        "grounding_score": 0.9,
        "safety_score": 0.92,
        "policy_compliance_score": 0.9,
        "case_id": case_id,
        "proposal_id": case_id,
    }
    headers = {"Content-Type": "application/json"}
    if settings.aegisai_auth_bearer:
        headers["Authorization"] = f"Bearer {settings.aegisai_auth_bearer}"
    headers["X-AegisAI-Principal"] = settings.aegisai_principal_id
    headers["X-AegisAI-Tenant"] = settings.aegisai_tenant_id
    headers["X-AegisAI-Roles"] = settings.aegisai_roles

    url = f"{settings.aegisai_api_base_url.rstrip('/')}/api/gateway/tool-request"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # noqa: BLE001
        logger.warning("AegisAI gateway unreachable: %s", exc)
        if settings.aegisai_gateway_fail_open:
            return GatewayAuthz(
                allowed=True,
                requires_approval=False,
                blocked=False,
                decision="allow",
                reason=f"gateway_error_fail_open:{exc}",
            )
        return GatewayAuthz(
            allowed=False,
            requires_approval=False,
            blocked=True,
            decision="block",
            reason=f"gateway_error:{exc}",
        )

    decision = str(data.get("gateway_decision", "block"))
    token = data.get("execution_token")
    allowed = decision == "allow" and bool(token)
    requires_approval = decision == "approval_required"
    blocked = decision in {"block", "deny", "frozen"}
    return GatewayAuthz(
        allowed=allowed,
        requires_approval=requires_approval,
        blocked=blocked,
        decision=decision,
        reason=str(data.get("business_explanation", decision)),
        case_id=str(data.get("case_id") or case_id or ""),
        raw=data,
    )


async def authorize_publish(platform: str, *, case_id: str) -> GatewayAuthz:
    tool_name = PUBLISH_TOOLS.get(platform, f"publish.{platform}")
    return await authorize_tool(
        tool_name=tool_name,
        action_type="publish_post",
        target_system=platform,
        case_id=case_id,
        customer_impact=True,
    )
