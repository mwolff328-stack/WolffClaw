---
date: 2026-04-16
name: SurvivorPulse Back Tester Prototype - Session State
description: Full state of the backtester prototype from Apr 10-16 2026
type: project
---

# SurvivorPulse Back Tester Prototype - Session State (2026-04-16)

## What This Is

Renamed from "CMEA Prototype" to "SurvivorPulse Back Tester". A standalone React 18 + Vite + TypeScript + Tailwind CSS app that backtests NFL survivor pool pick strategies against real season data (2021-2025).

**Repo:** git@github.com:mwolff328-stack/SurvivorPulse-BackTesting-Prototype.git
**Local:** ~/Projects/SurvivorPulse-BackTesting-Prototype
**Live URL:** https://survivorpulse-backtester-prototype.replit.app/
**Access Code:** SURVIVOR2026

## Major Features Built (Apr 10-16)

### Strategy Engine
- **7 strategy types**: Pure Win Prob, Weighted Blend, SP Expected Value, Expendable-First, Custom, plus composable advanced modes
- **Configurable weights**: Win Probability, Pick Share, Future Value (sum to 100%, 5% increments)
- **Advanced params**: lookahead window (0-10 weeks), decay type (linear/exponential), min win prob floor, EV mode
- **3 advanced modes**: Coordinated Diversification (skip-based pick spreading), Adaptive Blend (season-phase weight shifting), Scarcity-Aware (dynamic FV boost)
- **Expert game context filters**: Avoid Divisional (soft penalty/hard skip), Prefer Home (soft bonus/hard skip)
- **Per-entry strategies**: each entry can use a different strategy config
- **Buybacks**: configurable deadline week, revival fee, revivals per entry

### Virtual Pool System
- No dependency on DB pools. Everything client-side.
- Pool config: season (2021-2025), entries (1-50), entry fee, buybacks, team reuse
- Strategy consolidated into Pool Config panel

### Find Best Strategy (Optimization)
- Tests 27+ strategy configs across selected seasons (multi-select checkboxes)
- Ranks by total entry-weeks survived, tie-broken by lower SD
- Per-entry optimization with 15 mixed-strategy scenarios
- User's expert filters applied to all grid strategies (Same for All scope)
- Results table with strategy tooltips explaining each approach

### Performance Summary Visuals (new Apr 16)
- **Delta Gauges**: two cards showing +/- weeks vs baselines with color coding
- **Survival Timeline**: horizontal bar chart, animated, week axis ticks
- **Entry Survival Heatmap**: color-coded grid per entry per week (green/red/amber/gray), collapsible, shows current vs both baselines

### Available Teams Table
- All 32 teams sorted by Strategy Value (composite score)
- Columns: Team (sticky), Opponent (vs./@ prefix), Spread (normalized negative=favored), Strategy Value, Win Probability, Pick Share, Expected Value, Future Value
- All columns sortable (click header)
- Badges: DIV (divisional matchup), HOME/AWAY, Used, Picked
- Sticky header row + sticky Team column

### Access Gate + Feedback System
- Access code gate: SURVIVOR2026
- Name + email capture on first entry
- 5 progressive feedback questions (triggered by engagement milestones)
- Persistent mode after 5+ sessions: no dismiss, all questions shown
- Feedback stored in localStorage + forwarded to Notion via proxy endpoint
- Admin page at /admin for local feedback export
- "Update Feedback" tab after all questions answered

### Tutorial Overlay
- 17-step interactive tutorial with direct element highlighting
- Steps cover: Welcome, Pool Setup, Strategy, Mode, Scope, Template, Params, Expert Filters, Update, Performance Summary, Week Selector, Entry Picks, Available Teams, Find Best Strategy, Results (screenshot), Help, Done
- Jump-to-any-step navigation dots
- Scroll-to-top on launch, tooltip always above highlighted element
- Actions: auto-switch modes, auto-expand sections
- Persisted in localStorage, Tutorial tab to relaunch
- Step 15 shows static screenshot with "Enlarge in new tab" link

### User Guide
- Right-hand slide-out drawer
- Comprehensive: both modes, all settings, templates, optimization strategies, advanced modes, expert filters
- Tooltips on all fields via info icon (ⓘ) hover popovers

### Data Pipeline
- 5 seasons: 2021-2025
- Game data: nfl_data_py (local) + SurvivorPulse API (2025)
- Pick popularity: SurvivorGrid (scraped) + SurvivorPulse dynamics API
- Loaded into production Neon DB: ep-orange-bush-afg0m2nx
- Pool IDs: 2021=a1b2c3d4-2021-...-21, 2022=...-22, 2023=...-23, 2024=...-24, 2025=04e2471b-...
- Import script: ~/.openclaw/workspace/scripts/import-historical-seasons.py (supports --db-url and --seasons args)

### Progressive Loading
- Week 1 activates first (~1 second)
- Remaining weeks load in batches of 4
- "Computing picks..." indicator with progress count
- SWR cache: instant on repeat visits

### Branding
- Title: "SurvivorPulse Back Tester" with logo
- Description below title
- Dark-mode design system throughout

## Test Coverage
- **306 tests passing** across 13 test files
- Verification tests confirm prototype matches Stan's backtesting research
- Coverage: scoring, assignment, buybacks, optimization, game context filters, display formatting, performance summary utils

## Feedback Proxy
- Endpoint: POST https://survivorpulse.com/api/backtester/feedback
- Forwards to Notion database (82ca7841-8bb8-4796-a5ab-f8f1f792ec5e)
- Requires NOTION_API_KEY secret on SurvivorPulse Replit
- Requires x-sp-request header from client

## Key Files
- src/lib/assignIndependentPicks.ts - core simulation engine
- src/lib/optimization.ts - optimization grid + runner
- src/lib/performanceSummaryUtils.ts - visual computation helpers
- src/components/replay/SeasonReplayView.tsx - main orchestrator
- src/components/replay/PoolConfigPanel.tsx - all configuration
- src/components/replay/PerformanceSummaryVisual.tsx - 3 visual components
- src/components/TutorialOverlay.tsx - 17-step tutorial
- src/components/FeedbackCard.tsx - progressive feedback
- src/components/AccessGate.tsx - access code + signup
- src/components/replay/UserGuideDrawer.tsx - help drawer
- src/lib/feedback.ts - localStorage + Notion proxy

## Backtesting Research
- See memory/stan-backtesting-research.md for full results
- 70/30 Blend confirmed best across 5 seasons (consistency + performance)
- Research continues in Discord #backtesting-research channel
- Notion: https://www.notion.so/Back-Testing-Research-34029ce5833d8006bd12e10a4892cc4c

## Replit Deployment Notes
- Port 5173 required for Replit Preview
- Kill stale processes before restart: pkill -f vite; pkill -f node; sleep 2; npm run dev
- NOTION_API_KEY must be set as Replit secret on SurvivorPulse deployment
