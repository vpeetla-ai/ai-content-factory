"""Tests for draft quality rubrics and publish intents."""

from __future__ import annotations

import pytest

from agents.nodes.publish import publisher_agent
from agents.quality import score_draft, score_platform_drafts


def test_score_draft_linkedin_pass():
    result = score_draft(
        "linkedin",
        {
            "hook": "Most AI demos skip the gateway.",
            "content": (
                "Most AI demos skip the gateway. Here is why governed publish matters "
                "for content teams shipping to LinkedIn. Comment with your stack "
                "and I will share the checklist."
            ),
        },
    )
    assert result["pass"] is True
    assert result["score"] == 1.0


def test_score_draft_x_too_long():
    result = score_draft("x", {"content": "x" * 300, "hook": ""})
    assert result["pass"] is False
    assert any(i.startswith("too_long") for i in result["issues"])


def test_score_platform_drafts_keys():
    scores = score_platform_drafts(
        {
            "x": {"content": "Short but enough for X? http://example.com", "hook": ""},
            "linkedin": {"content": "tiny", "hook": ""},
        }
    )
    assert "x" in scores and "linkedin" in scores
    assert scores["linkedin"]["pass"] is False


@pytest.mark.asyncio
async def test_publish_emits_intents_not_fake_urls(sample_state):
    sample_state["hitl_approved"] = {
        "linkedin": {"approved": True},
        "x": {"approved": False, "skip": True},
    }
    sample_state["hitl_edits"] = {"linkedin": "Human-edited final copy"}
    result = await publisher_agent(sample_state)  # type: ignore[arg-type]
    published = result["published_results"]
    assert "linkedin" in published
    assert "x" not in published
    assert published["linkedin"]["pending_adapter"] is True
    assert published["linkedin"]["status"] == "selected"
    assert "Human-edited" in published["linkedin"]["content_preview"]
    assert "url" not in published["linkedin"]
    assert "post_id" not in published["linkedin"]
