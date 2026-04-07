# Session: 2026-04-06 12:37:08 UTC

- **Session Key**: agent:main:telegram:direct:8508558620
- **Session ID**: f2869469-05e6-46b6-b12a-b99db9a4aae5
- **Source**: telegram

## Conversation Summary

assistant: Notion's web page is client-rendered, so I need the API. Let me use the Notion skill and find the repos.
assistant: Two blockers before I can dig in:

**1. GitHub CLI not authenticated.** `gh auth login` hasn't been run on this machine, so I can't access the SurvivorPulse or CMEA-Prototype repos. Can you either:
- Run `gh auth login` and authenticate, or
- Tell me the exact repo URLs so I can try cloning with any existing SSH keys

**2. No Notion API key configured.** Notion pages are client-rendered, so I need the API to read them. To set this up:
- Go to https://notion.so/my-integrations and create an integration
- Copy the API key (starts with `ntn_`)
- Share the SurvivorPulse page (and sub-pages) with that integration ("..." > "Connect to" > your integration name)
- I'll store the key once you share it

Once both are in place I can do a full review of the product across all three sources. Want to knock these out now?
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "182",
  "sender_id": "8508558620",
  "sender": "Michael Wolff",
  "timestamp": "Sun 2026-04-05 21:57 PDT"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Michael Wolff (8508558620)",
  "id": "8508558620",
  "name": "Michael Wolff"
}
```

Notion API Key stored at ~/.config/notion/api_key (redacted from version control)
assistant: Got it. Let me search Notion for SurvivorPulse and check for GitHub SSH access to the repos.
assistant: Good news: GitHub SSH works. Bad news: the Notion integration can't see SurvivorPulse yet. You need to share the page with the integration.

Let me clone the repos while you do that.
assistant: Both repos cloned. Let me get an overview of each.
assistant: Good, getting solid context now. Let me grab more key files from both repos.
assistant: Now let me try Notion with the API. The page ID from the URL is `26329ce5833d800abe90ff530bddc59c`.
assistant: Got both repos reviewed. The Notion integration ("OpenClaw") exists but doesn't have access to the SurvivorPulse page yet.

**One thing left:** you need to share the SurvivorPulse Notion page with the "OpenClaw" integration. In Notion, open the SurvivorPulse page, click the "..." menu (top right), then "Connect to" and select "OpenClaw." That will cascade access to all sub-pages.

While you do that, here's my synthesis of what I've absorbed from both repos:

---

**SurvivorPulse: product overview**

A full-stack decision intelligence platform for NFL survivor pool optimization. Not a picks blog, not a sportsbook. Probability-first, built for serious players managing multiple entries across large pools.

**Core engine capabilities:**
- Recommendation engine blending win probability (ESPN FPI), betting spreads, pick popularity (Yahoo), contrarian value, and future option value into a composite 0-100 score with letter grades
- Pool Dynamics Engine: field survival baseline, chalk risk, leverage, expected equity, pool leverage intensity (schedule-type agnostic)
- Playoff Survivor Engine: multi-pick, percentile grading, portfolio diversification mode
- Portfolio Diversification Mode: coordinates picks across multiple entries to minimize correlated elimination risk
- Elimination detection and tracking

**Architecture:** React 18 + Vite + Tailwind/shadcn frontend. Node/Express + TypeScript backend. Drizzle ORM on Neon Postgres. Custom email/password auth with sessions, CSRF, rate limiting. Stripe subscriptions with founding member cap (50). Postmark for transactional email.

**Data sources:** ESPN FPI, The Odds API (betting lines), Yahoo pick popularity data, plus manual pool data entry.

**Key design invariants:**
- Determinism: same inputs = byte-identical outputs
- No inferred data, no silent fallbacks
- Canonical semantic game IDs (`2025-01-PHI-DAL`)
- Canonical spread contract with provenance and finality tiers
- All recommendations must be explainable in plain English

**Credibility Asset 1 (CA1):** A standalone analytical artifact proving SurvivorPulse's value proposition. Originally a simulation comparison, now reframed as a chalk collapse visibility case study (Week 14, 2025: Tampa Bay at 57% field ownership, 80% eliminated in one week). CA1 has its own deterministic engine, 8 development phases, governance spec, PDF/DOCX packaging pipeline, and tripwire-enforced spec compliance. This is the primary go-to-market proof asset.

**CMEA-Prototype:** A throwaway React+Vite frontend prototype for the Coordinated Multi-Entry Allocation experience. Calls SurvivorPulse APIs to replay a full 18-week 2025 season showing how portfolio diversification works across multiple entries. Two paths: Path A (authenticated, live pool data) and Path B (demo mode). Includes a feedback capture form. This is likely the sales demo / proof-of-concept for the multi-entry value prop.

**Current state indicators:**
- 1,631 files in the main repo, heavy test coverage (2,400+ unit tests, 180+ integration)
- Active spec (004): CA1 reframe to chalk collapse case study, Phase D ready
- v1/v2 app versioning in progress (separate build scripts, routers, entry points)
- Founding member subscription system built with Stripe integration
- Waitlist system in place

---

Once you share the Notion page I'll pull in whatever strategic context, roadmap, or backlog lives there. Anything specific you want me to focus on once I have it?
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "189",
  "sender_id": "8508558620",
  "sender": "Michael Wolff",
  "timestamp": "Sun 2026-04-05 22:07 PDT"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Michael Wolff (8508558620)",
  "id": "8508558620",
  "name": "Michael Wolff"
}
```

Try to access SurvivorPulse Notion page and sub-pages again
assistant: We're in. Let me pull the page content and all sub-pages.
assistant: Four sub-pages. Let me pull all of them in parallel.
assistant: Now let me grab the key strategic sub-pages.
assistant: Now let me save everything I've learned to memory and give you the full picture.
assistant: Done. Full review complete across all three sources. Here's the consolidated picture:

---

**SurvivorPulse is a portfolio risk management engine for NFL survivor pools.** Not a pick tool. The frozen doctrine: "Different teams can still be the same bet." The product helps serious multi-entry players (3-10+ entries) coordinate allocation across entries to avoid correlated elimination.

**Where things stand:**
- Production-grade deterministic engine is built (2,400+ tests, governance-enforced)
- CA1 (flagship proof artifact) reframed to chalk collapse case study, Phase D ready
- CMEA analytics unification shipped March 24. Prototype frontend exists in separate repo
- Stripe subscription system built (50 founding member cap)
- Offseason objectives frozen: 50 users, credibility assets, ship V1

**What I see as the critical path to September 2026 launch:**
1. **CA1 completion** (Phase D) -- this is the proof asset that unlocks credibility and acquisition
2. **CMEA prototype validation** -- proves the multi-entry coordination UVP with real users
3. **V1 hardening** -- the product roadmap parking lot has meaningful items (weekly email recommendations, UI v2, documentation) that need prioritization
4. **User acquisition** -- 50 offseason users target, currently unclear on progress

**What I don't yet know (and will need):**
- Current progress against the 50-user acquisition target
- Status of the weekly planning cadence (last entries are from Feb/March)
- Whether CA1 Phase D has started or is just approved
- Live product URL / current deployment state on Replit

What do you want to tackle first?
