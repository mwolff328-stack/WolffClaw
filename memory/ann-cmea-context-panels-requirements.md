---
name: CMEA Prototype — Context Panels Requirements
description: Ann's requirements for Pool Information panel, Entries summary, and Week selector. Prerequisite UI before demo moments.
type: project
date: 2026-04-09
---

# CMEA Prototype — Context Panels Requirements

**Author:** Ann (Business Analyst)
**Date:** 2026-04-09
**Status:** Draft — pending Mike's review

---

## Background

The prototype currently launches directly into the three demo moments (Portfolio Pick Slate, Correlated Elimination Risk, Personalization Statement) without establishing context. A user landing on the page doesn't know what pool they're looking at, how many entries they have, what the pool rules are, or what week they're viewing. These three components provide the foundation that makes the demo moments meaningful.

## API Reference (existing — no new endpoints)

**Pool Config** (`GET /api/pools/{poolId}`):

| Field | Type | Use |
|---|---|---|
| `id` | string | Pool ID display |
| `name` | string | Pool name |
| `contestType` | string | "survivor" |
| `sport` | string | "nfl" |
| `season` | number | 2025 |
| `totalEntries` | number | Entry count |
| `entryFee` | string | "$25.00" |
| `picksPerEntry` | number | 1 |
| `teamUseLimit` | string | "1" (once per season) |
| `allowBuybacks` | boolean | false |
| `startingWeek` | number | 1 |
| `poolType` | string | "regular" |
| `maxEntriesPerUser` | number | 5 |
| `isActive` | boolean | true |

**Portfolio Week** (`POST /api/pools/{poolId}/portfolio/week`):

Already fetched per week. Relevant fields for entries summary:

| Field | Type | Use |
|---|---|---|
| `allocation[].entryId` | string | Entry identifier |
| `allocation[].entryName` | string | Display name |
| `allocation[].assignedTeam` | string | Current week pick |
| `allocation[].outcome` | string/null | "Win", "Loss", or null |
| `aliveEntryCount` | number | Alive entries entering the week |
| `entriesAliveAfterWeek` | string[] | Entry IDs alive after outcomes |

---

## Component 1 — Pool Information Panel

### User Story

As a demo viewer landing on the CMEA Prototype page, I want to immediately see the key details about the pool I'm viewing — name, sport, season, entry fee, number of entries, pick rules — so I have context for everything below before I look at any picks or analysis.

### Functional Requirements

1. The Pool Information panel MUST be the first content on the page, above all three demo moments.
2. The panel MUST display the following fields from the pool config API response:
   - Pool Name (`name`)
   - Sport (`sport`, formatted: "NFL")
   - Season (`season`, formatted: "2025")
   - Schedule Type (`poolType`, formatted: "Regular Season")
   - Entry Fee (`entryFee`, formatted as currency: "$25.00")
   - Number of Entries (`totalEntries`)
   - Picks per Week (`picksPerEntry`)
   - Team Reuse (`teamUseLimit`, formatted: "Once per season" when "1")
   - Buybacks (`allowBuybacks`, formatted: "Not allowed" when false, "Allowed" when true)
3. The panel MUST NOT be a modal. It MUST be an inline section visible without any user interaction.
4. The panel MUST match the visual style of the production SurvivorPulse Pool Information modal (clean rows with icon + label + value layout) but rendered as a persistent page section, not a popup.
5. The panel SHOULD have a compact layout option — either collapsible or a summary bar that can expand to show all fields. Default state: expanded on first load.
6. The panel MUST show a loading skeleton while the pool config API call is in flight.
7. The panel MUST show a graceful error state if the pool config API fails.

### Acceptance Criteria

- AC1: On page load, Pool Information panel is visible above the Portfolio Pick Slate without any user interaction.
- AC2: All 9 listed fields are present with correct values from the API.
- AC3: The panel shows a loading state before data arrives.
- AC4: If the API fails, an error message is shown instead of a blank or broken panel.

### Edge Cases

- **Pool config API returns null/undefined for optional fields**: Display "—" for missing values. Do not crash.
- **`entryFee` is null or "0"**: Display "Free" instead of "$0.00".
- **`teamUseLimit` values other than "1"**: "unlimited" → "Unlimited", numeric N → "N times per season".

