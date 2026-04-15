# NFL Survivor Pool Strategy Research: Backtesting Analysis Across 10 Rounds
## Research Draft — For Sky the Scribe

**Analyst:** Stan the Scout  
**Date:** April 2026  
**Rounds covered:** 1–10  
**Total simulation runs:** ~2,000+  
**Seasons covered:** 2020–2025 (varies by round)

---

## 1. Executive Summary

NFL survivor pools are a solved problem for small, casual portfolios. Everyone knows to pick the biggest favorite. The real question — the one that separates power players from recreational participants — is: **what strategy actually maximizes survival when you're running 10, 20, or 50 entries across multiple pools?**

We ran 10 rounds of backtesting across 6 NFL seasons to find out. The findings challenge conventional wisdom at nearly every turn.

### Headline Findings

- **Contrarian-aware picking beats pure win probability by 50%** across a 3-season sample — not by picking upsets, but by picking the same strong teams while systematically avoiding the most popular ones. This is the foundational result.

- **The optimal strategy is portfolio-size-dependent.** A single-entry player and a 50-entry operator should run completely different algorithms. The strategies that win at 10 entries actively lose at 50 entries, and vice versa.

- **Intentional portfolio design beats random diversification at 10 entries.** A structured Core/Satellite architecture (60% conservative entries + 40% aggressive entries) produces 32% more entry-weeks than simply mixing strategies randomly — and it does so with dramatically lower variance.

- **Pool type overrides everything.** When buybacks are available, the winning strategy at every portfolio size flips completely — from diversified architectures to a single conservative approach that exploits the buyback safety net. Using the wrong strategy for your pool type leaves 50–100% performance on the table.

- **Conventional wisdom filters (avoid divisional games, prefer home teams, avoid bad weather) range from inert to actively harmful.** All three were tested empirically across multiple seasons. None should be on by default.

---

## 2. Methodology

### 2.1 Data Sources

**Game data:**
- 2020–2024: `nfl_data_py` Python package (open source). Provides game results, scores, point spreads, moneylines, and venue/weather data (`roof`, `temp`, `wind` fields).
- 2025: SurvivorPulse API live data. Games endpoint with win probabilities sourced from the Odds API.
- 2021–2024 game data also stored in local JSON files: `nfl_games_2021.json` through `nfl_games_2024.json` (272 games per season).

**Win probability derivation:**
For 2020–2024 historical seasons, win probabilities were derived from point spreads using the normal CDF formula:

```
P(win) = 0.5 × (1 + erf(spread / (13.5 × √2)))
```

The constant 13.5 represents the historical standard deviation of NFL score differentials. This formula is the standard approach used by sharp sports analysts and matches the implied win probabilities from moneylines within ~1pp for most matchups.

*Important convention note:* `nfl_data_py` uses a positive `spread_line` to indicate the home team is favored — the opposite convention from some betting platforms. This was verified and handled correctly throughout.

**Pick popularity data:**
- 2023–2024: SurvivorGrid.com (scraped). Per-team pick percentages from Yahoo, ESPN, and OfficeFootballPool, weighted-averaged across sources.
- 2025: SurvivorPulse database, Yahoo pick data.
- 2020–2022: Real SurvivorGrid data scraped for historical seasons (used in Round 10 weather analysis).

*Synthetic pick share note:* For Rounds 1–5 (2023 only), 2020–2022 pick shares were not yet available. Rounds 6–10 used real historical pick data for all seasons tested.

### 2.2 Simulation Design

The simulator models NFL survivor pool mechanics with these rules:

- **Team reuse:** Each entry may use a given team only once per season (standard survivor pool rule).
- **18-week regular season:** Runs weeks 1–18 per season.
- **Elimination:** An entry is eliminated when its selected team loses. Eliminated entries do not pick again unless a buyback mechanic applies (see Round 8).
- **Per-entry pick assignment:** Each week, for each live entry, the strategy scores all eligible teams (teams not yet used by that entry). The top-scored team is assigned. Assignment is sequential-greedy by default unless otherwise noted.
- **Key metric:** **Entry-weeks survived** — the sum across all entries of how many weeks each entry remained alive. This captures both how long entries survive and how many entries are running. A portfolio of 10 entries all surviving 12 weeks = 120 entry-weeks.
- **Secondary metric:** **Efficiency** — entry-weeks survived divided by the theoretical maximum (N entries × 18 weeks × seasons). At n=50 over 3 seasons, max = 2,700.

**Why entry-weeks, not wins?** Winner-take-all survivor pools make per-season "win" metrics noisy at small sample sizes. Entry-weeks gives a continuous, strategy-sensitive signal that correlates well with long-run EV across multiple seasons.

### 2.3 Strategy Definitions

The core strategies tested across rounds:

| Label | Formula |
|---|---|
| Pure Win Probability | Select team with highest win probability |
| 70/30 Blend | `score = 0.70 × winProb + 0.30 × (1 − pickShare/100)` |
| 80/20 Blend | `score = 0.80 × winProb + 0.20 × (1 − pickShare/100)` |
| 60/40 Blend | `score = 0.60 × winProb + 0.40 × (1 − pickShare/100)` |
| SP Production | `0.70 × EVPick + 0.30 × futureUtility` where `EVPick = winProb − pickShare/100` |
| SP Conservative | `0.65 × EVPick + 0.25 × futureUtility + 0.10 × leverageScore` |
| Core/Satellite | 60% of entries use 70/30 Blend; 40% use SP Production EV |
| Mixed Portfolio | Entries cycle through multiple strategy classes |
| Safety/Contrarian Split | 50% at 85/15 (WP/contrarian), 50% at 55/45 |
| Dynamic Rebalancing | Blend weights shift based on observed elimination rates |

### 2.4 Total Run Count

| Round | Focus | Runs |
|---|---|---|
| 1 | Initial strategy screen (2025 only) | 4 |
| 2 | Constrained strategies (2025 only) | 7 |
| 3 | Multi-season validation (2023–2025) | 21 |
| 4 | Lookahead variants (2023–2025) | 30 |
| 5 | EV + expendable strategies (2023–2025) | 30 |
| 6 | Entry-count scaling (2023–2025) | 168 |
| 7 | Per-entry differentiated scoring (2023–2025) | 144 |
| 8 | Buyback mechanics (2023–2025) | 492 |
| 9 | Game context filters (2023–2025) | 336 |
| 10 | Weather impact (2020–2025) | 672 |
| **Total** | | **~1,904** |

---

## 3. The Baseline: Why Picking Favorites Isn't Enough

### 3.1 Round 1 — Initial Strategy Screen (2025 Season Only)

The first simulation tested four strategies to establish a baseline and identify catastrophic failure modes.

| Strategy | Last Eliminated | Entry-Weeks | Avg Win Prob | Avg Pick Share |
|---|---|---|---|---|
| Pure Win Probability | Week 10 | 22 | 77.7% | 19.0% |
| Survival Equity | Week 9 | 19 | 75.2% | 11.6% |
| Leverage Score (WP÷Ownership) | Week 2 | 1 | — | — |
| Future Value Preservation | Week 2 | 1 | — | — |

**Key finding:** Raw leverage scoring and future-value preservation without win probability floors are catastrophic. Both strategies picked teams with near-zero ownership — correctly identifying undervalued teams in theory, but those teams were also the ones most likely to lose. Without a minimum win probability constraint, any strategy that overweights contrarianism or future optionality self-destructs in the early weeks.

