#!/usr/bin/env bash
# Copy enhanced READMEs to sibling agent-pattern repos.
# Expects repos cloned next to ai-content-factory, e.g.:
#   ~/projects/ai-content-factory
#   ~/projects/react-agent-pattern
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PATTERNS_DIR="$ROOT/docs/agent-patterns"
PARENT="$(cd "$ROOT/.." && pwd)"

copy_readme() {
  local repo="$1"
  local src="$PATTERNS_DIR/README-${repo}.md"
  local dest="$PARENT/${repo}/README.md"

  if [[ ! -f "$src" ]]; then
    echo "✗ Missing template: $src"
    return 1
  fi
  if [[ ! -d "$PARENT/${repo}" ]]; then
    echo "⊘ Skip $repo — not found at $PARENT/${repo}"
    echo "  Clone: git clone git@github.com:vpeetla-ai/${repo}.git $PARENT/${repo}"
    return 0
  fi

  cp "$src" "$dest"
  echo "✓ Updated $dest"
}

echo "Applying agent pattern READMEs from $PATTERNS_DIR"
echo ""

copy_readme "react-agent-pattern"
copy_readme "reflection-agent-pattern"
copy_readme "plan-execute-agent-pattern"
copy_readme "multi-agent-system-pattern"
copy_readme "swarm-agent-pattern"

echo ""
echo "Next: commit and push each updated repo."
echo "  cd ../react-agent-pattern && git add README.md && git commit -m 'Enhance README with series branding' && git push"
