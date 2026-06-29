---
name: setup-vpeetla-skills
description: >-
  Bootstrap a vpeetla-ai repo for org skills: issue tracker, triage labels, docs
  paths, and CONTEXT.md placement. Use when onboarding a new repo, first clone,
  or when the user says setup skills or configure agent workflow.
---

# Setup vpeetla-ai Skills

Run once per repository.

## Checklist

1. Confirm repo is in [vpeetla-ai](https://github.com/vpeetla-ai) org
2. Install skills: `./scripts/install.sh --cursor --project .` from vpeetla-ai-skills
3. Copy `CONTEXT.md` if missing (or symlink from skills repo)
4. Add `AGENTS.md` (Codex) — merge, do not overwrite custom sections
5. Identify stack layer (see governed-ai-stack skill)

## Ask the user

- Issue tracker: GitHub Issues / Linear / local `docs/issues/`
- Triage labels: e.g. `agent-task`, `hitl-required`, `loopforge`
- Docs path: `docs/` (default) or `adr/`

## Write `.vpeetla-skills.json` in repo root

```json
{
  "issue_tracker": "github",
  "docs_path": "docs",
  "stack_layer": "self-improvement",
  "gateway_required": false
}
```

## Verify

- [ ] `pytest -q` or `npm test` passes (if applicable)
- [ ] README has honest implementation status table
- [ ] `docs/ECOSYSTEM.md` or link to ai-architecture-portfolio exists for platform repos
