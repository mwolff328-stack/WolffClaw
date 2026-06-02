# MEMORY.md - Long-Term Memory

## Identity & Setup

- I am Luigi — infrastructure agent, separate gateway from Markus
- Gateway state dir: `~/.openclaw-luigi/` (port 18790)
- Workspace: `~/.openclaw-luigi/workspace/`
- Owner: Michael Wolff (Mike), timezone America/Los_Angeles
- Sister agent: Markus (personal assistant, separate gateway)

## Standing Directives

### Development Routing (2026-05-19, updated 2026-06-01)
All development work — SurvivorPulse or otherwise — routes through **Claude Code ACP** — not native subagents.
This applies to ALL sub-agents (including any newly uploaded ones). Covers everything: research, story writing, backlog management, design, coding, testing, deployment.

**How to spawn:**
```
sessions_spawn({
  runtime: "acp",
  agentId: "claude",
  thread: true,
  mode: "session",
  cwd: "/Users/mrwolff/Projects/SurvivorPulse",
  task: "<task description>"
})
```

Native subagents (Felix, Deb, Stan, etc.) are retired for SP work — they burn API tokens. Claude Code runs on a flat subscription.

**Split:** My own short coordination turns (routing, summarizing, deciding) stay native — cheap. Only actual task execution moves to Claude Code.

## Cron Jobs (2026-06-01 cleanup)

| Job | Schedule | Status |
|-----|----------|--------|
| Discord watchdog | Every 2h :30 | ✅ Fixed (was using haiku model) — now gemini-2.0-flash |
| OpenClaw post-update doctor | 3:15 AM nightly | ✅ Healthy |
| SP Claude Code daily init | 5:00 AM daily | ✅ Healthy (fires system event to my main session) |
| SP overnight watchdog | 7:00 AM daily | ✅ Fixed (was using haiku model) — now gemini-2.0-flash; formerly named "Felix overnight watchdog" |

## Workspace Notes (2026-06-01 cleanup)

- `agents/` dir: old agent definition files (Felix, Deb, Stan, etc.) — retired sub-agents, kept for reference
- `workspace-deb/`, `workspace-stan/`: deleted (2026-06-01, Mike confirmed)
- `claude/`: keeping (Mike's call, 2026-06-01)
- `memory/`: active, full of Stan research notes (stan-*.md files) — kept
- `luigi/BOOTSTRAP.md`: deleted (bootstrap complete)
- `IDENTITY.md` and `USER.md`: filled in (2026-06-01)

## Model Allowlist (current)
Valid models for cron jobs: anthropic/claude-haiku-4-5, anthropic/claude-opus-4-6, anthropic/claude-sonnet-4-6, google/gemini-2.0-flash, google/gemini-2.5-flash, google/gemini-2.5-pro, openai/gpt-5.4-mini, openai/gpt-5.5, openai/o3, openai/o4-mini
