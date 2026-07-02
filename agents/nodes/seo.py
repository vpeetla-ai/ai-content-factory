"""SEO Agent — keywords, hooks, hashtags."""

import json

from agents.context import set_run_context
from agents.llm import call_llm
from agents.observability import observe_node
from agents.state import ContentFactoryState

SEO_SYSTEM = """You are an SEO and social optimization expert.
Output JSON: {
  "keywords": ["kw1", "kw2"],
  "hooks": ["hook1", "hook2"],
  "hashtags": ["#tag1", "#tag2"]
}"""


@observe_node("seo")
async def seo_agent(state: ContentFactoryState) -> dict:
    set_run_context(state.get("run_id", ""), "seo")
    topic = state["topic"]
    drafts = state.get("platform_drafts", {})

    try:
        raw = await call_llm(
            "seo",
            SEO_SYSTEM,
            f"Topic: {topic}\nDrafts summary: {json.dumps(drafts)[:2000]}",
            temperature=0.5,
        )
        try:
            seo_data = json.loads(raw)
        except json.JSONDecodeError:
            seo_data = {"keywords": [], "hooks": [], "hashtags": []}

        return {"seo_data": seo_data, "error": None}
    except Exception as exc:
        return {"error": f"SEO agent failed: {exc}"}
