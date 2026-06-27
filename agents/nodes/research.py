"""Research Agent — Gemini 2.5 Flash + research cache."""

import hashlib
import json

from agents.context import set_run_context
from agents.llm import call_llm
from agents.state import ContentFactoryState
from app.core.config import get_settings
from app.core.redis import get_redis
from app.core.redis_keys import RESEARCH_CACHE

RESEARCH_SYSTEM = """You are a research analyst for a multi-platform content factory.
Produce a structured research brief with: key facts, trends, audience angles, and citations.
Output JSON: {"brief": "...", "sources": ["..."], "angles": ["..."]}"""


async def _fetch_external_sources(topic: str) -> str:
    """Tool stubs: web_search, arXiv, Semantic Scholar (local dev placeholders)."""
    return (
        f"[web_search] Recent articles on '{topic}'\n"
        f"[arxiv] Related papers tagged {topic.replace(' ', '+')}\n"
        f"[semantic_scholar] Citation graph summary for {topic}"
    )


async def research_agent(state: ContentFactoryState) -> dict:
    topic = state["topic"]
    run_id = state.get("run_id", "")
    set_run_context(run_id, "research")

    settings = get_settings()
    redis = get_redis()
    topic_hash = hashlib.sha256(topic.encode()).hexdigest()[:16]
    cache_key = RESEARCH_CACHE.format(topic_hash=topic_hash)

    cached = await redis.get(cache_key)
    if cached:
        return {"research_brief": cached, "error": None}

    try:
        sources = await _fetch_external_sources(topic)
        raw = await call_llm(
            "research",
            RESEARCH_SYSTEM,
            f"Topic: {topic}\n\nExternal sources:\n{sources}",
            temperature=0.3,
        )
        try:
            parsed = json.loads(raw)
            brief = parsed.get("brief", raw)
        except json.JSONDecodeError:
            brief = raw

        await redis.setex(cache_key, settings.research_cache_ttl, brief)
        return {"research_brief": brief, "error": None}
    except Exception as exc:
        return {"error": f"Research agent failed: {exc}"}
