---
name: governed-ai-stack
description: >-
  Maps tasks to the vpeetla-ai reference stack (VAP, AegisAI, RAG, DomainForge,
  AgentOps, FinOps, Content, LoopForge, Sentinel, vLLM, Evals, Interview). Use when
  choosing which repo to change.
---

# Governed AI Stack

Read [CONTEXT.md](../../../CONTEXT.md) for terms, demo URLs, and Jul 2026 org changes.

## Layer routing

| If the task is about… | Work in… |
|------------------------|----------|
| Multi-agent orchestration, RAG strategies, notify | venkat-ai-platform |
| Policy, HITL, audit, tool authorization | aegisai-enterprise-agent-platform |
| Retrieval, citations, access control, ingest | enterprise_rag_platform |
| RAG + PEFT, QLoRA, adapter registry, S0–S4 eval ladder | domainforge-rag-peft |
| Real-time voice ASR → LLM → TTS, latency budgets | voiceforge-assistant |
| Missions, traces, eval gates | aegisloop-agentops-workbench |
| Real usage metering, budgets, cost-breach signals | agent-finops |
| Content pipeline, publish, cron, OAuth | ai-content-factory |
| Overnight intelligence brief, governed email | sentinel-brief |
| Self-improving loops, repo fix, RAG tuning | loop-engine-agent-platform |
| LLM inference, KV cache, batching education | vllm-architecture-lab |
| Golden eval fixtures, regression contracts | golden-eval-registry |
| Interview prep — system design, STAR, trade-offs | ai-architect-interview-playbook |
| BYOK mock interview judge UI | ai-architect-practice-arena |
| Agent skills, MCP, protocol stack | vpeetla-ai-skills |
| ADRs, case studies, portfolio copy | ai-architecture-portfolio |
| Public site, ecosystem wiring | venkat-ai-portfolio |
| Single pattern reference (ReAct, etc.) | *-agent-pattern repos |

## Integration rules

- VAP **delegates** side effects; AegisAI **authorizes** them
- Enterprise RAG **feeds** VAP strategies; does not replace gateway
- DomainForge **complements** Enterprise RAG with PEFT behavior adaptation (ADR-019)
- LoopForge **improves** configs/prompts; does not replace orchestration
- AegisLoop **meters** via agent-finops; uses golden-eval CI for mission gates

## Production API keys (Jul 2026)

Several APIs gate writes: `VAP_API_KEY`, `LOOPFORGE_API_KEY`, Enterprise RAG API key, Sentinel run key, AegisLoop mission key. Check each repo's `.env.example` / `DEPLOYMENT.md`.

## Essay

[From Multi-Agent OS to Agent Governance](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/case-studies/from-multi-agent-os-to-agent-governance.md)