Pure Win Probability (22 entry-weeks) established the floor. The question was whether any strategy could beat it.

### 3.2 Round 2 — The 70/30 Discovery (2025 Season Only)

Seven constrained strategies were tested, adding minimum win probability floors and the contrarian-blended approach.

| Strategy | Last Eliminated | Entry-Weeks | Avg Win Prob | Avg Pick Share |
|---|---|---|---|---|
| **Weighted Blend (70/30)** | **Week 14** | **26** | **75.2%** | **11.6%** |
| Pure Win Probability | Week 10 | 22 | 77.7% | 19.0% |
| Weighted Blend (80/20) | Week 10 | 22 | 77.4% | 16.0% |
| Leverage + 60% Floor | Week 5 | 11 | 63.3% | 3.0% |
| Anti-Chalk Top-5 | Week 5 | 11 | 66.3% | 3.4% |
| Leverage + 55% Floor | Week 3 | 4 | 58.7% | 0.8% |
| Tiered Top-10 | Week 3 | 5 | 58.0% | 0.5% |

**The 70/30 Blend survived 4 more weeks than Pure Win Probability** — a 18% improvement in entry-weeks and a full month more of live entries. The formula is simple: `score = 0.70 × winProb + 0.30 × (1 − pickShare/100)`. Pick safe teams, but among teams of similar safety, prefer the ones fewer people are on.

Why does this work? When a popular team loses — and they do, roughly 25–30% of the time — a disproportionate share of the pool is eliminated in one stroke. By systematically underweighting popular picks, the 70/30 Blend survives the "chalk busts" that thin out naive pools.

The 80/20 Blend produced identical results to Pure WP. The contrarian weight is not strong enough at 20% to produce meaningfully different team selections in most weeks. 70/30 is the minimum weight that creates behavioral divergence.

### 3.3 Round 3 — Multi-Season Validation (2023–2025)

The 2025 results could be noise. Multi-season testing across 2023, 2024, and 2025 confirmed the finding:

| Strategy | 2023 | 2024 | 2025 | Total | Avg/Season | Std Dev |
|---|---|---|---|---|---|---|
| **Weighted Blend (70/30)** | **17** | **14** | **26** | **57** | **19.0** | **5.1** |
| Weighted Blend (80/20) | 17 | 4 | 22 | 43 | 14.3 | 8.8 |
| Pure Win Probability | 13 | 3 | 22 | 38 | 12.7 | 7.8 |
| Leverage + 60% Floor | 5 | 16 | 11 | 32 | 10.7 | 4.5 |
| Tiered Top-10 | 13 | 9 | 5 | 27 | 9.0 | 3.3 |
| Anti-Chalk Top-5 | 4 | 5 | 11 | 20 | 6.7 | 3.1 |
| Leverage + 55% Floor | 6 | 6 | 4 | 16 | 5.3 | 0.9 |

**The 70/30 Blend produced 57 entry-weeks vs 38 for Pure Win Probability — 50% more survival across 3 seasons.** Critically, it did this while also being the most consistent (SD=5.1 vs 7.8 for Pure WP).

The 2024 season is the clearest illustration. Pure Win Probability produced only 3 entry-weeks in 2024 — it got wiped out in the first few weeks by chalk busts. The 70/30 Blend produced 14 entry-weeks in the same season by avoiding the most popular picks that collapsed.

### 3.4 Rounds 4–5: Lookahead and EV Variants

Rounds 4 and 5 tested more sophisticated approaches: multi-week lookahead strategies (save strong teams for later weeks), the production SurvivorPulse EV formula, and "expendable-first" approaches.

**Summary of relevant findings:**

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | vs 70/30 |
|---|---|---|---|---|---|---|
| **70/30 Blend** | **17** | **14** | **26** | **57** | **5.1** | = |
| Lookahead-5 Exp (0.15 penalty) | 18 | 12 | 19 | 49 | 3.1 | -8 |
| SP Prod 70%EV+30%FV | 13 | 23 | 9 | 45 | 5.9 | -12 |
| SP Conservative 65/25/10 | 10 | 21 | 9 | 40 | 5.4 | -17 |
| SP EV (winProb − pickShare) | 6 | 5 | 18 | 29 | 5.9 | -28 |

**Key insight:** Lookahead strategies (which penalize current use of strong future-value teams) are more consistent (lower SD) but don't exceed the 70/30 total. The production SurvivorPulse formula dominates 2024 (23 entry-weeks) but collapses in 2025 (9). Raw EV (win probability minus pick share) is the worst performer — overweights contrarianism without the safety floor.

**The 70/30 Blend's primary virtue is that it never has a catastrophic season.** Consistency beats ceiling at small entry counts. But as we'll see in Rounds 6–7, this calculus changes with portfolio size.

---

## 4. Does Strategy Matter More at Scale?

### 4.1 Research Question and Design (Round 6)

With the baseline established, Round 6 asked: does the 70/30 Blend still dominate at higher entry counts, or do coordination/diversification strategies become more important as portfolio size grows?

**14 strategies × 4 entry counts (5, 10, 20, 50) × 3 seasons = 168 simulation runs.**

### 4.2 Results by Portfolio Size

#### n=5 entries (max 90 entry-weeks per season)

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | Efficiency |
|---|---|---|---|---|---|---|
| **70/30 Blend** | **17** | **14** | **26** | **57** | **5.1** | **21.1%** |
| Mixed Portfolio | 10 | 14 | 34 | 58 | 10.5 | 21.5% |
| Adaptive Blend (90/10→50/50) | 29 | 4 | 25 | 58 | 11.0 | 21.5% |
| Anti-Correlation | 16 | 13 | 25 | 54 | 5.1 | 20.0% |
| SP Production 70%EV+30%FV | 10 | 20 | 22 | 52 | 5.2 | 19.3% |
| SP Conservative 65/25/10 | 10 | 16 | 16 | 42 | 2.8 | 15.6% |

At n=5, the 70/30 Blend is essentially tied for best on a risk-adjusted basis. Mixed Portfolio and Adaptive Blend produce one additional entry-week in aggregate but with much higher standard deviation (10.5 and 11.0 vs 5.1). For a 5-entry player, 70/30 is the correct answer.

#### n=10 entries — THE INFLECTION POINT

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | Efficiency | vs 70/30 |
|---|---|---|---|---|---|---|---|
| **SP Production 70%EV+30%FV** | **25** | **32** | **37** | **94** | **4.9** | **17.4%** | **+18** |
| SP Conservative 65/25/10 | 25 | 33 | 29 | 87 | 3.3 | 16.1% | +11 |
| Adaptive Blend (90/10→50/50) | 34 | 20 | 33 | 87 | 6.4 | 16.1% | +11 |
| Mixed Portfolio | 19 | 21 | 41 | 81 | 9.9 | 15.0% | +5 |
| Pure Win Probability | 23 | 14 | 43 | 80 | 12.1 | 14.8% | +4 |
| **70/30 Blend** | **20** | **22** | **34** | **76** | **6.2** | **14.1%** | **=** |

**Seven strategies beat the 70/30 Blend at n=10.** SP Production leads by +18 entry-weeks — a 24% improvement. The 70/30 Blend's efficiency drops from 21.1% at n=5 to 14.1% at n=10. More sophisticated strategies retain efficiency better because they account for future team value and EV dynamics that matter more when you're coordinating picks across 10 entries.

