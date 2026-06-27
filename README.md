# AI Content Factory

Multi-agent content orchestration platform — **Free-First Stack** per architecture HLD + LLD.

## High-Level Design (HLD)

Nine-layer architecture — **free-first stack**, multi-agent orchestration with human-in-the-loop (HITL).

```mermaid
flowchart TB
    subgraph L0["L0 · Client"]
        direction LR
        NEXT["🖥️ Next.js 14<br/>App Router · RSC"]
        SPA["⚛️ React SPA<br/>Vite · shadcn/ui"]
        MOB["📱 Mobile<br/>React Native · Expo"]
    end

    subgraph L1["L1 · Edge / CDN"]
        direction LR
        CF["🌐 Cloudflare CDN<br/>WAF · DDoS"]
        VERCEL["▲ Vercel Edge<br/>ISR · Middleware"]
        AUTH_FE["🔐 Auth Layer<br/>Clerk · JWT · RBAC"]
    end

    subgraph L2["L2 · API Gateway"]
        direction LR
        NGINX["🔀 NGINX / Traefik<br/>TLS · Reverse proxy"]
        RATE["🚦 Rate Limiter<br/>Redis sliding window"]
        LITELLM_GW["🔁 LiteLLM Router<br/>Fallback · Load balance"]
        WS_GW["🔌 WS Gateway<br/>Socket.io · HITL events"]
    end

    subgraph L3["L3 · Backend Services"]
        direction LR
        API_SVC["⚡ API Service<br/>FastAPI · Pydantic v2"]
        PIPE_SVC["🔧 Pipeline Service<br/>LangGraph runner"]
        HITL_SVC["🧑‍💼 HITL Service<br/>Interrupt · Approval"]
        PUB_SVC["🚀 Publisher Service<br/>Platform adapters"]
        AUTH_SVC["🛡️ Auth Service<br/>JWT · API keys"]
    end

    subgraph L4["L4 · Agent Layer"]
        direction LR
        LG["🕸️ LangGraph Engine<br/>StateGraph · Checkpointer"]
        RES["🔬 Research<br/>Gemini Flash"]
        CONT["✍️ Content<br/>Gemini / Haiku"]
        SEO["📈 SEO<br/>Groq Llama 3.3"]
        VIS["🎨 Visual<br/>Groq · img prompts"]
    end

    subgraph L5["L5 · LLM Providers"]
        direction LR
        GEM["✦ Gemini 2.5 Flash"]
        GROQ["⚡ Groq"]
        CER["🧠 Cerebras"]
        HAIKU["◆ Claude Haiku"]
        OLL["🏠 Ollama local"]
    end

    subgraph L6["L6 · Data Layer"]
        direction LR
        PG["🐘 PostgreSQL<br/>Supabase / Neon"]
        REDIS["🔴 Redis<br/>Cache · Queue · State"]
        VEC["🌲 Pinecone / Qdrant<br/>Vector · RAG"]
        R2["🪣 Cloudflare R2<br/>Media assets"]
        LS["🔍 LangSmith<br/>Traces · Evals"]
    end

    subgraph L7["L7 · Publish Targets"]
        direction LR
        LI["💼 LinkedIn"]
        SS["📰 Substack"]
        MD["📝 Medium"]
        IG["📸 Instagram"]
        X["𝕏 X API v2"]
    end

    subgraph L8["L8 · Observability"]
        direction LR
        LF["📊 Langfuse"]
        GRAF["📈 Grafana + Prometheus"]
        SENTRY["🚨 Sentry"]
        OTEL["🔭 OpenTelemetry"]
    end

    L0 -->|"HTTPS · TLS 1.3"| L1
    L1 -->|"Internal VPC"| L2
    L2 -->|"HTTP/2"| L3
    L3 -->|"Celery · Redis Streams"| L4
    L4 -->|"OpenAI-compatible API"| L5
    L4 --> L6
    L3 --> L6
    L3 -->|"OAuth2 · Platform APIs"| L7
    L3 -.->|"Metrics · Traces"| L8
    L4 -.-> L8
    L5 -.-> L8

    style L0 fill:#0e1a2e,stroke:#38bdf8,color:#e2e4f0
    style L1 fill:#1a1408,stroke:#fb923c,color:#e2e4f0
    style L2 fill:#1a0a10,stroke:#ff4d6d,color:#e2e4f0
    style L3 fill:#12101f,stroke:#7c6fff,color:#e2e4f0
    style L4 fill:#0a1a18,stroke:#00e5c3,color:#e2e4f0
    style L5 fill:#14101f,stroke:#a78bfa,color:#e2e4f0
    style L6 fill:#1a1608,stroke:#ffb830,color:#e2e4f0
    style L7 fill:#0a1a12,stroke:#00d68f,color:#e2e4f0
    style L8 fill:#101018,stroke:#5a5a80,color:#e2e4f0
```

### Layer summary

| Layer | Components |
|-------|-----------|
| **L0 Client** | Next.js 14, React SPA, Mobile (Expo) |
| **L1 Edge / CDN** | Cloudflare, Vercel Edge, Clerk / JWT auth |
| **L2 API Gateway** | NGINX/Traefik, Redis rate limiter, LiteLLM router, Socket.io WS |
| **L3 Backend** | FastAPI — API, Pipeline, HITL, Publisher, Auth services |
| **L4 Agents** | LangGraph — Research → Content → Enrich (Visual+SEO) → HITL → Publish |
| **L5 LLM** | LiteLLM free-first — Gemini → Groq → Cerebras → Haiku → Ollama |
| **L6 Data** | PostgreSQL, Redis, Qdrant/Pinecone, Cloudflare R2, LangSmith |
| **L7 Publish** | LinkedIn, Substack, Medium, Instagram, X |
| **L8 Observability** | Langfuse, Grafana/Prometheus, Sentry, OpenTelemetry |

### Agent execution flow (LLD)

```mermaid
flowchart LR
    START((Start)) --> RESEARCH["🔬 Research Agent<br/>Gemini 2.5 Flash"]
    RESEARCH --> CONTENT["✍️ Content Agent<br/>5× platform drafts"]
    CONTENT --> ENRICH["⚡ Enrich<br/>Visual ∥ SEO"]
    ENRICH --> HITL{"🧑‍💼 HITL Gate<br/>interrupt_before"}
    HITL -->|"approve / edit"| PUBLISH["🚀 Publisher Agent<br/>Platform APIs"]
    HITL -->|"reject"| END_ERR((Stop))
    PUBLISH --> DONE((Done))

    style HITL fill:#0a2a1a,stroke:#00d68f,color:#e2e4f0
    style DONE fill:#0a2a1a,stroke:#00d68f,color:#e2e4f0
```

> Full interactive HLD + LLD (DB schema, API contracts, cost map): see [`ai-content-factory-architecture.html`](./ai-content-factory-architecture.html)

## Architecture (implementation map)

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
