---
name: Stan's Backtesting Research - Pick Strategy Analysis
description: Comprehensive backtesting research across 2023-2025 NFL seasons testing multiple survivor pool pick strategies
type: research
date: 2026-04-11
channel: backtesting-research (Discord channel 1492758599393349673)
---

# Stan's Backtesting Research: NFL Survivor Pool Pick Strategies

## Overview

Multi-season backtesting of survivor pool pick strategies across 2023, 2024, and 2025 NFL seasons. 5-entry pool, 18-week regular season, once-per-season team reuse. Goal: find the pick strategy that maximizes entry-weeks survived.

## Data Sources

### Game Data
- **2023 & 2024**: nfl_data_py Python package (free). Provides game results, scores, point spreads, moneylines.
- **2025**: SurvivorPulse API (live). Games endpoint with win probabilities from the Odds API.
- **Win probabilities** for 2023/2024 derived from spreads using normal CDF: `P = 0.5 * (1 + erf(spread / (13.5 * sqrt(2))))`
- **IMPORTANT**: nfl_data_py spread_line convention: positive = home team FAVORED (opposite of some other sources)

### Pick Popularity
- **2023 & 2024**: SurvivorGrid.com (scraped). Per-team pick percentages from Yahoo, ESPN, OfficeFootballPool. Weighted average used.
- **2025**: SurvivorPulse dynamics API (Yahoo pick data from DB)

### Data Files
- `~/Projects/CMEA-Prototype/data/nfl_games_2023.json` (272 games)
- `~/Projects/CMEA-Prototype/data/nfl_games_2024.json` (272 games)
- `~/Projects/CMEA-Prototype/data/survivorgrid_picks_2023.json` (18 weeks, 576 team records)
- `~/Projects/CMEA-Prototype/data/survivorgrid_picks_2024.json` (18 weeks, 576 team records)

### Data also loaded into SurvivorPulse Production DB
- Production DB: ep-orange-bush-afg0m2nx (Neon)
- Pool IDs: 2023=`a1b2c3d4-2023-4000-8000-000000000023`, 2024=`a1b2c3d4-2024-4000-8000-000000000024`, 2025=`04e2471b-6498-4a59-8a95-c0dc50221457`
- Pick popularity source field: 'survivorgrid' for 2023/2024, 'yahoo'/'csv' for 2025
- Import script: `~/.openclaw/workspace/scripts/import-historical-seasons.py`

---

## Round 1: Initial 4 Strategies (2025 only)

**Script**: `scripts/stan-pick-strategy-sim.py`

| Strategy | Last Elim | Entry-Weeks | Avg WP | Avg Own |
|---|---|---|---|---|
| Pure Win Probability | Week 10 | 22 | 77.7% | 19.0% |
| Survival Equity | Week 9 | 19 | 75.2% | 11.6% |
| Leverage Score (WP/Ownership) | Week 2 | 1 | - | - |
| Future Value Preservation | Week 2 | 1 | - | - |

**Finding**: Raw leverage/future value without safety floors = catastrophic failure. Picks unsafe teams with near-zero ownership.

---

## Round 2: 7 Constrained Strategies (2025 only)

**Script**: `scripts/stan-pick-strategy-sim-v2.py`

| Strategy | Last Elim | Entry-Weeks | Avg WP | Avg Own |
|---|---|---|---|---|
| **Weighted Blend (70/30)** | **Week 14** | **26** | **75.2%** | **11.6%** |
| Pure Win Probability | Week 10 | 22 | 77.7% | 19.0% |
| Weighted Blend (80/20) | Week 10 | 22 | 77.4% | 16.0% |
| Leverage + 60% Floor | Week 5 | 11 | 63.3% | 3.0% |
| Anti-Chalk Top-5 | Week 5 | 11 | 66.3% | 3.4% |
| Leverage + 55% Floor | Week 3 | 4 | 58.7% | 0.8% |
| Tiered Top-10 | Week 3 | 5 | 58.0% | 0.5% |

**Finding**: 70/30 Weighted Blend (`score = 0.7 * winProb + 0.3 * (1 - pickShare/100)`) survived 4 weeks longer than pure win probability. Sweet spot: pick safe teams but prefer ones fewer people are on.

---