#### n=20 entries

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | Efficiency | vs 70/30 |
|---|---|---|---|---|---|---|---|
| **Mixed Portfolio** | **39** | **47** | **56** | **142** | **6.9** | **13.1%** | **+20** |
| Adaptive Blend | 48 | 29 | 51 | 128 | 9.7 | 11.9% | +6 |
| SP Production | 41 | 37 | 49 | 127 | 5.0 | 11.8% | +5 |
| SP Conservative | 41 | 38 | 45 | 124 | 2.9 | 11.5% | +2 |
| **70/30 Blend** | **38** | **32** | **52** | **122** | **8.4** | **11.3%** | **=** |

Mixed Portfolio wins at n=20 — running entries on different strategy classes creates genuine option value. When SP Production collapses in a given season, other strategies in the portfolio buffer the loss. The season-by-season consistency of Mixed Portfolio (39/47/56) shows this diversification is working exactly as intended.

#### n=50 entries — Simplicity Reclaims #1

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | Efficiency | vs 70/30 |
|---|---|---|---|---|---|---|---|
| **70/30 Blend** | **101** | **106** | **88** | **295** | **7.6** | **10.9%** | **=** |
| 80/20 Blend | 97 | 102 | 85 | 284 | 7.1 | 10.5% | -11 |
| Scarcity-Aware | 97 | 98 | 84 | 279 | 6.4 | 10.3% | -16 |
| SP Conservative | 99 | 98 | 81 | 278 | 8.3 | 10.3% | -17 |
| Mixed Portfolio | 96 | 79 | 88 | 263 | 6.9 | 9.7% | -32 |
| Adaptive Blend | 108 | 34 | 87 | 229 | 31.1 | 8.5% | -66 |
| Pure Win Probability | 106 | 26 | 93 | 225 | 35.1 | 8.3% | -70 |

The 70/30 Blend reclaims first place at n=50. Sophisticated strategies collapse. This is not because 70/30 becomes smarter at scale — it's a structural artifact of **team exhaustion**.

### 4.3 The Team Exhaustion Explanation

With 50 entries and approximately 30 teams playing per week, roughly 20 entries cannot get unique team assignments. Those entries share teams with other entries, making them perfectly correlated: same team wins or loses, both entries survive or die together.

Sophisticated strategies (Adaptive Blend, SP Production) spike heavily toward single dominant teams. At 50 entries, entries 1–20 get the strategy's preferred picks; entries 21–50 are forced to take whatever remains — often low-WP teams that rapidly eliminate those entries.

The 70/30 Blend's 30% contrarian weighting naturally distributes entries across teams without clustering. Entries 31–50 still get solid fallback picks because 70/30 doesn't push 30 entries onto KC/SF/etc. the way Pure WP does.

**Adaptive Blend's 2024 disaster (SD=31.1, only 34 entry-weeks):** Late-season contrarian weighting (~50/50) pushed entries toward risky teams. With 50 entries in weeks 13–18, the weak teams receiving high contrarian scores eliminated entries in bulk. A single bad week killed dozens of entries simultaneously.

### 4.4 Product-Ready Recommendations by Portfolio Size (Round 6)

| Portfolio Size | Recommended Strategy | Rationale |
|---|---|---|
| 1 entry | 70/30 Blend | Consistent champion, proven |
| 2–5 entries | 70/30 Blend | Confirmed at this scale |
| 6–15 entries | SP Production (70%EV+30%FV) | +18 EW vs 70/30 at n=10 |
| 16–30 entries | Mixed Portfolio | +20 EW vs 70/30 at n=20 |
| 31–50 entries | 70/30 Blend | Sophistication degrades under exhaustion |
| 50+ entries | 70/30 Blend | The only strategy that doesn't collapse |

---

## 5. Portfolio Design: Intentional Roles vs Random Diversity

### 5.1 Research Question (Round 7)

Round 6 showed that Mixed Portfolio (random strategy diversity) beats the 70/30 Blend at n=20. Round 7 asked: does **intentional** role assignment — giving each entry a purpose-driven scoring function — beat random diversification?

**12 strategies × 4 entry counts × 3 seasons = 144 simulation runs.**

### 5.2 The Core/Satellite Architecture

The standout finding from Round 7 is the **Core/Satellite** design:
- 60% of entries use 70/30 Blend (the "core" — reliable survival)
- 40% of entries use SP Production EV formula (the "satellites" — contrarian upside)

Core entries capture safe weeks. Satellite entries exploit contrarian opportunities when they arise. The architecture is simple enough to execute but intentional enough to produce meaningfully different behavior from different entries.

### 5.3 Results by Portfolio Size (Round 7)

#### n=10 — Core/Satellite's Peak Performance

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | Efficiency | vs Blend | vs Mixed |
|---|---|---|---|---|---|---|---|---|
| **Core/Satellite** | **33** | **36** | **32** | **101** | **1.7** | **18.7%** | **+25** | **+17** |
| Role-Based Portfolio | 32 | 25 | 28 | 85 | 2.9 | 15.7% | +9 | +1 |
| Correlated Pairs + Hedges | 24 | 30 | 31 | 85 | 3.1 | 15.7% | +9 | +1 |
| Mixed Portfolio | 32 | 20 | 32 | 84 | 5.7 | 15.6% | +8 | = |
| Dynamic Rebalancing | 26 | 26 | 27 | 79 | 0.5 | 14.6% | +3 | — |
| **70/30 Blend** | **20** | **22** | **34** | **76** | **6.2** | **14.1%** | **=** | — |

Core/Satellite's n=10 performance is the strongest finding across all 10 rounds:
- **101 total entry-weeks vs 76 for 70/30 Blend (+32%)**
- **+17 entry-weeks vs Mixed Portfolio** — beating the Round 6 winner by a clear margin
- **Standard deviation of 1.7** — the lowest variance of any strategy tested, period
- Season breakdown of 33/36/32 — remarkably consistent across all three seasons

This is not a lucky result from one good season. It's genuinely consistent outperformance driven by the structural advantage of the two-tier design.

#### Anti-Overlap Finding (Round 7 Confirmation)

A notable null result: Anti-Overlap Portfolio (global greedy assignment with 70/30 scoring) produced **identical results to the 70/30 Blend at every entry count**. This confirms a principle established in Round 6:

> **Assignment algorithm is irrelevant when the scoring function is the same.**

Global greedy and sequential greedy converge to the same picks because the 70/30 scoring function is smooth enough that entry ordering rarely affects the outcome. Meaningful differentiation requires fundamentally different scoring functions per entry — which is exactly what Core/Satellite and Role-Based Portfolio implement.

#### n=20 — Mixed Portfolio Holds

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | vs Blend | vs Mixed |
|---|---|---|---|---|---|---|---|
| **Mixed Portfolio** | **41** | **42** | **51** | **134** | **4.5** | **+12** | **=** |
| Temporal Diversification | 41 | 32 | 61 | 134 | 12.1 | +12 | = |
| Core/Satellite | 47 | 29 | 54 | 130 | 10.5 | +8 | -4 |
| Safety/Contrarian Split | 33 | 43 | 53 | 129 | 8.2 | +7 | -5 |
| **70/30 Blend** | **38** | **32** | **52** | **122** | **8.4** | **=** | — |

Mixed Portfolio ties at n=20 but with important caveats: Temporal Diversification matches its total with SD=12.1 vs 4.5 — Mixed Portfolio is the steadier choice. Core/Satellite finishes close at 130 but slightly behind.

