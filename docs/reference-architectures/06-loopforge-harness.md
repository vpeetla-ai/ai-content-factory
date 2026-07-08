# 06 — Self-Improving Agent Harness

## Problem

Agents must improve via **eval-gated loops** without pushing directly to protected branches.

## Architecture

```text
EventBridge (schedule) → ECS LoopForge worker
                      → GitHub OIDC (scoped PR only)
                      → golden-eval-registry CI gate
                      → Langfuse harness export
                      → S3 (eval artifacts)
```

## Key decisions

| Decision | Rationale |
|----------|-----------|
| Branch `loopforge/fix-{id}` only | Never push to main |
| Gateway on git push | AegisAI HITL for PR create |
| ODAEU loop | Observe → Decide → Act → Evaluate → Update |

## Cost (USD/month)

| Tier | Est. |
|------|------|
| S | $90 |
| M | $400 |
| L | $1,800 |

## Terraform

[`infra/aws/06-loopforge-harness/`](../../infra/aws/06-loopforge-harness/)
