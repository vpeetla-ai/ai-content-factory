# 03 — Content Pipeline + HITL (AWS)

## Problem

Multi-platform content automation requires **human approval** before irreversible publish side effects.

## Architecture

```text
CloudFront → ALB → ECS (FastAPI + LangGraph worker)
                 → RDS Postgres (runs, traces, HITL state)
                 → ElastiCache Redis (checkpointer)
                 → S3 (media)
                 → Secrets Manager (OAuth tokens encrypted)
Step Functions (optional) → scheduled cron pipelines
```

## Key decisions

| Decision | Rationale |
|----------|-----------|
| `interrupt_before` HITL | LangGraph native pause/resume |
| Gateway on publish | AegisAI authorizes platform APIs |
| LinkedIn/X only auto-publish | Honest API scope (ADR-008) |

## Cost (USD/month)

| Tier | Est. |
|------|------|
| S | $100 |
| M | $400 |
| L | $1,500 |

## Terraform

[`infra/aws/03-content-factory-hitl/`](../../infra/aws/03-content-factory-hitl/)

## Related

- [SLO.md](../SLO.md) · [SCALE.md](../SCALE.md)