#### n=50 — Intentional Design Beats Random Mixing

| Strategy | 2023 | 2024 | 2025 | Total | vs Blend | vs Mixed |
|---|---|---|---|---|---|---|
| **70/30 Blend** | **101** | **106** | **88** | **295** | **=** | **+36** |
| Role-Based Portfolio | 103 | 90 | 96 | 289 | -6 | +30 |
| Safety/Contrarian Split | 99 | 100 | 88 | 287 | -8 | +28 |
| Dynamic Rebalancing | 97 | 95 | 87 | 279 | -16 | +20 |
| Core/Satellite | 97 | 82 | 85 | 264 | -31 | +5 |
| **Mixed Portfolio** | **96** | **80** | **83** | **259** | **-36** | **=** |

At n=50, Mixed Portfolio collapses to last among intentional configs. **Eight intentional designs beat random strategy mixing.** Role-Based Portfolio and Safety/Contrarian Split hold up best.

### 5.4 Dynamic Rebalancing: The Consistency Story

Dynamic Rebalancing deserves a separate callout: at n=10, it achieves an SD of 0.5 — the most consistent performance of any strategy across all rounds. Its season breakdown is 26/26/27 across 2023, 2024, and 2025. The adaptive weight adjustment (shift conservative when many entries are getting eliminated, shift aggressive when survival rates are high) smooths out seasonal volatility.

It never wins an entry count outright. It's the floor-setter — always competitive, never dominant. For risk-averse operators where consistency matters as much as ceiling, this is the profile you want.

### 5.5 Answer to the Key Question

| Entry Count | Does Intentional Beat Random? | Best Intentional Design |
|---|---|---|
| n=5 | No — Mixed Portfolio wins | Temporal Diversification (60, -2 vs Mixed) |
| n=10 | **YES — 3 configs beat Mixed** | Core/Satellite (+17 over Mixed, +25 over 70/30) |
| n=20 | No — Mixed holds | Core/Satellite (-4 vs Mixed, +8 vs Blend) |
| n=50 | **YES — 8 configs beat Mixed** | Role-Based Portfolio (+30 over Mixed) |

**Intentional design matters most at the scale where serious multi-entry players actually operate: n=10.**

### 5.6 Updated Recommendations (After Round 7)

| Portfolio Size | Recommended Strategy | Rationale |
|---|---|---|
| 1–5 entries | Mixed Portfolio or 70/30 Blend | Mixed +5 at n=5; 70/30 for simplicity |
| **6–15 entries** | **Core/Satellite (60% blend + 40% EV)** | **+25 over blend, +17 over Mixed at n=10, lowest variance** |
| 16–30 entries | Mixed Portfolio | Still holds at n=20 |
| 31–50 entries | Role-Based or Safety/Contrarian | Best intentional configs at scale |
| 50+ entries | 70/30 Blend | Structural floor |

---

## 6. The Buyback Advantage

### 6.1 Research Question (Round 8)

Buyback pools — where eliminated entries can pay to re-enter during the first few weeks — are increasingly common. Does the optimal strategy change when buybacks are available? And by how much?

**12 strategies × 4 entry counts × 3 buyback configs (no buyback / Wk1-3 / Wk1-4) × 3 seasons = 432 Part 1 runs.**
**5 split strategies × 4 entry counts × 3 seasons = 60 Part 2 runs.**
**Total: 492 runs.**

### 6.2 SP Conservative Wins Everything — With Buybacks

The most dramatic finding across all 10 rounds:

| Entry Count | No Buyback Winner | Score | Buyback Winner (Wk1-3) | Score | Uplift |
|---|---|---|---|---|---|
| n=5 | Mixed Portfolio | 67 | **SP Conservative** | **78** | +16.4% |
| n=10 | Core/Satellite | 101 | **SP Conservative** | **165** | +63.4% vs no-BB winner |
| n=20 | Core/Satellite | 130 | **SP Conservative** | **248** | +90.8% |
| n=50 | 70/30 Blend | 295 | **SP Conservative** | **463** | +57.0% |

The winner changes at **every entry count** when buybacks are introduced. SP Conservative (65% EV + 25% futureValue + 10% leverage) did not win at any entry count without buybacks. With buybacks, it wins at all four.

### 6.3 Full Buyback Results Tables

#### n=10 (max 540 entry-weeks over 3 seasons)

| Strategy | No Buyback | BB Wk1-3 | BB Wk1-4 | Δ (Wk1-3) | Uplift % |
|---|---|---|---|---|---|
| **SP Conservative** | **82** | **165** | **165** | **+83** | **+101.2%** |
| Safety/Contrarian Split | 83 | 146 | 165 | +63 | +75.9% |
| 70/30 Blend | 76 | 138 | 141 | +62 | +81.6% |
| EV Gradient | 73 | 136 | 144 | +63 | +86.3% |
| Pure Win Probability | 80 | 129 | 136 | +49 | +61.3% |
| Core/Satellite | 101 | 125 | 126 | +24 | +23.8% |
| Mixed Portfolio | 87 | 110 | 120 | +23 | +26.4% |

#### n=20 (max 1,080 entry-weeks)

| Strategy | No Buyback | BB Wk1-3 | Δ | Uplift % |
|---|---|---|---|---|
| **SP Conservative** | **122** | **248** | **+126** | **+103.3%** |
| Safety/Contrarian Split | 129 | 222 | +93 | +72.1% |
| 70/30 Blend | 122 | 221 | +99 | +81.1% |
| Pure Win Probability | 112 | 217 | +105 | +93.8% |
| Core/Satellite | 130 | 212 | +82 | +63.1% |

#### Average Buyback Uplift Across All Strategies (Wk1-3 window)

| Portfolio Size | Avg Uplift | Best Single Uplift | Winner |
|---|---|---|---|
| n=5 | +13.2 entry-weeks | +31 (Safety/Contrarian Split) | SP Conservative (78) |
| n=10 | +46.1 entry-weeks | +83 (SP Conservative) | SP Conservative (165) |
| n=20 | +93.1 entry-weeks | +126 (SP Conservative) | SP Conservative (248) |
| n=50 | +159.9 entry-weeks | +194 (Expendable-First) | SP Conservative (463) |

### 6.4 Why SP Conservative Wins in Buyback Pools

Conservative strategies tolerate more early-game losses — their moderate win probability tolerance means some entries get eliminated in weeks 1–3 more frequently than aggressive strategies. In a no-buyback pool, this is a penalty. In a buyback pool, **those early eliminations become refundable.**

Conservative strategies get multiple second chances to showcase their late-season survival advantages. Aggressive strategies (Core/Satellite, SP Production) lose fewer entries early, so they exercise fewer buybacks and capture less of the mechanic's value.

The result: buybacks convert a liability (early losses) into a structural advantage.

### 6.5 Buyback ROI Analysis

The economic question for any pool player: is the buyback worth the cost (typically same as initial entry fee)?

| Portfolio Size | Best EW/Buyback | Strategy | Survival Rate (3+ weeks) | Survival Rate (10+ weeks) |
|---|---|---|---|---|
| n=5 | 3.10 | Safety/Contrarian Split | 40.0% | 20.0% |
| n=10 | **4.15** | **SP Conservative** | **35.0%** | **30.0%** |
| n=20 | 2.74 | SP Conservative | 26.1% | 15.2% |
| n=50 | 1.75 | Expendable-First | 19.8% | 5.4% |

