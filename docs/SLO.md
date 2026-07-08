# Service Level Objectives — AI Content Factory

Production SLO definitions for portfolio reviewers and on-call runbooks.

## Service tiers

| Tier | Component | User impact if down |
|------|-----------|---------------------|
| **Tier 1** | Pipeline API (`POST /pipelines/run`) | Cannot create content runs |
| **Tier 1** | HITL approve (`POST /hitl/{id}/approve`) | Runs stuck at interrupt |
| **Tier 2** | OAuth connect (LinkedIn/X) | Cannot auto-publish |
| **Tier 3** | Public ops metrics | Portfolio dashboard stale |

## SLO targets

| SLI | Target | Measurement window | Error budget |
|-----|--------|-------------------|--------------|
| **API availability** | 99.5% | 30 days | 3.6 h downtime/month |
| **Pipeline success rate** | ≥ 95% | 7 days | 5% failed runs |
| **HITL resume latency** | P95 < 2s | 7 days | — |
| **Graph node latency** | P95 < 30s (mock LLM off) | 7 days | — |
| **Publish path gateway** | 100% side effects gated | Per release | 0 unauthorized publishes |

## How we measure

| Signal | Source |
|--------|--------|
| Availability | Render health checks + `/health` |
| Pipeline success | `pipeline_runs.status` in Postgres |
| Node latency | `agent_traces.latency_ms` |
| Cost per run | `pipeline_runs.total_cost_usd` |
| Eval regression | `golden-eval-registry` graph_hitl CI gate |

Public aggregate: `GET /api/v1/ops/metrics`

## Alerting (production)

| Condition | Action |
|-----------|--------|
| `/health` degraded > 5 min | Page on-call |
| Pipeline error rate > 10% / 1h | Slack + investigate Langfuse trace |
| Golden eval CI fail | Block merge |
| Budget breach (agent-finops) | Halt LLM dispatch |

## Related

- [SCALE.md](./SCALE.md) — S/M/L deployment tiers
- [DEVSECOPS.md](./DEVSECOPS.md) — build-time security gates
- [FINOPS.md](./FINOPS.md) — agent + cloud cost governance
