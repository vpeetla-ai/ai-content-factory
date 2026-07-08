#!/usr/bin/env python3
"""Score graph_hitl golden eval cases against real LangGraph publish behavior."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from agents.graph import build_graph
from agents.nodes.publish import publisher_agent


def score_graph_hitl_case(case: dict, actual: dict) -> tuple[bool, str]:
    expect = case["expect"]
    problems: list[str] = []

    expected_published = set(expect.get("published_platforms") or [])
    actual_published = set(actual.get("published_platforms") or [])
    if expected_published != actual_published:
        problems.append(f"published_platforms: expected {sorted(expected_published)}, got {sorted(actual_published)}")

    expected_skipped = set(expect.get("skipped_platforms") or [])
    actual_skipped = set(actual.get("skipped_platforms") or [])
    if expected_skipped != actual_skipped:
        problems.append(f"skipped_platforms: expected {sorted(expected_skipped)}, got {sorted(actual_skipped)}")

    if expect.get("requires_hitl_before_publish"):
        graph = build_graph()
        nodes = list(graph.get_graph().nodes.keys())
        if "hitl" not in nodes:
            problems.append("graph missing hitl node")

    return not problems, "; ".join(problems) or "ok"


async def run_publish_fixture(state_path: Path) -> dict:
    state = json.loads(state_path.read_text())
    result = await publisher_agent(state)  # type: ignore[arg-type]
    published = set((result.get("published_results") or {}).keys())
    all_platforms = set(state.get("platforms") or [])
    approved = {
        p
        for p, decision in (state.get("hitl_approved") or {}).items()
        if decision.get("approved") and not decision.get("skip")
    }
    skipped = all_platforms - published
    return {
        "published_platforms": sorted(published),
        "skipped_platforms": sorted(skipped),
        "requires_hitl_before_publish": True,
    }


async def main() -> int:
    suite_dir = ROOT / "tests" / "fixtures" / "golden_eval" / "content_factory_graph_v1"
    cases_path = suite_dir / "cases.jsonl"
    if not cases_path.exists():
        print(f"Missing suite at {cases_path}", file=sys.stderr)
        return 1

    failures = 0
    for line in cases_path.read_text().strip().splitlines():
        case = json.loads(line)
        state_ref = case["input"]["state_ref"]
        state_path = suite_dir / state_ref
        actual = await run_publish_fixture(state_path)
        passed, detail = score_graph_hitl_case(case, actual)
        status = "PASS" if passed else "FAIL"
        print(f"{status} {case['id']}: {detail}")
        if not passed:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
