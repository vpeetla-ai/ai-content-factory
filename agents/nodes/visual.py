"""Visual Agent — image prompt generation."""

import json

from agents.context import set_run_context
from agents.llm import call_llm
from agents.state import ContentFactoryState

VISUAL_SYSTEM = """You generate image prompts for social content.
Output JSON: {"prompts": ["prompt1", "prompt2", "prompt3"]}
Style: modern, professional, platform-ready. No text in images."""


async def visual_agent(state: ContentFactoryState) -> dict:
    set_run_context(state.get("run_id", ""), "visual")
    topic = state["topic"]
    brief = state.get("research_brief", "")

    try:
        raw = await call_llm(
            "visual",
            VISUAL_SYSTEM,
            f"Topic: {topic}\nBrief: {brief}\nGenerate 3 image prompts.",
            temperature=0.9,
        )
        try:
            prompts = json.loads(raw).get("prompts", [raw])
        except json.JSONDecodeError:
            prompts = [raw]

        return {"image_prompts": prompts, "error": None}
    except Exception as exc:
        return {"error": f"Visual agent failed: {exc}"}
