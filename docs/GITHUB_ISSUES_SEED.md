# Seed issues for GitHub

Create these after pushing issue templates. Label each `good first issue`.

Run: `gh auth login` then use GitHub UI or:

```bash
gh issue create --repo vpeetla-ai/ai-content-factory --title "..." --body "..." --label "good first issue"
```

---

## Issue 1: Add CI status badge to README

**Labels:** `good first issue`, `documentation`

**Body:**

Add a GitHub Actions CI badge to the top of `README.md`, linking to `.github/workflows/ci.yml`.

**Acceptance criteria:**
- Badge renders on main branch README
- Links to the correct workflow runs page
- No broken image URL

---

## Issue 2: Document MOCK_LLM vs real LLM in README

**Labels:** `good first issue`, `documentation`

**Body:**

Add a short section to README explaining:
- Default local behavior with `MOCK_LLM=true`
- How to enable real providers (`MOCK_LLM=false` + keys in `.env.local`)
- Which agents use which providers (reference `agents/llm.py` or config)

**Acceptance criteria:**
- New developer understands demo vs production LLM calls in under 2 minutes

---

## Issue 3: Add CONTRIBUTING link to issue template chooser

**Labels:** `good first issue`, `documentation`

**Body:**

Verify `.github/ISSUE_TEMPLATE/config.yml` includes a link to CONTRIBUTING.md and the good first issue label filter.

---

## Issue 4: LinkedIn publish adapter (OAuth scaffold)

**Labels:** `enhancement` (or `good first issue` if scoped small)

**Body:**

Scaffold the LinkedIn OAuth flow in `backend/app/services/publisher.py`:
- Env vars documented in `.env.example`
- Stub adapter with clear TODO for token exchange
- Unit test with mocked HTTP

Reference implementation status table in README (currently mock adapters).

---

## Issue 5: Add architecture PNG export for social sharing

**Labels:** `good first issue`, `documentation`

**Body:**

Export the HLD mermaid diagram from README to `docs/assets/architecture.png` for use in Substack/LinkedIn posts. Document export steps in `docs/content/flagship-article-draft.md`.

Tools: Mermaid Live Editor, or `mmdc` CLI.

---

## Issue 6: Enable GitHub Discussions + welcome post

**Labels:** `good first issue`, `documentation`

**Body:**

1. Enable Discussions in repo settings
2. Add a Welcome discussion pinned with links to quick start, deploy guide, and agent pattern series

Not a code change — document steps in a PR updating `docs/github-profile/PUBLISH.md` if settings are done manually.