---

## Component 2 — Entries Summary

### User Story

As a demo viewer, I want to see all my entries listed with their current status (alive or eliminated) and key details, so I know which entries are still in play before looking at picks and analysis for a specific week.

### Functional Requirements

1. The Entries Summary MUST appear below the Pool Information panel and above the demo moments.
2. The summary MUST list every entry in the pool, displaying:
   - Entry Name (`entryName` from `allocation[]`)
   - Entry Status: Alive or Eliminated (derived from client-side elimination tracking)
   - Current Week Pick (from `allocation[].assignedTeam` for the selected week, if alive)
   - Elimination Week (the week the entry was eliminated, if applicable)
3. Entry status MUST reflect the state as of the currently selected week (see Component 3). If viewing Week 3, show status entering Week 3 (based on outcomes through Week 2).
4. Alive entries MUST be visually distinct from eliminated entries (color, opacity, or badge).
5. The summary MUST derive entry data from the already-fetched week data — no new API calls.
6. The entries MUST be sorted by entry name (alphabetical, numeric-aware: Entry 1, Entry 2, ... Entry 10).
7. The summary MUST show all entries even when all are eliminated, with appropriate styling.
8. The summary MUST handle the case where week data is still loading (show skeleton/loading state).

### Acceptance Criteria

- AC1: All entries are listed with name and status visible without interaction.
- AC2: Alive and eliminated entries are visually distinct.
- AC3: When viewing a week where some entries are eliminated, those entries show as eliminated.
- AC4: Entries are sorted alphabetically by name.
- AC5: The summary updates when the selected week changes (Component 3).
- AC6: Loading state shown while week data is being fetched.

### Edge Cases

- **All entries alive**: No eliminated styling applied. All entries show "Alive".
- **All entries eliminated**: All entries show eliminated styling with their elimination week.
- **Week 1 selected**: All entries should show as alive (no outcomes have occurred yet entering Week 1).
- **Week data not yet loaded for selected week**: Show loading state, not stale data from a different week.

---

## Component 3 — Week Selector

### User Story

As a demo viewer, I want to select which week I'm viewing so I can see how picks and analysis change across the season, rather than being locked to a single week or scrolling a massive table.

### Functional Requirements

1. The Week Selector MUST appear between the Entries Summary (Component 2) and the demo moments (Moments 1-3).
2. The selector MUST allow choosing any week from 1 to 18 (regular season).
3. The selector MUST be a horizontal bar, dropdown, or tab strip — not a separate page or modal.
4. The currently selected week MUST be visually highlighted.
5. Weeks where all entries are eliminated MUST be visually indicated (grayed out, strikethrough, or labeled "Eliminated") but still selectable.
6. The selected week MUST drive the data displayed in:
   - Entries Summary (Component 2): entry status as of selected week
   - Portfolio Pick Slate (Moment 1): picks for selected week
   - Correlated Elimination Risk (Moment 2): risk analysis for selected week
   - Personalization Statement (Moment 3): entry count for selected week
7. The default selected week on page load MUST be Week 1.
8. When a week is selected, the page MUST NOT refetch data from the API — all 18 weeks of data are already loaded by `useSeasonData`. The selector only changes which week's data is displayed.
9. The selector MUST show the week number and date range (already available in `WeekViewModel.dateRange`).
10. The selector MUST be usable while weeks are still loading (weeks already loaded are selectable; weeks still loading show a loading indicator).

### Acceptance Criteria

- AC1: A week selector control is visible on the page between entries summary and demo moments.
- AC2: Clicking/selecting a week updates the Portfolio Pick Slate, Correlation Risk Panel, and Personalization Statement to show that week's data.
- AC3: The entries summary updates to reflect entry status as of the selected week.
- AC4: The default selected week is Week 1.
- AC5: Eliminated weeks are visually distinct but selectable.
- AC6: No new API calls are made when changing weeks.
- AC7: The currently selected week is visually highlighted.

### Edge Cases

