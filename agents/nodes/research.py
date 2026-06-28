"""Research Agent — Gemini + Redis cache + Qdrant/Pinecone RAG."""

import hashlib
import json

from agents.context import set_run_context
from agents.llm import call_llm, parse_llm_json
from agents.state import ContentFactoryState
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.redis import get_redis
from app.core.redis_keys import RESEARCH_CACHE
from app.services.vector_store import search_similar, upsert_research

logger = get_logger(__name__)

RESEARCH_SYSTEM = """You are a research analyst for a multi-platform content factory.
Produce a structured research brief with: key facts, trends, audience angles, and citations.
Output JSON only: {"brief": "...", "sources": ["..."], "angles": ["..."]}"""


async def _fetch_external_sources(topic: str) -> str:
    """Augment with vector RAG hits from prior research."""
    parts = [f"[topic] {topic}"]
    try:
        similar = await search_similar(topic, limit=5)
        for i, hit in enumerate(similar, 1):
            parts.append(f"[rag_{i}] (score={hit.get('score', 0):.2f}) {hit.get('topic')}: {hit.get('brief', '')[:500]}")
    except Exception as exc:
        logger.warning("rag_search_failed", error=str(exc))
    if len(parts) == 1:
        parts.append(f"[web_search] Recent articles on '{topic}'")
    return "\n".join(parts)


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
            f"Topic: {topic}\n\nContext:\n{sources}",
            temperature=0.3,
        )
        parsed = parse_llm_json(raw)
        if parsed:
            brief = parsed.get("brief", raw)
            if isinstance(brief, dict):
                brief = json.dumps(brief)
        else:
            brief = raw

        await redis.setex(cache_key, settings.research_cache_ttl, brief)
        try:
            await upsert_research(topic, str(brief), run_id)
        except Exception as exc:
            logger.warning("vector_upsert_failed", error=str(exc))

        return {"research_brief": brief, "error": None}
    except Exception as exc:
        return {"error": f"Research agent failed: {exc}"}
