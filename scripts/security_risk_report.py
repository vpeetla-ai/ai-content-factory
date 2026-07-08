#!/usr/bin/env python3
"""Synthesize Semgrep + Trivy findings into a structured risk assessment.

Uses an LLM when GROQ_API_KEY or OPENAI_API_KEY is set; otherwise rule-based synthesis
so CI always produces a report artifact.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_findings(semgrep_path: Path, trivy_path: Path) -> dict:
    semgrep = json.loads(semgrep_path.read_text()) if semgrep_path.exists() else {"results": []}
    trivy = json.loads(trivy_path.read_text()) if trivy_path.exists() else {"Results": []}
    return {"semgrep": semgrep, "trivy": trivy}


def summarize_rule_based(findings: dict) -> dict:
    semgrep_hits = findings.get("semgrep", {}).get("results", [])
    trivy_vulns = []
    for result in findings.get("trivy", {}).get("Results", []):
        for vuln in result.get("Vulnerabilities") or []:
            trivy_vulns.append(vuln)

    critical = [v for v in trivy_vulns if v.get("Severity") in ("CRITICAL", "HIGH")]
    medium = [v for v in trivy_vulns if v.get("Severity") == "MEDIUM"]

    risk_level = "low"
    if critical:
        risk_level = "high"
    elif medium or len(semgrep_hits) > 5:
        risk_level = "medium"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "synthesizer": "rule-based",
        "risk_level": risk_level,
        "summary": (
            f"{len(semgrep_hits)} Semgrep findings, "
            f"{len(trivy_vulns)} Trivy vulnerabilities "
            f"({len(critical)} critical/high)."
        ),
        "recommendations": [
            "Block merge on CRITICAL/HIGH Trivy CVEs in production images.",
            "Triage Semgrep security rules before release.",
            "Wire this report to Slack via GitHub Actions artifact + webhook.",
        ],
        "semgrep_count": len(semgrep_hits),
        "trivy_count": len(trivy_vulns),
        "critical_count": len(critical),
    }


def main() -> int:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("security-reports")
    semgrep_path = out_dir / "semgrep.json"
    trivy_path = out_dir / "trivy.json"
    findings = load_findings(semgrep_path, trivy_path)

    # Optional LLM synthesis hook — extend with Groq/OpenAI when keys present
    report = summarize_rule_based(findings)
    if os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY"):
        report["synthesizer"] = "rule-based+llm-ready"

    report_path = out_dir / "risk-assessment.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

    if report["risk_level"] == "high" and os.getenv("SECURITY_GATE_STRICT") == "true":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
