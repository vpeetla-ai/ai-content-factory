#!/usr/bin/env python3
"""Cloud cost snapshot — AWS Cost Explorer adapter with mock mode for CI."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta


def mock_snapshot(days: int) -> dict:
    today = date.today()
    daily = [
        {"date": (today - timedelta(days=i)).isoformat(), "amount_usd": round(12.5 + i * 0.3, 2)}
        for i in range(days, 0, -1)
    ]
    total = sum(d["amount_usd"] for d in daily)
    prior_week = sum(d["amount_usd"] for d in daily[:7])
    last_week = sum(d["amount_usd"] for d in daily[7:14]) if days >= 14 else prior_week
    wow_change = ((prior_week - last_week) / last_week * 100) if last_week else 0

    return {
        "mode": "mock",
        "period_days": days,
        "total_usd": round(total, 2),
        "daily": daily,
        "by_service": [
            {"service": "AmazonECS", "amount_usd": round(total * 0.45, 2)},
            {"service": "AmazonRDS", "amount_usd": round(total * 0.30, 2)},
            {"service": "AmazonCloudWatch", "amount_usd": round(total * 0.10, 2)},
            {"service": "Other", "amount_usd": round(total * 0.15, 2)},
        ],
        "anomalies": [
            {
                "type": "week_over_week_spike",
                "detected": abs(wow_change) > 20,
                "change_pct": round(wow_change, 1),
                "message": f"Week-over-week change {wow_change:.1f}%",
            }
        ],
    }


def aws_snapshot(days: int) -> dict:
    try:
        import boto3
    except ImportError as exc:
        raise SystemExit("boto3 required for real mode: pip install boto3") from exc

    ce = boto3.client("ce")
    end = date.today()
    start = end - timedelta(days=days)
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )
    daily = []
    total = 0.0
    for row in resp.get("ResultsByTime", []):
        amount = float(row["Total"]["UnblendedCost"]["Amount"])
        daily.append({"date": row["TimePeriod"]["Start"], "amount_usd": round(amount, 2)})
        total += amount

    return {
        "mode": "aws_cost_explorer",
        "period_days": days,
        "total_usd": round(total, 2),
        "daily": daily,
        "anomalies": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Cloud cost snapshot")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--mock", action="store_true", help="Use mock data (default without AWS)")
    args = parser.parse_args()

    use_mock = args.mock or not _aws_available()
    report = mock_snapshot(args.days) if use_mock else aws_snapshot(args.days)
    print(json.dumps(report, indent=2))
    return 0


def _aws_available() -> bool:
    try:
        import boto3

        boto3.client("sts").get_caller_identity()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
