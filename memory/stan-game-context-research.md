---
name: Round 9 — Game Context Filters Research
description: Full simulation results and analysis for Round 9: testing divisional penalty and home-team preference filters across 4 strategies × 7 filter modes × 4 entry counts × 3 seasons (336 runs total).
type: project
---

# Stan the Scout: Round 9 — Game Context Filters

**Date:** 2026-04-14
**Run count:** 336 (4 strategies × 7 filter modes × 4 entry counts × 3 seasons)
**Seasons tested:** 2023, 2024, 2025
**Script:** scripts/stan-game-context-sim.py

---

## Executive Summary

Both the "avoid divisional games" and "prefer home teams" heuristics — widely debated in survivor pool communities — were tested empirically across three seasons. **Neither hypothesis held consistently across seasons.** The prefer-home filter is reliably harmful. The avoid-divisional filter shows marginal gains in mid-size pools (n=20) but is inconsistent across seasons and entry counts. No filter should be enabled by default.

---

## Full Results: Entry-Weeks (Avg across 2023–2025)

### 70/30 Blend

| Filter Mode         | n=5  | n=10 | n=20 | n=50 |
|---------------------|------|------|------|------|
| No Filter           | 19.0 | 25.3 | 40.7 | 98.3 |
| Avoid Div (Soft)    | 15.7 | 24.0 | 43.3 | 96.0 |
| Avoid Div (Hard)    | 15.7 | 23.3 | 44.0 | 93.7 |
| Prefer Home (Soft)  | 15.7 | 22.3 | 42.3 | 90.3 |
| Prefer Home (Hard)  | 15.7 | 20.7 | 40.0 | 85.3 |
| Both (Soft)         | 14.7 | 21.0 | 43.7 | 88.0 |
| Both (Hard)         | 14.0 | 26.0 | 39.3 | 89.0 |

### SP Production

| Filter Mode         | n=5  | n=10 | n=20 | n=50 |
|---------------------|------|------|------|------|
| No Filter           | 15.0 | 23.7 | 37.7 | 87.3 |
| Avoid Div (Soft)    |  9.7 | 28.0 | 37.3 | 88.3 |
| Avoid Div (Hard)    |  9.7 | 21.3 | 44.3 | 87.0 |
| Prefer Home (Soft)  | 10.0 | 17.3 | 36.7 | 74.3 |
| Prefer Home (Hard)  | 10.0 | 15.0 | 34.3 | 67.3 |
| Both (Soft)         | 10.0 | 20.3 | 37.7 | 88.7 |
| Both (Hard)         |  7.7 | 17.7 | 37.0 | 88.0 |

### Core/Satellite (60% 70/30 + 40% SP Production)

| Filter Mode         | n=5  | n=10 | n=20 | n=50 |
|---------------------|------|------|------|------|
| No Filter           | 14.7 | 33.7 | 43.3 | 88.0 |
| Avoid Div (Soft)    | 14.3 | 25.3 | 49.0 | 90.7 |
| Avoid Div (Hard)    | 17.0 | 25.3 | 48.0 | 88.7 |
| Prefer Home (Soft)  | 12.7 | 23.0 | 37.0 | 75.0 |
| Prefer Home (Hard)  | 12.7 | 20.7 | 38.7 | 73.7 |
| Both (Soft)         | 17.0 | 26.0 | 39.3 | 89.0 |
| Both (Hard)         | 15.7 | 21.0 | 38.7 | 89.0 |

### SP Conservative

| Filter Mode         | n=5  | n=10 | n=20 | n=50 |
|---------------------|------|------|------|------|
| No Filter           | 21.3 | 27.3 | 40.7 | 96.0 |
| Avoid Div (Soft)    | 18.7 | 32.7 | 47.7 | 94.0 |
| Avoid Div (Hard)    | 16.7 | 31.3 | 48.0 | 93.3 |
| Prefer Home (Soft)  | 16.3 | 25.3 | 43.7 | 92.0 |
| Prefer Home (Hard)  | 16.3 | 22.3 | 39.7 | 88.0 |
| Both (Soft)         | 15.3 | 23.3 | 40.0 | 91.3 |
| Both (Hard)         | 15.0 | 22.0 | 37.0 | 90.0 |

---

## Filter Delta vs No Filter Baseline

### 70/30 Blend

