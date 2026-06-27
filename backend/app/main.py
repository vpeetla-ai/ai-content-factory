"""FastAPI application entrypoint."""

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
from app.core.checkpointer import init_graph, shutdown_graph
from app.core.config import get_settings
from app.websocket.gateway import sio

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_graph(settings.redis_url, ttl_seconds=settings.pipeline_state_ttl)
    yield
    await shutdown_graph()


app = FastAPI(
    title="AI Content Factory API",
    description="Multi-agent content orchestration — HLD + LLD architecture",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
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

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
app = socket_app


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-content-factory-api", "mock_llm": settings.app_env == "development"}
