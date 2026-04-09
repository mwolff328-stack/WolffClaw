---
name: CMEA Prototype Redesign — Requirements Doc
description: Ann's functional requirements for the three SurvivorPulse demo moments: unified portfolio slate, correlated elimination risk, and personalization story
type: project
date: 2026-04-08
---

# CMEA Prototype Redesign — Requirements Doc

**Author:** Ann (Business Analyst)
**Date:** 2026-04-08
**Status:** Ready for Vlad validation and Felix build

---

## API Reference (existing — do not invent new endpoints)

Live API at survivorpulse.com returns the following fields used across all three moments:

| Field | Type | Notes |
|---|---|---|
| `allocation[]` | array | Coordinated pick assignments per entry |
| `independentPicks[]` | array | What each entry would pick without coordination |
| `coordinatedSurvivalProbability` | number | Portfolio survival probability with coordination |
| `independentSurvivalProbability` | number | Portfolio survival probability without coordination |
| `portfolioSurvivalDelta` | number | Delta between coordinated and independent |
| `duplicateTeamsAvoided[]` | array | Teams that would have been duplicated without coordination |
| `yahooPickPct` | number | Per-entry field ownership percentage |
| `perPickReasonByTeamId` | object | Per-entry rationale string keyed by team ID |
| `outcome` | string/enum | Per-entry outcome (alive, eliminated, etc.) |
| `pWinNow` | number | Per-entry win probability |
| `overallScore100` | number | Per-entry overall score (0–100) |

---

## Moment 1 — Unified Portfolio Pick Slate

### User Story

As a Circa Survivor player running multiple entries this week, I want to see all of my entries and their assigned picks displayed side by side — with a clear reason for each pick — so that I can immediately understand my coordinated portfolio strategy without having to click through each entry individually.

### Functional Requirements

1. The portfolio slate MUST be the first visible content on the demo screen — no scroll, no click required to reach it.
2. Each entry MUST be displayed as a column or card showing: entry name/number, assigned team name (from `allocation[]`), and rationale text (from `perPickReasonByTeamId` for the assigned team).
3. All entries MUST be visible simultaneously — no pagination, no tabs, no "view more" for a standard demo entry count (≤10 entries).
4. The rationale text MUST explain the coordination logic, not just team quality (e.g., "chalk avoidance," "future team value preserved," "field divergence"). It MUST come from `perPickReasonByTeamId` — no fabricated copy.
5. Entries that are eliminated (`outcome === 'eliminated'` or equivalent) MUST be visually distinct (e.g., grayed out, strikethrough) but still displayed in the slate to preserve portfolio context.
6. The assigned team for each entry MUST come from `allocation[]`, not `independentPicks[]`.
7. If `allocation[]` and `independentPicks[]` differ for an entry, the divergence MUST be surfaced visually (e.g., a subtle indicator: "coordinated pick differs from independent recommendation").
8. The current week number MUST be displayed in the header of the slate.
9. Field ownership percentage (`yahooPickPct`) MUST be shown for each entry's assigned pick, positioned so it reads as "how popular this pick is with the rest of the field."
10. The component MUST render correctly when `allocation[]` contains between 1 and 10 entries.

### Acceptance Criteria

- AC1: On page load, at least 1 entry card is visible without any user interaction.
- AC2: Each entry card displays: entry label, team name, rationale text, and yahooPickPct — all four fields present and non-empty for a live entry.
- AC3: An eliminated entry renders visually different from a live entry (distinct style applied).
- AC4: A coordinated pick that differs from the independent pick shows a visual indicator on that entry card.
- AC5: The week number is present in the section header.
- AC6: The slate renders with 1 entry, 5 entries, and 10 entries without layout breakage.
- AC7: If the API returns no entries, a graceful empty state is shown (not a blank screen or JS error).

### Edge Cases

- **All entries eliminated**: Display all entries in eliminated state with a portfolio-level message ("Season complete"). Do not show an empty slate.
- **Missing `perPickReasonByTeamId` for an entry's assigned team**: Display a fallback string ("Rationale unavailable") rather than blank or error.
- **Missing `yahooPickPct`**: Display "—" or "N/A" rather than 0% (to avoid misleading "no one picked this" reading).
- **`allocation[]` is empty or null**: Show an empty state with a message ("No picks assigned for this week") rather than crashing.
- **API timeout / fetch error**: Show an error state with a retry prompt. Do not show a blank slate.
- **Single entry**: The layout must not look broken or oddly sparse with only 1 entry card.