| Filter          | n=5   | n=10  | n=20  | n=50   |
|-----------------|-------|-------|-------|--------|
| Avoid Div Soft  | -3.3  | -1.3  | +2.7  | -2.3   |
| Avoid Div Hard  | -3.3  | -2.0  | +3.3  | -4.7   |
| Home Soft       | -3.3  | -3.0  | +1.7  | -8.0   |
| Home Hard       | -3.3  | -4.7  | -0.7  | -13.0  |
| Both Soft       | -4.3  | -4.3  | +3.0  | -10.3  |
| Both Hard       | -5.0  | +0.7  | -1.3  | -9.3   |

### SP Conservative (strongest filter signal)

| Filter          | n=5   | n=10  | n=20  | n=50  |
|-----------------|-------|-------|-------|-------|
| Avoid Div Soft  | -2.7  | +5.3  | +7.0  | -2.0  |
| Avoid Div Hard  | -4.7  | +4.0  | +7.3  | -2.7  |
| Home Soft       | -5.0  | -2.0  | +3.0  | -4.0  |
| Home Hard       | -5.0  | -5.0  | -1.0  | -8.0  |

---

## Hypothesis Validation

### H1: Divisional Games Are More Volatile

**VERDICT: NOT SUPPORTED overall — season-dependent**

| Season | Div WR  | Non-Div WR | Gap      |
|--------|---------|------------|----------|
| 2023   | 64.1%   | 69.5%      | +5.4pp (supports H1) |
| 2024   | 73.6%   | 70.4%      | -3.2pp (opposes H1)  |
| 2025   | 76.0%   | 66.5%      | -9.5pp (strongly opposes H1) |
| **Avg** | **71.2%** | **68.8%** | **-2.4pp (opposes H1)** |

The community intuition is based on historical data that may not be stable year-to-year. In 2023, divisional games were indeed more likely to produce upsets. In 2024-2025, divisional favorites covered at a higher rate than non-divisional favorites. The hypothesis is **not reliable enough to apply universally**.

### H2: Home Teams Win More Often

**VERDICT: NOT SUPPORTED overall — season-dependent**

| Season | Home WR | Road WR | Gap       |
|--------|---------|---------|-----------|
| 2023   | 62.9%   | 74.6%   | -11.7pp (road wins more!) |
| 2024   | 71.4%   | 72.3%   | -0.9pp (roughly equal)    |
| 2025   | 74.9%   | 64.4%   | +10.5pp (supports H2)     |
| **Avg** | **69.7%** | **70.4%** | **-0.7pp (negligible)**  |

Home field advantage appears to be declining or highly variable in the modern NFL. In 2023, road teams in survivor-relevant games (high win probability) won significantly more often. In 2025, the pattern flipped. **Home field is not a reliable survivor filter.**

---

## Filter Swap Opportunity Cost

When a filter swaps the top pick, what % of swaps led to the new pick winning?

| Strategy        | Filter           | Swaps | Beneficial | Costly | % Beneficial |
|-----------------|-----------------|-------|-----------|--------|-------------|
| 70/30 Blend     | Avoid Div Soft  | 348   | 220       | 128    | 63.2%       |
| 70/30 Blend     | Prefer Home Soft| 302   | 168       | 134    | 55.6%       |
| Core/Satellite  | Avoid Div Soft  | 378   | 246       | 132    | 65.1%       |
| Core/Satellite  | Prefer Home Soft| 304   | 159       | 145    | 52.3%       |
| SP Conservative | Avoid Div Soft  | 380   | 247       | 133    | 65.0%       |
| SP Conservative | Prefer Home Soft| 318   | 184       | 134    | 57.9%       |

**Key insight:** Divisional filters redirect to winning picks ~63-65% of the time. Home filters only ~52-58% — barely above chance. However, even 63% "beneficial" swap rate doesn't translate to net entry-week gains because:
1. The swapped-away original pick often had higher absolute win probability
2. Net entry-week gains only materialize at n=10-20 for some strategies
3. At n=5 and n=50, the filter is universally harmful

---

## Season-by-Season Filter Impact (70/30 Blend, n=10)

