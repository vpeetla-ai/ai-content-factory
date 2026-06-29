---
name: langgraph-orchestration
description: >-
  Build or modify LangGraph StateGraph agents in vpeetla-ai repos: typed state,
  nodes, conditional edges, MemorySaver, interrupt_before HITL. Use when adding
  orchestrators, coding loops, or multi-agent graphs.
---

# LangGraph Orchestration

## Standard pattern

```text
START → observe/plan → specialist nodes → evaluate → route (retry|pass|hitl) → END
```

## State

- Use `TypedDict` with `total=False` for optional fields
- Accumulate `trace_events` explicitly (list replacement per node unless using reducer)
- Set `max_iterations` in state; enforce in routing

## Nodes

- **Async** wrappers: `async def n_x(state): return sync_node(state, deps)`
- One responsibility per node (orchestrate, act, review, quality)
- Return partial state updates only

## Routing

```python
builder.add_conditional_edges("quality", route_fn, {"retry": "plan", "pass": "ship", "escalate": "hitl"})
```

- Security failures → escalate/HITL
- Max iterations → escalate, never infinite loop

## HITL

```python
graph.compile(checkpointer=MemorySaver(), interrupt_before=["hitl"])
```

Resume with `graph.ainvoke(update, config)` after human approval.

## Reference implementations

- `loop-engine-agent-platform/src/loop_engine/graph/build.py`
- `loop-engine-agent-platform/src/loop_engine/graph/repo_build.py`
- venkat-ai-platform orchestrators

## Tests

- Mock LLM for deterministic paths
- `pytest.mark.asyncio` + `tmp_path` for filesystem side effects
