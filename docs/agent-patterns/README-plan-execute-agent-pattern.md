# Plan and Execute Agent Pattern

[![Part of Production Agent Patterns](https://img.shields.io/badge/series-Production%20Agent%20Patterns-purple)](https://github.com/vpeetla-ai/plan-execute-agent-pattern)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Part 3 of 5** in the [Production Agent Patterns](https://github.com/vpeetla-ai/react-agent-pattern) series.

Production-grade reference implementation of the **Plan and Execute** pattern for research, reporting, data analysis, and controlled multi-step workflows.

| # | Pattern | Repository | Use when |
|---|---------|------------|----------|
| 1 | ReAct | [react-agent-pattern](https://github.com/vpeetla-ai/react-agent-pattern) | Tool use + reasoning loops |
| 2 | Reflection | [reflection-agent-pattern](https://github.com/vpeetla-ai/reflection-agent-pattern) | Self-critique and improve output |
| 3 | **Plan-Execute** | **this repo** | Decompose goals into steps |
| 4 | Multi-Agent | [multi-agent-system-pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern) | Specialized role delegation |
| 5 | Swarm | [swarm-agent-pattern](https://github.com/vpeetla-ai/swarm-agent-pattern) | Parallel autonomous agents |

[📖 Full series roadmap](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/agent-patterns/ROADMAP.md) · [🚀 See in production — AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

---

## What you'll learn

- Planner produces **explicit executable steps**
- Executor handles one step at a time with observable state
- Observations feed back into workflow state
- Status is inspectable and resumable (production checkpointing mindset)

## Highlights

- Planner produces explicit executable steps
- Executor handles one step at a time
- Observations are fed back into state
- Workflow status is inspectable and resumable

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m plan_execute_agent_pattern
pytest
```

Runs without API keys using deterministic stubs.

```bash
cp .env.example .env
```

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for production setup.

## Related

- **Previous:** [Reflection Agent Pattern](https://github.com/vpeetla-ai/reflection-agent-pattern)
- **Next:** [Multi-Agent System Pattern](https://github.com/vpeetla-ai/multi-agent-system-pattern)
- **Full pipeline:** [AI Content Factory](https://github.com/vpeetla-ai/ai-content-factory)

⭐ Star the repo if this pattern helps your work.
