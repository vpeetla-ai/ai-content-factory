---
name: grill-with-context
description: >-
  Interview the user about a plan or design until decisions are resolved, while
  updating CONTEXT.md terms and noting ADR candidates. Use before large features,
  cross-repo integrations, or when requirements feel vague.
disable-model-invocation: true
---

# Grill With Context

Inspired by [mattpocock/skills grill-with-docs](https://github.com/mattpocock/skills) — org-specific version.

## When to use

- New feature spanning multiple stack layers
- Unclear which repo should own the change
- User says "build X" without success criteria

## Process

1. **Restate** the goal in one sentence; ask if correct
2. **Grill** — ask one question at a time until resolved:
   - Which stack layer? (see governed-ai-stack)
   - What defines done? (test, demo URL, metric)
   - Side effects? (gateway/HITL required?)
   - Stub mode or live API keys?
3. **Sharpen vocabulary** — if the user uses vague terms, propose CONTEXT.md entries
4. **ADR candidates** — flag decisions that need an ADR in ai-architecture-portfolio
5. **Output** — short plan with repo, files, test strategy, out-of-scope list

## Rules

- Do not start coding until grilling is complete
- Do not ask five questions in one message
- Prefer multiple-choice when options are finite

## After grilling

Suggest **tdd-agent-loops** for implementation or **to-prd** equivalent: write plan to `docs/plans/<slug>.md`
