"""Content Agent — platform-specific drafts."""

import json

from agents.context import set_run_context
from agents.llm import call_llm
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
Respect platform character limits and tone."""


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

        return {"platform_drafts": drafts, "error": None}
    except Exception as exc:
        return {"error": f"Content agent failed: {exc}"}
