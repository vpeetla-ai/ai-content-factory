"""Visual Agent — image prompt generation + optional R2 media cards."""

import json

from agents.context import set_run_context
from agents.llm import call_llm
from agents.observability import observe_node
from agents.state import ContentFactoryState


VISUAL_SYSTEM = """You generate image prompts for social content.
Output JSON: {"prompts": ["prompt1", "prompt2", "prompt3"]}
Style: modern, professional, platform-ready. No text in images."""


@observe_node("visual")
async def visual_agent(state: ContentFactoryState) -> dict:
    set_run_context(state.get("run_id", ""), "visual")
    topic = state["topic"]
    brief = state.get("research_brief", "")
    run_id = state.get("run_id", "")

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

        media_assets: list = []
        try:
            from app.services.media_assets import materialize_media_assets

            media_assets = await materialize_media_assets(
                run_id=run_id,
                topic=topic,
                prompts=prompts if isinstance(prompts, list) else [str(prompts)],
            )
        except Exception:
            media_assets = []

        return {"image_prompts": prompts, "media_assets": media_assets, "error": None}
    except Exception as exc:
        return {"error": f"Visual agent failed: {exc}"}