### Component Changes

- **New component**: `PortfolioSlate` — top-level container for the side-by-side entry view. This is new; no existing component maps to this layout.
- **New component**: `EntryCard` — individual entry card showing team, rationale, yahooPickPct, and coordination indicator. New.
- **Existing component to deprioritize**: The season replay table — move below the fold or behind a tab; it should not compete for first-screen real estate.
- **Existing component to update**: Any existing week/round header component — confirm it surfaces the current week number prominently.

### API Dependencies

- **Primary**: `allocation[]` — team assignment per entry (required for every card)
- **Primary**: `perPickReasonByTeamId` — rationale per entry per team (required for rationale copy)
- **Supporting**: `yahooPickPct` — per entry (required for field ownership display)
- **Supporting**: `independentPicks[]` — per entry (required to detect and flag coordination divergence)
- **Supporting**: `outcome` — per entry (required to style eliminated entries)

---

## Moment 2 — Correlated Elimination Risk

### User Story

As a Circa Survivor player with multiple entries, I want to see a named metric showing how correlated my entries are this week — and understand what would happen if the wrong game goes against me — so that I can feel the concrete risk reduction that coordinated picks provide compared to running all entries on the same team.

### Functional Requirements

1. A named metric labeled "Correlated Elimination Risk" (or equivalent approved name) MUST be displayed as a distinct visual element — not buried in a table.
2. The metric value MUST be derived from existing API fields. Acceptable derivation: percentage of entries sharing the same assigned team this week (from `allocation[]`), or the ratio of `coordinatedSurvivalProbability` to `independentSurvivalProbability`.
3. A contrast display MUST show two states side by side or sequentially: (a) the player's actual coordinated slate, and (b) an uncoordinated baseline where all entries are on the same team.
4. The uncoordinated baseline MUST visually illustrate what "all entries eliminated at once" looks like — not as a probability number, but as an emotionally legible representation (e.g., all cards going red/strikethrough simultaneously).
5. The `portfolioSurvivalDelta` field MUST be used to power or label the improvement narrative ("Your coordinated portfolio survives X% better than if you ran the same pick everywhere").
6. The `duplicateTeamsAvoided[]` array MUST be referenced: the UI MUST name at least one team that coordination prevented from appearing across multiple entries.
7. The metric and contrast view MUST NOT require the player to understand the underlying math — the emotional message is "one bad game hurts you less."
8. The section MUST render correctly whether `duplicateTeamsAvoided[]` contains 0, 1, or multiple teams.
9. If `portfolioSurvivalDelta` is 0 (no improvement this week), the section MUST still render with a neutral/informational message rather than a misleading positive message.

### Acceptance Criteria

- AC1: A named "Correlated Elimination Risk" metric (or equivalent) is visible without scroll from the Moment 1 slate (one natural scroll or same-screen placement).
- AC2: The metric value is non-zero and derived from real API data for a week where coordination diverged.
- AC3: A contrast display is present showing coordinated vs. uncoordinated state.
- AC4: At least one team from `duplicateTeamsAvoided[]` is named in the UI copy.
- AC5: `portfolioSurvivalDelta` is reflected in UI copy or a labeled improvement number.
- AC6: When `portfolioSurvivalDelta` is 0, the section renders without showing a fake benefit.
- AC7: The contrast display does not require any player interaction to understand — it reads on its own.

### Edge Cases

- **`duplicateTeamsAvoided[]` is empty**: Do not claim any teams were avoided. Show a message like "No duplicate avoidance needed this week — all entries naturally diverged." Do not crash or show blank.
- **`portfolioSurvivalDelta` is 0 or null**: Show neutral message. Do not display 0% as a positive improvement.
- **`coordinatedSurvivalProbability` and `independentSurvivalProbability` are equal**: Acknowledge this week's allocation happened to produce the same survival odds — do not fabricate a delta.
- **All entries on different teams (correlation = 0%)**: The metric should show "No correlation this week" as a positive signal, not as a broken state.
- **All entries on the same team (correlation = 100%)**: This is the uncoordinated worst-case — if this somehow occurs in the coordinated allocation, flag it as a warning state for demo data integrity.
- **API timeout / fetch error**: Same graceful error state as Moment 1.

### Component Changes

