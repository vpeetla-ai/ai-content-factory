"""Tests for AegisAI gateway authorization on publish paths."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.integrations.aegis_gateway import GatewayAuthz, authorize_publish, gateway_enabled


def test_gateway_disabled_by_default_in_test_env():
    assert gateway_enabled() is False


@pytest.mark.asyncio
async def test_authorize_publish_fail_open_when_disabled():
    authz = await authorize_publish("linkedin", case_id="case-1")
    assert authz.allowed is True
    assert authz.decision == "allow"
    assert authz.reason == "gateway_disabled"


@pytest.mark.asyncio
async def test_production_strict_blocks_when_gateway_disabled():
    """ADR-024: PRODUCTION_STRICT requires a configured gateway for publish."""
    with patch("app.integrations.aegis_gateway.get_settings") as mock_settings:
        settings = mock_settings.return_value
        settings.aegisai_api_base_url = ""
        settings.aegisai_gateway_enabled = True
        settings.aegisai_gateway_fail_open = True
        settings.production_strict = True
        with patch("app.integrations.aegis_gateway.gateway_enabled", return_value=False):
            authz = await authorize_publish("linkedin", case_id="case-strict")
    assert authz.allowed is False
    assert authz.blocked is True
    assert authz.reason == "production_strict_gateway_required"


@pytest.mark.asyncio
async def test_authorize_publish_blocks_on_gateway_deny():
    with patch("app.integrations.aegis_gateway.gateway_enabled", return_value=True):
        with patch("app.integrations.aegis_gateway.get_settings") as mock_settings:
            settings = mock_settings.return_value
            settings.aegisai_api_base_url = "https://aegis.example"
            settings.aegisai_gateway_enabled = True
            settings.aegisai_gateway_fail_open = False
            settings.aegisai_tenant_id = "t1"
            settings.aegisai_agent_id = "acf"
            settings.aegisai_principal_id = "p1"
            settings.aegisai_roles = "editor"
            settings.aegisai_auth_bearer = ""

            mock_response = AsyncMock()
            mock_response.raise_for_status = lambda: None
            mock_response.json = lambda: {
                "gateway_decision": "block",
                "business_explanation": "policy_violation",
                "case_id": "case-1",
            }

            with patch("httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
                authz = await authorize_publish("linkedin", case_id="case-1")

    assert authz.blocked is True
    assert authz.allowed is False


@pytest.mark.asyncio
async def test_publisher_service_respects_gateway_block():
    import uuid

    from app.models import ContentDraft, Platform
    from app.services.publisher import PublishBlockedError, PublisherService

    run_id = uuid.uuid4()
    draft = ContentDraft(
        id=uuid.uuid4(),
        run_id=run_id,
        platform=Platform.linkedin,
        draft_content="Hello",
        edited_content=None,
    )

    with patch(
        "app.services.publisher.authorize_publish",
        new_callable=AsyncMock,
        return_value=GatewayAuthz(
            allowed=False,
            requires_approval=False,
            blocked=True,
            decision="block",
            reason="test_block",
        ),
    ):
        svc = PublisherService()
        with pytest.raises(PublishBlockedError, match="test_block"):
            await svc.publish_draft(draft, case_id="case-1")