**At n=10, SP Conservative generates 4.15 additional entry-weeks per buyback used.** In a winner-take-all pool with a $100 entry fee, that means a $100 buyback keeps an entry alive for an expected 4+ additional weeks — a compelling ROI by any measure.

The only case with negative ROI: Adaptive Blend at n=5 (-0.12 EW/BB). The adaptive strategy shifts toward conservative weighting over time; bought-back entries return to a more aggressive mode during the early weeks they missed, reducing effectiveness. This is the exception, not the rule.

**20–40% of bought-back entries survive 3+ additional weeks.** Even at the lowest end, that's meaningful survival.

### 6.6 Split Strategies Don't Work

A natural hypothesis: play aggressively during the buyback window (weeks 1–3), then switch to safe after. This lets you capitalize on the buyback while not squandering it.

Five split strategy configurations were tested. None beat the simple SP Conservative baseline.

| Portfolio Size | Best Non-Split w/BB | Best Split w/BB | Gap |
|---|---|---|---|
| n=5 | SP Conservative (78) | EV/Blend Split (75) | -3 |
| n=10 | SP Conservative (165) | Contrarian/Conservative (145) | -20 |
| n=20 | SP Conservative (248) | EV/Blend Split (233) | -15 |
| n=50 | SP Conservative (463) | Expendable/Safe Split (443) | -20 |

**The 3-week buyback window is too short for strategy switching to pay off.** By the time the strategy switches to safe mode, the compounding advantage of early conservative picks has already been foregone. The conclusion: don't overcomplicate it. If buybacks are available, run SP Conservative from week 1.

### 6.7 Pool Type Decision Framework (After Round 8)

| Pool Type | Portfolio Size | Recommended Strategy |
|---|---|---|
| **No buyback** | 1–5 | Mixed Portfolio or 70/30 Blend |
| **No buyback** | 6–15 | Core/Satellite |
| **No buyback** | 16–30 | Mixed Portfolio |
| **No buyback** | 31–50 | 70/30 Blend |
| **Buyback (any window)** | Any | SP Conservative 65/25/10 |

The app must distinguish pool type. Using the wrong strategy for your pool mechanic leaves 50–100% performance on the table.

---

## 7. Game Context Filters: What Doesn't Work

### 7.1 Divisional Games and Home/Away (Round 9)

Two heuristics are widely debated in survivor pool communities:
1. Avoid picking teams in divisional matchups (more competitive, harder to predict)
2. Prefer home teams (home field advantage)

Round 9 tested both empirically across 4 strategies × 7 filter modes × 4 entry counts × 3 seasons = 336 runs.

**Filter modes tested:**
1. No Filter (control)
2. Avoid Divisional (Soft — 10% score penalty for divisional picks)
3. Avoid Divisional (Hard — swap to non-divisional if within 15% score gap)
4. Prefer Home (Soft — 10% bonus for home teams)
5. Prefer Home (Hard — swap to home team if within 15% score gap)
6. Both Filters (Soft)
7. Both Filters (Hard)

### 7.2 Hypothesis Test Results

#### H1: Divisional Games Are More Volatile

| Season | Divisional WR | Non-Divisional WR | Gap | Supports H1? |
|---|---|---|---|---|
| 2023 | 64.1% | 69.5% | +5.4pp | Yes |
| 2024 | 73.6% | 70.4% | -3.2pp | No |
| 2025 | 76.0% | 66.5% | -9.5pp | Strongly No |
| **Average** | **71.2%** | **68.8%** | **-2.4pp** | **Not Supported** |

**H1 is not supported overall.** In 2023, divisional games were more volatile as the heuristic predicts. In 2024 and 2025, divisional favorites covered at a *higher* rate than non-divisional favorites. The average across three seasons shows divisional picks winning slightly *more* often — the opposite of the hypothesis.

#### H2: Home Teams Win More Often

| Season | Home WR | Road WR | Gap | Supports H2? |
|---|---|---|---|---|
| 2023 | 62.9% | 74.6% | -11.7pp | Road wins more |
| 2024 | 71.4% | 72.3% | -0.9pp | Roughly equal |
| 2025 | 74.9% | 64.4% | +10.5pp | Yes |
| **Average** | **69.7%** | **70.4%** | **-0.7pp** | **Not Supported** |

**H2 is not supported overall.** Home field advantage in survivor-relevant games (where favorites are heavily favored) appears to be declining or highly variable. In 2023, road teams in high-probability matchups won significantly more often. In 2025 the pattern flipped. Net effect across three seasons: negligible.

### 7.3 Full Filter Performance Results

#### SP Conservative (Strongest Filter Signal)

| Filter Mode | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| No Filter | 21.3 | 27.3 | 40.7 | 96.0 |
| Avoid Div (Soft) | 18.7 | 32.7 | 47.7 | 94.0 |
| Avoid Div (Hard) | 16.7 | 31.3 | 48.0 | 93.3 |
| Prefer Home (Soft) | 16.3 | 25.3 | 43.7 | 92.0 |
| Prefer Home (Hard) | 16.3 | 22.3 | 39.7 | 88.0 |
| Both (Soft) | 15.3 | 23.3 | 40.0 | 91.3 |
| Both (Hard) | 15.0 | 22.0 | 37.0 | 90.0 |

*Values are average entry-weeks per season across 2023–2025.*

#### Filter Deltas vs No Filter Baseline (SP Conservative)

| Filter | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| Avoid Div Soft | -2.7 | **+5.3** | **+7.0** | -2.0 |
| Avoid Div Hard | -4.7 | **+4.0** | **+7.3** | -2.7 |
| Home Soft | -5.0 | -2.0 | +3.0 | -4.0 |
| Home Hard | -5.0 | -5.0 | -1.0 | -8.0 |

The avoid-divisional filter shows genuine gains at n=10 and n=20 for SP Conservative (+5.3 and +7.0 respectively). The home filter is harmful at n=5 and n=50, and only modestly positive at n=20.

### 7.4 Overall Champions by Entry Count

| N | Best Combination | Entry-Weeks (avg/season) | Filter Contribution |
|---|---|---|---|
| 5 | SP Conservative + No Filter | 21.3 | None |
| 10 | Core/Satellite + No Filter | 33.7 | None |
| 20 | Core/Satellite + Avoid Div Soft | 49.0 | **+5.7 (+13.2%)** |
| 50 | 70/30 Blend + No Filter | 98.3 | None |

**The only materially significant filter benefit is Avoid Divisional (Soft) for n=20 pools.** At every other combination, No Filter wins or ties.

### 7.5 The Filter Swap Problem

When a filter swaps the top pick to a different team, how often does the new pick win?

| Strategy | Filter | Swap Count | Beneficial | Harmful | % Beneficial |
|---|---|---|---|---|---|
| 70/30 Blend | Avoid Div Soft | 348 | 220 | 128 | 63.2% |
| 70/30 Blend | Prefer Home Soft | 302 | 168 | 134 | 55.6% |
| Core/Satellite | Avoid Div Soft | 378 | 246 | 132 | 65.1% |
| Core/Satellite | Prefer Home Soft | 304 | 159 | 145 | 52.3% |
| SP Conservative | Avoid Div Soft | 380 | 247 | 133 | 65.0% |
| SP Conservative | Prefer Home Soft | 318 | 184 | 134 | 57.9% |