## Round 3: Multi-Season (2023, 2024, 2025)

**Script**: `scripts/stan-multi-season-sim.py`

| Strategy | 2023 | 2024 | 2025 | TOTAL | Avg/Season | SD |
|---|---|---|---|---|---|---|
| **Weighted Blend (70/30)** | **17** | **14** | **26** | **57** | **19.0** | **5.1** |
| Weighted Blend (80/20) | 17 | 4 | 22 | 43 | 14.3 | 8.8 |
| Pure Win Probability | 13 | 3 | 22 | 38 | 12.7 | 7.8 |
| Leverage + 60% Floor | 5 | 16 | 11 | 32 | 10.7 | 4.5 |
| Tiered Top-10 | 13 | 9 | 5 | 27 | 9.0 | 3.3 |
| Anti-Chalk Top-5 | 4 | 5 | 11 | 20 | 6.7 | 3.1 |
| Leverage + 55% Floor | 6 | 6 | 4 | 16 | 5.3 | 0.9 |

**Finding**: 70/30 Blend confirmed as best overall. 50% more entry-weeks than pure win prob across 3 seasons. Most consistent (SD=5.1). Pure win prob collapsed in 2024 (only 3 entry-weeks).

---

## Round 4: Future Value Lookahead (2023, 2024, 2025)

**Script**: `scripts/stan-future-value-sim.py`

Tested 8 lookahead variants (3-week and 5-week windows, linear and exponential decay, various penalty factors) against the 70/30 Blend baseline.

| Strategy | 2023 | 2024 | 2025 | TOTAL | SD |
|---|---|---|---|---|---|
| **70/30 Blend** | **17** | **14** | **26** | **57** | **5.1** |
| Lookahead-5 Exp (0.15) | 18 | 12 | 19 | 49 | 3.1 |
| Lookahead-3 Linear (0.10) | 18 | 12 | 15 | 45 | 2.4 |
| Lookahead-5 Exp (0.10) | 10 | 14 | 19 | 43 | 3.7 |
| Lookahead-3 Aggressive (0.20) | 12 | 12 | 19 | 43 | 3.3 |
| Pure Win Probability | 13 | 3 | 22 | 38 | 7.8 |

**Finding**: Lookahead strategies are MORE CONSISTENT (lower SD) but don't beat 70/30 total. Lookahead costs you in favorable seasons (2025). The penalty for saving teams outweighs the benefit when there are plenty of good options.

---

## Round 5: Expendable-First + SurvivorPulse EV (2023, 2024, 2025)

**Script**: `scripts/stan-expendable-first-sim.py`

Tested the actual SurvivorPulse EV formula (`evPick = winProb - pickShare`), the production scoring weights, and an "expendable-first" approach (reward low-future-value teams instead of penalizing high ones).

| Strategy | 2023 | 2024 | 2025 | TOTAL | SD |
|---|---|---|---|---|---|
| **70/30 Blend** | **17** | **14** | **26** | **57** | **5.1** |
| Pure Win Probability | 13 | 3 | 35 | 51 | 13.4 |
| Expendable 65/25/10 3wk | 7 | 12 | 32 | 51 | 10.8 |
| SP Prod: 70% EV + 30% FV | 13 | **23** | 9 | 45 | 5.9 |
| SP Conservative: 65/25/10 | 10 | **21** | 9 | 40 | 5.4 |
| SP Balanced: 55/25/20 | 10 | 18 | 9 | 37 | 4.0 |
| SP EV (winProb - pickShare) | 6 | 5 | 18 | 29 | 5.9 |

**Findings**:
1. SurvivorPulse EV alone is too aggressive (29 total, worst). Overweights contrarian without safety.
2. SP production formula (70% EV + 30% FV) dominated 2024 (23) but collapsed in 2025 (9). Inconsistent.
3. Expendable-first 65/25/10 crushed 2025 (32) but underperformed 2023 (7).
4. 70/30 Blend wins because it never has a terrible season. Consistency > ceiling.

---

## SurvivorPulse Production Scoring Reference

From `shared/scoring/score100.ts` and `shared/survivorMath.ts`:

