# MEMORY.md - Long-term Memory

## Identity
- I am Luigi. Orchestrator and chief of staff for Mike (Michael Wolff).
- My job: decompose goals, select agents, assign tasks, manage handoffs, validate outputs.
- I do not implement. Ever.

## Mike
- Solopreneur founder. Multiple domains: SaaS, fintech, fantasy sports, real estate, investing, eCommerce.
- Reasonably technical. Uses Claude, OpenAI, OpenClaw, Cursor, Replit, GitHub, Neon, Notion, Stripe, Telegram, Postmark, Google Workspace.
- Communicates via Telegram.

## Priorities (set 2026-03-31)
- P1: SurvivorPulse (NFL survivor pool, launch before Sept 2026)
- P2: Product discovery engine (repeatable AI-driven validation)
- P3: Automated content system (thought leadership pipeline)

## Sub-agents (v1.1, updated 2026-04-05)

**Intelligence layer:**
- Stan the Scout: research, market analysis, competitive intelligence (P1, P2, P3)

**Product layer (new):**
- Pam the Product Owner: roadmap, backlog, requirements direction (P1, P2)
- Ann the Analyst: detailed requirements and acceptance criteria (P1, P2)

**Build layer:**
- Felix the Forge: technical implementation, dev coordination (P1, P2)
- Deb the Designer: UX design, front-end implementation (P1, P2, P3)
- Vlad the Verifier: QA, hypothesis testing, validation (P1, P2)
- Rita the Relay (was Rex): workflow automation, OpenClaw tasks, API integration (P1, P2, P3)

**Output layer:**
- Hank the Hawk: client acquisition, marketing, revenue (P1, P3)
- Sky the Scribe (was Stu): content authoring, thought leadership (P3)
- Arlo the Amplifier: publishing, channel distribution (P3)

Full specs: ~/.claude/agents/*.md

**Key v1.1 change:** Build layer now gates on Ann's requirements. No requirements = no build. Delegation sequence: Stan -> Pam -> Ann -> Felix/Deb/Rita -> Vlad.

## Preferences
- Auto-commit and push workspace changes to WolffClaw repo (git@github.com:mwolff328-stack/WolffClaw.git) after meaningful updates. Set 2026-04-02.
- Auto-sync ~/.claude with WolffClaude repo (git@github.com:mwolff328-stack/WolffClaude.git). Push local changes, pull remote changes. Set 2026-04-03.

## SurvivorPulse (P1) - Deep Context

**Doctrine (frozen):** "SurvivorPulse helps serious survivor players manage correlation, future value, and risk across their entries and pools, because different teams can still be the same bet."

**What it is:** Decision-support system for serious NFL survivor pool players. Portfolio-level risk management engine. Deterministic, governance-grade, reproducible.
**What it is not:** Pick list, favorites engine, content site, gambling tout, Monte Carlo simulation.

**Primary ICP:** Serious multi-entry player (3-10+ entries). Manages pick distribution, uses tools like PoolCrunch/SurvivorGrid, currently allocates by gut/spreadsheet. Validated via Reddit outreach.
**Secondary ICP:** Scaling player (1-2 entries, looking to grow to 3+). Longer conversion timeline.

**Architecture:** React 18 + Vite + Tailwind/shadcn frontend. Node/Express + TypeScript backend. Drizzle ORM on Neon Postgres. Custom auth with sessions, CSRF, rate limiting. Stripe subscriptions (founding member cap: 50). Postmark transactional email.

**Key repos:**
- SurvivorPulse (main): git@github.com:mwolff328-stack/SurvivorPulse.git (1,631 files, 2,400+ unit tests, 180+ integration)
- CMEA-Prototype: git@github.com:mwolff328-stack/CMEA-Prototype.git (throwaway React+Vite prototype for coordinated multi-entry allocation validation)

**Notion workspace:** Page ID 26329ce5-833d-800a-be90-ff530bddc59c. Sub-pages: Initiative briefing, Strategy & Growth (15 sub-pages), Product & Engineering (20+ sub-pages), Historical Account.

**Offseason objectives (frozen):**
1. Acquire 50 high-signal offseason users
2. Produce credibility assets proving the Flagship Artifact
3. Ship stable, opinionated V1 enforcing doctrine

**CA1 status:** Reframed to chalk collapse visibility case study. Active spec 004 (Phase D ready). Anchor: Week 14, 2025 Tampa Bay 57% ownership event.

**CMEA status:** Analytics Unification complete (shipped March 24, 2026). Prototype frontend exists in separate repo. Validates coordinated multi-entry allocation via 2025 season replay.

**Dev workflow:** AI-assisted (Claude AI + Claude Code + Cursor + GitHub + Replit). Hosted on Replit.

**Notion API:** Key stored at ~/.config/notion/api_key. Integration name: "OpenClaw".

## Lessons learned
_(none yet)_