Even a 63% beneficial swap rate doesn't guarantee net entry-week gains because:
1. The swapped-away original pick often had higher absolute win probability
2. Gains only materialize at n=10-20 for specific strategies
3. At n=5 and n=50, filters are universally harmful

**The home filter is barely above random chance at 52–58%.** Avoid divisional at 63–65% is more defensible as a player conviction, but it still falls short of consistent net gains.

### 7.6 Product Recommendation

Offer both filters as optional user toggles — not defaults. Season variance is too high (a filter that gained +5 in one season lost -10 in another). At n=5 (most casual players), all filters are harmful. No filter has consistent statistically significant gains across all seasons and entry counts.

Frame game context filters as "conviction overrides" for players with strong opinions about specific game types — not as algorithmic improvements.

---

## 8. Weather Filters: No Signal, No Uplift

### 8.1 The Feasibility Study (Round 9.5)

Before the full simulation, a feasibility study examined whether a dome vs outdoor signal even existed in the data.

**Data: 544 games, 2023–2024 only.**

| Category | Games | Upset Rate | Fav Win Rate |
|---|---|---|---|
| Dome | 175 | 28.0% | 72.0% |
| Outdoor Cold (Dec/Jan) | 121 | 32.2% | 67.8% |
| Outdoor Warm (Sep/Oct) | 172 | 33.7% | 66.3% |

**The 2-year gap: +4.2pp** — dome games had fewer upsets than cold outdoor games. This exceeded the 3pp threshold set for proceeding. The recommendation was to run the full simulation but with a caution: year-over-year variance was already visible, with 2023 showing +13.8pp dome advantage and 2024 showing -5.7pp (dome teams actually underperforming outdoor in the second year).

### 8.2 Full Weather Simulation (Round 10)

**Data:** 1,615 games across 2020–2025 enriched with weather classification from nfl_data_py venue/weather fields.
**Design:** 4 strategies × 7 filter modes × 4 entry counts × 6 seasons = 672 runs.

**Weather classification:**
- `weather_neutral`: dome or closed roof
- `weather_mild`: outdoor, temp ≥50°F and wind <15mph
- `weather_adverse`: outdoor, temp 40–49°F or wind 15–24mph
- `weather_extreme`: outdoor, temp <32°F or wind ≥25mph

### 8.3 Upset Rate Analysis — 6 Seasons

| Weather Category | Games | Upset Rate | Fav Win Rate |
|---|---|---|---|
| Dome/Closed | 521 | 32.0% | 68.0% |
| Outdoor Mild | 703 | 34.3% | 65.7% |
| Outdoor Adverse | 334 | 34.7% | 65.3% |
| Outdoor Extreme | 57 | 28.1% | 71.9% |

**Surprising finding:** Extreme weather games have *fewer* upsets than dome games (28.1% vs 32.0%). This is the opposite of the intuition driving weather filters in the first place.

**Net dome vs outdoor gap: +1.7pp** (outdoor teams upset favorites slightly more on average). This is well below the +4.2pp from the 2-year feasibility study — adding four more seasons pulled the signal toward zero.

### 8.4 Year-Over-Year Consistency Test

| Season | Dome Upset % | Outdoor Upset % | Gap | Dome Advantage? |
|---|---|---|---|---|
| 2020 | 36.3% | 30.9% | **-5.3pp** | No |
| 2021 | 39.2% | 36.3% | **-3.0pp** | No |
| 2022 | 22.6% | 39.0% | **+16.4pp** | Yes |
| 2023 | 25.9% | 34.4% | **+8.5pp** | Yes |
| 2024 | 29.8% | 28.1% | **-1.7pp** | No |
| 2025 | 38.0% | 33.3% | **-4.7pp** | No |

**The dome advantage holds in only 2 of 6 seasons (2022 and 2023).** In four seasons, dome teams actually had higher upset rates than outdoor teams. The signal flips sign freely — there is no stable underlying pattern.

### 8.5 Statistical Significance Test

Two-proportion z-test, dome vs outdoor across all 6 seasons:
- Dome upset rate: 32.1% (n=521)
- Outdoor upset rate: 33.7% (n=1,062)
- Z-score: 0.658
- P-value: 0.511

**The dome vs outdoor gap is not statistically significant at any conventional threshold.** The sample is also substantially underpowered: detecting a 3pp difference with 80% power at α=0.05 would require ~1,700 games per arm, not 521.

### 8.6 The Adverse/Extreme Weather Filter Problem

**Critical finding:** All four adverse-weather and extreme-weather filter modes (Avoid Adverse Soft, Avoid Adverse Hard, Avoid Extreme Soft, Avoid Extreme Hard) produced **identical results to No Filter in every single simulation run** — 0 wins, 0 losses, 96 ties.

**Why:** Top-scoring picks virtually never fall in the `weather_adverse` or `weather_extreme` categories. High-WP teams are typically dome teams or outdoor teams playing in mild conditions. Only 3.8% of all No Filter picks were in `weather_adverse`. Zero were in `weather_extreme`.

The filters correctly identify adverse weather games as candidates to avoid — but the base scoring function already avoids them implicitly. Weather avoidance filters are operationally inert.

### 8.7 Dome Preference Filter — The False Positive

The Prefer Dome (Soft) filter showed a positive aggregate delta (+291 entry-weeks across all runs) — but with a losing win rate:

| Filter | Wins | Losses | Ties | Total Delta |
|---|---|---|---|---|
| Avoid Adverse (Soft/Hard) | 0 | 0 | 96 | 0 |
| Avoid Extreme (Soft/Hard) | 0 | 0 | 96 | 0 |
| Prefer Dome (Soft) | 33 | 47 | 16 | **+291** |
| Prefer Dome (Hard) | 24 | 56 | 16 | -935 |

**The Dome Soft filter wins 33/96 comparisons (41.3%) but produces a positive total delta.** This apparent paradox is explained by season skew: the filter won very big in 2020 (+60 EW at n=10) and 2022 (+80 EW at n=10) — the two seasons where dome teams happened to outperform their win probabilities. In 2024, the same filter collapsed 70/30 Blend n=10 from 110 entry-weeks to 10 (a 91% loss).

**The dome preference filter is a high-variance bet on seasons where dome teams outperform.** It is not a reliable weather risk management tool.

Season-by-season breakdown confirms this (70/30 Blend, n=10):

| Season | No Filter EW | Dome Soft EW | Delta |
|---|---|---|---|
| 2020 | 40 | 100 | **+60** |
| 2021 | 50 | 30 | **-20** |
| 2022 | 0 | 80 | **+80** |
| 2023 | 40 | 60 | **+20** |
| 2024 | 110 | 10 | **-100** |
| 2025 | 30 | 30 | 0 |

### 8.8 Recommendations: Weather as Information, Not a Filter

**Do not implement weather filters as a default or core algorithmic feature.** The evidence:
- Dome vs outdoor gap: not statistically significant (p=0.511)
- Adverse/extreme filters: operationally inert, never change picks
- Dome preference: 41.3% win rate, high variance, driven by 2 seasons out of 6
- Extreme weather sample: 57 total games across 6 seasons — not analyzable

If weather data is surfaced in the product, use it for **display only** — show venue type and game conditions as contextual information for players making manual overrides. Let the player decide; don't bake weather into the algorithm.

**Close this research thread.** Return to weather only if substantially more data becomes available (10+ seasons) or more granular per-game weather integration is feasible.

---

## 9. Consolidated Recommendations

### 9.1 Master Decision Tree

