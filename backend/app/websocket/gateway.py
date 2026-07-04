"""Socket.io WebSocket gateway — authenticated HITL push events."""

import socketio

from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.security import decode_token

settings = get_settings()
logger = get_logger(__name__)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.cors_origin_list,
)

# sid -> user_id
_sessions: dict[str, str] = {}
# run_id -> set of session ids
_run_rooms: dict[str, set[str]] = {}


def _extract_token(environ: dict) -> str | None:
    query = environ.get("QUERY_STRING") or ""
    for part in query.split("&"):
        if part.startswith("token="):
            return part.split("=", 1)[1]
    auth_header = environ.get("HTTP_AUTHORIZATION") or ""
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:]
    return None


@sio.event
async def connect(sid, environ, auth):
    token = None
    if isinstance(auth, dict):
        token = auth.get("token")
    if not token:
        token = _extract_token(environ)

    if settings.is_production or not settings.allow_dev_auth:
        if not token:
            logger.warning("ws_connect_rejected", reason="missing_token", sid=sid)
            return False
        try:
            payload = decode_token(token)
            _sessions[sid] = payload.get("sub", "")
        except Exception:
            logger.warning("ws_connect_rejected", reason="invalid_token", sid=sid)
            return False
    elif token:
        try:
            payload = decode_token(token)
            _sessions[sid] = payload.get("sub", "")
        except Exception:
            pass

    await sio.emit("connected", {"sid": sid}, to=sid)
    return True


@sio.event
async def disconnect(sid):
    _sessions.pop(sid, None)
    for room, members in list(_run_rooms.items()):
        members.discard(sid)
        if not members:
            del _run_rooms[room]


@sio.on("join_run")
async def join_run(sid, data):
    run_id = data.get("run_id") if isinstance(data, dict) else None
    if not run_id:
        return
    await sio.enter_room(sid, run_id)
    _run_rooms.setdefault(run_id, set()).add(sid)


@sio.on("hitl:approve")
async def ws_hitl_approve(sid, data):
    run_id = data.get("run_id") if isinstance(data, dict) else None
    if run_id:
        await sio.emit("hitl:processing", data, room=run_id)


@sio.on("hitl:edit")
async def ws_hitl_edit(sid, data):
    run_id = data.get("run_id") if isinstance(data, dict) else None
    if run_id:
        await sio.emit("agent:chunk", {"agent_name": "hitl", "token": "edit received"}, room=run_id)


@sio.on("cancel_run")
async def ws_cancel_run(sid, data):
    run_id = data.get("run_id") if isinstance(data, dict) else None
    if not run_id:
        return
    from app.core.cancel_registry import cancel_run as registry_cancel

    registry_cancel(str(run_id))
    await emit_pipeline_error(str(run_id), "Cancelled by user")


async def emit_agent_chunk(run_id: str, agent_name: str, token: str):
    await sio.emit("agent:chunk", {"agent_name": agent_name, "token": token}, room=run_id)


async def emit_pipeline_error(run_id: str, error_msg: str):
    await sio.emit("pipeline:error", {"run_id": run_id, "error_msg": error_msg}, room=run_id)


async def emit_agent_start(run_id: str, agent_name: str):
    await sio.emit("agent:start", {"agent_name": agent_name}, room=run_id)


async def emit_agent_done(run_id: str, agent_name: str, output_key: str):
    await sio.emit("agent:done", {"agent_name": agent_name, "output_key": output_key}, room=run_id)


async def emit_hitl_ready(run_id: str, drafts: list):
    await sio.emit("hitl:ready", {"run_id": run_id, "drafts": drafts}, room=run_id)


async def emit_publish_result(
    run_id: str,
    platform: str,
    post_id: str,
    url: str,
    *,
    not_supported: bool = False,
    draft_content: str = "",
):
    await sio.emit(
        "publish:result",
        {
            "platform": platform,
            "post_id": post_id,
            "url": url,
            "not_supported": not_supported,
            "draft_content": draft_content,
        },
        room=run_id,
    )
