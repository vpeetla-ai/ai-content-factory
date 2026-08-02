---
name: repo-fix-pr
description: >-
  Run or extend LoopForge repo-fix workflow: clone GitHub repo, pytest scan,
  LangGraph patch loop, branch loopforge/fix-{id}, open PR never push main. Use
  when fixing bugs across repos, extending workspace/git tools, or debugging
  /api/repo-fix.
---

# Repo Fix → PR Workflow

## Flow

```text
clone → scan (pytest) → orchestrate → code → review → quality
  → git checkout -b loopforge/fix-{run_id} → commit → push branch → GitHub PR
```

## API

```bash
curl -X POST https://loopforge-api.onrender.com/api/repo-fix \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $LOOPFORGE_API_KEY" \
  -d '{"repo_url":"https://github.com/org/repo.git","task":"Fix failing tests","create_pr":true}'
```

## Env (Render)

- `GROQ_API_KEY` — live LLM
- `GITHUB_TOKEN` — fine-grained PAT: Contents + Pull requests write
- `LOOPFORGE_API_KEY` — **required in production**; without it `/api/repo-fix` and
  `/api/hitl/resume` have no authentication at all (see
  [ADR-002](https://github.com/vpeetla-ai/loop-engine-agent-platform/blob/main/docs/ADR-002-repo-fix-auth-and-isolation.md))

## Rules

- **Never** push to `main`
- Branch: `loopforge/fix-{run_id[:12]}`
- PR body includes run_id, review score, test status
- **Git author:** always `Venkata Peetla <vpeetla.ai@gmail.com>` (author + committer). Never
  `Co-authored-by: Cursor`. See skill `git-commit-author`.
- `local_path` only works when `LOOPFORGE_API_KEY` is unset (dev-only) — rejected once the
  key is enforced
- Even authenticated, `run_pytest` executes cloned code with no container isolation — only
  point this at trusted repos until sandboxing lands (ADR-002 follow-up)

## Extending

- `src/loop_engine/workspace/git_ops.py` — clone, branch, PR API
- `src/loop_engine/graph/repo_nodes.py` — patch parse, quality gate
- Add project detectors (npm, cargo) beside pytest

## Demo

https://demo-omega-taupe.vercel.app
