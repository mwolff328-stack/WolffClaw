---
name: CMEA Prototype - Strategy Configuration Requirements
description: Requirements for per-entry strategy assignment, configurable entry count, buybacks, and full strategy parameter control
type: project
date: 2026-04-12
---

# CMEA Prototype - Strategy Configuration Requirements

**Author:** Ann (Business Analyst), with product direction from Pam
**Date:** 2026-04-12
**Status:** Ready for build

---

## Feature 1: Configurable Entry Count

### User Story
As a prototype user, I want to specify how many entries (1-10) my simulated pool has, so I can test strategies at different scales.

### Functional Requirements
1. Add an "Entries" control in the ScenarioControls panel, positioned after the season selector.
2. Accept values from 1 to 10 (dropdown or numeric stepper, increment of 1).
3. Default: 5 (matches current behavior).
4. When entry count changes:
   - The simulation re-runs with N virtual entries (Entry 1, Entry 2, ... Entry N).
   - Entries Summary, Entry Cards, and Week Selector all update.
   - Reset week selector to Week 1.
5. The entry count is a frontend-only simulation parameter. It does NOT create/modify DB entries. The simulation creates virtual entry IDs internally.
6. The existing 5 DB entries are only used to bootstrap entry names/IDs for the portfolio API call. For N != 5, generate synthetic entry IDs and names.

### Implementation Notes
- In `assignIndependentPicks`, the entry list is currently derived from the first week's allocation data (5 entries from DB). For N != 5, generate entries: `[{entryId: 'virtual-1', entryName: 'Entry 1'}, ...]`.
- The portfolio API still returns 5 entries, but we only use the allocation data for team candidates (win prob, spread, etc.), not for entry-specific assignments. Entry assignments are computed client-side.

---

## Feature 2: Per-Entry Strategy Assignment

### User Story
As a prototype user, I want to assign a different pick strategy to each entry, OR use the same strategy for all entries, so I can compare how different approaches perform side-by-side in the same pool.

### Functional Requirements
1. Add a strategy assignment mode toggle: "Same for All" (default) vs "Per Entry".
2. **Same for All mode**: One strategy config applies to all entries. This is the current behavior extended with the strategy selector (Feature 4).
3. **Per Entry mode**: Each entry gets its own strategy config. Display a strategy selector for each entry.
4. In the Entry Cards (PortfolioSlate), when Per Entry mode is active, show which strategy each entry is using (e.g., a small label like "70/30 Blend" or "Pure WP").
5. The simulation must support mixed strategies: Entry 1 might use Pure WP while Entry 2 uses 70/30 Blend. The greedy assignment still applies (entries assigned in alphabetical order), but each entry scores teams differently.
6. In Same for All mode, changing the strategy re-runs simulation for all entries.
7. In Per Entry mode, changing one entry's strategy re-runs the entire simulation (because entry assignments are interdependent via the greedy algorithm).

### Implementation Notes
- The `assignIndependentPicks` function currently takes global `wpWeight` and `psWeight`. Refactor to accept a per-entry strategy config array: `strategyByEntry: StrategyConfig[]`.
- `StrategyConfig` type:
  ```typescript
  interface StrategyConfig {
    strategyType: StrategyType  // which strategy template
    wpWeight: number            // 0-100
    psWeight: number            // 0-100
    fvWeight: number            // 0-100 (future value / expendability)
    lookahead: number           // 0-10 weeks
    decayType: 'linear' | 'exponential'
    penaltyFactor: number       // 0-1
    minWinProb: number          // 0-1 (floor)
    evMode: boolean             // use SP EV formula instead of blend
    useLeverage: boolean        // include leverage vs chalk
    leverageWeight: number      // 0-100
  }
  ```
- Default config matches current 70/30 Blend: `{wpWeight: 70, psWeight: 30, fvWeight: 0, ...}`

---

## Feature 3: Buyback Toggle

### User Story
As a prototype user, I want to toggle buybacks on/off for all entries, so I can see how re-entering after elimination affects survival outcomes.

### Functional Requirements
1. Add a "Buybacks" toggle (on/off) in the ScenarioControls panel.
2. Default: Off (matches current behavior).
3. When buybacks are ON:
   - An eliminated entry is automatically revived the week after elimination.
   - The revived entry keeps its used-teams history (cannot reuse teams it already picked).
   - The revived entry is treated as alive starting the following week.
   - Each entry gets at most 1 buyback (matches common pool rules).
   - Entries that have already used their buyback and get eliminated again are permanently eliminated.
