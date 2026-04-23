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

## Sub-agents (v1.2, updated 2026-04-23)

**Intelligence layer:**
- Stan the Scout: research, market analysis, competitive intelligence (P1, P2, P3)

**Product layer:**
- Pam the Product Owner: roadmap, backlog, requirements direction (P1, P2)
- Ann the Analyst: detailed requirements and acceptance criteria (P1, P2)

**Build layer:**
- Felix the Forge: technical implementation, dev coordination (P1, P2)
- Deb the Designer: UX design, front-end implementation, visual brand system (P1, P2, P3)
- Vlad the Verifier: QA, hypothesis testing, validation (P1, P2)
- Rita the Relay: workflow automation, OpenClaw tasks, API integration (P1, P2, P3)

**Output layer:**
- Hank the Hawk: client acquisition, marketing, revenue, PR, lead nurturing, referral strategy (P1, P3)
- Sky the Scribe: content authoring, all formats -- long-form, social, X threads, Reddit posts (P1, P3)
- Arlo the Amplifier: publishing and channel distribution -- LinkedIn, Medium, X, Reddit, Facebook, Discord (P1, P3)
- Meg the Megaphone (new): social presence, community building, daily engagement, reply management (P1, P3)
- Paige the Page (new): public website strategy, SEO, landing pages, conversion optimization (P1)
- Rex the Referral (new): referral program execution, affiliate partnerships, commissioner outreach (P1)

