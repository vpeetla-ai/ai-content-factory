# AWS AI Reference Architectures

Six production-shaped patterns for the [vpeetla-ai](https://github.com/vpeetla-ai) governed agent stack.

Each includes: problem statement, architecture diagram, key decisions, S/M/L cost analysis, Well-Architected checklist, and Terraform skeleton.

| # | Pattern | Maps to | Terraform |
|---|---------|---------|-----------|
| 01 | Governed multi-agent API | VAP + AegisAI | [infra/aws/01-governed-agents/](../infra/aws/01-governed-agents/) |
| 02 | Enterprise RAG (access-aware) | enterprise_rag_platform | [infra/aws/02-enterprise-rag/](../infra/aws/02-enterprise-rag/) |
| 03 | Content pipeline + HITL | ai-content-factory | [infra/aws/03-content-factory-hitl/](../infra/aws/03-content-factory-hitl/) |
| 04 | Agent FinOps metering | agent-finops | [infra/aws/04-agent-finops/](../infra/aws/04-agent-finops/) |
| 05 | DevSecOps + AI pipeline | CI security synthesis | [infra/aws/05-devsecops-ai/](../infra/aws/05-devsecops-ai/) |
| 06 | Self-improving agent harness | LoopForge | [infra/aws/06-loopforge-harness/](../infra/aws/06-loopforge-harness/) |

## Well-Architected lens (all patterns)

| Pillar | How we address it |
|--------|-------------------|
| **Operational excellence** | Langfuse traces, golden eval CI, `/ops/metrics` |
| **Security** | Gateway + HITL, Semgrep/Trivy CI, secrets in SM |
| **Reliability** | Multi-AZ RDS, health checks, decline-to-answer |
| **Performance** | Redis checkpointer, hybrid RAG, LiteLLM routing |
| **Cost** | Fargate spot, S/M/L tiers, agent-finops budgets |
| **Sustainability** | Right-size Fargate; batch overnight jobs |

## Cost summary (USD/month, us-east-1)

| Pattern | S | M | L |
|---------|---|---|---|
| 01 Governed agents | $80 | $350 | $1,200 |
| 02 Enterprise RAG | $120 | $500 | $2,000 |
| 03 Content + HITL | $100 | $400 | $1,500 |
| 04 Agent FinOps | $40 | $150 | $400 |
| 05 DevSecOps AI | $30 | $100 | $250 |
| 06 LoopForge harness | $90 | $400 | $1,800 |

*Estimates are order-of-magnitude for architecture reviews — adjust for traffic.*

## Related

- [ADR-015 Real AWS/GCP infra](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-015-real-aws-gcp-infra-phase-c.md)
- [SCALE.md](../SCALE.md)
