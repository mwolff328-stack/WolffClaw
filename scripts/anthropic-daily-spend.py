#!/usr/bin/env python3
"""
anthropic-daily-spend.py
Pulls accurate usage and cost data from Anthropic's Usage & Cost Admin API.
Requires Admin API key in macOS Keychain:
  security add-generic-password -a "anthropic-admin" -s "anthropic-admin-key" -w "KEY" -U

Usage:
  python3 anthropic-daily-spend.py             # today
  python3 anthropic-daily-spend.py --days 7    # last 7 days
  python3 anthropic-daily-spend.py --json      # output JSON for other scripts
"""

import json
import sys
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Pricing (per million tokens) ──────────────────────────────
# Update these when Anthropic changes rates
PRICING = {
    "claude-opus-4-6":    {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-opus-4-7":    {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-sonnet-4-6":  {"input":  3.00, "output": 15.00, "cache_write":  3.75, "cache_read": 0.30},
    "claude-sonnet-4-7":  {"input":  3.00, "output": 15.00, "cache_write":  3.75, "cache_read": 0.30},
    "claude-haiku-4":     {"input":  0.80, "output":  4.00, "cache_write":  1.00, "cache_read": 0.08},
    "claude-haiku-4-5":   {"input":  0.80, "output":  4.00, "cache_write":  1.00, "cache_read": 0.08},
}

DAILY_LIMIT = 50.00  # Alert threshold


def get_admin_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-a", "anthropic-admin", "-s", "anthropic-admin-key", "-w"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("ERROR: Admin API key not found in keychain.", file=sys.stderr)
        print("Run: security add-generic-password -a 'anthropic-admin' -s 'anthropic-admin-key' -w 'YOUR_KEY' -U", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def get_price(model, key):
    if model:
        for k, v in PRICING.items():
            if k in model:
                return v.get(key, 0.0)
    # Fallback to Sonnet pricing
    return PRICING["claude-sonnet-4-6"].get(key, 0.0)


def compute_cost(r, model):
    cc = r.get("cache_creation") or {}
    cw = cc.get("ephemeral_5m_input_tokens", 0) + cc.get("ephemeral_1h_input_tokens", 0)
    cr = r.get("cache_read_input_tokens", 0)
    uncached = r.get("uncached_input_tokens", 0)
    out = r.get("output_tokens", 0)
    web = (r.get("server_tool_use") or {}).get("web_search_requests", 0)

    cost = (
        (uncached / 1e6) * get_price(model, "input") +
        (cw / 1e6) * get_price(model, "cache_write") +
        (cr / 1e6) * get_price(model, "cache_read") +
        (out / 1e6) * get_price(model, "output") +
        (web / 1000) * 10.0  # $10/1k web searches
    )
    return cost, cw, cr, uncached, out, web


def fetch_usage(admin_key, start_iso, end_iso):
    params = urllib.parse.urlencode([
        ("starting_at", start_iso),
        ("ending_at", end_iso),
        ("bucket_width", "1d"),
        ("group_by[]", "model"),
    ])
    url = f"https://api.anthropic.com/v1/organizations/usage_report/messages?{params}"
    req = urllib.request.Request(url, headers={
        "anthropic-version": "2023-06-01",
        "x-api-key": admin_key,
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def main():
    days = 1
    output_json = False
    for arg in sys.argv[1:]:
        if arg == "--json":
            output_json = True
        elif arg == "--days" and len(sys.argv) > sys.argv.index(arg) + 1:
            days = int(sys.argv[sys.argv.index(arg) + 1])

    now = datetime.now(timezone.utc)
    end = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start = end - timedelta(days=days)

    admin_key = get_admin_key()
    data = fetch_usage(admin_key, start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ"))

    if "error" in data:
        print(f"API error: {data['error']['message']}", file=sys.stderr)
        sys.exit(1)

    # Process results
    daily = {}  # date -> {model -> {cost, tokens}}
    for bucket in data.get("data", []):
        date = bucket["starting_at"][:10]
        daily.setdefault(date, {})
        for r in bucket.get("results", []):
            model = r.get("model") or "unknown"
            cost, cw, cr, uncached, out, web = compute_cost(r, model)
            daily[date].setdefault(model, {"cost": 0, "cw": 0, "cr": 0, "out": 0, "web": 0})
            daily[date][model]["cost"] += cost
            daily[date][model]["cw"] += cw
            daily[date][model]["cr"] += cr
            daily[date][model]["out"] += out
            daily[date][model]["web"] += web

    # Today's total
    today_str = now.strftime("%Y-%m-%d")
    today_total = sum(v["cost"] for v in daily.get(today_str, {}).values())

    if output_json:
        print(json.dumps({
            "today": today_str,
            "today_total": round(today_total, 2),
            "daily_limit": DAILY_LIMIT,
            "daily": {
                date: {
                    "total": round(sum(v["cost"] for v in models.values()), 2),
                    "by_model": {m: round(v["cost"], 2) for m, v in models.items()}
                }
                for date, models in daily.items()
            }
        }, indent=2))
        return

    # Human-readable output
    print(f"\n{'='*70}")
    print(f"  Anthropic Spend Report — {now.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"{'='*70}")

    for date in sorted(daily.keys()):
        models = daily[date]
        day_total = sum(v["cost"] for v in models.values())
        status = "🚨" if day_total > DAILY_LIMIT else "✅"
        print(f"\n{status} {date}  —  ${day_total:.2f}")
        for model, v in sorted(models.items(), key=lambda x: -x[1]["cost"]):
            short = model.replace("claude-", "").replace("-latest", "")
            print(f"   {short:<25} cache_write:{v['cw']:>10,}  cache_read:{v['cr']:>12,}  output:{v['out']:>8,}  ${v['cost']:.2f}")

    print(f"\n{'─'*70}")
    all_totals = {d: sum(v["cost"] for v in m.values()) for d, m in daily.items()}
    print(f"  Period total ({days}d): ${sum(all_totals.values()):.2f}")
    print(f"  Daily avg:            ${sum(all_totals.values())/max(len(all_totals),1):.2f}")
    print(f"  Daily limit:          ${DAILY_LIMIT:.2f}")

    if today_total > DAILY_LIMIT:
        print(f"\n🚨 TODAY OVER LIMIT: ${today_total:.2f} (limit ${DAILY_LIMIT:.2f})")
    elif today_total > DAILY_LIMIT * 0.8:
        print(f"\n⚠️  TODAY APPROACHING LIMIT: ${today_total:.2f} (limit ${DAILY_LIMIT:.2f})")
    else:
        print(f"\n✅ Today: ${today_total:.2f} of ${DAILY_LIMIT:.2f} limit")
    print()


if __name__ == "__main__":
    main()
