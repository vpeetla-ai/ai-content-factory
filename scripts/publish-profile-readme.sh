#!/usr/bin/env bash
# Create github.com/vpeetla-ai/vpeetla-ai and push the profile README.
# Prerequisites: gh auth login (see docs/github-profile/PUBLISH.md)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=gh-env.sh
source "$SCRIPT_DIR/gh-env.sh"

PROFILE_DIR="${PROFILE_DIR:-$HOME/vpeetla-ai}"
SOURCE_README="$(cd "$SCRIPT_DIR/.." && pwd)/docs/github-profile/README.md"

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

ensure_remote() {
  local url="https://github.com/vpeetla-ai/vpeetla-ai.git"
  if git remote get-url origin &>/dev/null; then
    git remote set-url origin "$url"
  else
    git remote add origin "$url"
  fi
}

if gh repo view vpeetla-ai/vpeetla-ai &>/dev/null; then
  echo "Repo exists — pushing..."
  ensure_remote
  git push -u origin main
else
  echo "Creating vpeetla-ai/vpeetla-ai..."
  if gh repo create vpeetla-ai --public \
    --description "GitHub profile README — Overview banner for @vpeetla-ai" \
    --source=. --remote=origin --push 2>&1; then
    :
  else
    echo "gh repo create reported an error — retrying push if repo exists..."
    if gh repo view vpeetla-ai/vpeetla-ai &>/dev/null; then
      ensure_remote
      git push -u origin main
    else
      exit 1
    fi
  fi
fi

echo ""
echo "Done. View: https://github.com/vpeetla-ai"
