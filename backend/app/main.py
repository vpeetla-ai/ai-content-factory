"""FastAPI application entrypoint — production bootstrap."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.api.routes.auth import auth_router, users_router
from app.api.routes.content import router as content_router
from app.api.routes.hitl import router as hitl_router
from app.api.routes.pipelines import router as pipelines_router
from app.core.checkpointer import init_graph, is_memory_checkpointer, shutdown_graph
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.observability import flush_observability, init_observability
from app.websocket.gateway import sio

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


async def _run_migrations() -> None:
    if not settings.run_migrations_on_startup:
        return
    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        logger.info("migrations_applied")
    except Exception as exc:
        logger.error("migration_failed", error=str(exc))
        if settings.is_production:
            raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_observability()
    await _run_migrations()
    await init_graph(settings.redis_url, ttl_seconds=settings.pipeline_state_ttl)

    from app.services.vector_store import ensure_collection

    try:
        await ensure_collection()
    except Exception as exc:
        logger.warning("vector_store_init_skipped", error=str(exc))

    logger.info("application_started", app_env=settings.app_env)
    yield
    await shutdown_graph()
    flush_observability()
    logger.info("application_stopped")


app = FastAPI(
    title="AI Content Factory API",
    description="Multi-agent content orchestration — production API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FastAPI()
api.include_router(pipelines_router)
api.include_router(hitl_router)
api.include_router(content_router)
api.include_router(auth_router)
api.include_router(users_router)

app.mount("/api/v1", api)


@app.get("/health")
async def health():
    from agents.llm import use_mock_llm

    return {
        "status": "ok",
        "service": "ai-content-factory-api",
        "version": "1.0.0",
        "environment": settings.app_env,
        "mock_llm": use_mock_llm(),
        "checkpointer": "memory" if is_memory_checkpointer() else "redis",
        "llm_keys_configured": bool(
            settings.google_api_key or settings.groq_api_key or settings.anthropic_api_key
        ),
        "clerk_configured": settings.clerk_configured,
        "vector_backend": settings.vector_backend if settings.vector_enabled else "disabled",
        "langsmith": settings.langsmith_enabled,
        "langfuse": settings.langfuse_configured,
    }


socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
app = socket_app
