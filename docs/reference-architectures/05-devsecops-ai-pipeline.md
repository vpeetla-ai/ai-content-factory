# 05 — DevSecOps + AI Pipeline

## Problem

Embed AI into existing developer workflows: scan PRs, synthesize risk, track posture over time.

## Architecture

```text
GitHub PR → Actions: Semgrep + Trivy
         → risk synthesizer (LLM or rule-based)
         → artifact + PR comment
         → DynamoDB (historical snapshots)
         → Slack webhook
```

Implemented in this repo: [DEVSECOPS.md](../DEVSECOPS.md), [security-scan.yml](../../.github/workflows/security-scan.yml).

## Cost (USD/month)

| Tier | Est. |
|------|------|
| S | $30 (Actions minutes only) |
| M | $100 (+ DynamoDB) |
| L | $250 (+ Security Hub optional) |

## Terraform

[`infra/aws/05-devsecops-ai/`](../../infra/aws/05-devsecops-ai/)
