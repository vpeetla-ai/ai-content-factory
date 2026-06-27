"""Track in-flight and cancelled pipeline runs."""

import asyncio

_inflight: dict[str, asyncio.Task] = {}
_cancelled: set[str] = set()


def register_task(run_id: str, task: asyncio.Task) -> None:
    _inflight[run_id] = task


def unregister_task(run_id: str) -> None:
    _inflight.pop(run_id, None)


def cancel_run(run_id: str) -> bool:
    _cancelled.add(run_id)
    task = _inflight.get(run_id)
    if task and not task.done():
        task.cancel()
        return True
    return run_id in _cancelled


def is_cancelled(run_id: str) -> bool:
    return run_id in _cancelled


def clear_cancelled(run_id: str) -> None:
    _cancelled.discard(run_id)