- **All weeks eliminated after Week 5**: Weeks 6-18 show as eliminated but remain selectable (user can see what happened).
- **Data still loading**: Weeks not yet loaded show a loading indicator in the selector. Selecting a loading week shows a loading state in the demo moments below.
- **Single week with data (edge case)**: Selector still renders, showing Week 1 selected.

---

## Page Layout Order (updated)

1. **Pool Information Panel** (Component 1) — always visible, top of page
2. **Entries Summary** (Component 2) — below pool info, reflects selected week
3. **Week Selector** (Component 3) — navigation control
4. **Portfolio Pick Slate** (Moment 1) — for selected week
5. **Correlated Elimination Risk** (Moment 2) — for selected week
6. **Personalization Statement** (Moment 3) — for selected week
7. **Season Replay Table** (existing) — full season view, below demo moments

---

## State Management Note

Currently, the three demo moments derive their week data internally from the `weeks[]` array (they scan for the "latest week with alive entries"). With the Week Selector, all three moments must instead accept the selected week's data as a prop or consume it from a shared context. This is a refactor of how data flows to Moments 1-3, not a change to what data exists.

**Recommended approach:** Add a `selectedWeek` state to `SeasonReplayView` (or lift to context). Pass the selected `WeekViewModel` to all three moment components and the Entries Summary. The Week Selector controls this state.

---

## Component 4 — Client-Side Data Cache (Stale-While-Revalidate)

### User Story

As a demo viewer returning to the prototype, I want the page to load instantly using my previous session's data, while fresh data is fetched in the background, so I never wait for the loading waterfall on repeat visits.

### Functional Requirements

1. All fetched data MUST be cached in `localStorage`, keyed by pool ID. Cached data includes:
   - Pool config response (`GET /api/pools/{poolId}`)
   - All 18 weeks of portfolio data (`POST /api/pools/{poolId}/portfolio/week`)
   - Game week schedule data (`GET /api/games?season=2025`)
2. On page load, if cached data exists for the current pool ID:
   - Render immediately from cache (no loading spinners, no waterfall).
   - Begin background refresh of all data from the API.
   - If background refresh returns data that differs from cache, update cache and re-render silently.
   - If background refresh returns identical data, no-op (no re-render).
3. On page load, if no cached data exists for the current pool ID:
   - Show loading states as currently implemented.
   - Cache all data once fetched.
4. Cache MUST be invalidated (cleared) if the pool ID changes (different `poolId` URL param).
5. If `localStorage` is unavailable or full, the app MUST fall back to normal fetch behavior (no cache). Do not crash.
6. The cache strategy is stale-while-revalidate: always serve stale, always background refresh. No staleness window or TTL for now.
7. Background refresh MUST NOT block the UI or show loading indicators when cached data is already displayed.
8. If background refresh fails (network error, API error), keep displaying cached data. Do not show an error state over working cached content.

### Acceptance Criteria

- AC1: On first visit, data loads normally and is cached in `localStorage`.
- AC2: On second visit (same pool ID), the page renders instantly from cache with no loading spinners.
- AC3: Background refresh runs silently after cache-based render.
- AC4: If API data has changed since last cache, the UI updates to reflect new data without a full page reload.
- AC5: If `localStorage` is unavailable, the app works normally (just without caching).
- AC6: Changing the pool ID in the URL clears the old cache and fetches fresh.

### Edge Cases

- **`localStorage` quota exceeded**: Catch the error, skip caching, continue normally.
- **Corrupted cache data (invalid JSON)**: Clear the corrupted entry, fetch fresh.
- **Partial cache (some weeks cached, some not)**: Render what's cached, fetch missing weeks normally, update cache when complete.
- **Multiple tabs open to different pool IDs**: Each pool ID has its own cache key. No cross-contamination.

### Implementation Notes

- Cache key format: `cmea-cache-{poolId}` (for the combined payload) or separate keys per data type: `cmea-pool-{poolId}`, `cmea-weeks-{poolId}`, `cmea-schedule-{season}`.
- The `useSeasonData` hook is the primary integration point. It should check cache before starting the fetch waterfall, and write to cache after each week completes.
- Pool config fetch in `SeasonReplayView` should similarly check cache first.
- Use `JSON.stringify` comparison for change detection (simple, sufficient for this data size).
