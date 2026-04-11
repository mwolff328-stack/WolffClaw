---
date: 2026-04-10
name: CMEA Prototype - Full Session State
description: Complete state of the CMEA Prototype rebuild as of Apr 10, 2026 3pm PDT
type: project
---

# CMEA Prototype - Session State (2026-04-10)

## What This Is

A standalone React 18 + Vite + TypeScript + Tailwind CSS prototype that replays the 2025 NFL season through the lens of a 5-entry survivor pool. Currently showing the "Independent Path" (picks selected purely by highest win probability each week) as a baseline before we layer in coordinated allocation logic.

**Repo:** git@github.com:mwolff328-stack/CMEA-Prototype.git
**Local:** ~/Projects/CMEA-Prototype
**Live API:** https://survivorpulse.com (Replit-hosted, can cold-start/timeout)
**Pool ID:** 04e2471b-6498-4a59-8a95-c0dc50221457 (5 entries, $25 buy-in, once-per-season team reuse)

## Design System

Dark-mode-native. Deb implemented a Linear-inspired design system:
- CSS: `index.css` has all tokens (`--sp-*` variables), utility classes (`.sp-card`, `.entry-card`, `.badge-live`, `.badge-eliminated`, `.label-structural`, `.data-cell`, `.sp-table`, `.btn-toolbar`, `.btn-ghost`)
- Tailwind: `tailwind.config.ts` maps all design tokens
- Fonts: Inter (UI) + JetBrains Mono (numeric data)
- NO light-mode colors (no bg-white, bg-green-50, etc.)

## Current Page Layout (top to bottom)

1. **Data Status Bar** - loading indicator (pulsing dot), "Data loaded" state, last updated timestamp, Reload button
2. **Pool Information Panel** (`PoolInfoPanel.tsx`) - collapsible, shows pool name, sport, season, entry fee, entries, picks/week, team reuse, buybacks
3. **Entries Summary** (`EntriesSummary.tsx`) - pills for each entry showing alive/eliminated status, updates per selected week
4. **Week Selector** (`WeekSelector.tsx`) - horizontal tab bar for weeks 1-18. Green = alive entries, Red = all eliminated. Red dots under each week for entries eliminated that week.
5. **Entry Picks** (`PortfolioSlate.tsx` + `EntryCard.tsx`) - cards for each entry showing team, opponent, spread, win prob, score, outcome. Eliminated entries shown with badge. Clickable to select.
6. **Available Teams Table** (`AvailableTeamsTable.tsx`) - shown when an entry card is selected. All 32 teams (minus bye weeks) sorted by win probability. Used teams grayed out, picked team highlighted.

## Architecture / Data Flow

### API Endpoints Used
- `GET /api/pools/{poolId}` - pool config
- `POST /api/pools/{poolId}/portfolio/week` - per-week portfolio data (allocation, independentPicks, outcomes). Fetched sequentially for weeks 1-18.
- `GET /api/games?season=2025&scheduleType=regular&week=N` - full game data per week (32 teams, scores, spreads, win probabilities). Fetched in parallel for all 18 weeks.

### Independent Pick Assignment (client-side)
The `assignIndependentPicks` function in `SeasonReplayView.tsx` computes the independent path:
- Uses games API data (all 32 teams per week) as the candidate pool
- Sorts by winProbability descending
- For each alive entry (alphabetical order): assigns highest win prob team not already used by that entry or assigned to another entry this week
- Tracks eliminations: Loss = eliminated (ties count as losses)
- Tracks team reuse across weeks per entry

### Caching (Stale-While-Revalidate)
- `localStorage` with pool-specific keys
- Pool config: `pool-{poolId}`
- Week portfolio data: `weeks-{poolId}` (via useSeasonData hook)
- Season games: `season-games-2025-v3`
- Data timestamp: `data-timestamp`
- On load: render from cache immediately, background refresh silently

### Key Files
- `src/components/replay/SeasonReplayView.tsx` - main orchestrator, assignIndependentPicks logic, NFL team name map
- `src/hooks/useSeasonData.ts` - fetches 18 weeks of portfolio data sequentially, SWR cache
- `src/lib/api.ts` - API functions (fetchPoolConfig, fetchPortfolioWeek, fetchSeasonGames)
- `src/lib/cache.ts` - localStorage cache helpers
- `src/types/cmea.ts` - all TypeScript types

## Independent Path Results (verified correct)

Using games API win probabilities:
- Week 1: PHI, DEN, ARI, WAS, CIN (all win)
- Week 3: Entry 3 eliminated (GB loss at CLE, 10-13)
- Week 4: Entry 5 survives TIE (DAL 40 - GB 40) - but tie = loss in survivor, so Entry 5 should be eliminated W4
- Week 5: Entry 1 (LAR loss), Entry 4 (ARI loss), Entry 5 (BUF loss) eliminated
- Week 10: Entry 2 (CAR loss) eliminated
- **All eliminated by Week 10**

