"""Lightweight media cards from visual prompts — PNG for LinkedIn/X, no paid image API."""

from __future__ import annotations

import hashlib
import io
import re
import textwrap


def _slug(text: str, limit: int = 40) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (cleaned or "card")[:limit]


def render_prompt_card_png(*, topic: str, prompt: str, index: int) -> bytes:
    """Generate a simple branded PNG card (1200x630) with Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1200, 630
    accents = [(15, 118, 110), (29, 78, 216), (124, 58, 237)]
    accent = accents[index % 3]
    img = Image.new("RGB", (width, height), (11, 18, 32))
    draw = ImageDraw.Draw(img)
    # gradient-ish bottom strip
    draw.rectangle([0, 520, width, height], fill=(17, 24, 39))
    draw.rounded_rectangle([48, 48, 64, 582], radius=8, fill=accent)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 28)
        foot_font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = title_font
        foot_font = title_font

    title = (topic or "AI Content Factory")[:72]
    body = (prompt or "Visual concept")[:220]
    draw.text((96, 90), title, fill=(229, 231, 235), font=title_font)
    y = 180
    for line in textwrap.wrap(body, width=52):
        draw.text((96, y), line, fill=(203, 213, 225), font=body_font)
        y += 36
        if y > 480:
            break
    draw.text(
        (96, 560),
        f"AI Content Factory · visual card {index + 1}",
        fill=(100, 116, 139),
        font=foot_font,
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_prompt_card_svg(*, topic: str, prompt: str, index: int) -> bytes:
    """Legacy SVG helper kept for unit tests / non-raster previews."""
    import html

    title = html.escape((topic or "AI Content Factory")[:72])
    body = html.escape((prompt or "Visual concept")[:160])
    accent = ["#0f766e", "#1d4ed8", "#7c3aed"][index % 3]
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#0b1220"/>
  <rect x="48" y="48" width="16" height="534" rx="8" fill="{accent}"/>
  <text x="96" y="120" fill="#e5e7eb" font-family="sans-serif" font-size="42">{title}</text>
  <text x="96" y="220" fill="#cbd5e1" font-family="sans-serif" font-size="28">{body[:80]}</text>
</svg>
"""
    return svg.encode("utf-8")


def card_object_key(run_id: str, prompt: str, index: int, *, ext: str = "png") -> str:
    digest = hashlib.sha256(prompt.encode()).hexdigest()[:10]
    return f"runs/{_slug(run_id, 24)}/card-{index}-{digest}.{ext}"
