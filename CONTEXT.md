# vpeetla-ai Domain Model

Shared vocabulary for all org repos. Agents should use these terms consistently.

## Stack layers (6 questions)

| Layer | Question | Repo | Demo |
|-------|----------|------|------|
| Orchestration | What should agents do? | venkat-ai-platform | venkat-ai-platform.vercel.app |
| Governance | What are agents allowed? | aegisai-enterprise-agent-platform | aegisai-enterprise-agent-platform.vercel.app |
| Knowledge | What knowledge can they use? | enterprise_rag_platform | enterprise-rag-platform.vercel.app |
| AgentOps | How do we operate fleets? | aegisloop-agentops-workbench | aegisloop-agentops-workbench.vercel.app |
| Application | What do they produce? | ai-content-factory | ai-content-factory-iota.vercel.app |
| Self-improvement | How do agents improve? | loop-engine-agent-platform | demo-omega-taupe.vercel.app |

## Core terms

| Term | Meaning |
|------|---------|
| **Harness** | Outer scheduler: budgets, tracing, eval gates, loop termination (LoopForge, ODAEU) |
| **Gateway** | AegisAI runtime control plane — policy + HITL + audit before tool side effects |
| **ODAEU** | Observe → Decide → Act → Evaluate → Update (outer self-improve loop) |
| **Access-before-ranking** | Filter chunks by principal clearance before hybrid retrieval scores |
| **HITL** | Human-in-the-loop gate before irreversible actions (publish, push, deploy) |
| **Mission** | Bounded AgentOps unit in AegisLoop (research, content, incident, etc.) |
| **Orchestrator** | LangGraph node that plans and routes between specialist agents |
| **loopforge/fix-{id}** | Branch name for automated repo fixes — never push directly to `main` |
| **Stub mode** | `AGENT_RUNTIME_MODE=local_stub` or MockLLM — no API keys required |

## Agent patterns (VAP series)

| Pattern | Repo | Use when |
|---------|------|----------|
| ReAct | react-agent-pattern | Tool loops with thought → action → observation |
| Reflection | reflection-agent-pattern | Critique-and-revise before delivery |
| Plan-Execute | plan-execute-agent-pattern | Explicit plan before multi-step execution |
| Multi-Agent | multi-agent-system-pattern | Role specialists + orchestrator delegation |
| Swarm | swarm-agent-pattern | Parallel workers + aggregation |

## Deploy boundaries (ADR-005)

- **UI** → Vercel (static or Next.js)
- **API** → Render (Docker or native Python)
- **Vectors** → Qdrant Cloud (optional)
- **LLM** → Groq / OpenRouter / LiteLLM routing
- **Free tier** → `plan: free` in render.yaml; expect cold starts

## Integration rule

Side effects (notify, publish, deploy, git push to protected branch) → **gateway or HITL** unless explicitly in local stub mode.