Full specs: ~/.claude/agents/*.md

**Key v1.1 change:** Build layer now gates on Ann's requirements. No requirements = no build. Delegation sequence: Stan -> Pam -> Ann -> Felix/Deb/Rita -> Vlad.

**Key v1.2 changes (2026-04-23):**
- Hank expanded: channel priorities (X > Reddit > Facebook > Discord > LinkedIn), PR ownership, lead nurturing ownership, referral strategy, paid acquisition gating criteria (not a hard block)
- Sky expanded: SurvivorPulse content domains, social-format content (X posts, threads, Reddit posts), X and Reddit platform guidelines
- Arlo expanded: X, Reddit, Facebook, Discord channels with format guidelines, social scheduling/tracking, Meg handoff protocol
- Deb expanded: explicit visual brand system ownership (logo, color, typography, tokens); Sky owns written voice, Deb owns visual brand
- Meg the Megaphone: social presence and community engagement layer; activates after Arlo publishes; channels in priority order: X, Reddit, Facebook, Discord, LinkedIn
- Paige the Page: public site strategy and SEO; coordinates Sky (copy), Deb (design), Ann+Felix (build), Hank (conversion goals)
- Rex the Referral: referral and affiliate execution; commissioner partnerships are primary target; all incentives require founder approval

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
- SurvivorPulse-BackTesting-Prototype: git@github.com:mwolff328-stack/SurvivorPulse-BackTesting-Prototype.git (React+Vite prototype for coordinated multi-entry allocation / backtesting validation; formerly CMEA-Prototype)

**Notion workspace:** Page ID 26329ce5-833d-800a-be90-ff530bddc59c. Sub-pages: Initiative briefing, Strategy & Growth (15 sub-pages), Product & Engineering (20+ sub-pages), Historical Account.

**Offseason objectives (frozen):**
1. Acquire 50 high-signal offseason users
2. Produce credibility assets proving the Flagship Artifact
3. Ship stable, opinionated V1 enforcing doctrine

**CA1 status:** Reframed to chalk collapse visibility case study. Active spec 004 (Phase D ready). Anchor: Week 14, 2025 Tampa Bay 57% ownership event.

**CMEA status:** Analytics Unification complete (shipped March 24, 2026). Prototype frontend exists in separate repo. Validates coordinated multi-entry allocation via 2025 season replay.

**Dev workflow:** AI-assisted (Claude AI + Claude Code + Cursor + GitHub + Replit). Hosted on Replit.

**Notion API:** Key stored at ~/.config/notion/api_key. Integration name: "OpenClaw".

**Master Backlog:** Notion database (db_id: 29d643cd-9eb9-4897-9027-8efbd73c0f1d, data_source_id: 8c2ca295-bf31-4bbe-8643-a2f2781297fc). Schema: Task (title), Status (Today/This Week/In Progress/Backlog/Deferred/On Hold/Done), Area (select), Priority (High/Medium/Low), Size (Small/Medium/Large), Due Date, Completion Date, Outcome Type (MIT/Primary/Secondary/Maintenance), Dependencies (relation), Parent Task (relation), Recurring (checkbox), Frequency (Daily/Weekly), Notes (rich text).

**Active SurvivorPulse tasks (as of 2026-04-06):**
- Today: Improve CMEA Prototype; Start automated dev system with OpenClaw/Claude Code
- This Week: Share CMEA Prototype with TAM; Groom Product Backlog; Discord CMEA recruitment
- In Progress: Validate CMEA UVP (Large); CMEA Prototype build (Large)
- Backlog: Update Offseason Plan per UVP validation; Update elevator pitch; Reframe CA1/Update Spec; Migrate SubscriptionGuard to dynamic checkout; X engagement (@SurvivorSweat/@CircaSports, manual only); LinkedIn series
- Deferred: Implement Reframed CA1; Reddit follow-up for CMEA validation
- On Hold: Competitive Analysis

**Immediate focus (set 2026-04-06):** Get CMEA Prototype to a state that convinces early adopters to sign up. Mike wants to revisit what we're trying to accomplish and how best to show it in the prototype before starting work. Waiting for his go-ahead.

**Environment secrets:** Stored at .env.survivorpulse (gitignored). Covers: Neon DB, Stripe (live), Postmark, Odds API, session secret, Replit object store. Note: GIT_URL contains a PAT that should be rotated.

## Google Drive Access
SurvivorPulse shared drive now accessible at:
`~/Library/CloudStorage/GoogleDrive-michael.wolff@survivorpulse.com/Shared drives/SurvivorPulse/`
Two top-level folders: Strategy & Growth, Product & Engineering.

## SurvivorPulse - Additional Context from Drive

**Market (TAM/SAM/SOM v5, Feb 2026):**
- TAM: ~$1B annual entry-fee spend across survivor formats
- NFL Survivor SAM: $110M–$140M (paid pools, serious repeat players)
- Conservative path: ~$750K/year at 30K users, $25 ARPU (NFL only)
- Base case: $2.5M–$3M by Year 6–8 with strong PMF
- Expansion to MM (Year 3), NBA (Year 5), MLB (Year 7) only after NFL dominance criteria met
- Hard rule: no expansion until one full NFL season with dominance metrics tracked
- Falsification criteria: ARPU <$50 after 2 seasons, retention <60%, commissioner adoption <30%, organic acquisition <40%
- Non-target: casual/free pools, single-entry pick-seekers

**Competitive landscape (v1.0, Feb 2026):**
- Two real threats: PoolGenius (TeamRankings) and PoolCrunch — both explicit about portfolio/EV language
- Win condition: simpler, more opinionated operating system for multi-entry/multi-pool risk allocation
- Risk: drifting into generic pick recommendations = differentiation collapse
- Must win via clarity, workflow, and a wedge that's hard to explain away
- DIY spreadsheets remain sticky for technical users (control, but brittle)

**CA1 Credibility Asset - Current State:**
- Completed artifact: `CA1_Rewrite_Final.md` + full JSON output in Drive
- Headline: portfolio approach outlasted independent entries by +1.04 weeks avg
- Key event: Week 2 was highest concentration week; independent path went 3→1 entries; portfolio stayed 3/3
- Week 14 chalk collapse: Tampa Bay 57% ownership, Loss → 80% field eliminated
- Correlation Delta metric: positive = harmful correlation; negative = diversification benefit
- CA1 spec at v1.8 (Phase D ready per active spec 004 in SurvivorPulse repo)
- Artifact data: real Yahoo pick percentages all 18 weeks, deterministic engine, byte-identical reproducible
- Season results: 78.9% wipeout probability (all entries), 21.1% chance ≥1 survives to end

**Off-season plan (from TAM/SAM/SOM):**
- Phase 1 (now→Super Bowl): credibility extraction, post-mortems, proof artifacts
- Phase 2 (Feb→May): authority building, 5–10 high-signal content pieces, email list
- Phase 3 (Jun→Aug): acquisition readiness, onboarding, waitlist, commissioner seeding
- Acquisition window: late Aug → Week 2 (only real window)
- 90-day checklist: 3 credibility assets by March 1 (already have CA1), 1 insight/week for 12 weeks, 10–25 serious testers before June, pricing locked by July 1

**Data in Drive:**
- Full 2025 season data: Yahoo pick distributions weeks 1–18, 4for4 spreads weeks 1–17, playoff rounds
- Weekly NFL optimizer spreadsheets v1–v24 (Week 1 iteration history visible)
- 2025 NFL schedule xlsx

## Research Artifact Workflow
Research artifacts from Stan (and other agents) go to:
1. **SurvivorPulse repo**: `docs/research/` directory, committed and pushed
2. **Notion**: Under Strategy & Growth > Competitive Intelligence (page ID: 33d29ce5-833d-81dc-befe-f1ae89fdb645)

When a new research artifact is produced, auto-sync to both locations. Pattern established 2026-04-09.

Existing pages:
- Competitive Intelligence parent: 33d29ce5-833d-81dc-befe-f1ae89fdb645
- PoolGenius & PoolCrunch audit: 33d29ce5-833d-8108-bb5a-f2f218b36e7f
- CMEA Prototype Product Brief: 33d29ce5-833d-8161-827d-ea90f9fa8dbb

## Discord Channels
- **#infra** (channel id: 1491786035980537978) — ops, CI, integrations, automation, Rita-type tasks. Created 2026-04-09.

## Model Strategy (set 2026-04-11)
- Luigi runs on Sonnet by default. Switch to Opus for strategy, complex synthesis, architecture decisions.
- Sub-agents default to Sonnet. Pass model override per task when Opus is warranted (deep research, etc.).
- Routing: exec for one-shot tasks; ACP for multi-turn, interactive, or persistent sessions.

## Claude Code ACP (wired 2026-04-11)
- ACP enabled in openclaw.json: acp.enabled=true, acp.defaultAgent=claude, acp.backend=acpx
- permissionMode=approve-all (required for non-interactive file writes)
- Discord thread bindings enabled: spawnAcpSessions=true
- Spawn from Discord: /acp spawn claude --thread auto OR /acp spawn claude --bind here
- Health check: /acp doctor

## CI Pipeline (updated 2026-04-09)
- Two workflows on push to main: Pre-Publish Gate (ship gate) and Release Guardian (contract/governance gate)
- Shared DB setup extracted into composite action: `.github/actions/ci-db-setup/action.yml`
- Stage failure tracking via FAILED_STAGE env var in every test step
- Telegram + Discord notifications on pass/fail (both workflows)
- Telegram bot: @survivorpulse_ci_bot, chat ID 8508558620
- GitHub secrets: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DISCORD_WEBHOOK_URL
- PR #37 merged 2026-04-09
- gh CLI authenticated on Mac mini (mwolff328-stack, HTTPS, scopes: gist, read:org, repo, workflow)

## Design System (updated 2026-04-10)
- Selected **Linear** as base DESIGN.md (from 58 options evaluated by Deb)
- Customizations: IBM Carbon status tokens (danger/success/warning/info), Sentry uppercase label pattern, JetBrains Mono replacing Berkeley Mono
- Testing on CMEA-Prototype first (PR #7), then bring to main SurvivorPulse repo
- Custom DESIGN.md: 797 lines, Stitch format, dark-first (#08090a canvas), Inter Variable + JetBrains Mono
- Tailwind config extended with status colors, surface elevation tokens, brand indigo-violet

## Notion Pages Index (supplement to existing entries)
- CI Pipeline doc: 33e29ce5-833d-812b-ba51-dcf566081316 (Product & Engineering > Architecture & Infrastructure)
- DESIGN.md Shortlist: 33e29ce5-833d-8105-abd8-e9ffff821d3e (Product & Engineering > UX)

## Backtesting Research — Stan
- Round 1–5 results: `memory/stan-backtesting-research.md` — 5 entries, 3 seasons, 70/30 Blend wins every round
- Round 6 (entry scaling): `memory/stan-entry-scale-research.md` — 14 strategies × 4 entry counts × 3 seasons
  - 70/30 Blend loses crown at n=10 (beaten by 7 strategies) and n=20 (beaten by 4)
  - SP Production 70%EV+30%FV wins at n=10; Mixed Portfolio wins at n=20
  - 70/30 Blend reclaims #1 at n=50 (team exhaustion makes sophistication backfire)
  - Product implication: strategy recommendation should adapt to portfolio size

## Lessons learned
_(none yet)_
