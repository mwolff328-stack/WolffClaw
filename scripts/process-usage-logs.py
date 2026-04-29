#!/usr/bin/env python3
"""
process-usage-logs.py
Reads all OpenClaw cron run JSONL logs, computes estimated costs, and writes
enriched records to workspace/logs/usage.jsonl. Deduplicates by sessionId.
"""

import json
import os
import sys
import glob
from datetime import datetime, timezone
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_DIR = SCRIPT_DIR.parent
LOGS_DIR = WORKSPACE_DIR / "logs"
PRICING_FILE = SCRIPT_DIR / "model-pricing.json"
USAGE_FILE = LOGS_DIR / "usage.jsonl"
STATE_FILE = LOGS_DIR / "usage-state.json"
CRON_RUNS_DIR = Path.home() / ".openclaw" / "cron" / "runs"

# Job name registry (jobId → name)
# Populated from cron list or inferred from run files
JOB_NAME_MAP = {
    "1343655e-e234-4793-b001-f01c07c3f909": "Daily spend alert",
    "6c645059-36b4-4383-9c87-e6587999072f": "SurvivorPulse channel context save",
    "0cad2ec1-b90a-42e9-b749-6de52b454dcb": "unknown",
    "703e0af6-a784-47f9-9f3d-5c723317169d": "unknown",
    "cb772d41-bdff-406f-be3d-b43cb5abf0db": "unknown",
    "e5820629-9445-4bb1-8b8d-7dc6aa7902c1": "unknown",
}

# Task type mapping by job name
TASK_TYPE_MAP = {
    "SurvivorPulse channel context save": "memory",
    "Daily spend alert": "monitoring",
}

def get_task_type(job_name: str) -> str:
    return TASK_TYPE_MAP.get(job_name, "cron")

def normalize_model(model: str, provider: str) -> str:
    """Normalize model name to provider/model format."""
    if "/" in model:
        return model
    if provider:
        return f"{provider}/{model}"
    return model

def load_pricing() -> dict:
    with open(PRICING_FILE) as f:
        return json.load(f)

def compute_cost(input_tokens: int, output_tokens: int, model_key: str, pricing: dict) -> float:
    """Compute estimated cost in USD."""
    if model_key not in pricing:
        return 0.0
    rates = pricing[model_key]
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    return round(input_cost + output_cost, 6)

def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed_session_ids": []}

def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_existing_session_ids() -> set:
    """Load sessionIds already written to usage.jsonl."""
    ids = set()
    if USAGE_FILE.exists():
        with open(USAGE_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    if "sessionId" in r:
                        ids.add(r["sessionId"])
                except json.JSONDecodeError:
                    continue
    return ids

def process():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    pricing = load_pricing()
    state = load_state()

    # Use existing usage.jsonl as source of truth for deduplication
    seen_ids = load_existing_session_ids()

    # Also include state-tracked IDs (for backwards compat)
    seen_ids.update(state.get("processed_session_ids", []))

    new_records = []
    new_ids = []

    jsonl_files = sorted(glob.glob(str(CRON_RUNS_DIR / "*.jsonl")))
    if not jsonl_files:
        print(f"No JSONL files found in {CRON_RUNS_DIR}", file=sys.stderr)
        return

    for fpath in jsonl_files:
        job_id = Path(fpath).stem
        job_name = JOB_NAME_MAP.get(job_id, "unknown")

        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Skip entries without usage data
                usage = entry.get("usage")
                if not usage:
                    continue

                session_id = entry.get("sessionId", "")
                if not session_id:
                    # Use jobId+ts as fallback key
                    session_id = f"{job_id}:{entry.get('ts', '')}"

                if session_id in seen_ids:
                    continue

                ts = entry.get("ts", 0)
                # ts is in milliseconds
                date_str = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

                model_raw = entry.get("model", "")
                provider = entry.get("provider", "")
                model_key = normalize_model(model_raw, provider)

                input_tokens = usage.get("input_tokens", 0)
                output_tokens = usage.get("output_tokens", 0)
                total_tokens = usage.get("total_tokens", 0)
                # cache tokens = total - input - output (if total > input+output)
                cache_tokens = max(0, total_tokens - input_tokens - output_tokens)

                cost = compute_cost(input_tokens, output_tokens, model_key, pricing)
                task_type = get_task_type(job_name)

                record = {
                    "ts": ts,
                    "date": date_str,
                    "jobId": job_id,
                    "jobName": job_name,
                    "sessionId": session_id,
                    "model": model_key,
                    "provider": provider,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "cache_tokens": cache_tokens,
                    "estimated_cost_usd": cost,
                    "duration_ms": entry.get("durationMs", 0),
                    "status": entry.get("status", ""),
                    "task_type": task_type,
                }
                new_records.append(record)
                new_ids.append(session_id)
                seen_ids.add(session_id)

    if new_records:
        with open(USAGE_FILE, "a") as f:
            for r in new_records:
                f.write(json.dumps(r) + "\n")

        state["processed_session_ids"] = list(seen_ids)
        save_state(state)
        print(f"Processed {len(new_records)} new records → {USAGE_FILE}")
    else:
        print("No new records to process (all up to date).")

if __name__ == "__main__":
    process()
