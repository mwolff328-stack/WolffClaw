#!/usr/bin/env python3
"""
cost-report.py
Generates cost reports from workspace/logs/usage.jsonl.

Usage:
  python3 cost-report.py --period daily|weekly|monthly
                         [--model <model>]
                         [--task-type <type>]
                         [--date YYYY-MM-DD]
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_DIR = SCRIPT_DIR.parent
USAGE_FILE = WORKSPACE_DIR / "logs" / "usage.jsonl"

DAILY_LIMIT_USD = 50.00


def parse_args():
    parser = argparse.ArgumentParser(description="OpenClaw model cost report")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"], required=True)
    parser.add_argument("--model", default=None, help="Filter by model")
    parser.add_argument("--task-type", default=None, dest="task_type", help="Filter by task type")
    parser.add_argument("--date", default=None, help="Reference date YYYY-MM-DD (default: today)")
    return parser.parse_args()


def get_date_range(period: str, ref_date: str) -> tuple[str, str]:
    """Return (start_date, end_date) inclusive, as YYYY-MM-DD strings."""
    if ref_date:
        ref = datetime.strptime(ref_date, "%Y-%m-%d").date()
    else:
        ref = datetime.now(timezone.utc).date()

    if period == "daily":
        return str(ref), str(ref)
    elif period == "weekly":
        # Start from Monday of ref week
        start = ref - timedelta(days=ref.weekday())
        end = start + timedelta(days=6)
        return str(start), str(end)
    elif period == "monthly":
        start = ref.replace(day=1)
        # Last day of month
        if ref.month == 12:
            end = ref.replace(month=12, day=31)
        else:
            end = ref.replace(month=ref.month + 1, day=1) - timedelta(days=1)
        return str(start), str(end)


def load_records(start_date: str, end_date: str, model_filter: str, task_type_filter: str) -> list:
    if not USAGE_FILE.exists():
        return []

    records = []
    with open(USAGE_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue

            date = r.get("date", "")
            if not (start_date <= date <= end_date):
                continue
            if model_filter and r.get("model") != model_filter:
                continue
            if task_type_filter and r.get("task_type") != task_type_filter:
                continue
            records.append(r)

    return records


def format_report(period: str, start_date: str, end_date: str, records: list) -> str:
    lines = []

    # Header
    if period == "daily":
        title = f"Daily Cost Report: {start_date}"
    elif period == "weekly":
        title = f"Weekly Cost Report: {start_date} → {end_date}"
    elif period == "monthly":
        month_label = datetime.strptime(start_date, "%Y-%m-%d").strftime("%B %Y")
        title = f"Monthly Cost Report: {month_label}"

    lines.append(f"=== {title} ===")
    lines.append("")

    if not records:
        lines.append("No data found for this period.")
        return "\n".join(lines)

    # By model
    by_model = defaultdict(lambda: {"runs": 0, "cost": 0.0})
    by_task = defaultdict(lambda: {"runs": 0, "cost": 0.0})
    total_runs = 0
    total_cost = 0.0

    for r in records:
        m = r.get("model", "unknown")
        t = r.get("task_type", "cron")
        c = r.get("estimated_cost_usd", 0.0)

        by_model[m]["runs"] += 1
        by_model[m]["cost"] += c

        by_task[t]["runs"] += 1
        by_task[t]["cost"] += c

        total_runs += 1
        total_cost += c

    # Model section
    lines.append("By model:")
    model_col_width = max((len(m) for m in by_model), default=10)
    for m in sorted(by_model, key=lambda x: by_model[x]["cost"], reverse=True):
        runs = by_model[m]["runs"]
        cost = by_model[m]["cost"]
        lines.append(f"  {m:<{model_col_width}}  {runs:>4} runs   ${cost:.2f}")

    lines.append("")
    lines.append("By task type:")
    task_col_width = max((len(t) for t in by_task), default=10)
    for t in sorted(by_task, key=lambda x: by_task[x]["cost"], reverse=True):
        runs = by_task[t]["runs"]
        cost = by_task[t]["cost"]
        lines.append(f"  {t:<{task_col_width}}  {runs:>4} runs   ${cost:.2f}")

    lines.append("")
    lines.append(f"TOTAL: {total_runs} runs, ${total_cost:.2f}")
    lines.append("")

    if period == "daily":
        remaining = max(0.0, DAILY_LIMIT_USD - total_cost)
        lines.append(f"Daily limit: ${DAILY_LIMIT_USD:.2f}  |  Remaining: ${remaining:.2f}")

    return "\n".join(lines)


def main():
    args = parse_args()
    start_date, end_date = get_date_range(args.period, args.date)
    records = load_records(start_date, end_date, args.model, args.task_type)
    report = format_report(args.period, start_date, end_date, records)
    print(report)


if __name__ == "__main__":
    main()
