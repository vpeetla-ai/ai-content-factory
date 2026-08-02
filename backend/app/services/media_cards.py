"""Lightweight SVG media cards from visual prompts — no external image API."""

from __future__ import annotations

import hashlib
import html
import re


def _slug(text: str, limit: int = 40) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (cleaned or "card")[:limit]


def render_prompt_card_svg(*, topic: str, prompt: str, index: int) -> bytes:
    """Generate a simple branded SVG card (public CDN-friendly)."""
    title = html.escape((topic or "AI Content Factory")[:72])
    body = html.escape((prompt or "Visual concept")[:160])
    accent = ["#0f766e", "#1d4ed8", "#7c3aed"][index % 3]
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="48" y="48" width="16" height="534" rx="8" fill="{accent}"/>
  <text x="96" y="120" fill="#e5e7eb" font-family="Georgia, serif" font-size="42" font-weight="700">{title}</text>
  <foreignObject x="96" y="180" width="1000" height="320">
    <div xmlns="http://www.w3.org/1999/xhtml" style="color:#cbd5e1;font-family:system-ui,sans-serif;font-size:28px;line-height:1.4">{body}</div>
  </foreignObject>
  <text x="96" y="560" fill="#64748b" font-family="system-ui,sans-serif" font-size="20">AI Content Factory · visual card {index + 1}</text>
</svg>
"""
    return svg.encode("utf-8")


def card_object_key(run_id: str, prompt: str, index: int) -> str:
    digest = hashlib.sha256(prompt.encode()).hexdigest()[:10]
    return f"runs/{_slug(run_id, 24)}/card-{index}-{digest}.svg"
