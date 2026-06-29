---
name: loop-engineering
description: >-
  Implement ODAEU harness loops, RAG evolve tuning, and procedural memory in
  LoopForge or similar systems. Use when building self-improving agents, eval
  gates, MCP tool bridges, or RAG version trees.
---

# Loop Engineering

## ODAEU outer loop

| Phase | Action |
|-------|--------|
| Observe | Load RAG config vN, memory hints, corpus context |
| Decide | Plan ReAct steps or orchestrator decomposition |
| Act | MCP tools (`read_file`, `search_docs`) or repo patches |
| Evaluate | Recall, faithfulness, pytest, review score |
| Update | Tune RAG (`top_k`, `hybrid_alpha`) + write lesson |

## RAG evolve signals

| Failure | Tune |
|---------|------|
| low_recall | ↑ top_k, ↑ hybrid_alpha |
| low_faithfulness | ↑ rerank_threshold, ↓ hybrid_alpha |

## Memory

- `Lesson(failure_mode, lesson, rag_version)` → JSON store (v1)
- Hints injected on next run via `hints_for_query`

## MCP bridge

- Local adapters in `mcp/bridge.py`; extensible to stdio MCP servers
- Never give agents raw shell without allowlist

## Reference

- `loop-engine-agent-platform/src/loop_engine/harness/`
- `loops/support-intelligence.yaml`
- ADR-001 in LoopForge repo
