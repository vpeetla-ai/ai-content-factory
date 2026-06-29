---
name: tdd-agent-loops
description: >-
  Test-driven development for agent systems: red-green-refactor on graphs,
  mocked LLM fixtures, pytest-asyncio, trace assertions. Use when adding agent
  nodes, fixing loop bugs, or building pattern repos.
---

# TDD for Agent Loops

Inspired by [mattpocock/skills tdd](https://github.com/mattpocock/skills) — adapted for LangGraph.

## Red → Green → Refactor

1. **Red** — Write failing test for routing or node output (mock LLM)
2. **Green** — Minimal node/routing fix
3. **Refactor** — Extract helpers only when second test needs it

## What to test

| Layer | Test |
|-------|------|
| Routing | `route_after_quality` returns `retry`/`pass`/`escalate` |
| Nodes | Given state in, partial state out (no real LLM) |
| Integration | Full graph with `FakeLLM` fixture |
| Repo-fix | Clone fixture repo, assert branch + patch count |

## Fixtures

```python
@pytest.fixture
def fake_llm():
    return FakeLLM(responses=[{"content": "..."}])
```

## Async

```python
@pytest.mark.asyncio
async def test_graph_happy_path(tmp_path):
    ...
```

## Avoid

- Tests that only assert "graph compiles"
- Snapshotting full LLM prose (flaky)
- Hitting live Groq in CI

## Reference

- `loop-engine-agent-platform/tests/test_repo_fix.py`
- `*-agent-pattern/tests/` — minimal pattern coverage