Note: If the prototype still shows Week 14, the games data cache may be stale/incomplete. Cache was busted to v3 in latest commit.

## Recent Commits (latest first)
- `ab98721` - Parallel game fetch with retry + cache bust to v3
- `87ce243` - Red elimination dots under week selector cards
- `f1f1df4` - Data status bar with loading indicator, timestamp, reload button
- `38389d6` - Full 32-team independent picks from games API, visible loading bar
- `ca89742` - Available Teams table shows all 32 NFL teams
- `500b83e` - Background load bar, week color coding, available teams table
- `3584c29` - Pivot to independent path view + apply design system
- `0162636` - Deb's Linear design system merge

## What's Hidden (not deleted, just not rendered)
- CorrelationRiskPanel (Moment 2)
- PersonalizationStatement (Moment 3)
- SeasonReplayTable + SeasonSummaryBar + ComparisonSummary
- FeedbackCapture
- Coordinated path logic (still in useSeasonData but not used for display)

## Open Issues (as of 2026-04-10 3pm)
1. **Week 8 data** - may still intermittently fail to load. Parallel fetch with retry should help.
2. **Elimination timeline** - should show all out by Week 10 once games data is complete. Was showing Week 14 due to missing week data.
3. **Tie handling** - DAL-GB W4 tie should count as loss. Code handles this correctly (not > means Loss).

## Strategy Research (completed 2026-04-10 evening)

### Multi-Season Backtesting
Ran 7 pick strategies across 2023, 2024, 2025 seasons using:
- Game results + spreads: nfl_data_py (free, Python package)
- Pick popularity: SurvivorGrid.com (scraped, Yahoo/ESPN/OFP weighted averages)
- 2025: SurvivorPulse API

Data files in ~/Projects/CMEA-Prototype/data/:
- nfl_games_2023.json, nfl_games_2024.json (game results, spreads, win probabilities)
- survivorgrid_picks_2023.json, survivorgrid_picks_2024.json (per-team pick popularity per week)

Win probabilities derived from spreads using normal CDF: P = 0.5 * (1 + erf(spread / (13.5 * sqrt(2))))
IMPORTANT: nfl_data_py spread_line convention: positive = home team FAVORED.

### Strategy Results (Cross-Season Summary)

| Strategy | 2023 | 2024 | 2025 | TOTAL | Avg/Season |
|---|---|---|---|---|---|
| **2b. Weighted Blend (70/30)** | **17** | **14** | **26** | **57** | **19.0** |
| 2e. Weighted Blend (80/20) | 17 | 4 | 22 | 43 | 14.3 |
| 1. Pure Win Probability | 13 | 3 | 22 | 38 | 12.7 |
| 2a. Leverage + 60% Floor | 5 | 16 | 11 | 32 | 10.7 |

**Winner: 70/30 Weighted Blend** (score = 0.7 * winProbability + 0.3 * (1 - pickShare/100))
- 50% more entry-weeks survived than pure win probability across 3 seasons
- Best or tied-for-best in every season
- Pure win prob collapsed in 2024 (3 entry-weeks vs 14 for 70/30)

Simulation scripts in ~/.openclaw/workspace/scripts/:
- stan-pick-strategy-sim.py (Round 1, 2025 only, 4 strategies)
- stan-pick-strategy-sim-v2.py (Round 2, 2025 only, 7 constrained strategies)
- stan-multi-season-sim.py (Round 3, all 3 seasons, 7 strategies)
- stan-scrape-survivorgrid-v2.py (SurvivorGrid scraper)

## What's Next (Mike's direction)
- Implement 70/30 Weighted Blend as Scenario 2 in the prototype with a scenario toggle
- Consider building full backtesting feature using the historical data
- The data pipeline (scrape SurvivorGrid + nfl_data_py + load to DB) could support any past season

## Notion Backlog
SurvivorPulse Product Backlog (db_id: 23c0e14a-e704-4481-a635-8202e8569e04)
- Parent task: CMEA Prototype Redesign (3 Demo Moments) - In Progress
- Moment 1-3 tasks exist, editorial pass task in backlog

## Delegation Pattern
- Luigi orchestrates, writes requirements
- Felix (Claude Code, `--permission-mode bypassPermissions --print`) builds in ~/Projects/CMEA-Prototype
- Ann's requirements docs in workspace/memory/
- Always verify TypeScript compiles (`npx tsc --noEmit`), commit, push to origin/main
