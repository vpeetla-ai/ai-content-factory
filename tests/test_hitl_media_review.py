"""HITL review payload includes media + quality fields from state_snapshot."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models import PipelineStatus
from app.services.hitl import HITLService


@pytest.mark.asyncio
async def test_get_review_includes_media_and_quality():
    run_id = uuid.uuid4()
    run = MagicMock()
    run.id = run_id
    run.status = PipelineStatus.hitl_wait
    run.state_snapshot = {
        "media_assets": [{"url": "https://cdn.example/card.svg", "prompt": "navy diagram"}],
        "image_prompts": ["navy diagram"],
        "quality_scores": {"linkedin": {"pass": True, "score": 1.0, "issues": []}},
        "research_meta": {
            "cache_hit": False,
            "enterprise_rag": {"configured": True, "used": True, "cite_count": 2},
        },
    }

    draft = MagicMock()
    draft.id = uuid.uuid4()
    draft.platform = MagicMock(value="linkedin")
    draft.draft_content = "Body"
    draft.edited_content = None
    draft.seo_keywords = None
    draft.hashtags = None
    draft.hook_variant = "Hook"
    draft.char_count = 4

    db = MagicMock()
    run_result = MagicMock()
    run_result.scalar_one_or_none.return_value = run
    drafts_result = MagicMock()
    drafts_result.scalars.return_value.all.return_value = [draft]
    db.execute = AsyncMock(side_effect=[run_result, drafts_result])

    with patch("app.services.hitl.PipelineService"):
        review = await HITLService(db).get_review(run_id)

    assert review is not None
    assert review["media_assets"][0]["url"].endswith("card.svg")
    assert review["image_prompts"] == ["navy diagram"]
    assert review["quality_scores"]["linkedin"]["pass"] is True
    assert review["research_meta"]["enterprise_rag"]["used"] is True
    assert review["drafts"][0]["platform"] == "linkedin"
