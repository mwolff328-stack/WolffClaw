# Stan the Scout — Backtesting Consistency Report

**Date:** 2026-05-14
**Priority:** P1 (SurvivorPulse)
**Status:** Investigation complete. Root cause identified. Reference scenarios defined.

---

## Executive Summary

The SurvivorPulse backtesting engine is **deterministic** — there is no randomness. The two apps (SurvivorPulse main app and Back Testing Prototype) produce different results for identical user inputs because they are **running against different datasets**, not because their algorithms differ. The algorithm code is functionally identical.

**The primary root cause is a split data backend:**
- Main app fetches from the **local Neon DB** (`/api/...` → `heliumdb` on Replit)
- Prototype fetches from the **production server** (`https://survivorpulse.com/api/...`)

The pick share (dynamics) data for historical seasons 2021–2024 differs between these two backends, causing different teams to be selected by the simulation, cascading into different entry-week totals and a different winner.

---

## Observed Discrepancy

**Inputs:** 5 seasons (2021–2025), 5 entries, no buybacks, 1 pick/week, Find Best Strategy, Same for All

| App | Winner | Total Entry-Weeks |
|---|---|---|
| SurvivorPulse (main) | Coordinated Diversification (70/30, Skip 1) | 97 |
| Back Testing Prototype | 70/30 Blend | 94 |

Not just the winner — per-season breakdowns differ substantially across many strategies.

---

## Root Cause Analysis

### Root Cause 1: Different Data Backends (PRIMARY — CONFIRMED)

**Main app (`client/src/backtester/lib/api.ts`):**
```typescript
const res = await fetch(`/api/games?season=${season}`, { credentials: 'include' })
```
Uses relative URLs → hits the local Replit dev server → reads from local Neon DB (`postgresql://postgres:password@helium/heliumdb`).

**Prototype (`src/lib/api.ts`):**
```typescript
const BASE_URL = 'https://survivorpulse.com'
const res = await fetch(`${BASE_URL}/api/games?season=${season}`, { credentials: 'omit' })
```
Uses absolute URL → hits the production SurvivorPulse server → reads from production DB.

**Impact:** Pick share (dynamics) data for 2021–2024 can differ between these two databases if:
- The local DB was seeded from a different source (survivorgrid.com flat files) than production
- The local DB was not fully synced with production
- The pick_popularity table in local DB was populated at a different time or from a different import run

Pick share data directly controls team scoring (`computeTeamScore` blends win probability with anti-chalk pick share penalty). Different pick shares → different ranked teams → different assignments → different survival outcomes. A 2–3 pick share percentage point difference on a key game can flip which team is selected across 5 entries and cascade for the rest of the season.

**Verification:** Running the optimization against the prototype's local static data files (survivorgrid.com, version-controlled in `data/`) consistently produces Coord Div as the winner over 2021–2024. This strongly implies the local Neon DB data is closer to the survivorgrid source, while the production DB was populated from a different source or at a different time.

---

### Root Cause 2: Browser Cache Contamination (SECONDARY — PLAUSIBLE)

Both apps use browser localStorage caching under the same key scheme:
- `season-games-${season}-v3` for game records
- `dynamics-${poolId}-${season}` for pick share data

