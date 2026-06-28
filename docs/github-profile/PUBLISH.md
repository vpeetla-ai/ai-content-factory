# Optimize your GitHub profile (not a new “project”)

Your profile is already here: **[github.com/vpeetla-ai](https://github.com/vpeetla-ai)**

You do **not** need a second GitHub account or a duplicate profile. Everything below improves that **same** profile and your **existing** repositories.

---

## How GitHub profile pages work

When someone opens [github.com/vpeetla-ai](https://github.com/vpeetla-ai), they see two different things:

| Tab | What it shows | How you control it |
|-----|---------------|-------------------|
| **Overview** | Bio, links, pinned repos, optional big README banner | Profile settings + pins + optional special README repo |
| **Repositories** | All your repos ([8 public today](https://github.com/vpeetla-ai?tab=repositories)) | Each repo’s README, description, topics |

```text
github.com/vpeetla-ai
├── Overview tab     ← “landing page” (often empty without a profile README)
└── Repositories tab ← ai-content-factory, enterprise_rag_platform, patterns, etc.
```

---

## The `vpeetla-ai` repo — optional, not a new product

GitHub has one quirky rule: to show a **custom README on your Overview tab**, you create **one repo whose name equals your username**:

- Repo: `vpeetla-ai/vpeetla-ai`
- Contains: only a `README.md`
- Effect: that markdown renders **on top of** [github.com/vpeetla-ai](https://github.com/vpeetla-ai) (Overview)

This is **not**:

- ❌ A second GitHub profile
- ❌ An 11th application to maintain
- ❌ Required for SEO on your real projects

This **is**:

- ✅ A free “homepage banner” for your existing profile
- ✅ A table of links to `ai-content-factory`, RAG, agent patterns, etc.
- ✅ Optional — you can skip it and still optimize every real repo

**If you skip it:** set a strong bio, pin 6 repos, and polish each repository README (most important for stars and search).

---

## Priority 1 — Every real repository (highest SEO impact)

GitHub search ranks **repository name, description, topics, and README text**. Do this for **each** repo on [your repositories tab](https://github.com/vpeetla-ai?tab=repositories):

1. **Description** (Settings → General) — one sentence with keywords  
   Example: `Multi-agent content pipeline with HITL, LangGraph, FastAPI, Next.js`

2. **Topics** — 5–8 tags (`langgraph`, `rag`, `ai-agents`, …)

3. **README** — hook in first 10 lines, demo link, quick start, architecture diagram

4. **Homepage URL** — live demo or docs (e.g. ai-content-factory → Vercel URL)

**Automate descriptions + topics** (after `gh auth login`):

```bash
./scripts/set-github-metadata.sh
```

**Agent pattern READMEs** — copy enhanced series READMEs to each pattern repo:

```bash
./scripts/apply-agent-pattern-readmes.sh
```

**Flagship repo** — `ai-content-factory/README.md` is already enhanced in this workspace; push to GitHub.

---

## Priority 2 — Profile settings (5 minutes, no extra repo)

Go to [github.com/settings/profile](https://github.com/settings/profile):

| Field | Suggested value |
|-------|-----------------|
| **Name** | Venkata Peetla |
| **Bio** | AI Architect · Production multi-agent systems, enterprise RAG, AgentOps · Open source |
| **URL** | https://venkat-ai.com |
| **Social** | LinkedIn, Substack (already linked — good) |

---

## Priority 3 — Pin 6 repositories

On [github.com/vpeetla-ai](https://github.com/vpeetla-ai) → **Customize your pins**:

1. `ai-content-factory` (flagship + live demo)
2. `enterprise_rag_platform` (thought leadership)
3. `aegisloop-agentops-workbench` (AgentOps)
4. `react-agent-pattern` (series entry point)
5. `multi-agent-system-pattern`
6. `plan-execute-agent-pattern`

Pins appear on **both** Overview and Repositories — they guide visitors to your best work.

---

## Priority 4 — Optional profile README repo

Only if you want a rich Overview banner (links table, series roadmap, “currently building”):

1. [Create new repo](https://github.com/new) named exactly **`vpeetla-ai`**
2. Paste content from [README.md](./README.md) in this folder
3. Commit — refresh [github.com/vpeetla-ai](https://github.com/vpeetla-ai) Overview tab

Repo contains **one file**. No app, no deploy, no maintenance beyond occasional edits.

---

## Your repositories (public)

| Repository | SEO action |
|------------|------------|
| ai-content-factory | Push updated README, set topics, add demo GIF |
| enterprise_rag_platform | Expand README, add topics |
| aegisloop-agentops-workbench | Add README + description + topics |
| react-agent-pattern | Apply series README from `docs/agent-patterns/` |
| reflection-agent-pattern | Same |
| plan-execute-agent-pattern | Same |
| multi-agent-system-pattern | Same |
| swarm-agent-pattern | Same |

If you have **private** repos counted in your “11 projects,” add them to `scripts/set-github-metadata.sh` when you want them public.

---

## Troubleshooting: `gh auth login` permission denied

If you see:

```text
mkdir /Users/.../.config/gh: permission denied
```

Your `~/.config` folder is owned by **root**. Browser auth may succeed, but **gh cannot save the token**.

**Fix** — use a writable config path, then log in again:

```bash
export GH_CONFIG_DIR=~/.local/gh-config
mkdir -p ~/.local/gh-config
gh auth login
cd /path/to/ai-content-factory
./scripts/publish-profile-readme.sh
./scripts/set-github-metadata.sh
```

Project scripts set `GH_CONFIG_DIR` automatically via `scripts/gh-env.sh`.

**Permanent fix (optional):** `sudo chown -R "$(whoami)" ~/.config`

---

## Checklist

- [ ] Push `ai-content-factory` growth assets to GitHub
- [ ] Run `./scripts/set-github-metadata.sh` for descriptions + topics
- [ ] Apply agent-pattern READMEs and push each repo
- [ ] Update profile bio + pin 6 repos
- [ ] *(Optional)* Create `vpeetla-ai/vpeetla-ai` for Overview README
- [ ] Record demo GIF → `docs/assets/demo.gif` (see [DEMO_GIF.md](../DEMO_GIF.md))
- [ ] Publish article from [flagship-article-draft.md](../content/flagship-article-draft.md)
