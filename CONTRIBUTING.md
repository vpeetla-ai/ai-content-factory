# Contributing to AI Content Factory

Thank you for your interest in contributing. This project is a production reference for multi-agent content orchestration — issues, docs improvements, and focused PRs are all valuable.

## Ways to contribute

| Area | Examples |
|------|----------|
| **Good first issues** | Docs, README, tests, small UI polish |
| **Platform adapters** | Wire OAuth for LinkedIn, Substack, Medium, Instagram, X |
| **Observability** | Langfuse dashboards, Sentry breadcrumbs, trace examples |
| **RAG** | Qdrant/Pinecone ingestion scripts, eval fixtures |
| **Agent layer** | Prompt tuning, new nodes, error recovery |

Browse [open issues](https://github.com/vpeetla-ai/ai-content-factory/issues) or open a new one before large changes.

## Development setup

```bash
cp .env.example .env
cp .env.local.example .env.local
cp frontend/.env.local.example frontend/.env.local

make install
make up
make migrate
make api        # terminal 1
make frontend   # terminal 2
make test
```

See [README.md](README.md) and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full details.

## Pull request guidelines

1. **One concern per PR** — e.g. "Add Substack OAuth adapter", not "misc fixes"
2. **Run tests** — `make test` before opening
3. **No secrets** — never commit `.env`, API keys, or tokens
4. **Match conventions** — follow existing patterns in `agents/`, `backend/`, `frontend/`
5. **Update docs** — if you change env vars, API routes, or deploy steps

## Commit messages

Use clear, imperative subjects:

```
Add LinkedIn publish adapter with token refresh
Fix HITL WebSocket auth on reconnect
Document Qdrant collection setup in DEPLOYMENT.md
```

## Code of conduct

Be respectful and constructive. Assume good intent. Focus feedback on the work, not the person.

## Questions

- Open a [GitHub Discussion](https://github.com/vpeetla-ai/ai-content-factory/discussions) (enable in repo settings if not yet on)
- Connect on [LinkedIn](https://linkedin.com/in/venkata-peetla)
