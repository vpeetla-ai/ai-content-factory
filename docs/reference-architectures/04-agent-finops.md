# 04 — Agent FinOps Metering

## Problem

Agent fleets burn token budgets silently — enterprises need a **canonical cost ledger** with breach actions.

## Architecture

```text
Agent consumers → agent-finops API → RDS (usage events)
                                  → Budget rules → SNS/Slack alert
                                  → Kill switch callback (AegisAI)
Cost Explorer (read-only) → anomaly job → weekly report
```

## Cost (USD/month)

| Tier | Est. |
|------|------|
| S | $40 |
| M | $150 |
| L | $400 |

## Terraform

[`infra/aws/04-agent-finops/`](../../infra/aws/04-agent-finops/)