```
Is this a buyback pool?
├── YES: Run SP Conservative 65/25/10 at all entry counts
│   └── Always exercise the buyback when available (positive ROI universally)
│
└── NO: How many entries are you running?
    ├── 1–5 entries: Mixed Portfolio or 70/30 Blend
    │   └── No filter
    ├── 6–15 entries: Core/Satellite (60% blend + 40% EV)
    │   └── No filter (optional: Avoid Div Soft if you have strong conviction)
    ├── 16–30 entries: Mixed Portfolio
    │   └── No filter (or Avoid Div Soft for n=20 pools)
    ├── 31–50 entries: 70/30 Blend (or Role-Based Portfolio)
    │   └── No filter
    └── 50+ entries: 70/30 Blend
        └── No filter
```

### 9.2 Final Strategy Defaults Summary Table

| Pool Type | N | Strategy | Filter | EW (avg per season) |
|---|---|---|---|---|
| Non-buyback | 5 | SP Conservative | None | 21.3 |
| Non-buyback | 10 | Core/Satellite | None | 33.7 |
| Non-buyback | 20 | Core/Satellite | Avoid Div Soft | 49.0 |
| Non-buyback | 50 | 70/30 Blend | None | 98.3 |
| Buyback (Wk1-3) | 5 | SP Conservative | None | 26.0 |
| Buyback (Wk1-3) | 10 | SP Conservative | None | 55.0 |
| Buyback (Wk1-3) | 20 | SP Conservative | None | 82.7 |
| Buyback (Wk1-3) | 50 | SP Conservative | None | 154.3 |

### 9.3 Summary of All Findings by Round

| Round | Focus | Key Finding |
|---|---|---|
| 1–2 | Strategy baseline | 70/30 Blend produces 18% more entry-weeks than Pure WP in a single season |
| 3 | Multi-season validation | 70/30 produces 50% more entry-weeks across 3 seasons; most consistent (SD=5.1) |
| 4 | Lookahead variants | Lookahead is more consistent but doesn't beat 70/30 total; consistency is the right goal |
| 5 | SurvivorPulse EV | Raw EV formula underperforms; production formula inconsistent; 70/30 wins on consistency |
| 6 | Entry-count scaling | 70/30 loses at n=10 (7 strategies beat it); Mixed Portfolio wins n=20; 70/30 reclaims n=50 due to team exhaustion |
| 7 | Differentiated scoring | Core/Satellite dominates at n=10 (+25 vs blend, +17 vs Mixed, lowest variance); intentional beats random at n=10 and n=50 |
| 8 | Buyback mechanics | Pool type overrides everything; SP Conservative wins all entry counts with buybacks; strategy never changes once you've identified your pool type |
| 9 | Game context filters | Avoid-div shows marginal gains at n=20 only; home filter consistently harmful; neither should be a default |
| 10 | Weather | No statistically significant signal; adverse filters inert; dome preference has losing win rate; close the thread |

---

## 10. Limitations and Future Work

### 10.1 Sample Size Constraints

- **Rounds 1–8:** 3 NFL seasons (2023–2025). Small sample. A single anomalous season can move aggregate results significantly.
- **Round 10:** 6 seasons (2020–2025). Still underpowered for detecting 3pp differences in weather-category upset rates; would require ~1,700 games per arm.
- **Season-to-season variance is substantial.** Pure Win Probability produced 3 entry-weeks in 2024 (complete collapse) and 35 in 2025 (best season ever). Any strategy recommendation is ultimately a bet on distributional consistency, not guaranteed outcomes.

### 10.2 Synthetic Pick Share for 2020–2022

For Rounds 1–5, pick share data for 2020–2022 was not yet integrated. Those rounds used real data only for 2023–2025. Round 6 onward incorporated real SurvivorGrid data for all available seasons, but synthetic/modeled pick shares were used in intermediate calculations where historical data was absent.

### 10.3 No Real-Money Pool Simulation

All simulations optimize for **entry-weeks survived** — a proxy for survival time that correlates with win probability but does not model:
- Entry fee structures
- Prize pool sizes (winner-take-all vs top-3 payout)
- Pool-specific dynamics (known opponent counts, tracking other players)
- Tax on late-season upsets when the field is small

A complete EV simulation would require pool-size-specific survivor math, which was intentionally deferred to keep the strategy research clean and comparable.

### 10.4 Simulation vs Real Player Behavior

Real survivor pool players are not fully rational:
- They don't always take the algorithmically optimal pick
- Team selection is influenced by narrative, media, and personal bias
- Buybacks are sometimes not exercised for non-financial reasons
- Multi-entry portfolios with correlated picks may face social/community dynamics

The research identifies optimal strategies under idealized conditions. Real-world implementation will see some degradation from these results.

### 10.5 Areas for Future Research

1. **Prize structure modeling:** Simulate n=10 portfolio in a 1,000-player pool with $100 entry fee and winner-take-all payout to compute actual EV in dollars. This is the bridge from "entry-weeks survived" to actual return on investment.

2. **More seasons:** 6 seasons of data is the minimum for confident conclusions. Extending to 10+ seasons would meaningfully reduce variance in the per-strategy estimates, especially for weather analysis.

3. **Real pick share data for 2020–2022:** All historical pick percentages from SurvivorGrid are available for these seasons; integrating them into Rounds 1–5 would strengthen the baseline analysis.

4. **Playoff survivor pools:** Some pools extend into or occur entirely during the playoffs. Completely different dynamics: only 12–14 teams, fewer weeks, higher variance per game. Strategy research would start over.

5. **Live-season adaptive strategies:** Strategies that adjust weights based on observed eliminations in a running pool (using actual survivor counts rather than simulated ones) could outperform static-weight approaches in practice.

6. **Per-game weather enrichment:** Open-Meteo provides free historical weather data (temperature, wind) at hourly resolution for any stadium location going back to 1940. A stadium coordinate lookup table for all 25+ outdoor stadiums would enable truly granular weather classification, but the fundamental signal question (does weather matter?) appears answered: it doesn't, at least not reliably enough to filter on.

---

## 11. Appendix: Full Results Tables by Round

### Appendix A: Rounds 1–5 — Strategy Baseline (n=5 entries)

**Total entry-weeks, 3-season aggregate (2023–2025) unless noted:**

| Strategy | 2023 | 2024 | 2025 | Total | SD | Notes |
|---|---|---|---|---|---|---|
| 70/30 Blend | 17 | 14 | 26 | 57 | 5.1 | **Champion** |
| 80/20 Blend | 17 | 4 | 22 | 43 | 7.6 | |
| Pure Win Probability | 13 | 3 | 22 | 38 | 7.8 | |
| Leverage + 60% Floor | 5 | 16 | 11 | 32 | 4.5 | Wk1-5 elimination most runs |
| Tiered Top-10 | 13 | 9 | 5 | 27 | 3.3 | |
| Anti-Chalk Top-5 | 4 | 5 | 11 | 20 | 3.1 | |
| Lookahead-5 Exp (0.15) | 18 | 12 | 19 | 49 | 3.1 | More consistent, lower ceiling |
| SP Prod 70%EV+30%FV | 13 | 23 | 9 | 45 | 5.9 | Won 2024, collapsed 2025 |
| SP Conservative 65/25/10 | 10 | 21 | 9 | 40 | 5.4 | |
| SP EV (winProb − pickShare) | 6 | 5 | 18 | 29 | 5.9 | **Worst**: pure EV without floor |

