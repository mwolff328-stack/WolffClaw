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
- **Git commit rules (set 2026-04-29, updated 2026-05-14):** WolffClaw workspace repo is ONLY for OpenClaw setup/config changes. All SurvivorPulse-related changes (docs, code, product work) commit to SurvivorPulse repo (`/Users/mrwolff/Projects/SurvivorPulse`, git@github.com:mwolff328-stack/SurvivorPulse.git) only. Sub-agents doing SP work must target the SurvivorPulse repo, not the workspace. **All SP documentation must be committed to the SurvivorPulse repo upon creation** — this applies to design docs, specs, and any other docs produced for SP by any agent.

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

**Master Backlog:** Notion database (db_id: 29d643cd-9eb9-4897-9027-8efbd73c0f1d, data_source_id: 8c2ca295-bf31-4bbe-8643-a2f2781297fc). Schema: Task (title), Status (Today/This Week/In Progress/Backlog/Deferred/On Hold/Done), Area (select), Priority (High/Medium/Low), Size (Small/Medium/Large), Due Date, Completion Date, Outcome Type (MIT/Primary/Secondary/Maintenance), Dependencies (relation), Parent Task (relation), Recurring (checkbox), Frequency (Daily/Weekly), Notes (rich text). ⚠️ DO NOT put SurvivorPulse product development tasks here. Use the SP Product Backlog instead.

**SurvivorPulse Product Management (migrated 2026-07-14):** 4-database structure replacing the old flat backlog. ALL SurvivorPulse product dev work goes here, not in Master Backlog.

- **SP Features** (db_id: 35929ce5-833d-81c0-b483-cd5616ebece2): Top-level features. Schema: Name, Description, Status (Planned/Active/Complete), Priority.
- **SP Epics** (db_id: 35929ce5-833d-81ef-82c5-dfb677eb90b4): Epics grouped under Features. Schema: Name, Description, Status (Planned/Active/Complete/On Hold), Priority, Feature (relation). 27 epics auto-created from old backlog naming convention.
- **SP Sprints** (db_id: 35929ce5-833d-81c6-ade8-d4a8843deb03): Sprint tracking. Schema: Name, Status (Planning/Active/Complete), Goal, Dates (start+end).
- **SP Stories & Tasks** (db_id: 35929ce5-833d-813d-ac22-ef23bb216120): 99 items migrated from old flat backlog. Schema: Item (title), Status (Today/This Week/In Progress/Backlog/Deferred/On Hold/Done), Category, Phase, Priority, Size, Type, Notes, Epic (relation), Sprint (relation). Naming convention: "[Epic Name] (X.Y): [Description]".

Old flat backlog (23c0e14a-e704-4481-a635-8202e8569e04) preserved for verification — Mike to delete manually.

**SP Stories & Tasks conventions:**
- Every story must have Description, Acceptance Criteria, and Test Cases populated in their respective rich text fields (added 2026-05-11).
- Description: 2-4 sentence user story or feature description.
- Acceptance Criteria: Given/When/Then style or numbered list of verifiable criteria.
- Test Cases: Numbered list of test scenarios with expected outcomes.
- Sprint relation: assign to the appropriate sprint at story creation or grooming time.

**Active SurvivorPulse tasks (as of 2026-04-06):**
- Today: Improve CMEA Prototype; Start automated dev system with OpenClaw/Claude Code
- This Week: Share CMEA Prototype with TAM; Groom Product Backlog; Discord CMEA recruitment
- In Progress: Validate CMEA UVP (Large); CMEA Prototype build (Large)
- Backlog: Update Offseason Plan per UVP validation; Update elevator pitch; Reframe CA1/Update Spec; Migrate SubscriptionGuard to dynamic checkout; X engagement (@SurvivorSweat/@CircaSports, manual only); LinkedIn series
- Deferred: Implement Reframed CA1; Reddit follow-up for CMEA validation
- On Hold: Competitive Analysis
- DESIGN.md Shortlist: 33e29ce5-833d-8105-abd8-e9ffff821d3e (Product & Engineering > UX)

## Backtesting Research — Stan
- Round 1–5 results: `memory/stan-backtesting-research.md` — 5 entries, 3 seasons, 70/30 Blend wins every round
- Round 6 (entry scaling): `memory/stan-entry-scale-research.md` — 14 strategies × 4 entry counts × 3 seasons
  - 70/30 Blend loses crown at n=10 (beaten by 7 strategies) and n=20 (beaten by 4)
  - SP Production 70%EV+30%FV wins at n=10; Mixed Portfolio wins at n=20
  - 70/30 Blend reclaims #1 at n=50 (team exhaustion makes sophistication backfire)
  - Product implication: strategy recommendation should adapt to portfolio size

## Strategy-to-Context Matching Sims (2026-04-28 to 2026-05-04)
All 5 validation sims complete. Scripts + memory writeups in survivorpulse-workspace/scripts/ and memory/.
- **Sim 1 (Dynamic Strategy Switching):** `stan-dynamic-strategy-sim.md` — +25% EW at n=10 vs best static. Core/Satellite role assignment is the mechanism, not inventory switching.
- **Sim 2 (Cross-Entry Correlation):** `stan-correlation-sim.md` — Uncoordinated portfolios hit 100% correlation rate; coordinated strategies hit 0%. $10K vs $1K single-week risk at n=10/$1K buy-in.
- **Sim 3 (Inventory Death Analysis):** `stan-inventory-death-sim.md` — Entry deaths are primarily bad luck (high-WP picks that lost), not inventory depletion. SP Conservative entries have the best inventory profiles at death.
- **Sim 4 (Multi-Life/Strike Format):** `stan-multilife-strategy-sim.md` — Strike formats flip the strategy leaderboard. blend_70_30 becomes #1, adaptive_blend jumps from last to 2nd, SP strategies drop to #6-7. Strike2 is the sweet spot. Recommendation engine must be format-aware.
- **Sim 5 (Field Size Effects):** `stan-field-size-sim.md` — Optimal contrarian weight is monotonically increasing with field size. Small pools (<50) favor CW=0%; large pools (500+) favor CW=50%. EW is flat across CW range (~27-28). Chalk upset co-elimination drops 64% at CW=50% in Circa-scale pools. Pool size should be required input to tune CW recommendation.

## Story QA Gate (set 2026-05-14)
Every story must pass BOTH of these before being marked Done:
1. **Vlad (test cases):** All test cases pass. Suite stays green. If any fail → reassign to developer, set In Progress, comment with failures.
2. **Ann (acceptance criteria):** All AC verified against implementation. If any unmet → reassign to developer, set In Progress, comment with gaps.
Only when both give PASS can the story be marked Done. Developers fix issues, update comments with resolution, then re-submit to Vlad + Ann.

## Sub-agent roster additions
- Ann the Analyst: added to OpenClaw config 2026-05-14. agentDir: ~/.openclaw/agents/ann/agent

## Lessons learned
_(none yet)_
