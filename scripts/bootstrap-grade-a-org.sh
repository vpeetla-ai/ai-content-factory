#!/usr/bin/env bash
# Bootstrap Grade A assets across vpeetla-ai org repos (SLO + DevSecOps).
set -euo pipefail

ACF="/Users/lakshmipraveenabodempudi/ai-content-factory"
HOME_DIR="/Users/lakshmipraveenabodempudi"

copy_security() {
  local repo="$1"
  local dest="$HOME_DIR/$repo"
  [[ -d "$dest" ]] || return 0
  mkdir -p "$dest/scripts" "$dest/.github/workflows" "$dest/docs"
  cp "$ACF/.github/workflows/security-scan.yml" "$dest/.github/workflows/security-scan.yml"
  cp "$ACF/scripts/security_risk_report.py" "$dest/scripts/security_risk_report.py"
  chmod +x "$dest/scripts/security_risk_report.py"
  echo "  security-scan -> $repo"
}

write_slo() {
  local repo="$1"
  local service="$2"
  local dest="$HOME_DIR/$repo/docs/SLO.md"
  [[ -d "$HOME_DIR/$repo" ]] || return 0
  mkdir -p "$(dirname "$dest")"
  cat > "$dest" <<EOF
# Service Level Objectives — ${service}

Production SLO definitions for portfolio reviewers and on-call runbooks.

## SLO targets

| SLI | Target | Measurement window |
|-----|--------|-------------------|
| **API availability** | 99.5% | 30 days |
| **Eval regression** | 0 failures | Per merge (golden-eval-registry) |
| **Security scan** | No CRITICAL CVEs | Per PR (Semgrep + Trivy) |

## How we measure

| Signal | Source |
|--------|--------|
| Availability | Render/Vercel health + \`/health\` |
| Eval regression | \`golden-eval-registry\` CI gate |
| Security posture | \`.github/workflows/security-scan.yml\` |

## Org reference

- [AI Content Factory SLO](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/SLO.md)
- [Org Grade A tracker](https://github.com/vpeetla-ai/ai-architecture-portfolio/blob/main/docs/ORG_GRADE_A.md)
- [Reference architectures](https://github.com/vpeetla-ai/ai-content-factory/blob/main/docs/reference-architectures/)
EOF
  echo "  SLO.md -> $repo"
}

REPOS=(
  "sentinel-brief:Sentinel Brief"
  "loop-engine-agent-platform:LoopForge"
  "domainforge-rag-peft:DomainForge"
  "venkat-ai-platform:Venkat AI Platform"
  "aegisai-enterprise-agent-platform:AegisAI"
  "enterprise_rag_platform:Enterprise RAG"
  "aegisloop-agentops-workbench:AegisLoop"
  "agent-finops:Agent FinOps"
  "voiceforge-assistant:VoiceForge"
  "golden-eval-registry:Golden Eval Registry"
)

echo "Bootstrapping Grade A assets..."
for entry in "${REPOS[@]}"; do
  repo="${entry%%:*}"
  service="${entry#*:}"
  copy_security "$repo"
  write_slo "$repo" "$service"
done
echo "Done."
