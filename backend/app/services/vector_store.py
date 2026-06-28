"""Vector store — Qdrant (local/prod) or Pinecone with embedding-backed RAG."""

from __future__ import annotations

import hashlib
import uuid
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_collection_ready = False


async def embed_text(text: str) -> list[float]:
    """Generate embeddings via Google Gemini (free tier)."""
    settings = get_settings()
    if not settings.google_api_key:
        # Deterministic fallback for dev without keys — not for semantic search quality
        digest = hashlib.sha256(text.encode()).digest()
        return [((digest[i % len(digest)] / 255.0) * 2 - 1) for i in range(settings.embedding_dimensions)]

    try:
        from litellm import aembedding

        response = await aembedding(
            model=f"gemini/{settings.embedding_model}",
            input=[text[:8000]],
            api_key=settings.google_api_key,
        )
        return response.data[0]["embedding"]
    except Exception as exc:
        logger.warning("embedding_failed", error=str(exc))
        digest = hashlib.sha256(text.encode()).digest()
        return [((digest[i % len(digest)] / 255.0) * 2 - 1) for i in range(settings.embedding_dimensions)]


async def ensure_collection() -> None:
    global _collection_ready
    if _collection_ready:
        return

    settings = get_settings()
    if not settings.vector_enabled:
        return

    if settings.vector_backend == "qdrant":
        await _ensure_qdrant_collection(settings)
    elif settings.vector_backend == "pinecone":
        await _ensure_pinecone_index(settings)

    _collection_ready = True


async def _ensure_qdrant_collection(settings) -> None:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.models import Distance, VectorParams

    client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
    collections = await client.get_collections()
    names = {c.name for c in collections.collections}
    if settings.qdrant_collection not in names:
        await client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=settings.embedding_dimensions, distance=Distance.COSINE),
        )
        logger.info("qdrant_collection_created", collection=settings.qdrant_collection)


async def _ensure_pinecone_index(settings) -> None:
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key=settings.pinecone_api_key)
    if settings.pinecone_index not in pc.list_indexes().names():
        pc.create_index(
            name=settings.pinecone_index,
            dimension=settings.embedding_dimensions,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.pinecone_environment),
        )
        logger.info("pinecone_index_created", index=settings.pinecone_index)


async def upsert_research(topic: str, brief: str, run_id: str = "") -> None:
    settings = get_settings()
    if not settings.vector_enabled:
        return

    await ensure_collection()
    vector = await embed_text(f"{topic}\n{brief}")

    if settings.vector_backend == "qdrant":
        await _upsert_qdrant(settings, topic, brief, run_id, vector)
    elif settings.vector_backend == "pinecone":
        await _upsert_pinecone(settings, topic, brief, run_id, vector)


async def _upsert_qdrant(settings, topic: str, brief: str, run_id: str, vector: list[float]) -> None:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.models import PointStruct

    client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
    point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{topic}:{run_id or brief[:64]}"))
    await client.upsert(
        collection_name=settings.qdrant_collection,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"topic": topic, "brief": brief[:4000], "run_id": run_id},
            )
        ],
    )


async def _upsert_pinecone(settings, topic: str, brief: str, run_id: str, vector: list[float]) -> None:
    from pinecone import Pinecone

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index)
    point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{topic}:{run_id or brief[:64]}"))
    index.upsert(
        vectors=[{"id": point_id, "values": vector, "metadata": {"topic": topic, "brief": brief[:1000], "run_id": run_id}}]
    )


async def search_similar(topic: str, limit: int = 5) -> list[dict[str, Any]]:
    settings = get_settings()
    if not settings.vector_enabled:
        return []

    await ensure_collection()
    vector = await embed_text(topic)

    if settings.vector_backend == "qdrant":
        return await _search_qdrant(settings, vector, limit)
    if settings.vector_backend == "pinecone":
        return await _search_pinecone(settings, vector, limit)
    return []


async def _search_qdrant(settings, vector: list[float], limit: int) -> list[dict[str, Any]]:
    from qdrant_client import AsyncQdrantClient

    client = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
    results = await client.search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=limit,
        with_payload=True,
    )
    return [
        {"topic": hit.payload.get("topic", ""), "brief": hit.payload.get("brief", ""), "score": hit.score}
        for hit in results
        if hit.payload
    ]


async def _search_pinecone(settings, vector: list[float], limit: int) -> list[dict[str, Any]]:
    from pinecone import Pinecone

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index)
    response = index.query(vector=vector, top_k=limit, include_metadata=True)
    return [
        {
            "topic": m.metadata.get("topic", ""),
            "brief": m.metadata.get("brief", ""),
            "score": m.score,
        }
        for m in response.matches
        if m.metadata
    ]
