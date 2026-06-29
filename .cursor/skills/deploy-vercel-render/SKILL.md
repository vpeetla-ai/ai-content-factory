---
name: deploy-vercel-render
description: >-
  Deploy vpeetla-ai demos: Vercel static/Next.js frontends, Render FastAPI
  backends, env vars, free tier gotchas. Use when shipping demos, fixing deploy
  failures, or adding render.yaml / vercel.json.
---

# Deploy: Vercel + Render

## Standard split

| Layer | Host | Config |
|-------|------|--------|
| UI demo | Vercel | `vercel.json`, `config.js` API URL |
| Python API | Render | `render.yaml`, Dockerfile |

## Render free tier

```yaml
# render.yaml
plan: free   # REQUIRED — avoids credit card prompt
```

## Env vars (Render)

- `GROQ_API_KEY`, `GITHUB_TOKEN` (LoopForge)
- `AEGISAI_API_BASE_URL` (gateway integrations)
- Never commit secrets — Render dashboard only

## Vercel

- Deploy from subfolder: `cd demo && vercel --prod`
- Point `LOOPFORGE_API` / `API_BASE` in `config.js` to Render URL

## Health checks

```bash
curl https://loopforge-api.onrender.com/health
```

## Cold start

- Render free spins down ~15min idle — document in README
- Vercel edge is always warm for static

## Reference deploys

| Project | Demo | API |
|---------|------|-----|
| LoopForge | demo-omega-taupe.vercel.app | loopforge-api.onrender.com |
| Enterprise RAG | enterprise-rag-platform.vercel.app | — |
| VAP | venkat-ai-platform.vercel.app | — |

## Docs

Each repo: `docs/DEPLOY.md` with exact commands and env table