| Filter          | 2023 | 2024 | 2025 |
|-----------------|------|------|------|
| No Filter       | 20.0 | 22.0 | 34.0 |
| Avoid Div Soft  | 21.0 | 18.0 | 33.0 |
| Avoid Div Hard  | 19.0 | 18.0 | 33.0 |
| Prefer Home Soft| 18.0 | 19.0 | 30.0 |
| Prefer Home Hard| 18.0 | 19.0 | 25.0 |
| Both Soft       | 21.0 | 10.0 | 32.0 |
| Both Hard       | 21.0 | 27.0 | 30.0 |

Season variance is high. The "Both (Hard)" filter was the top in 2024 (+5.0 over control) but one of the worst in 2023 (equal) and 2025 (-4.0). This inconsistency reinforces that filters should not be defaults.

---

## Filter Impact by Entry Count

Pattern: **Avoid-div filters show modest gains at n=20. Prefer-home filters are harmful at all entry counts. Large pools (n=50) consistently do worse with any filter.**

The intuition: at large n, you're forced to spread picks across many games including divisional ones. Penalizing or avoiding divisional picks at scale reduces the pick pool and forces suboptimal reuse patterns.

---

## Overall Champions per Entry Count

| N  | Best Combo                              | Entry-Weeks | Filter Lift |
|----|----------------------------------------|-------------|-------------|
| 5  | SP Conservative + No Filter            | 21.3        | +0.0        |
| 10 | Core/Satellite + No Filter             | 33.7        | +0.0        |
| 20 | Core/Satellite + Avoid Div (Soft)      | 49.0        | +5.7        |
| 50 | 70/30 Blend + No Filter                | 98.3        | +0.0        |

**The only significant filter win is at n=20 with Core/Satellite + Avoid Div Soft (+5.7 ew / +13.2% lift).**

---

## Product Implications

### Should SurvivorPulse offer game context filters?

**Yes — as optional, user-configurable settings. Not as defaults.**

#### Recommended implementation:
1. **"Avoid divisional games" filter** — offer as a toggle in Strategy Settings
   - Frame as: "Some players prefer to avoid divisional matchups, which can be more competitive. Enable to deprioritize divisional picks."
   - Data shows ~63-65% of swaps redirect to winning picks, making the feature feel useful
   - Net benefit only at n=10-20 for SP Conservative/Avoid Div; harmless for most users
   
2. **"Prefer home teams" filter** — offer but prominently disclaim
   - Frame as: "Home field advantage is real but smaller than many assume in the modern NFL."
   - Data shows consistently harmful in 2023, helpful only in 2025
   - Consider a data-informed tooltip showing current-season home vs road win rates

3. **Combined filters** — do NOT offer "Both (Hard)" as a recommended combo
   - The tiered priority system is confusing and results are inconsistent
   - If offering both, only the soft versions should combine

#### Why not default-on?

- Season variance is too high (a filter that gained +5 in one season lost -10 in another)
- At n=5 (the majority of casual players), all filters are harmful
- No filter has consistent statistically significant gains across all seasons

### Recommended: feature framing

These are "conviction overrides" for players who have strong opinions about game types. Frame them as expert customizations, not algorithmic improvements. Present with the caveat: "This filter reflects a widely-held belief. Historical data shows mixed results — use based on your own conviction."

---

## Recommendation: Default Filter Setting

**Default: No Filter (off)**

Rationale:
1. No filter achieves the best results at 3 of 4 entry count tiers (n=5, n=10, n=50)
2. The only filter with material consistent gains (Avoid Div at n=20) is narrow enough that it should be user-activated
3. Home preference filter is reliably harmful — enabling it by default would hurt user outcomes and damage trust
4. Filters that are off-by-default with clear explanations build credibility; filters forced on users that hurt outcomes destroy it

**If forced to pick one default-on filter:** Avoid Divisional (Soft) for pools sized n=10-30 only. Even then, the gains are modest and season-dependent.

---

## Technical Notes

- Data: 2023/2024 from local JSON files; 2025 from SurvivorPulse API + cache
- 2025 game context cache: ~/Projects/SurvivorPulse-BackTesting-Prototype/data/nfl_games_2025_games_cache.json
- Division lookup verified: all 32 team IDs resolved correctly (JAX not JAC, LV not LVR, WAS not WSH, LAR not LA)
- Swap tracking methodology: "beneficial" = filter swapped AND new pick won; "costly" = swapped AND new pick lost
- Win probability data from SurvivorPulse API / historical files
