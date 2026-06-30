"""Pytest fixtures — mock external services for agent graph tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("MOCK_LLM", "true")
os.environ.setdefault("VECTOR_BACKEND", "none")
os.environ.setdefault("AEGISAI_GATEWAY_ENABLED", "false")


@pytest.fixture
def sample_state() -> dict:
    return {
        "topic": "AI agent governance",
        "platforms": ["linkedin", "x"],
        "run_id": "test-run-001",
        "platform_drafts": {
            "linkedin": {"content": "Draft for LinkedIn"},
            "x": {"content": "Short post"},
        },
        "hitl_approved": {"linkedin": {"approved": True}, "x": {"approved": True}},
        "hitl_edits": {},
        "messages": [],
    }
