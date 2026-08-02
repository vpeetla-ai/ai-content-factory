"""Content Agent — platform-specific drafts + rubric scores."""

import json

from agents.context import set_run_context
from agents.llm import call_llm
from agents.observability import observe_node
from agents.quality import score_platform_drafts
from agents.state import ContentFactoryState

PLATFORMS = ["linkedin", "substack", "medium", "x", "instagram"]

CONTENT_SYSTEM = """You are a multi-platform content writer.
Given a research brief, write platform-optimized drafts.
Output JSON: {
  "linkedin": {"content": "...", "hook": "..."},
  "substack": {"content": "...", "hook": "..."},
  "medium": {"content": "...", "hook": "..."},
  "x": {"content": "...", "hook": "..."},
  "instagram": {"content": "...", "hook": "..."}
}
Respect platform character limits and tone. Include a clear hook and a soft CTA per platform."""


@observe_node("content")
async def content_agent(state: ContentFactoryState) -> dict:
    set_run_context(state.get("run_id", ""), "content")
    topic = state["topic"]
    brief = state.get("research_brief", "")
    platforms = state.get("platforms", PLATFORMS)

    try:
        raw = await call_llm(
            "content",
            CONTENT_SYSTEM,
            f"Topic: {topic}\n\nResearch:\n{brief}\n\nPlatforms: {', '.join(platforms)}",
            temperature=0.8,
        )
        try:
            drafts = json.loads(raw)
        except json.JSONDecodeError:
            drafts = {p: {"content": raw, "hook": ""} for p in platforms}

        quality_scores = score_platform_drafts(
            {p: drafts[p] for p in platforms if p in drafts}
        )
        return {
            "platform_drafts": drafts,
            "quality_scores": quality_scores,
            "error": None,
        }
    except Exception as exc:
        return {"error": f"Content agent failed: {exc}"}
