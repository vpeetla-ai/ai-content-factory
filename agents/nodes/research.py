"""Research Agent — Gemini + Redis cache + Qdrant/Pinecone RAG (+ optional ERAG)."""

import hashlib
import json

import httpx

from agents.context import set_run_context
from agents.llm import call_llm, parse_llm_json
from agents.observability import observe_node
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


async def _fetch_enterprise_rag(topic: str) -> list[str]:
    """Optional compose to Enterprise RAG (access-before-ranking). Fail soft."""
    settings = get_settings()
    base = (settings.enterprise_rag_api_url or "").rstrip("/")
    if not base:
        return []
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if settings.enterprise_rag_api_key:
        headers["X-API-Key"] = settings.enterprise_rag_api_key
        headers["Authorization"] = f"Bearer {settings.enterprise_rag_api_key}"
    url = f"{base}/v1/answer"
    payload = {
        "query": topic,
        "tenant_id": "ai-content-factory",
        "user_id": "acf-research",
        "groups": ["engineering", "content"],
        "clearance": "internal",
        "top_k": 5,
        "rerank": True,
        "agentic": False,
    }
    try:
        async with httpx.AsyncClient(timeout=settings.enterprise_rag_timeout_s) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code >= 400:
                logger.warning(
                    "enterprise_rag_failed",
                    status=response.status_code,
                    body=response.text[:200],
                )
                return []
            data = response.json()
    except Exception as exc:
        logger.warning("enterprise_rag_error", error=str(exc))
        return []

    parts: list[str] = []
    answer = data.get("answer") or data.get("text") or ""
    if answer:
        parts.append(f"[enterprise_rag_answer] {str(answer)[:1500]}")
    citations = data.get("citations") or data.get("sources") or []
    for i, cite in enumerate(citations[:5], 1):
        if isinstance(cite, dict):
            snippet = cite.get("text") or cite.get("snippet") or cite.get("uri") or str(cite)
            page = cite.get("page")
            page_s = f" p.{page}" if page is not None else ""
            parts.append(f"[enterprise_rag_cite_{i}{page_s}] {str(snippet)[:400]}")
        else:
            parts.append(f"[enterprise_rag_cite_{i}] {str(cite)[:400]}")
    if data.get("declined"):
        parts.append("[enterprise_rag] declined_to_answer")
    return parts


async def _fetch_external_sources(topic: str) -> str:
    """Augment with Enterprise RAG (optional) + local vector hits from prior research."""
    parts = [f"[topic] {topic}"]
    erag_parts = await _fetch_enterprise_rag(topic)
    parts.extend(erag_parts)
    try:
        similar = await search_similar(topic, limit=5)
        for i, hit in enumerate(similar, 1):
            parts.append(
                f"[rag_{i}] (score={hit.get('score', 0):.2f}) "
                f"{hit.get('topic')}: {hit.get('brief', '')[:500]}"
            )
    except Exception as exc:
        logger.warning("rag_search_failed", error=str(exc))
    if len(parts) == 1:
        parts.append(f"[web_search] Recent articles on '{topic}'")
    return "\n".join(parts)


@observe_node("research")
async def research_agent(state: ContentFactoryState) -> dict:
    topic = state["topic"]
    run_id = state.get("run_id", "")
    set_run_context(run_id, "research")

    settings = get_settings()
    redis = get_redis()
    topic_hash = hashlib.sha256(topic.encode()).hexdigest()[:16]
    cache_key = RESEARCH_CACHE.format(topic_hash=topic_hash)

    logger.info("research_started", topic=topic, cache_key=cache_key[:16])

    cached = await redis.get(cache_key)
    if cached:
        logger.info("research_cache_hit", topic=topic)
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

        logger.info("research_completed", topic=topic, brief_chars=len(str(brief)))
        return {"research_brief": brief, "error": None}
    except Exception as exc:
        logger.error("research_failed", topic=topic, error=str(exc))
        return {"error": f"Research agent failed: {exc}"}
