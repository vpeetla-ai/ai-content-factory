"""Enrich node — runs Visual + SEO agents in parallel."""

import asyncio

from agents.context import set_run_context
from agents.nodes.seo import seo_agent
from agents.nodes.visual import visual_agent
from agents.observability import observe_node
from agents.state import ContentFactoryState


@observe_node("enrich")
async def enrich_node(state: ContentFactoryState) -> dict:
    visual_result, seo_result = await asyncio.gather(
        visual_agent(state),
        seo_agent(state),
    )
    merged: dict = {}
    for result in (visual_result, seo_result):
        if result.get("error"):
            merged["error"] = result["error"]
        merged.update({k: v for k, v in result.items() if k != "error" or "error" not in merged})
    return merged
