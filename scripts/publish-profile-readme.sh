#!/usr/bin/env bash
# Create github.com/vpeetla-ai/vpeetla-ai and push the profile README.
# Prerequisites: gh auth login
set -euo pipefail

PROFILE_DIR="${PROFILE_DIR:-$HOME/vpeetla-ai}"
SOURCE_README="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/docs/github-profile/README.md"

mkdir -p "$PROFILE_DIR"

# Strip internal HTML comment from template
if grep -q '^<!-- Profile README' "$SOURCE_README"; then
  tail -n +5 "$SOURCE_README" > "$PROFILE_DIR/README.md"
else
  cp "$SOURCE_README" "$PROFILE_DIR/README.md"
fi

cd "$PROFILE_DIR"

if [[ ! -d .git ]]; then
  git init
  git branch -m main
fi

git add README.md
if git diff --cached --quiet; then
  echo "README unchanged."
else
  git commit -m "Update GitHub profile README"
fi

if gh repo view vpeetla-ai/vpeetla-ai &>/dev/null; then
  echo "Repo exists — pushing..."
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/vpeetla-ai/vpeetla-ai.git"
  git push -u origin main
else
  echo "Creating vpeetla-ai/vpeetla-ai..."
  gh repo create vpeetla-ai --public \
    --description "GitHub profile README — Overview banner for @vpeetla-ai" \
    --source=. --remote=origin --push
fi

echo ""
echo "Done. View: https://github.com/vpeetla-ai"
