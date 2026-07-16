# FinOps — Agent + Cloud Cost Intelligence

Dual-layer cost governance for the vpeetla-ai stack.

## Two FinOps layers

| Layer | Service | What it meters |
|-------|---------|----------------|
| **Agent FinOps** | [agent-finops](https://github.com/vpeetla-ai/agent-finops) | LLM tokens, model calls, budget breach → kill switch |
| **Cloud FinOps** | `scripts/cloud_cost_snapshot.py` | AWS Cost Explorer (or mock) — infra spend |

Content Factory records per-run cost in `pipeline_runs.total_cost_usd` via `RunMetrics`.

## Agent cost flow

```text
LangGraph node → agents/llm.py → (optional) aegis-llm-gateway → RunMetrics → pipeline_runs.total_cost_usd
                                      ↓
                              agent-finops POST /v1/usage when AGENTFINOPS_URL set
```

When the LLM gateway is configured, ACF **selects** agent→thesis/tier headers; the gateway meters usage (ADR-028/029).

Public aggregate: `GET /api/v1/ops/metrics` → `total_cost_usd`, `avg_pipeline_cost_usd`

### Cost per compliant outcome (ADR-029)

Optional plane KPI:

```bash
POST {AGENTFINOPS_URL}/v1/outcomes
GET  {AGENTFINOPS_URL}/v1/kpi/cost-per-compliant-outcome?tenant_id=ai-content-factory
```

Compliant = eval pass + no policy deny + HITL when required + budget OK.

## Cloud cost snapshot

```bash
# Mock mode (no AWS credentials) — CI + local
python scripts/cloud_cost_snapshot.py --mock

# Real mode — requires AWS CE read IAM
AWS_PROFILE=finops-read python scripts/cloud_cost_snapshot.py --days 30
```

Output: JSON with daily spend, service breakdown, anomaly flags (spike > 20% WoW).

## Cost tiers (Content Factory)

| Tier | Est. cost/run (real LLM) | Monthly at 100 runs |
|------|--------------------------|---------------------|
| Mock LLM | $0 | $0 |
| Groq Llama 3.3 | $0.02–$0.08 | $2–$8 |
| Gemini Flash + Haiku mix | $0.10–$0.25 | $10–$25 |

## Governance actions

| Signal | Action |
|--------|--------|
| `MISSION_BUDGET_USD` exceeded | Halt further agent dispatch (AegisLoop pattern) |
| agent-finops breach | Kill switch via AegisAI |
| Cloud anomaly | Review in weekly FinOps report |

## Related

- [ADR-011 Agent FinOps standalone](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-011-agent-finops-standalone-service.md)
- [ADR-029 App-owned role-aware routing + cost-per-compliant-outcome](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-029-app-owned-role-aware-routing-contract.md)
- [SCALE.md](./SCALE.md)
