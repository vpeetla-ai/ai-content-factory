# AI Content Factory

Multi-agent content orchestration platform — **Free-First Stack** per architecture HLD + LLD.

## Architecture

```
Client (Next.js) → CDN/Edge → API Gateway → FastAPI Services → LangGraph Agents → LLM Providers → Data Layer → Publish Targets → Observability
```

| Layer | Components |
|-------|-----------|
| **Frontend** | Next.js 14, React Query, Zustand, Socket.io, SSE |
| **Backend** | FastAPI — API, Pipeline, HITL, Publisher, Auth services |
| **Agents** | LangGraph — Research → Content → Enrich (Visual+SEO) → HITL → Publish |
| **LLM** | LiteLLM router — Gemini → Groq → Cerebras → Claude Haiku → Ollama |
| **Data** | PostgreSQL, Redis, Qdrant/Pinecone, Cloudflare R2 |
| **Observability** | Langfuse, LangSmith, Sentry, OpenTelemetry |

## Project Structure

```
ai-content-factory/
├── agents/              # LangGraph state machine + 5 agents
├── backend/             # FastAPI microservices
│   ├── app/
│   │   ├── api/routes/  # REST contracts (/api/v1)
│   │   ├── services/    # Pipeline, HITL, Publisher
│   │   ├── models/      # SQLAlchemy (6 tables)
│   │   └── websocket/   # Socket.io gateway
│   └── alembic/         # DB migrations
├── frontend/            # Next.js 14 dashboard
├── docker-compose.yml   # Local dev stack
├── litellm_config.yaml  # Free-first model routing
└── .env.example
```

## Local verification (mock LLM — no API keys)

```bash
cp .env.example .env   # MOCK_LLM=true by default
docker compose up -d postgres redis
cd backend && pip install -r requirements.txt && alembic upgrade head
uvicorn app.main:app --reload --port 8000

# separate terminal
cd frontend && npm install && npm run dev
```

1. Open http://localhost:3000
2. Start a pipeline — agents run with **mock responses** (no API keys needed)
3. Watch **Agent Orchestration** log via WebSocket + SSE live stream
4. Approve at **HITL gate** — pipeline resumes via **Redis checkpointer**
5. Verify `published_posts` and `agent_traces` in Postgres

```bash
# Check traces + published posts
psql postgresql://acf:acf@localhost:5432/ai_content_factory -c "SELECT agent_name, model_used, input_tokens FROM agent_traces LIMIT 10;"
psql postgresql://acf:acf@localhost:5432/ai_content_factory -c "SELECT platform, external_post_id, post_url FROM published_posts;"
```

Set `MOCK_LLM=false` and add `GOOGLE_API_KEY` / `GROQ_API_KEY` when ready for real providers.


### 1. Environment

```bash
cp .env.example .env
# Add GOOGLE_API_KEY, GROQ_API_KEY (free tiers)
```

### 2. Docker (recommended)

```bash
docker compose up -d postgres redis qdrant
docker compose up api
```

### 3. Database migrations

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### 5. API docs

http://localhost:8000/docs (FastAPI auto-docs)

## API Contracts

Base URL: `/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/pipelines/run` | Start content pipeline |
| GET | `/pipelines/{run_id}` | Get run state |
| GET | `/pipelines/{run_id}/stream` | SSE agent outputs |
| POST | `/hitl/{run_id}/approve` | Approve HITL gate |
| POST | `/auth/token` | Exchange Clerk → JWT |

## Agent Pipeline

```
START → Research (Gemini) → Content (Gemini/Haiku) → Enrich [Visual + SEO parallel] → HITL ✋ → Publish → END
```

## Cost (Dev Phase)

~$1–5/month — Claude Haiku fallback only paid component.

## License

MIT
