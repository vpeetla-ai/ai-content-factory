"""Per-run context for tracing (set during graph execution)."""

import contextvars

run_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("run_id", default=None)
agent_name_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("agent_name", default=None)


def set_run_context(run_id: str | None, agent_name: str | None = None) -> None:
    if run_id is not None:
        run_id_var.set(run_id)
    if agent_name is not None:
        agent_name_var.set(agent_name)


def get_run_id() -> str | None:
    return run_id_var.get()


def get_agent_name() -> str | None:
    return agent_name_var.get()