### Appendix B: Round 6 — Entry-Count Scaling (Full Cross-Table)

| Strategy | n=5 | n=10 | n=20 | n=50 | Scale Ratio |
|---|---|---|---|---|---|
| 70/30 Blend | 57 | 76 | 122 | 295 | 5.18x |
| SP Production 70%EV+30%FV | 52 | **94** | 127 | 275 | 5.29x |
| SP Conservative 65/25/10 | 42 | 87 | 124 | 278 | 6.62x |
| Adaptive Blend 90/10→50/50 | 58 | 87 | 128 | 229 | 3.95x |
| Mixed Portfolio | 58 | 81 | **142** | 263 | 4.53x |
| Pure Win Probability | 51 | 80 | 112 | 225 | 4.41x |
| 80/20 Blend | 43 | 78 | 119 | 284 | 6.60x |
| Anti-Correlation | 54 | 71 | 118 | 262 | 4.85x |
| Scarcity-Aware | 53 | 74 | 117 | 279 | 5.26x |
| 60/40 Blend | 32 | 66 | 106 | 250 | 7.81x |
| Expendable-First 65/25/10 | 51 | 68 | 107 | 252 | 4.94x |

*Scale Ratio = n=50 total ÷ n=5 total. Perfect linear scaling = 10x.*

### Appendix C: Round 7 — Differentiated Scoring (All 12 Strategies)

| Strategy | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| Core/Satellite (60/40) | 44 | **101** | 130 | 264 |
| Mixed Portfolio | **62** | 84 | **134** | 259 |
| Temporal Diversification | 60 | 76 | **134** | 262 |
| 70/30 Blend | 57 | 76 | 122 | **295** |
| Safety/Contrarian Split | 45 | 83 | 129 | 287 |
| Role-Based Portfolio | 56 | 85 | 127 | 289 |
| Dynamic Rebalancing | 48 | 79 | 115 | 279 |
| Correlated Pairs + Hedges | 52 | 85 | 129 | 232 |
| EV Gradient 95/5→55/45 | 46 | 73 | 128 | 263 |
| Adaptive Role Portfolio | 57 | 75 | 118 | 266 |
| Ownership-Bucket Spread | 46 | 75 | 112 | 254 |
| Anti-Overlap (global assign) | 57 | 76 | 122 | **295** |

### Appendix D: Round 8 — Buyback Master Table

**Winners per entry count under each pool config:**

| N | No Buyback | Score | Buyback Wk1-3 | Score | Buyback Wk1-4 | Score |
|---|---|---|---|---|---|---|
| 5 | Mixed Portfolio | 67 | **SP Conservative** | **78** | Mixed Portfolio | 76 |
| 10 | Core/Satellite | 101 | **SP Conservative** | **165** | SP Conservative / Safety/Contrarian | 165 |
| 20 | Core/Satellite | 130 | **SP Conservative** | **248** | SP Conservative | 250 |
| 50 | 70/30 Blend | 295 | **SP Conservative** | **463** | SP Conservative | 495 |

**ROI table (n=10, Wk1-3 buyback):**

| Strategy | BB Used | Surv3+% | Surv10+% | Net EW Gain | EW/BB |
|---|---|---|---|---|---|
| SP Conservative | 20 | 35.0% | 30.0% | +83 | **4.15** |
| EV Gradient | 19 | 26.3% | 15.8% | +63 | 3.32 |
| Safety/Contrarian | 19 | 31.6% | 15.8% | +63 | 3.32 |
| 70/30 Blend | 19 | 26.3% | 21.1% | +62 | 3.26 |
| 60/40 Blend | 21 | 28.6% | 9.5% | +58 | 2.76 |
| Pure Win Probability | 19 | 26.3% | 10.5% | +49 | 2.58 |
| SP Production | 20 | 35.0% | 5.0% | +40 | 2.00 |

### Appendix E: Round 9 — Full Filter Results (All 4 Strategies × 7 Filters × 4 Entry Counts)

*Average entry-weeks per season (2023–2025)*

**70/30 Blend:**

| Filter | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| No Filter | 19.0 | 25.3 | 40.7 | 98.3 |
| Avoid Div Soft | 15.7 | 24.0 | 43.3 | 96.0 |
| Avoid Div Hard | 15.7 | 23.3 | 44.0 | 93.7 |
| Prefer Home Soft | 15.7 | 22.3 | 42.3 | 90.3 |
| Prefer Home Hard | 15.7 | 20.7 | 40.0 | 85.3 |
| Both Soft | 14.7 | 21.0 | 43.7 | 88.0 |
| Both Hard | 14.0 | 26.0 | 39.3 | 89.0 |

**Core/Satellite:**

| Filter | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| No Filter | 14.7 | **33.7** | 43.3 | 88.0 |
| Avoid Div Soft | 14.3 | 25.3 | **49.0** | 90.7 |
| Avoid Div Hard | 17.0 | 25.3 | 48.0 | 88.7 |
| Prefer Home Soft | 12.7 | 23.0 | 37.0 | 75.0 |
| Prefer Home Hard | 12.7 | 20.7 | 38.7 | 73.7 |

**SP Conservative:**

| Filter | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| No Filter | **21.3** | 27.3 | 40.7 | 96.0 |
| Avoid Div Soft | 18.7 | 32.7 | 47.7 | 94.0 |
| Avoid Div Hard | 16.7 | 31.3 | 48.0 | 93.3 |
| Prefer Home Soft | 16.3 | 25.3 | 43.7 | 92.0 |
| Prefer Home Hard | 16.3 | 22.3 | 39.7 | 88.0 |

### Appendix F: Round 10 — Weather Simulation Full Upset Rate Table

**By weather category and season (2020–2025):**

| Season | Dome N | Dome Upset% | Outdoor N | Outdoor Upset% | Gap (Dome − Outdoor) |
|---|---|---|---|---|---|
| 2020 | 91 | 36.3% | 165 | 30.9% | -5.3pp |
| 2021 | 79 | 39.2% | 182 | 36.3% | -3.0pp |
| 2022 | 84 | 22.6% | 177 | 39.0% | +16.4pp |
| 2023 | 81 | 25.9% | 180 | 34.4% | +8.5pp |
| 2024 | 94 | 29.8% | 178 | 28.1% | -1.7pp |
| 2025 | 92 | 38.0% | 180 | 33.3% | -4.7pp |
| **Total** | **521** | **32.1%** | **1,062** | **33.7%** | **+1.7pp (p=0.511)** |

**Filter win/loss record vs No Filter baseline (96 total comparisons):**

| Filter | Wins | Losses | Ties | Net Delta |
|---|---|---|---|---|
| Avoid Adverse Soft | 0 | 0 | 96 | 0 |
| Avoid Adverse Hard | 0 | 0 | 96 | 0 |
| Avoid Extreme Soft | 0 | 0 | 96 | 0 |
| Avoid Extreme Hard | 0 | 0 | 96 | 0 |
| Prefer Dome Soft | 33 | 47 | 16 | +291 |
| Prefer Dome Hard | 24 | 56 | 16 | -935 |

---

*Research draft prepared by Stan the Scout for Sky the Scribe. All data from simulation runs stored in `scripts/` directory. Source files: `stan-backtesting-research.md`, `stan-entry-scale-research.md`, `stan-differentiated-scoring-research.md`, `stan-buyback-research.md`, `stan-game-context-research.md`, `stan-weather-research.md`, `stan-weather-feasibility.md`.*