- **New component**: `CorrelationRiskPanel` — container for the named metric, contrast display, and narrative copy. New.
- **New component**: `CoordinatedVsUncoordinatedContrast` — side-by-side or animated comparison of the two states. New.
- **Existing data already available**: No new API calls needed — all fields listed above are in the existing response.

### API Dependencies

- **Primary**: `allocation[]` — to compute or display how many entries share a team
- **Primary**: `portfolioSurvivalDelta` — the improvement number for narrative copy
- **Primary**: `coordinatedSurvivalProbability` / `independentSurvivalProbability` — for contrast display values
- **Supporting**: `duplicateTeamsAvoided[]` — for naming what coordination prevented

---

## Moment 3 — Personalization Story

### User Story

As a Circa Survivor player who has seen my coordinated slate and correlation risk, I want to understand that this strategy is built specifically for my entries — not a generic recommendation sent to thousands of subscribers — so that I believe SurvivorPulse's advice is uniquely valuable to my portfolio and not already priced in by the field.

### Functional Requirements

1. A short, explicit contrast statement MUST appear in the UI comparing SurvivorPulse's per-user coordination to the subscriber-dilution model of mass-market tools.
2. The copy MUST NOT name PoolGenius by brand name unless Mike confirms legal clearance. Default: "Unlike tools that send the same recommendation to tens of thousands of subscribers..." or equivalent approved language.
3. The contrast MUST specifically reference the EV-collapse problem: when 50,000 subscribers pick the same team, the edge disappears. The UI copy MUST make this point without requiring the player to know what "EV" means.
4. The personalization statement MUST reference something specific to the player's portfolio — not just generic copy. Acceptable: "Your 5 entries are running a strategy no other subscriber is running" (using entry count from `allocation[]`).
5. This moment MUST appear after Moments 1 and 2 in the page flow — it is a conclusion, not an introduction.
6. The section MUST be brief: 2–4 sentences maximum. It is a punctuation mark, not a feature explanation.
7. The section MUST NOT contain any statistics, probabilities, or math. Plain language only.
8. The entry count used in copy MUST be derived dynamically from `allocation[]` length — not hardcoded.

### Acceptance Criteria

- AC1: A personalization contrast statement is visible below the correlation risk section.
- AC2: The copy references the player's actual entry count (from `allocation[]` length).
- AC3: The copy does not name a competitor brand unless Mike has confirmed clearance.
- AC4: The copy contains no survival probabilities, percentages, or math.
- AC5: The section is 4 sentences or fewer.
- AC6: The section renders correctly with 1 entry and with 10 entries — the copy reads naturally in both cases (singular/plural handling for "entry/entries").

### Edge Cases

- **Single entry**: Copy MUST use singular ("Your 1 entry is running a strategy...") — or use a plural-safe phrasing ("Your entries are...") that reads naturally for both cases.
- **All entries eliminated**: Section MUST still render (season context still makes the personalization story relevant for next season). Do not hide it.
- **`allocation[]` length is 0 or null**: Use a fallback entry count phrase ("your entries") rather than "0 entries" or crashing.
- **API timeout**: Same graceful error state as Moments 1 and 2. The section should show a loading or unavailable state, not a hardcoded copy fallback that may not match the player's actual entry count.

### Component Changes

- **New component**: `PersonalizationStatement` — small text block with dynamic entry count interpolation. Simple stateless component.
- **No existing components need modification** for this moment beyond page layout ordering.

### API Dependencies

- **Primary**: `allocation[]` — length used for entry count in copy only
- No other API fields required for this moment

---

## Cross-Cutting Requirements

### Page Load Order (all three moments)

1. `PortfolioSlate` (Moment 1) renders first, above the fold.
2. `CorrelationRiskPanel` (Moment 2) renders on first scroll.
3. `PersonalizationStatement` (Moment 3) renders after Moment 2.
4. Season replay table (existing) renders last — below all three moments.

### Loading States

- All three moments MUST show skeleton/loading states while the API call is in flight.
- No moment should render with empty/null data as if it were a complete state.

### Error States

- All three moments MUST handle API failure gracefully with a user-visible error message and retry option.
- No moment should crash the page on API failure.

### Accessibility

- All entry cards and metric panels MUST have appropriate ARIA labels for screen readers.
- Color-based indicators (eliminated entry graying, correlation risk coloring) MUST have a non-color fallback (icon or text label).