Each app runs in a different browser context (different origin/port), so their localStorage is independent. If either app has stale cached data from a previous run (e.g., a prior API version, a cleared-and-repopulated DB, or a different season's data mis-keyed), the simulation runs against that stale data without any user-visible indication.

**Workaround:** Both apps have a "Clear Cache" button. Mike should clear the cache in both apps before comparing results. But this is a workaround, not a fix.

---

### Root Cause 3: SST-124/125 Code Fix — NOT the Issue (RULED OUT)

There is a confirmed code divergence in `assignIndependentPicks.ts`:

**Main app:**
```typescript
const firstWeekWithData = weeks.find(w => !w.isLoading && w.portfolioData !== null)
```

**Prototype:**
```typescript
const firstWeekWithData = weeks.find(w => !w.isLoading && (w.portfolioData?.allocation?.length ?? 0) > 0)
```

The main app was updated to fix SST-124/SST-125. However, this difference **does not affect optimization runs**. `buildSyntheticWeeks()` always creates portfolioData with a non-empty allocation stub (1 dummy entry), satisfying both conditions identically. This code difference would only matter for real season replays with live API data that sometimes returns empty allocations.

---

### Root Cause 4: 2025 Season Data Unavailable Locally (CONTRIBUTING — CONFIRMED)

The prototype's local data files (`data/`) contain game and pick data for 2021–2024 only. There is no `survivorgrid_picks_2025.json`. The 2025 season data is fetched entirely from the production API at runtime.

The main app also fetches 2025 data from its local server. If the local server's 2025 data differs from production (e.g., partial season data, different game records), the two apps will diverge on 2025 even if 2021–2024 is fixed.

---

## Algorithm Equivalence Verification

The following were verified to be **functionally identical** between both apps:

| Component | Status |
|---|---|
| `OPTIMIZATION_GRID` (all strategy configs) | Identical |
| `runOptimization()` logic | Identical |
| `buildSyntheticWeeks()` | Identical |
| `countEntryWeeksOptim()` | Identical |
| `computeTeamScore()` scoring formula | Identical |
| `assignIndependentPicks()` logic for optimization path | Functionally identical (SST-124 fix irrelevant to this path) |
| Field normalizers (`normalizeIndependentPick`, `normalizeAllocationEntry`) | Identical |
| `fetchSeasonDynamics()` | Identical |
| Pool IDs per season (2021–2025) | Identical |
| `optimizeStrategyMode` default ('same') | Identical |

---

## Ground Truth Reference Values

These values were computed by running the prototype's `runOptimization()` against version-controlled static data files (`data/nfl_games_*.json` + `data/survivorgrid_picks_*.json`). These fixtures are deterministic and pinned — they are the canonical reference.

**Note:** 2025 data is not available as a static fixture. Scenarios are defined for 2021–2024 only. Any scenario involving 2025 requires API data and cannot be pinned without a new 2025 fixture file.

### Reference Test Scenarios

| ID | Seasons | Entries | Buybacks | Expected Winner | Winner Total | Confidence |
|---|---|---|---|---|---|---|
| REF-001 | 2023 only | 5 | No | 90/10 Blend | 21 | HIGH |
| REF-002 | 2024 only | 5 | No | Coordinated Diversification (70/30, Skip 1) | 25 | HIGH |
| REF-003 | 2021 only | 5 | No | Coordinated Diversification (70/30, Skip 2) | 24 | HIGH |
| REF-004 | 2022 only | 5 | No | 70/30 Blend + Prefer Home (Soft 10%) | 20 | HIGH |
| REF-005 | 2021–2024 | 5 | No | Coordinated Diversification (70/30, Skip 1) | 64 | HIGH |
| REF-006 | 2023 only | 1 | No | Pure Win Probability (tie) | 9 | HIGH |
| REF-007 | 2024 only | 1 | No | 70/30 Blend (tie w/ Coord Div) | 11 | HIGH |
| REF-008 | 2023 only | 5 | Yes | Coordinated Diversification (70/30, Skip 1) | 37 | HIGH |

### Per-Strategy Breakdowns for REF-001 through REF-005

**REF-001 — 2023, 5 entries, no buyback:**
| Strategy | Entry-Weeks | Last Elim Week |
|---|---|---|
| Pure Win Probability | 13 | 10 |
| 70/30 Blend | 17 | 12 |
| 80/20 Blend | 17 | 10 |
| 90/10 Blend | 21 | 11 |
| Coordinated Diversification (70/30, Skip 1) | 21 | 12 |
| SurvivorPulse Expected Value | 6 | 4 |

**REF-002 — 2024, 5 entries, no buyback:**
| Strategy | Entry-Weeks | Last Elim Week |
|---|---|---|
| Pure Win Probability | 3 | 2 |
| 70/30 Blend | 14 | 12 |
| 80/20 Blend | 4 | 3 |
| 90/10 Blend | 4 | 3 |
| Coordinated Diversification (70/30, Skip 1) | 25 | 12 |
| SurvivorPulse Expected Value | 5 | 3 |

**REF-005 — 2021–2024, 5 entries, no buyback:**
| Strategy | 2021 | 2022 | 2023 | 2024 | Total |
|---|---|---|---|---|---|
| Pure Win Probability | 21 | 8 | 13 | 3 | 45 |
| 70/30 Blend | 15 | 10 | 17 | 14 | 56 |
| 80/20 Blend | 17 | 13 | 17 | 4 | 51 |
| 90/10 Blend | 17 | 7 | 21 | 4 | 49 |
| Coordinated Diversification (70/30, Skip 1) | 15 | 3 | 21 | 25 | **64** |
| SurvivorPulse Expected Value | 6 | 9 | 6 | 5 | 26 |

---

## Recommended Fix for Felix / Vlad

### Fix 1 — Unify the data backend (REQUIRED)

The prototype should either:
- **Option A:** Switch to relative URLs and run against the same local server as the main app during development
- **Option B:** Both apps point to the same data fixture layer (static JSON files or a shared staging DB)
- **Option C:** Keep the prototype on production, but also point the main app at production data for consistency checks

The simplest path: update the main app to also use absolute production URLs when running backtests for historical seasons, or better, seed the local DB from the same survivorgrid export files that the prototype's test fixtures use.

### Fix 2 — Add a data source indicator to the UI (RECOMMENDED)

Both apps should display which data backend they're using (local vs production) so discrepancies are visible to the user.

### Fix 3 — Add API-backed integration tests (REQUIRED)

The prototype already has deterministic unit tests against local fixtures. The main app has none. Felix should port the prototype's `verification.test.ts` to the main app's backtester test suite, using the same static fixture files as canonical inputs.

Both apps must pass these tests with the same expected values before either is considered "correct."

### Fix 4 — Pin a 2025 data fixture (REQUIRED for 5-season scenarios)

Create `data/survivorgrid_picks_2025.json` from either:
- The survivorgrid.com 2025 export
- A snapshot of the production API dynamics data for season 2025

Add it to both repos under the same `data/` directory structure. Add a `verification.test.ts` case for 2025.

### Fix 5 — Cache key versioning (RECOMMENDED)

If the data schema or source changes, bump the cache key version suffix (currently `-v3` for games). This forces a refresh when data is updated, preventing stale-cache divergence.

---

## Immediate Red Flags

1. **Both apps running different historical data in production-like settings** — any results shown to end users from the main app are currently unverified against a ground truth. The product should not claim strategy rankings as reliable until both apps agree on 2021–2024 results.

2. **2025 data is unfixed** — even if the root cause is resolved for 2021–2024, 2025 results depend on live API data that can change as the season advances (completed game outcomes, updated pick shares). Any "best strategy for 2021–2025" result is a moving target unless 2025 data is snapshotted.

3. **No test coverage in the main app's backtester** — the main SurvivorPulse app has zero automated tests for its backtester. Any regression (a bad deploy, a data migration) could silently produce wrong results with no alerting.

---

## Files Investigated

| File | App | Notes |
|---|---|---|
| `client/src/backtester/lib/optimization.ts` | Main | Algorithm identical to prototype |
| `client/src/backtester/lib/assignIndependentPicks.ts` | Main | SST-124 fix; irrelevant to optimization path |
| `client/src/backtester/lib/api.ts` | Main | Relative URLs → local server |
| `client/src/backtester/hooks/useSeasonData.ts` | Main | React Query + useRef, `makeFallbackPortfolioData()` |
| `client/src/backtester/components/replay/SeasonReplayView.tsx` | Main | Has `optimizeStrategyMode` toggle |
| `src/lib/optimization.ts` | Prototype | Algorithm identical to main |
| `src/lib/assignIndependentPicks.ts` | Prototype | Pre-SST-124 condition |
| `src/lib/api.ts` | Prototype | Absolute URL `https://survivorpulse.com` |
| `src/hooks/useSeasonData.ts` | Prototype | Simpler useState/useEffect |
| `src/components/replay/SeasonReplayView.tsx` | Prototype | Also has `optimizeStrategyMode` |
| `data/nfl_games_202{1-4}.json` | Prototype | Pinned game records (source: nfl_data_py) |
| `data/survivorgrid_picks_202{1-4}.json` | Prototype | Pinned pick shares (source: survivorgrid.com) |
| `src/lib/__tests__/verification.test.ts` | Prototype | Existing accuracy tests — all passing |
| `shared/backtester/parameterSweep.ts` | Main | Not present in prototype; no impact on optimization |
