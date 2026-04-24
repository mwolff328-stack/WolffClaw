# Usage Tracking — Cron Job Integration Notes

## Daily Spend Alert (1343655e)
Updated prompt now runs:
1. `python3 /Users/mrwolff/.openclaw/workspace/scripts/process-usage-logs.py` — ingests new cron run logs
2. `python3 /Users/mrwolff/.openclaw/workspace/scripts/cost-report.py --period daily` — generates today's report
3. Posts full report to #infra

## SurvivorPulse Channel Context Save (6c645059)
**Recommendation:** After the channel save job completes, also run the usage processor as a final step so that context save run's own token usage gets captured immediately.

Add this to the channel context save job's prompt as a final step:
```
After completing all save steps, run the usage processor to capture this run's token data:
exec: python3 /Users/mrwolff/.openclaw/workspace/scripts/process-usage-logs.py
```

To update the channel context save job:
```
openclaw cron edit 6c645059-36b4-4383-9c87-e6587999072f --message "<existing prompt + the above step>"
```

**Note:** The processor is idempotent and deduplicates by sessionId, so running it multiple times is safe.

## Architecture
- `scripts/model-pricing.json` — per-1M-token pricing for all supported models
- `scripts/process-usage-logs.py` — reads `~/.openclaw/cron/runs/*.jsonl`, enriches with cost, deduplicates by sessionId
- `scripts/cost-report.py` — reads `logs/usage.jsonl`, generates daily/weekly/monthly reports
- `logs/usage.jsonl` — enriched usage records (append-only)
- `logs/usage-state.json` — processed sessionId registry for deduplication

## Known Limitations
- Model names in cron logs use short form (`claude-opus-4-6`) not full form (`anthropic/claude-opus-4-6`). The processor normalizes using the `provider` field.
- `total_tokens` in raw logs often exceeds `input_tokens + output_tokens` (likely cache read tokens). The processor computes `cache_tokens = total - input - output` and costs are computed on input+output only.
- Job names for some job IDs are hardcoded in `process-usage-logs.py`. Update `JOB_NAME_MAP` if new cron jobs are added.
