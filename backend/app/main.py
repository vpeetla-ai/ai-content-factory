"""FastAPI application entrypoint — production bootstrap."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Docker: /app/app/main.py → parents[1] = /app (agents package lives here)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.api.routes.auth import auth_router, users_router
from app.api.routes.content import router as content_router
from app.api.routes.hitl import router as hitl_router
from app.api.routes.pipelines import router as pipelines_router
from app.core.checkpointer import is_graph_ready, is_memory_checkpointer, shutdown_graph
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.observability import flush_observability, init_observability
from app.websocket.gateway import sio

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Keep startup minimal — graph/vector init is lazy (first pipeline request)
    init_observability()
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
    return {
        "status": "ok",
        "service": "ai-content-factory-api",
        "version": "1.0.0",
        "environment": settings.app_env,
        "mock_llm": settings.mock_llm,
        "graph_ready": is_graph_ready(),
        "checkpointer": "memory" if is_memory_checkpointer() else ("redis" if is_graph_ready() else "pending"),
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