4. The Entries Summary and Entry Cards should indicate buyback status:
   - "Alive" / "Eliminated (W3)" / "Bought Back (W4)" / "Eliminated (final, W7)"
5. The Week Selector elimination dots should account for buybacks (an entry might be eliminated, bought back, then eliminated again).
6. When buybacks toggle changes, re-run simulation.

### Implementation Notes
- In `assignIndependentPicks`, after processing eliminations for a week, check if buybacks are enabled. If an entry was just eliminated and hasn't used its buyback yet, mark it for revival next week.
- Add `buybackUsed: boolean` and `buybackWeek: number | null` to the entry tracking state.
- The `IndependentPick` type needs `isBoughtBack: boolean` and `buybackWeek: number | null` fields.

---

## Feature 4: Strategy Templates with Full Parameter Control

### User Story
As a prototype user, I want to select from predefined strategy templates (matching Stan's backtested approaches) AND customize all parameters, so I can explore the full strategy space.

### Functional Requirements
1. Strategy selector offers these templates (matching Stan's research):
   - **Pure Win Probability**: wpWeight=100, psWeight=0, all others off
   - **Weighted Blend (70/30)**: wpWeight=70, psWeight=30 (default)
   - **Weighted Blend (80/20)**: wpWeight=80, psWeight=20
   - **SurvivorPulse EV**: evMode=true (score = winProb - pickShare)
   - **Leverage + Floor**: wpWeight=0, psWeight=0, leverage scoring with minWinProb floor
   - **Expendable-First**: wpWeight + psWeight + fvWeight = 100, with lookahead config
   - **SP Production**: evMode-based with futureValue weight
   - **Custom**: all parameters manually editable

2. When a template is selected, its parameters populate the controls. User can then modify any parameter (which switches to "Custom" label).

3. Parameter controls (all user-editable):
   - **Win Probability Weight**: 0-100, step 5
   - **Pick Share Weight**: 0-100, step 5
   - **Future Value Weight**: 0-100, step 5
   - **Constraint**: wpWeight + psWeight + fvWeight must sum to 100 (when not in evMode)
   - **Lookahead Window**: 0-10 weeks (0 = disabled)
   - **Decay Type**: Linear / Exponential (only when lookahead > 0)
   - **Min Win Probability Floor**: 0-100% (filter out teams below this threshold)
   - **EV Mode toggle**: When on, uses SP EV formula (winProb - pickShare) as base score
   - **Leverage toggle**: When on, adds leverage vs chalk component
   - **Leverage Weight**: 0-50 (only when leverage enabled)

4. The parameter panel should be collapsible (expanded = show all params, collapsed = show just the template name and key weights).

5. For "Same for All" mode, one parameter panel. For "Per Entry" mode, a compact parameter panel per entry (showing template name + key override values, expandable for full control).

### Design Notes (Deb)
- Strategy template selector: dropdown or pill buttons showing template names
- Parameter controls: use the existing slider style from the weight controls, extended
- Per-entry panels: compact cards, each with a template badge + expandable detail
- Use label-structural for parameter labels, data-cell for values
- When constraints are violated (weights don't sum to 100), show a warning with --sp-warning colors

---

## Page Layout (updated)

1. **ScenarioControls** (expanded):
   - Row 1: Season selector (2023 | 2024 | 2025) + Entry Count (1-10)
   - Row 2: Strategy Mode (Same for All | Per Entry) + Buybacks (On/Off)
   - Row 3: Strategy template selector + weight summary
   - Row 4 (expandable): Full parameter controls
2. Data Status Bar
3. Pool Information Panel
4. Entries Summary
5. Week Selector
6. Entry Picks (with strategy labels per entry in Per Entry mode)
7. Available Teams Table

---

## State Management

The strategy configuration state is complex. Recommend creating a new context or reducer:

```typescript
interface SimulationConfig {
  season: number
  entryCount: number
  buybacksEnabled: boolean
  strategyMode: 'same' | 'perEntry'
  // For 'same' mode: single config
  globalStrategy: StrategyConfig
  // For 'perEntry' mode: one config per entry
  entryStrategies: StrategyConfig[]
}
```

This should live in SeasonReplayView state or a dedicated SimulationContext. All downstream components receive their config as props.
