# Scale Tiers — AI Content Factory

S/M/L deployment models for Principal-level architecture reviews.

## Summary

| Tier | Runs/day | Users | Stack | Est. monthly cost |
|------|----------|-------|-------|-------------------|
| **S — Demo** | < 50 | < 20 | Vercel + Render free + Neon free | $0–$25 |
| **M — Team** | 50–500 | 20–200 | Vercel Pro + Render Standard + Neon + Upstash | $150–$400 |
| **L — Production** | 500+ | 200+ | AWS ECS Fargate + RDS + ElastiCache + CloudFront | $800–$2,500 |

See [reference-architectures/03-content-factory-hitl.md](./reference-architectures/03-content-factory-hitl.md) for AWS Terraform skeleton.

## S — Small (current default)

```text
Vercel (Next.js) → Render (FastAPI Docker) → Neon Postgres + Upstash Redis
                                              → Qdrant Cloud (optional)
                                              → Groq / Gemini via LiteLLM
```

**Trade-offs:** Cold starts on Render free tier; single-region; manual scale.

**When to use:** Portfolio demos, invite-only pilots, interview walkthroughs.

## M — Medium

| Change | Why |
|--------|-----|
| Render `standard` plan or 2+ instances | Remove cold start |
| Redis checkpointer always on | Durable HITL resume |
| Langfuse Cloud + Sentry Pro | Trace retention + alerting |
| Rate limits per user (existing) | Abuse protection |

**Capacity:** ~10 concurrent pipelines, P95 end-to-end < 3 min with real LLMs.

## L — Large (AWS reference)

```text
CloudFront → ALB → ECS Fargate (API + worker)
                 → RDS Postgres Multi-AZ
                 → ElastiCache Redis
                 → S3 (media) + Bedrock/OpenSearch (RAG at scale)
                 → Step Functions (optional cron orchestration)
```

**Capacity:** Horizontal worker pool; autoscale on queue depth.

**Well-Architected highlights:**

- **Reliability:** Multi-AZ RDS, health checks, circuit breakers on LLM providers
- **Security:** WAF on ALB, secrets in Secrets Manager, gateway fail-closed
- **Cost:** Fargate spot for workers, S3 lifecycle for media
- **Performance:** Connection pooling, Redis checkpointer, CDN for static

## Scaling bottlenecks

| Bottleneck | Mitigation |
|------------|------------|
| LLM rate limits | LiteLLM router + multi-provider fallback |
| Postgres writes (traces) | Batch trace flush; archive to S3 |
| HITL human latency | Not a system bottleneck — by design |
| Vector ingest | Async Celery worker (Phase 2) |

## Related

- [SLO.md](./SLO.md)
- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [ADR-005](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/adr/ADR-005-reference-stack-free-tier.md)
