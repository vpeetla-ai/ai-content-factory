# Production Deployment & Configuration Guide

AI Content Factory deploys as a **free-tier cloud stack**. Push to `main` triggers CI/CD (Render API + Vercel frontend).

**Repository:** https://github.com/vpeetla-ai/ai-content-factory

---

## Table of contents

1. [Architecture overview](#1-architecture-overview)
2. [Prerequisites checklist](#2-prerequisites-checklist)
3. [Step-by-step: Neon Postgres](#3-step-by-step-neon-postgres)
4. [Step-by-step: Upstash Redis](#4-step-by-step-upstash-redis)
5. [Step-by-step: Qdrant Cloud (vector DB)](#5-step-by-step-qdrant-cloud-vector-db)
6. [Step-by-step: Clerk auth](#6-step-by-step-clerk-auth)
7. [Step-by-step: LangSmith](#7-step-by-step-langsmith)
8. [Step-by-step: Langfuse](#8-step-by-step-langfuse)
9. [Step-by-step: Sentry](#9-step-by-step-sentry)
10. [Step-by-step: Render (API + agents)](#10-step-by-step-render-api--agents)
11. [Step-by-step: Vercel (frontend)](#11-step-by-step-vercel-frontend)
12. [Step-by-step: GitHub Actions CD](#12-step-by-step-github-actions-cd)
13. [Environment variable reference](#13-environment-variable-reference)
14. [Local development](#14-local-development)
15. [Verify production](#15-verify-production)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Architecture overview

```mermaid
flowchart LR
    User[User Browser] --> Vercel[Vercel — Next.js + Clerk UI]
    Vercel -->|REST + WebSocket| Render[Render — FastAPI + LangGraph]
    Render --> Neon[(Neon Postgres)]
    Render --> Upstash[(Upstash Redis)]
    Render --> Qdrant[(Qdrant Cloud)]
    Render -.-> LangSmith
    Render -.-> Langfuse
    Render -.-> Sentry
    Vercel --> Clerk[Clerk Auth]
    Render -->|Verify JWT| Clerk
```

| Component | Local | Production |
|-----------|-------|------------|
| Frontend | `localhost:3000` | Vercel |
| Backend + Agents | `localhost:8000` | Render (Docker) |
| Postgres | Docker | Neon |
| Redis | Docker | Upstash |
| Vector DB | Docker Qdrant | Qdrant Cloud |
| Auth | Dev bypass optional | Clerk required |

---

## 2. Prerequisites checklist

Create accounts (all have free tiers):

- [ ] [GitHub](https://github.com) — repo already at `vpeetla-ai/ai-content-factory`
- [ ] [Render](https://render.com) — API hosting
- [ ] [Vercel](https://vercel.com) — frontend hosting
- [ ] [Neon](https://neon.tech) — Postgres
- [ ] [Upstash](https://upstash.com) — Redis
- [ ] [Qdrant Cloud](https://cloud.qdrant.io) — vector DB
- [ ] [Clerk](https://clerk.com) — authentication
- [ ] [LangSmith](https://smith.langchain.com) — LLM traces
- [ ] [Langfuse](https://cloud.langfuse.com) — LLM observability
- [ ] [Sentry](https://sentry.io) — error tracking
- [ ] [Google AI Studio](https://aistudio.google.com) — Gemini API key
- [ ] [Groq](https://console.groq.com) — Groq API key

**Recommended order:** Neon → Upstash → Qdrant → Clerk → LangSmith/Langfuse/Sentry → Render → Vercel → GitHub secrets

---

## 3. Step-by-step: Neon Postgres

1. Go to https://console.neon.tech and sign up.
2. Click **New Project** → name it `ai-content-factory`.
3. Select region closest to your Render region (e.g. `us-east-1`).
4. After creation, open **Dashboard** → **Connection Details**.
5. Copy the **Connection string** (pooled recommended for serverless):
   ```
   postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
6. Convert for the app (Render will accept either; the app auto-converts `postgres://`):
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/ai_content_factory?sslmode=require
   ```
7. In Neon SQL Editor, optionally create the database:
   ```sql
   CREATE DATABASE ai_content_factory;
   ```
   (Or use the default `neondb` — update `DATABASE_URL` accordingly.)

**Save for Render:** `DATABASE_URL`

> Migrations run automatically on Render startup (`RUN_MIGRATIONS_ON_STARTUP=true`).

---

## 4. Step-by-step: Upstash Redis

LangGraph checkpointer requires Redis with search modules. Upstash free tier works for production traffic at low volume.

1. Go to https://console.upstash.com and sign up.
2. Click **Create Database**.
3. Name: `acf-redis`, type: **Regional**, region: same as Render/Neon.
4. Enable **Eviction** → `noeviction` (important for checkpoint data).
5. After creation, open the database → **Connect**.
6. Copy the **Redis URL** (TLS):
   ```
   rediss://default:AYxxx...@xxx.upstash.io:6379
   ```
7. Use the `rediss://` (double s) URL — TLS is required.

**Save for Render:** `REDIS_URL=rediss://default:...@....upstash.io:6379`

**Verify:** After deploy, health check should show `"checkpointer": "redis"`. If Redis fails, the app falls back to in-memory (pipelines won't survive restarts).

---

## 5. Step-by-step: Qdrant Cloud (vector DB)

Research agent stores embeddings for RAG (retrieval-augmented generation).

1. Go to https://cloud.qdrant.io and sign up.
2. Click **Create Cluster** → **Free** tier.
3. Name: `acf-research`, region: closest to Render.
4. Wait for cluster status **Healthy**.
5. Open cluster → **Data Access** → **API Key** → **Create**.
6. Copy:
   - **Cluster URL:** `https://xxxxxxxx.us-east-1-0.aws.cloud.qdrant.io:6333`
   - **API Key:** `eyJ...`

**Save for Render:**
```env
VECTOR_BACKEND=qdrant
QDRANT_URL=https://xxxxxxxx.us-east-1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJ...
QDRANT_COLLECTION=acf_research
EMBEDDING_MODEL=text-embedding-004
EMBEDDING_DIMENSIONS=768
```

**Verify:** Run a pipeline in production → Qdrant dashboard → **Collections** → `acf_research` should appear with points.

### Alternative: Pinecone

1. Go to https://app.pinecone.io → create free **Starter** index.
2. Index name: `acf-research`, dimensions: `768`, metric: `cosine`.
3. Copy API key from **API Keys** page.

**Render env:**
```env
VECTOR_BACKEND=pinecone
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX=acf-research
PINECONE_ENVIRONMENT=us-east-1
```

---

## 6. Step-by-step: Clerk auth

Production requires Clerk — the smoke test script bypasses Clerk and won't appear in Clerk logs.

### 6.1 Create Clerk application

1. Go to https://dashboard.clerk.com and sign up.
2. Click **Add application** → name: `AI Content Factory`.
3. Choose sign-in methods: **Email**, **Google** (optional).
4. Select **Production** when ready for live (use **Development** for staging first).

### 6.2 Get API keys

1. In Clerk Dashboard → **Configure** → **API Keys**.
2. Copy:
   - **Publishable key:** `pk_live_...` (or `pk_test_...` for staging)
   - **Secret key:** `sk_live_...`

### 6.3 Get JWKS URL (backend JWT verification)

1. Clerk Dashboard → **Configure** → **API Keys** → scroll to **Advanced**.
2. Copy **JWKS URL**, format:
   ```
   https://<your-app>.clerk.accounts.dev/.well-known/jwks.json
   ```
   For production instance:
   ```
   https://clerk.<your-domain>.com/.well-known/jwks.json
   ```

### 6.4 Configure allowed origins

1. Clerk Dashboard → **Configure** → **Domains**.
2. Add your Vercel URL: `https://your-app.vercel.app`
3. Add Render API if needed for direct calls: `https://acf-api.onrender.com`

### 6.5 Set environment variables

**Render (backend):**
```env
CLERK_SECRET_KEY=sk_live_...
CLERK_JWKS_URL=https://<your-app>.clerk.accounts.dev/.well-known/jwks.json
ALLOW_DEV_AUTH=false
```

**Vercel (frontend):**
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
```

### 6.6 Verify Clerk integration

1. Open your Vercel URL → click **Sign in**.
2. Complete sign-in with email or Google.
3. Clerk Dashboard → **Users** → new user should appear.
4. Start a pipeline → backend creates/links user in Postgres with `clerk_id`.

---

## 7. Step-by-step: LangSmith

LangSmith captures LangGraph/LangChain traces automatically when env vars are set.

1. Go to https://smith.langchain.com and sign up.
2. Create or select organization.
3. Click **Settings** → **API Keys** → **Create API Key**.
4. Copy key: `lsv2_pt_...`
5. Note your project name (default: create `ai-content-factory`).

**Render env:**
```env
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=ai-content-factory
LANGSMITH_TRACING=true
```

**Verify:**
1. Run a pipeline in production.
2. LangSmith → **Projects** → `ai-content-factory` → traces appear within ~30 seconds.
3. Each agent node (research, content, enrich) shows as a trace span.

**Free tier:** 5,000 traces/month.

---

## 8. Step-by-step: Langfuse

Langfuse tracks individual LLM calls with token counts and latency.

1. Go to https://cloud.langfuse.com and sign up.
2. Create project: `ai-content-factory`.
3. Open project → **Settings** → **API Keys**.
4. Copy:
   - **Public key:** `pk-lf-...`
   - **Secret key:** `sk-lf-...`

**Render env:**
```env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_ENABLED=true
```

**Verify:**
1. Run a pipeline.
2. Langfuse → **Traces** → filter by project.
3. Each LLM call (research, content, visual, seo) appears as a generation.
4. Postgres `agent_traces.langfuse_trace_id` column links to Langfuse trace IDs.

**Free tier:** 50,000 events/month.

---

## 9. Step-by-step: Sentry

1. Go to https://sentry.io and sign up.
2. **Create Project** → platform: **FastAPI** (or Python).
3. Copy the **DSN**:
   ```
   https://xxx@xxx.ingest.sentry.io/xxx
   ```

**Render env:**
```env
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_TRACES_SAMPLE_RATE=0.2
```

**Verify:** Trigger an error (e.g. invalid pipeline config) → Sentry **Issues** shows the exception.

---

## 10. Step-by-step: Render (API + agents)

### 10.1 Create Web Service (Docker)

1. Go to https://dashboard.render.com → **New** → **Web Service**.
2. Connect GitHub repo: `vpeetla-ai/ai-content-factory`.
3. Configure:
   | Setting | Value |
   |---------|-------|
   | Name | `acf-api` |
   | Region | Same as Neon/Upstash |
   | Branch | `main` |
   | Runtime | **Docker** |
   | Dockerfile path | `backend/Dockerfile` |
   | Docker context | `.` (repository root) |
   | Instance type | Free |
4. Click **Advanced** → Health Check Path: `/health`
5. Click **Create Web Service**.

### 10.2 Set environment variables

Render Dashboard → `acf-api` → **Environment** → add all variables:

```env
# Core
APP_ENV=production
MOCK_LLM=false
ALLOW_DEV_AUTH=false
APP_SECRET_KEY=<run: openssl rand -hex 32>
RUN_MIGRATIONS_ON_STARTUP=true
LOG_JSON=true
WORKERS=2

# Database (from Neon)
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/ai_content_factory?sslmode=require

# Redis (from Upstash)
REDIS_URL=rediss://default:...@....upstash.io:6379

# LLM
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...
USE_LITELLM_PROXY=false

# Clerk
CLERK_SECRET_KEY=sk_live_...
CLERK_JWKS_URL=https://....clerk.accounts.dev/.well-known/jwks.json

# Vector DB
VECTOR_BACKEND=qdrant
QDRANT_URL=https://....cloud.qdrant.io:6333
QDRANT_API_KEY=eyJ...

# Observability
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=ai-content-factory
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
SENTRY_DSN=https://...@sentry.io/...

# URLs — update AFTER Vercel deploy
FRONTEND_URL=https://your-app.vercel.app
CORS_ORIGINS=https://your-app.vercel.app
```

6. Click **Save Changes** → Render redeploys automatically.

### 10.3 Get Deploy Hook (for GitHub Actions)

1. Render → `acf-api` → **Settings** → **Deploy Hook**.
2. Copy URL: `https://api.render.com/deploy/srv-...?key=...`
3. Save for GitHub secret `RENDER_DEPLOY_HOOK`.

### 10.4 Verify Render deploy

```bash
curl https://acf-api.onrender.com/health
```

Expected:
```json
{
  "status": "ok",
  "environment": "production",
  "mock_llm": false,
  "checkpointer": "redis",
  "clerk_configured": true,
  "vector_backend": "qdrant",
  "langsmith": true,
  "langfuse": true
}
```

> **Note:** Free Render services sleep after 15 min idle. First request after sleep takes ~30–60 seconds (cold start).

### 10.5 Alternative: Render Blueprint

1. Render → **New** → **Blueprint**.
2. Connect repo — Render reads `render.yaml`.
3. Creates API + Postgres automatically.
4. Still add external vars manually: Redis, Clerk, Qdrant, observability, LLM keys.

---

## 11. Step-by-step: Vercel (frontend)

### 11.1 Import project

1. Go to https://vercel.com/new.
2. Import GitHub repo `vpeetla-ai/ai-content-factory`.
3. Configure:
   | Setting | Value |
   |---------|-------|
   | Framework Preset | Next.js |
   | Root Directory | `frontend` |
   | Build Command | `npm run build` (default) |
   | Output Directory | `.next` (default) |

### 11.2 Set environment variables

Vercel → Project → **Settings** → **Environment Variables**:

| Variable | Value | Environment |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://acf-api.onrender.com/api/v1` | Production |
| `NEXT_PUBLIC_WS_URL` | `https://acf-api.onrender.com` | Production |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | `pk_live_...` | Production |

For **Preview** deployments, use the same or staging Clerk keys.

### 11.3 Deploy

1. Click **Deploy**.
2. Note your URL: `https://ai-content-factory-xxx.vercel.app`

### 11.4 Update Render CORS

Go back to Render → Environment:
```env
FRONTEND_URL=https://ai-content-factory-xxx.vercel.app
CORS_ORIGINS=https://ai-content-factory-xxx.vercel.app
```
Save → Render redeploys.

### 11.5 Get Vercel IDs for GitHub Actions

1. **Vercel Token:** Account Settings → **Tokens** → Create → copy `VERCEL_TOKEN`.
2. **Org ID & Project ID:** Project → **Settings** → **General** → scroll to **Project ID**.
   Or run locally:
   ```bash
   npx vercel link
   cat .vercel/project.json
   ```
   Copy `orgId` and `projectId`.

---

## 12. Step-by-step: GitHub Actions CD

1. Go to https://github.com/vpeetla-ai/ai-content-factory/settings/secrets/actions
2. Add repository secrets:

| Secret name | Value | Source |
|-------------|-------|--------|
| `RENDER_DEPLOY_HOOK` | `https://api.render.com/deploy/srv-...?key=...` | Render Deploy Hook |
| `VERCEL_TOKEN` | `vercel_...` | Vercel Account Tokens |
| `VERCEL_ORG_ID` | `team_...` | Vercel project.json |
| `VERCEL_PROJECT_ID` | `prj_...` | Vercel project.json |

3. Push to `main` — workflows run:
   - `ci.yml` — backend import + frontend build
   - `deploy.yml` — triggers Render + Vercel deploy

```bash
git push origin main
```

Monitor: GitHub → **Actions** tab.

---

## 13. Environment variable reference

### Render (backend) — complete list

See `.env.production.example` for full template.

### Vercel (frontend) — complete list

See `frontend/.env.production.example`.

### Local — complete list

See `.env.local.example` and `frontend/.env.local.example`.

---

## 14. Local development

```bash
cp .env.example .env
cp .env.local.example .env.local
cp frontend/.env.local.example frontend/.env.local

make install
make up          # postgres + redis + qdrant
make migrate
make api         # terminal 1
make frontend    # terminal 2
make test
```

To test Clerk locally, add test keys to `.env.local` and `frontend/.env.local`, then restart.

---

## 15. Verify production

### End-to-end test

1. Open Vercel URL → Sign in with Clerk.
2. Enter a topic → **Start Pipeline**.
3. Watch agent log stream (WebSocket).
4. Approve at HITL gate.
5. Check integrations:

| Service | Where to look |
|---------|---------------|
| LangSmith | Project `ai-content-factory` → Traces |
| Langfuse | Traces → generations per agent |
| Clerk | Users → your account |
| Qdrant | Collection `acf_research` → points count |
| Sentry | Issues (only if errors occurred) |
| Postgres | Render logs or Neon SQL: `SELECT * FROM agent_traces ORDER BY id DESC LIMIT 5` |

### Health check script

```bash
curl -s https://<your-api>/health | python3 -m json.tool
```

---

## 16. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Empty LangSmith | Missing API key | Set `LANGSMITH_API_KEY`, redeploy Render |
| Empty Langfuse | Missing keys | Set both `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` |
| Empty Clerk logs | Dev bypass or no UI sign-in | Sign in via Vercel UI, not smoke script |
| Empty Qdrant | No pipeline run yet | Run pipeline; check `VECTOR_BACKEND=qdrant` |
| CORS error | Wrong origin | Set `CORS_ORIGINS` to exact Vercel URL (no trailing slash) |
| WebSocket disconnect | Missing token | Ensure signed in; token passed in WS auth |
| 401 on API | Clerk misconfigured | Verify `CLERK_JWKS_URL` matches Clerk instance |
| Cold start 60s | Render free tier sleep | Upgrade Render or accept cold starts |
| Redis fallback memory | Upstash URL wrong | Use `rediss://` TLS URL from Upstash |
| Migration failed | DB URL wrong | Check Neon connection string + SSL |

---

## Cost map (free tiers)

| Service | Free limit |
|---------|------------|
| Vercel | 100 GB bandwidth |
| Render | 750 hrs/mo (sleeps after 15 min idle) |
| Neon | 0.5 GB storage |
| Upstash Redis | 10K commands/day |
| Clerk | 10K MAU |
| LangSmith | 5K traces/mo |
| Langfuse Cloud | 50K events/mo |
| Qdrant Cloud | 1 GB cluster |
| Gemini / Groq | Provider free tiers |

For always-on API without cold starts: Render Starter plan (~$7/mo).
