"""Agent trace persistence + token/cost accounting."""

import time
import uuid
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentTrace, PipelineRun

# Approximate $/token for cost map fallback models (dev estimates)
COST_PER_1K_INPUT = 0.00025
COST_PER_1K_OUTPUT = 0.00125


@dataclass
class RunMetrics:
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    _node_started: dict[str, float] = field(default_factory=dict)
    llm_calls: list[dict] = field(default_factory=list)

    def start_node(self, agent_name: str) -> None:
        self._node_started[agent_name] = time.monotonic()

    def node_latency_ms(self, agent_name: str) -> int:
        started = self._node_started.pop(agent_name, None)
        if started is None:
            return 0
        return int((time.monotonic() - started) * 1000)

    def add_llm_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        *,
        model: str = "mock",
    ) -> None:
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        if model != "mock":
            self.total_cost_usd += (input_tokens / 1000) * COST_PER_1K_INPUT
            self.total_cost_usd += (output_tokens / 1000) * COST_PER_1K_OUTPUT


async def record_agent_trace(
    db: AsyncSession,
    run_id: uuid.UUID,
    agent_name: str,
    *,
    model_used: str | None,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    error_msg: str | None = None,
) -> None:
    db.add(
        AgentTrace(
            run_id=run_id,
            agent_name=agent_name,
            model_used=model_used,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            error_msg=error_msg,
        )
    )


async def apply_run_metrics(db: AsyncSession, run: PipelineRun, metrics: RunMetrics) -> None:
    run.total_tokens = metrics.total_input_tokens + metrics.total_output_tokens
    run.total_cost_usd = metrics.total_cost_usd
