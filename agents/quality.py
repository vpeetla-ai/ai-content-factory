"""Draft quality rubrics — deterministic platform checks before HITL.

Scores are structural (length, hook presence, CTA cues), not LLM-as-judge.
Attach results on the content node so editors and Langfuse can see failures early.
"""

from __future__ import annotations

from typing import Any

# Soft character guidance (not hard API limits except X).
PLATFORM_RUBRICS: dict[str, dict[str, Any]] = {
    "linkedin": {
        "min_chars": 120,
        "max_chars": 3000,
        "require_hook": True,
        "cta_cues": ("learn", "comment", "share", "dm", "link", "read", "try", "?"),
    },
    "x": {
        "min_chars": 20,
        "max_chars": 280,
        "require_hook": False,
        "cta_cues": ("?", "thread", "reply", "http"),
    },
    "medium": {
        "min_chars": 400,
        "max_chars": 50_000,
        "require_hook": True,
        "cta_cues": ("##", "conclusion", "takeaway", "http"),
    },
    "substack": {
        "min_chars": 400,
        "max_chars": 50_000,
        "require_hook": True,
        "cta_cues": ("##", "subscribe", "takeaway", "http"),
    },
    "instagram": {
        "min_chars": 80,
        "max_chars": 2200,
        "require_hook": True,
        "cta_cues": ("#", "link", "bio", "comment", "?"),
    },
}


def score_draft(platform: str, draft: dict | str) -> dict[str, Any]:
    """Return a rubric score dict for one platform draft."""
    rubric = PLATFORM_RUBRICS.get(platform)
    if not rubric:
        return {"platform": platform, "pass": True, "score": 1.0, "issues": ["unknown_platform"]}

    if isinstance(draft, dict):
        content = str(draft.get("content") or "")
        hook = str(draft.get("hook") or "")
    else:
        content = str(draft or "")
        hook = ""

    issues: list[str] = []
    checks = 0
    passed = 0

    checks += 1
    n = len(content)
    if n < rubric["min_chars"]:
        issues.append(f"too_short:{n}<{rubric['min_chars']}")
    elif n > rubric["max_chars"]:
        issues.append(f"too_long:{n}>{rubric['max_chars']}")
    else:
        passed += 1

    if rubric.get("require_hook"):
        checks += 1
        if hook.strip() or (content and len(content.split("\n")[0]) >= 20):
            passed += 1
        else:
            issues.append("missing_hook")

    checks += 1
    lower = content.lower()
    if any(cue in lower for cue in rubric["cta_cues"]):
        passed += 1
    else:
        issues.append("weak_cta")

    score = passed / checks if checks else 1.0
    return {
        "platform": platform,
        "pass": len(issues) == 0,
        "score": round(score, 3),
        "char_count": n,
        "issues": issues,
    }


def score_platform_drafts(drafts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Score every platform draft present in the content agent output."""
    return {platform: score_draft(platform, draft) for platform, draft in (drafts or {}).items()}
