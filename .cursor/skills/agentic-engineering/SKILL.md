---
name: agentic-engineering
description: >-
  Apply Karpathy agentic engineering discipline: think before coding, minimal
  diffs, surgical changes, test-verified completion. Use for any implementation
  task in vpeetla-ai repos when quality bar matters.
---

# Agentic Engineering

Not vibe coding — preserve professional quality while moving faster.

## Before writing code

1. State **assumptions** and **success criteria** (tests, API response, UI behavior)
2. Identify **smallest change** that satisfies the request
3. Read surrounding files — match naming, types, error handling

## While coding

- **Simplicity first** — no speculative abstractions or "while I'm here" refactors
- **Surgical diffs** — touch only files required for the task
- **Match conventions** — see target repo's pyproject.toml, eslint, existing patterns

## Before claiming done

1. Run relevant tests (`pytest -q`, `npm test`, typecheck)
2. For agent graphs: verify routing + at least one happy-path trace
3. Summarize what changed and what was **not** changed (scope boundary)

## Red flags — stop and ask

- Request touches governance + orchestration in one PR (split layers)
- Side effect without gateway/HITL (publish, push, notify)
- No test strategy for new behavior

## Reference

Karpathy: [From Vibe Coding to Agentic Engineering](https://www.youtube.com/watch?v=96jN2OCOfLs)