- **EV Pick**: `evPick = pW - qW` (win probability minus pick share)
- **Weekly Score**: normalized EV across eligible teams
- **Core Score (Regular Season)**: `0.70 * weeklyScore + 0.30 * futureUtility`
- **Composite Score**: `0.80 * coreScore + 0.20 * poolDynamicsScore`
- **Overall Score**: `0.60 * compositeScore + 0.40 * safetyScore`
- **Leverage Profiles**: Conservative (65/25/10), Balanced (55/25/20)
- **Leverage vs Chalk**: `p_team * (1 - p_chalk) * q_chalk`
- **Expected Equity**: `p_team / expectedSurvivors`
- **Fair Share**: `winProbability / totalWinProb`
- **Future Value**: graded A-F with scarcity count, futureUtility from best future week with decay

---

## Why Future Value Doesn't Dominate in Our Backtesting

1. **Small entry count** (5 entries). Team scarcity barely bites with 32 teams and 5 picks/week. With 10+ entries, future value would matter more.
2. **Hindsight data**. We know all outcomes. Real players face uncertainty, making optionality preservation more valuable.
3. **Only 3 seasons**. Small sample. SP production formula won 2024 convincingly.
4. **Rare catastrophic scarcity**. The scenario where you run out of good teams is devastating but infrequent in 3 years of data.

---

## Key Insight for Product

The 70/30 Blend's simplicity is its strength. No magic formula dominates every season. The real product value is giving users the ability to adjust weights based on their own risk tolerance and pool dynamics. The backtesting feature proves that pick popularity awareness consistently outperforms pure win probability.

---

## Content Asset Potential

This research can be repurposed as:
- White paper: "Does Contrarian Picking Actually Work? A 3-Season NFL Survivor Pool Analysis"
- Blog series on pick strategy optimization
- Product marketing: "Our algorithm survived 50% longer than picking favorites"
- Help content explaining the weight sliders in the prototype
- Credibility asset for TAM education

---

## Simulation Scripts

All in `~/.openclaw/workspace/scripts/`:
- `stan-pick-strategy-sim.py` - Round 1 (4 strategies, 2025 only)
- `stan-pick-strategy-sim-v2.py` - Round 2 (7 constrained, 2025 only)
- `stan-multi-season-sim.py` - Round 3 (7 strategies, 3 seasons)
- `stan-future-value-sim.py` - Round 4 (10 lookahead strategies, 3 seasons)
- `stan-expendable-first-sim.py` - Round 5 (10 EV + expendable strategies, 3 seasons)
- `stan-scrape-survivorgrid-v2.py` - SurvivorGrid scraper
- `import-historical-seasons.py` - DB import script

## Round 6: Entry-Count Scaling (2026-04-11)

**Script**: `scripts/stan-entry-scale-sim.py`
**Full analysis**: `memory/stan-entry-scale-research.md`
**Results JSON**: `scripts/stan-entry-scale-results.json`

14 strategies x 4 entry counts (5, 10, 20, 50) x 3 seasons = 168 runs.

**Winners per entry count:**
- n=5: 70/30 Blend (57, tied with Adaptive/Mixed at 58 but best SD)
- n=10: SP Production 70%EV+30%FV (94, +18 vs 70/30)
- n=20: Mixed Portfolio (142, +20 vs 70/30)
- n=50: 70/30 Blend reclaims #1 (295)

**CMEA thesis**: Partially confirmed. Coordination/diversification strategies win at n=10-20 (the ICP sweet spot) but collapse at n=50 due to team exhaustion.

**Product recommendation**: Portfolio-size-aware strategy defaults. 1-5 entries → 70/30; 6-15 → SP Production; 16-30 → Mixed Portfolio; 31+ → 70/30.

## Round 7: Per-Entry Differentiated Scoring (2026-04-11)

**Script**: `scripts/stan-differentiated-scoring-sim.py`
**Full analysis**: `memory/stan-differentiated-scoring-research.md`
**Results JSON**: `scripts/stan-differentiated-scoring-results.json`

12 strategies x 4 entry counts (5, 10, 20, 50) x 3 seasons = 144 runs.

**Winners per entry count:**
- n=5: Mixed Portfolio (62, +5 vs 70/30)
- n=10: Core/Satellite [60%blend+40%EV] (101, +25 vs 70/30, +17 vs Mixed Portfolio) ★
- n=20: Mixed Portfolio tied with Temporal Diversification (134, +12 vs 70/30)
- n=50: 70/30 Blend / Anti-Overlap tied #1 (295); Mixed Portfolio collapses to 259 (-36)

