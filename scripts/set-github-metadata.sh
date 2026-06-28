#!/usr/bin/env bash
# Set GitHub repo descriptions and topics for vpeetla-ai org/user repos.
# Prerequisites: gh auth login (see docs/github-profile/PUBLISH.md)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=gh-env.sh
source "$SCRIPT_DIR/gh-env.sh"

OWNER="vpeetla-ai"

set_repo() {
  local repo="$1"
  local description="$2"
  shift 2
  local topics=("$@")

  echo "→ $OWNER/$repo"
  gh repo edit "$OWNER/$repo" --description "$description"
  gh api -X PUT "repos/$OWNER/$repo/topics" \
    -H "Accept: application/vnd.github+json" \
    --input - <<EOF
{"names":$(printf '%s\n' "${topics[@]}" | jq -R . | jq -s .)}
EOF
}

set_repo "ai-content-factory" \
  "Multi-agent content pipeline with HITL, LangGraph, FastAPI, Next.js — production deploy on free cloud" \
  "langgraph" "multi-agent" "fastapi" "nextjs" "rag" "human-in-the-loop" "ai-agents" "content-automation"

set_repo "enterprise_rag_platform" \
  "Production RAG reference — governed retrieval, access control, evals, guardrails, observability" \
  "rag" "enterprise" "llm" "vector-database" "ai-governance" "langchain"

set_repo "aegisloop-agentops-workbench" \
  "AgentOps workbench for tracing, evals, and production agent monitoring" \
  "agentops" "langsmith" "observability" "llm" "ai-agents"

set_repo "react-agent-pattern" \
  "ReAct agent pattern reference — LangGraph minimal implementation with tests" \
  "langgraph" "react-agent" "ai-agents" "tutorial" "python"

set_repo "reflection-agent-pattern" \
  "Reflection agent pattern — self-critique loop for higher-quality LLM output" \
  "langgraph" "ai-agents" "reflection" "tutorial" "python"

set_repo "plan-execute-agent-pattern" \
  "Plan-Execute agent pattern — decompose goals into steps then execute" \
  "langgraph" "ai-agents" "plan-execute" "tutorial" "python"

set_repo "multi-agent-system-pattern" \
  "Multi-agent system pattern — specialized roles and delegation" \
  "langgraph" "multi-agent" "ai-agents" "tutorial" "python"

set_repo "swarm-agent-pattern" \
  "Swarm agent pattern — parallel autonomous agents with coordination" \
  "langgraph" "swarm" "ai-agents" "tutorial" "python"

echo ""
echo "Done. Verify at https://github.com/$OWNER"
