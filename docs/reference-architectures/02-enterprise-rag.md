# 02 — Enterprise RAG (Access-Aware)

## Problem

Document Q&A must enforce **access before ranking** and provide citations with decline-to-answer.

## Architecture

```text
API Gateway → Lambda/ECS (RAG API)
           → OpenSearch (hybrid vectors + BM25)
           → S3 (document store)
           → Bedrock (embeddings + optional generation)
           → Principal ACL index (per-chunk clearance)
```

## Key decisions

| Decision | Rationale |
|----------|-----------|
| Access-before-ranking | Security is not post-hoc filtering |
| Cross-encoder rerank | Quality on top-50 candidates |
| Decline-to-answer | Hallucination mitigation |

## Cost (USD/month)

| Tier | Est. |
|------|------|
| S | $120 (OpenSearch t3.small.search + S3) |
| M | $500 |
| L | $2,000 (multi-AZ, larger index) |

## Terraform

[`infra/aws/02-enterprise-rag/`](../../infra/aws/02-enterprise-rag/)
