---
name: git-commit-author
description: >-
  Always set Venkata Peetla as git commit author/committer when committing or
  opening PRs. Use whenever creating commits, pushing branches, or running gh pr create.
---

# Git commit author — Venkata Peetla

## Required identity

| Field | Value |
|-------|--------|
| Name | `Venkata Peetla` |
| Email | `vpeetla.ai@gmail.com` |
| GitHub | `vpeetla-ai` |

## Commit command

Do **not** rewrite `git config`. Pass identity per commit:

```bash
git -c user.name="Venkata Peetla" -c user.email="vpeetla.ai@gmail.com" \
  commit --author="Venkata Peetla <vpeetla.ai@gmail.com>" \
  -m "$(cat <<'EOF'
Commit message.

EOF
)"
```

Ensure committer matches (Cursor sandboxes sometimes set Committer to GitHub/Cursor):

```bash
export GIT_COMMITTER_NAME="Venkata Peetla"
export GIT_COMMITTER_EMAIL="vpeetla.ai@gmail.com"
```

## Forbidden

- `Co-authored-by: Cursor` / `cursoragent@cursor.com`
- Author or committer of `Cursor`, `cursoragent`, or `GitHub <noreply@github.com>`

## PRs

- `gh pr create` as authenticated `vpeetla-ai`
- No “Made with Cursor” footer unless Venkata asks