**Key answer**: Intentional role assignment beats random strategy diversity (Mixed Portfolio) at n=10 (+17) and n=50 (8 configs beat Mixed). Does NOT beat it at n=5 or n=20. At the ICP sweet spot (n=10), Core/Satellite is the dominant design.

**Product recommendation updated**: 1-5 → Mixed Portfolio; 6-15 → Core/Satellite; 16-30 → Mixed Portfolio or Temporal Div; 31-50 → Role-Based or Safety/Contrarian; 50+ → 70/30 Blend.

## Round 8: Buyback Mechanics (2026-04-12)

**Script**: `scripts/stan-buyback-sim.py`
**Full analysis**: `memory/stan-buyback-research.md`

12 strategies × 4 entry counts × 3 seasons × 3 buyback configs (no buyback / Wk1-3 / Wk1-4) = 432 Part 1 runs. Plus 5 split strategies × 4 × 3 = 60 Part 2 runs. 492 total.

**Biggest finding:** Pool mechanics completely change the optimal strategy. SP Conservative 65/25/10 wins at ALL entry counts once buybacks are available — and loses at all entry counts without them.

**Winners per entry count WITH Buyback Wk1-3:**
- n=5: SP Conservative 65/25/10 (78, +14 vs no-buyback)
- n=10: SP Conservative 65/25/10 (165, +83 — doubles from 82 baseline!)
- n=20: SP Conservative 65/25/10 (248, +126)
- n=50: SP Conservative 65/25/10 (463, +175)

**Average buyback uplift (all strategies):** +13.2 (n=5) → +46.1 (n=10) → +93.1 (n=20) → +159.9 (n=50)

**Split strategies (aggressive early, safe late):** None beat the simple SP Conservative baseline. All underperform. The 3-week window is too short for strategy switching to pay off.

**Buyback ROI:** 1.07–4.15 entry-weeks per buyback used. n=10 SP Conservative: 4.15 EW/BB — best ROI across all runs. The only negative ROI: Adaptive Blend at n=5 (−0.12).

**Survival rates:** 20–40% of bought-back entries survive 3+ more weeks; 0–30% to week 10+.

**Product recommendation updated**: The app MUST distinguish buyback vs non-buyback pool type.
- Non-buyback pools: Core/Satellite (n≤20), 70/30 Blend (n=50)
- Buyback pools: SP Conservative at ALL entry counts
- Wider buyback window = stronger case for SP Conservative
- Always recommend exercising the buyback (positive ROI across the board)

## Round 9: Game Context Filters (2026-04-14)

**Script**: `scripts/stan-game-context-sim.py`
**Full analysis**: `memory/stan-game-context-research.md`

4 strategies × 7 filter modes × 4 entry counts × 3 seasons = 336 runs.

**Filter modes tested:**
1. No Filter (control)
2. Avoid Divisional (Soft — 10% score penalty)
3. Avoid Divisional (Hard — swap if non-div alt within 15%)
4. Prefer Home (Soft — 10% score bonus)
5. Prefer Home (Hard — swap if home alt within 15%)
6. Both Filters (Soft)
7. Both Filters (Hard — tiered priority)

**Hypothesis validation results:**

- **H1 (Divisional games more volatile):** NOT SUPPORTED overall. Divisional picks won at 71.2% vs non-div 68.8%. Huge season variance: div WR was 64.1% in 2023 (supports H1), 73.6% in 2024, 76.0% in 2025 (both oppose H1).
- **H2 (Home teams win more):** NOT SUPPORTED overall. Home 69.7% vs road 70.4%. 2023: road teams won WAY more (road 74.6% vs home 62.9%). 2025: home won (74.9% vs 64.4%). No reliable pattern.

**Overall champions per entry count:**
- n=5: SP Conservative + No Filter (21.3 ew) — filters hurt small pools
- n=10: Core/Satellite + No Filter (33.7 ew) — No Filter still wins
- n=20: Core/Satellite + Avoid Div Soft (49.0 ew, +5.7 / +13.2% lift) — ONLY case where filter helps
- n=50: 70/30 Blend + No Filter (98.3 ew) — filters harmful at scale

