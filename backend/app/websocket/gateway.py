"""Socket.io WebSocket gateway — HITL push events."""

import socketio

from app.core.config import get_settings

settings = get_settings()

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[settings.frontend_url, "http://localhost:3000"],
)

# run_id -> set of session ids
_run_rooms: dict[str, set[str]] = {}


@sio.event
async def connect(sid, environ):
    await sio.emit("connected", {"sid": sid}, to=sid)


@sio.event
async def disconnect(sid):
    for room, members in list(_run_rooms.items()):
        members.discard(sid)
        if not members:
            del _run_rooms[room]


@sio.on("join_run")
async def join_run(sid, data):
    run_id = data.get("run_id")
    if not run_id:
        return
    await sio.enter_room(sid, run_id)
    _run_rooms.setdefault(run_id, set()).add(sid)


@sio.on("hitl:approve")
async def ws_hitl_approve(sid, data):
    run_id = data.get("run_id")
    await sio.emit("hitl:processing", data, room=run_id)


@sio.on("hitl:edit")
async def ws_hitl_edit(sid, data):
    run_id = data.get("run_id")
    await sio.emit("agent:chunk", {"agent_name": "hitl", "token": "edit received"}, room=run_id)


@sio.on("cancel_run")
async def ws_cancel_run(sid, data):
    run_id = data.get("run_id")
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


async def emit_publish_result(run_id: str, platform: str, post_id: str, url: str):
    await sio.emit(
        "publish:result",
        {"platform": platform, "post_id": post_id, "url": url},
        room=run_id,
    )