**Best filter for SP Conservative at n=20:** Avoid Div Soft +7.0, Avoid Div Hard +7.3. Largest gains of any combo.

**Filter swap opportunity cost:**
- Divisional filters: 61–65% of swaps lead to winning new pick
- Home filters: only 52–58% — barely above random chance
- Even 63% "beneficial" swaps don't always translate to net entry-week gains

**Product recommendation:** Offer both filters as OPTIONAL user toggles (not defaults). Home filter especially should be disclaimed — historically hurt outcomes. Avoid-div filter is defensible as optional for mid-size pools (n=10-30).

**Updated strategy defaults:**
- Non-buyback, n=5: SP Conservative + No Filter
- Non-buyback, n=10: Core/Satellite + No Filter
- Non-buyback, n=20: Core/Satellite + Avoid Div Soft (or No Filter for simplicity)
- Non-buyback, n=50: 70/30 Blend + No Filter
- Buyback pools: SP Conservative + No Filter at all entry counts (unchanged from Round 8)

## Round 10: Weather Impact Simulation (2026-04-14)

**Script**: `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/scripts/stan-weather-sim.py`
**Full analysis**: `memory/stan-weather-research.md`
**Results JSON**: `scripts/stan-weather-sim-results.json`

4 strategies × 7 filter modes × 4 entry counts × 6 seasons = 672 runs. Data: 1,615 games (2020-2025) enriched with weather classification from nfl_data_py roof/temp/wind fields.

**Hypothesis test results:**

- **Dome vs outdoor gap:** 1.7pp (32.1% dome vs 33.7% outdoor upset rate). NOT significant (p=0.511, z=0.658). REJECTED.
- **Year-over-year consistency:** Dome gap ranges from -5.3pp (2020) to +16.4pp (2022). Flips sign in 4 of 6 seasons. NO signal stability.
- **Extreme weather:** Only 4-15 games/season qualify. Upset rates range from 9.1% (2024) to 75.0% (2023). Pure noise. Sample too small.
- **Adverse/extreme weather filters:** INERT. All 4 adverse/extreme filter modes produced identical results to No Filter in every single run. Top picks never land in adverse weather — base scoring implicitly avoids them already. 0% of top picks were weather_extreme; 3.8% were weather_adverse.
- **Dome preference (Soft):** Has positive aggregate total (+291 delta) but a LOSING head-to-head record (33 wins, 47 losses, 41.3%). Wins big in 2020 and 2022 where dome teams outperformed; destroys value in 2021 and 2024. Not a reliable filter.

**Overall simulation champions (Total EW across 6 seasons):**
- n=5: SP Conservative + Prefer Dome (Soft) (160 EW) — driven by 2020/2022 dome outperformance
- n=10: SP Conservative + Prefer Dome (Soft) (320 EW)
- n=20: SP Conservative + Prefer Dome (Soft) (640 EW)
- n=50: SP Conservative + Prefer Dome (Soft) (1,600 EW)

**Caveat:** These results are dominated by 2 seasons (2020, 2022) where dome preference happened to align with actual outcomes. In 2024, the 70/30 Blend at n=10 collapsed from 110 EW (No Filter) to 10 EW (Dome Soft) — a 91% loss.

**Product recommendation:** Do NOT implement weather filters as a default or core feature. The dome vs outdoor signal is statistically insignificant. The adverse weather filters are operationally inert (never fire). The dome preference filter has a losing head-to-head record and is driven by 2 good seasons out of 6. Offer venue type as informational display only. Close this research thread.

**Revised strategy defaults — unchanged from Round 9:**
- Non-buyback, n=5: SP Conservative + No Filter
- Non-buyback, n=10: Core/Satellite + No Filter
- Non-buyback, n=20: Core/Satellite + Avoid Div Soft (or No Filter)
- Non-buyback, n=50: 70/30 Blend + No Filter
- Buyback pools: SP Conservative + No Filter at all entry counts

## Continuation

Research continues in Discord channel #backtesting-research (1492758599393349673).
Notion page: https://www.notion.so/Back-Testing-Research-34029ce5833d8006bd12e10a4892cc4c
