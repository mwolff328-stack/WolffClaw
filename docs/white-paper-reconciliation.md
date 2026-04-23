# White Paper Reconciliation Report

**Prepared by:** Stan the Scout  
**Date:** 2026-04-21  
**Purpose:** Compare the backtesting white paper (written from 3-season data, 2023-2025) against the 5-season backtesting results (2021-2025) and flag every conclusion that changed, shifted, or needs qualification.

---

## 1. Summary of Changes

The 5-season expansion adds 2021 and 2022 data. Both were hard seasons (12.2% and 11.2% survival rates at n=10 vs 12.1-18.7% for 2023-2025). The additional data does not invalidate the white paper's structure, but it materially shifts several headline claims:

1. **Core/Satellite loses its crown at n=10.** Adaptive Blend 90/10→50/50 is the new no-buyback champion (144 vs 132). Core/Satellite's remarkable 3-season consistency (SD=1.7) was partly an artifact of a narrow sample; 5-season SD jumps to 9.0. SP Balanced (132, SD=3.4) ties Core/Satellite on total and beats it on consistency.

2. **The 70/30 Blend vs Pure Win Probability gap collapses at n=5.** From 50% advantage (57 vs 38) to 2.5% (82 vs 80). The 2021-2022 seasons favored Pure WP at small entry counts.

3. **SP Conservative edges 70/30 Blend at n=50 no-buyback.** 441 vs 438. The "simplicity reclaims the top" narrative is technically wrong, though the margin is negligible (3 EW).

4. **Buyback dominance shifts from SP Conservative to a split with SP Balanced.** SP Balanced wins n=5 and n=50 (Wk1-3 buyback). SP Conservative holds n=10 and n=20. The "SP Conservative wins everything with buybacks" claim needs qualification.

5. **SP Balanced 55/25/20 emerges as a major player.** Not present in the white paper as a recommended strategy at any entry count, but it wins or contends at multiple configurations in 5-season data (n=5 buyback, n=10 no-buyback #2, n=20 no-buyback #1, n=50 buyback).

6. **Most specific numbers in the paper need updating** (entry-week totals, efficiency percentages, SD values, avg per-season figures). Directional conclusions are mostly intact, but magnitudes change.

---

## 2. Finding-by-Finding Comparison

### 2.1 70/30 Blend as Baseline Champion (Section 4)

**White paper claim:** 70/30 Blend produces 50% more survival than Pure Win Probability across 3 seasons (57 vs 38 entry-weeks at n=5). SD=5.1 vs 7.8. "The 70/30 Blend's primary virtue is that it never has a catastrophic season."

**5-season result:** 70/30 Blend: 82 EW (SD=5.3). Pure Win Probability: 80 EW (SD=11.2). The gap shrinks from +50% to +2.5%. In 2021-2022, Pure WP outscored 70/30 (21+8=29 vs 15+10=25).

**Status:** SHIFTED. The directional finding holds (70/30 still beats Pure WP), but the magnitude collapses from a dramatic 50% to a marginal 2.5%.

**Recommended action:**
- Section 4 title and opening framing overstates the case. The "50% more survival" claim must be downgraded or reframed as a 3-season finding with qualification that the 5-season gap is much smaller.
- The "never has a catastrophic season" claim holds (70/30 worst season = 10 EW in 2022; Pure WP worst = 3 in 2024), but the ceiling gap narrowed.
- The 3-season validation table (Section 4.3) should note the sample expansion shows reduced advantage.
- The executive summary's first headline finding ("50%") needs updating.

---

### 2.2 80/20 Blend Produces Identical Results to Pure WP

**White paper claim:** "The 80/20 Blend produced identical results to Pure Win Probability... the contrarian weight needs to be at least 30% to create meaningfully different team selection."

**5-season result:** At n=5, 80/20 Blend: 73 EW, Pure WP: 80 EW. They are no longer identical; 80/20 actually underperforms Pure WP by 7 EW.

**Status:** NEEDS QUALIFICATION. The claim that 80/20 = Pure WP was true in 3 seasons but diverges in 5. The broader point (30% contrarian weight is needed for meaningful divergence) still holds directionally.

**Recommended action:** Soften from "identical" to "roughly equivalent" and note that with more data, 80/20 actually underperforms Pure WP slightly. The threshold claim remains valid.

---

### 2.3 Core/Satellite as n=10 Champion (Section 6)

**White paper claim:** Core/Satellite at n=10 is "the strongest finding in the entire study": 101 EW, +25 vs 70/30 Blend, +17 vs Mixed Portfolio, SD=1.7 (lowest variance of any strategy), season breakdown 33/36/32 "nearly identical results in every season tested."

**5-season result:** Core/Satellite at n=10: 132 EW, SD=9.0. Ranks 2nd/3rd (tied with SP Balanced at 132). Adaptive Blend wins at 144 (SD=6.9). Season breakdown: 17/14/33/36/32. The 2021-2022 seasons (17, 14) are dramatically below the 2023-2025 average.

**Status:** SHIFTED. Core/Satellite is no longer the n=10 champion. Its consistency story (SD 1.7) was a 3-season artifact; 5-season SD is 9.0. SP Balanced (132, SD=3.4) is the consistency leader. Adaptive Blend is the total-EW leader.

**Recommended action:**
- Section 6 requires the most significant rewrite. The "strongest finding in the entire study" framing must be revised.
- Core/Satellite remains a strong n=10 strategy (2nd/3rd place, +21 vs 70/30), but it is not the clear winner.
- The SD=1.7 and 33/36/32 consistency narrative must be updated or reframed with the caveat that 2021-2022 data weakens consistency significantly.
- The product recommendation for n=6-15 should shift to either Adaptive Blend (if optimizing total EW) or SP Balanced (if optimizing consistency), with Core/Satellite as a strong contender.
- The blockquote claiming "32% more survival... with the lowest variance" needs updating: 5-season advantage is 19% (132/111), not 32%, and variance is no longer lowest.

---

### 2.4 Mixed Portfolio as n=16-30 Champion (Section 5 / Decision Framework)

**White paper claim:** Mixed Portfolio wins at n=20 no-buyback. The decision framework recommends Mixed Portfolio for 16-30 entries.

**5-season result:** SP Balanced wins n=20 at 221 EW (SD=6.2). Adaptive Blend 216. Mixed Portfolio 214. 70/30 Blend 198. Core/Satellite 194.

**Status:** SHIFTED. Mixed Portfolio drops from 1st to 3rd. SP Balanced is the new champion, also with excellent consistency.

**Recommended action:**
- Decision framework tree should update n=16-30 recommendation from Mixed Portfolio to SP Balanced.
- Section 5 n=20 results table needs 5-season update.
- The narrative about "true diversification across strategy classes creates genuine option value" for Mixed Portfolio at n=20 is weakened, though Mixed Portfolio remains competitive.

---

### 2.5 70/30 Blend Reclaiming at n=50 (Section 5)

**White paper claim:** "The 70/30 Blend wins again" at n=50 with 295 EW. "Sophisticated strategies collapse."

**5-season result:** SP Conservative wins n=50 with 441. 70/30 Blend is 2nd at 438. Gap is only 3 EW. Core/Satellite 3rd at 430 (but with best consistency: SD=5.7 vs 18.5/19.0).

**Status:** NEEDS QUALIFICATION. 70/30 is no longer #1 at n=50 but the difference is negligible (3 EW). The broader narrative (simple strategies hold up at scale) is confirmed, though the specific winner shifted to SP Conservative. The "sophisticated strategies collapse" claim is weakened: Core/Satellite (430, SD=5.7) is remarkably consistent at n=50 in 5-season data.

**Recommended action:**
- Update to acknowledge SP Conservative as the marginal winner at n=50 no-buyback, with 70/30 essentially tied.
- Note that Core/Satellite, far from collapsing, is the most consistent n=50 strategy (SD=5.7, CV=0.067).
- The "Adaptive Blend catastrophe" narrative (2024 collapse) remains valid and even slightly confirmed (5-season SD=29.6 at n=50).
- The team exhaustion explanation remains sound.

---

### 2.6 Buyback Findings - SP Conservative Dominance (Section 7)

**White paper claim:** "SP Conservative wins everything -- with buybacks" at all four entry counts. "The winner completely reverses at every portfolio size." Table shows SP Conservative winning n=5 (78), n=10 (165), n=20 (248), n=50 (463).

**5-season result (Wk1-3 buyback):**
- n=5: **SP Balanced wins** (128) over SP Conservative (121)
- n=10: SP Conservative wins (239) ✓
- n=20: SP Conservative wins (357) ✓
- n=50: **SP Balanced wins** (736) over SP Conservative (733)

**Status:** SHIFTED. SP Conservative does not win "everything" with buybacks. It wins n=10 and n=20. SP Balanced wins n=5 and n=50 (Wk1-3). The broader claim that conservative-family strategies dominate buyback pools is confirmed, but the specific "SP Conservative at all four" needs correction.

**Recommended action:**
- Section 7 heading and framing need nuancing. "SP Conservative wins everything" becomes "conservative strategies (SP Conservative and SP Balanced) dominate buyback pools."
- The buyback uplift table should be updated with 5-season numbers.
- The n=5 and n=50 buyback recommendations should shift to SP Balanced, or recommend "SP Conservative/SP Balanced family" as the approach.
- The split-strategy finding (none beat simple conservative) likely still holds but wasn't retested in 5-season data. Note this.
- Buyback ROI per-buyback numbers were from 3-season data and weren't recalculated in 5-season runs. Flag as needing validation.

---

### 2.7 The "Three Myths" (Section 8)

**White paper claim:** Divisional avoidance, home field preference, and weather avoidance are all empirically rejected.

**5-season data impact:** The 5-season backtesting did NOT include filter analysis. Round 9 (divisional/home) used 3 seasons (2023-2025). Round 10 (weather) used 6 seasons (2020-2025). The 5-season expansion tested strategies x entry counts x buyback configs but not filter modes.

**Status:** NOT DIRECTLY TESTED in 5-season expansion.

**Recommended action:**
- Note explicitly that the "three myths" findings rest on their original data: 3 seasons for divisional/home, 6 seasons for weather.
- The weather finding (p=0.511) used 6 seasons and is the most robust.
- Divisional and home field findings use only 3 seasons and would benefit from 5-season retesting, but this wasn't done. Flag as a limitation.
- No changes needed to the myth conclusions themselves, but the paper should be transparent about which findings use which sample sizes.

---

### 2.8 The Decision Framework Table (Section 9)

**White paper framework:**

| Pool Type | N | Strategy | EW/season |
|---|---|---|---|
| Non-buyback | 5 | SP Conservative | 21.3 |
| Non-buyback | 10 | Core/Satellite | 33.7 |
| Non-buyback | 20 | Core/Satellite + Div Soft | 49.0 |
| Non-buyback | 50 | 70/30 Blend | 98.3 |
| Buyback Wk1-3 | 5 | SP Conservative | 26.0 |
| Buyback Wk1-3 | 10 | SP Conservative | 55.0 |
| Buyback Wk1-3 | 20 | SP Conservative | 82.7 |
| Buyback Wk1-3 | 50 | SP Conservative | 154.3 |

**5-season revised framework:**

| Pool Type | N | Strategy | EW/season |
|---|---|---|---|
| Non-buyback | 5 | 70/30 Blend | 16.4 |
| Non-buyback | 10 | Adaptive Blend 90/10→50/50 | 28.8 |
| Non-buyback | 20 | SP Balanced 55/25/20 | 44.2 |
| Non-buyback | 50 | SP Conservative | 88.2 |
| Buyback Wk1-3 | 5 | SP Balanced 55/25/20 | 25.6 |
| Buyback Wk1-3 | 10 | SP Conservative | 47.8 |
| Buyback Wk1-3 | 20 | SP Conservative | 71.4 |
| Buyback Wk1-3 | 50 | SP Balanced 55/25/20 | 147.2 |

**Status:** SHIFTED at 6 of 8 positions.

**Recommended action:** Complete rewrite of the decision framework table and the master decision tree. See Section 4 below for prioritized edits.

---

### 2.9 Specific Numbers Cited Throughout

**White paper claim (Section 1):** "a 10-entry portfolio where every entry runs the same pick-the-biggest-favorite strategy produces 24% fewer entry-weeks than a portfolio built with intentional role design."

**5-season result:** Core/Satellite 132 vs Pure WP 130 at n=10. That's only 1.5% more, not 24%. If comparing to Adaptive Blend (the new winner): 144 vs 130 = 10.8%.

**Status:** REVERSED in magnitude. The specific "24%" figure does not hold at all.

**Recommended action:** Recompute from 5-season data. The most defensible comparison is Adaptive Blend (144) vs 70/30 Blend (111) = +30%, or vs Pure WP (130) = +10.8%.

---

**White paper claim (Section 6):** "SP Production leads by 24%" at n=10 (94 vs 76 for 70/30 over 3 seasons).

**5-season result:** SP Production at n=10 = 97, 70/30 = 111. SP Production actually underperforms 70/30 by 13% in 5-season data. This is a reversal.

**Status:** REVERSED. SP Production was a 3-season favorite at n=10 but drops to 13th of 14 strategies in 5-season data at n=10.

**Recommended action:** Remove SP Production as a recommended strategy. The paper's Section 5 n=10 table needs full replacement.

---

**White paper claim (Section 6):** 70/30 Blend efficiency drops from 21.1% at n=5 to 14.1% at n=10.

**5-season result:** 70/30 efficiency at n=5 = 18.2%, at n=10 = 12.3%. The drop pattern holds but both numbers are lower.

**Status:** CONFIRMED directionally. Numbers need updating.

---

## 3. New Findings Not in the White Paper

### 3.1 SP Balanced 55/25/20 as a Major Strategy

SP Balanced is mentioned only in passing in the white paper (Rounds 4-5 appendix, never in the main narrative). In 5-season data, it emerges as:
- n=5 buyback champion (128 EW)
- n=10 no-buyback tied 2nd (132 EW, lowest SD at 3.4)
- n=20 no-buyback champion (221 EW)
- n=50 buyback Wk1-3 champion (736 EW)

This is arguably the most well-rounded strategy in the 5-season dataset. The white paper should introduce it as a primary strategy, not a footnote.

### 3.2 Adaptive Blend 90/10→50/50 as n=10 Champion

Not discussed anywhere in the white paper's main text. Mentioned in Round 6 appendix as "Adaptive Blend" with SD=11.0. In 5-season data, it's the clear n=10 no-buyback winner at 144 EW with reasonable consistency (SD=6.9). The paper needs to introduce this strategy and explain its mechanics.

### 3.3 Season Difficulty Variation

The 5-season data includes a "Season Difficulty" table showing all five seasons are "Hard" (11.2-18.7% survival rate at n=10). The 2021 and 2022 seasons are the hardest. This contextualizes why many strategies perform worse in the expanded dataset and is useful framing for readers.

### 3.4 Regime Analysis (Early vs Late Seasons)

The 5-season report includes regime analysis (2021-2022 vs 2023-2025) showing which strategies improved vs declined over time. Key finding: Core/Satellite improved the most from early to late (+18.2 at n=10), explaining why it looked dominant in 3-season data. SP Balanced was remarkably stable across regimes (+2.3 at n=10). This regime sensitivity is important context the paper doesn't address.

### 3.5 Core/Satellite Consistency at n=50

Core/Satellite at n=50 has the lowest SD (5.7) and lowest CV (0.067) of any strategy. This is a genuinely new finding: at scale, Core/Satellite doesn't collapse like other sophisticated strategies. The white paper's narrative that "sophisticated strategies self-destruct" at n=50 is not universally true.

### 3.6 Pure Win Probability Recovery

Pure Win Probability at n=10 jumps to 130 EW in 5-season data (near the top). The 2021 and 2025 seasons (28 and 43) were strong for naive strategies. The white paper's framing of Pure WP as clearly inferior is less convincing with more data.

---

## 4. Recommended White Paper Updates

Prioritized from most critical to least.

### P1: Critical (Headline claims that are wrong)

1. **Rewrite Section 6 (Core/Satellite)** - Remove "strongest finding in the entire study." Core/Satellite is no longer the n=10 champion, its consistency story collapsed (SD 1.7 → 9.0), and the 32% advantage claim is now 19%. Introduce Adaptive Blend and SP Balanced as the new leaders.

2. **Update the Decision Framework (Section 9)** - 6 of 8 positions changed. The master decision tree needs rebuilding. The "strategy performance by configuration" table needs all new numbers.

3. **Revise the 50% headline (Sections 1 and 4)** - The "50% more survival" claim (70/30 vs Pure WP at n=5) shrinks to ~2.5% in 5-season data. This is the opening hook of the paper and the executive summary's first headline. Must be restated or reframed.

4. **Fix the "24% fewer entry-weeks" claim (Section 1)** - The specific opening-section number doesn't hold. Recompute from 5-season data.

5. **Qualify the buyback universality claim (Section 7)** - SP Conservative does not win all four entry counts with buybacks. SP Balanced wins n=5 and n=50. Reframe as "conservative-family strategies dominate."

### P2: Important (Materially shifted findings)

6. **Update n=20 no-buyback recommendation** - From Mixed Portfolio to SP Balanced.

7. **Update n=50 no-buyback winner** - From 70/30 Blend to SP Conservative (marginal).

8. **Introduce SP Balanced 55/25/20** - Currently absent from the main narrative. Needs a paragraph or subsection explaining where it wins and why.

9. **Update Section 5 n=10 table** - SP Production is no longer the n=10 leader. The entire inflection-point narrative needs reworking.

10. **Revise the executive summary** - All three headline findings need number updates.

### P3: Minor (Still true but numbers changed)

11. **Update all entry-week totals** from 3-season to 5-season across every table.

12. **Update efficiency percentages** throughout.

13. **Update the methodology section** - Run count changes if 5-season runs are included. The "1,904 simulations" figure needs revision (5-season adds 840 runs).

14. **Add a "Season Difficulty" or "Regime Analysis" section** explaining the harder 2021-2022 seasons.

15. **Clarify which analyses used which sample sizes** - Myths section uses 3-season (divisional/home) and 6-season (weather). Main strategy findings now have 5-season data. Be explicit.

16. **Note that buyback ROI analysis and split-strategy analysis** were not re-run in 5-season. Flag as 3-season-only findings requiring validation.

---

## 5. Numbers That Need Updating

### Key Metrics - No Buyback

| Number Location | White Paper Value (3-season) | 5-Season Value | Change | Notes |
|---|---|---|---|---|
| 70/30 vs Pure WP at n=5 (total EW) | 57 vs 38 (+50%) | 82 vs 80 (+2.5%) | **Major shrink** | Opening hook of the paper |
| 70/30 SD at n=5 | 5.1 | 5.3 | Minor | |
| Pure WP SD at n=5 | 7.8 | 11.2 | Increased | |
| 70/30 efficiency at n=5 | 21.1% | 18.2% | Decreased | |
| Core/Satellite total at n=10 | 101 | 132 | +31 (5 seasons) | No longer champion |
| Core/Satellite SD at n=10 | 1.7 | 9.0 | **5.3x increase** | Consistency claim collapses |
| Core/Satellite efficiency at n=10 | 18.7% | 14.7% | Decreased | |
| Core/Satellite vs 70/30 at n=10 | +25 (+32%) | +21 (+19%) | Advantage shrunk | |
| Core/Satellite vs Mixed at n=10 | +17 | +4 | **Major shrink** | |
| n=10 champion | Core/Satellite (101) | Adaptive Blend (144) | **Changed** | |
| n=10 champion SD | 1.7 | 6.9 (Adaptive) / 3.4 (SP Balanced) | Changed | |
| SP Production at n=10 | 94 (+18 vs 70/30) | 97 (-14 vs 70/30) | **Reversed** | SP Prod underperforms 70/30 |
| Mixed Portfolio at n=20 | 142 | 214 | +72 (5 seasons) | No longer champion |
| n=20 champion | Mixed Portfolio (142) | SP Balanced (221) | **Changed** | |
| 70/30 at n=50 | 295 (#1) | 438 (#2) | No longer #1 | SP Conservative 441 wins |
| n=50 champion | 70/30 Blend (295) | SP Conservative (441) | **Changed** | Marginal (3 EW gap) |
| 70/30 SD at n=50 | 7.6 | 19.0 | Increased | |
| Adaptive Blend worst SD at n=50 | 31.1 | 29.6 | Slightly improved | Narrative holds |

### Key Metrics - Buyback (Wk1-3)

| Number Location | White Paper Value (3-season) | 5-Season Value | Change | Notes |
|---|---|---|---|---|
| n=5 buyback champion | SP Conservative (78) | SP Balanced (128) | **Changed** | |
| n=10 buyback champion | SP Conservative (165) | SP Conservative (239) | Confirmed | Value changed |
| n=20 buyback champion | SP Conservative (248) | SP Conservative (357) | Confirmed | Value changed |
| n=50 buyback champion | SP Conservative (463) | SP Balanced (736) | **Changed** | |
| n=10 buyback uplift | +63.4% vs no-BB winner | +66% (239 vs 144) | Confirmed | |
| n=20 buyback uplift | +90.8% | +61.4% (357 vs 221) | Decreased | |
| Buyback ROI (EW/BB) at n=10 | 4.15 | Not retested | Unknown | Flag as 3-season only |

### Framework Table - Avg EW/Season

| Config | White Paper (3-season avg) | 5-Season Avg | Change |
|---|---|---|---|
| Non-BB n=5 best | 21.3 (SP Conservative) | 17.4 (Mixed Portfolio) | Changed strategy and value |
| Non-BB n=10 best | 33.7 (Core/Satellite) | 28.8 (Adaptive Blend) | Changed strategy and value |
| Non-BB n=20 best | 49.0 (Core/Sat + filter) | 44.2 (SP Balanced, no filter) | Changed strategy and value |
| Non-BB n=50 best | 98.3 (70/30 Blend) | 88.2 (SP Conservative) | Changed strategy and value |
| BB Wk1-3 n=5 | 26.0 (SP Conservative) | 25.6 (SP Balanced) | Changed strategy, value similar |
| BB Wk1-3 n=10 | 55.0 (SP Conservative) | 47.8 (SP Conservative) | Same strategy, lower value |
| BB Wk1-3 n=20 | 82.7 (SP Conservative) | 71.4 (SP Conservative) | Same strategy, lower value |
| BB Wk1-3 n=50 | 154.3 (SP Conservative) | 147.2 (SP Balanced) | Changed strategy, lower value |

### Section 1 Opening Numbers

| Claim | White Paper | 5-Season | Action |
|---|---|---|---|
| "24% fewer entry-weeks" (undiversified vs role-designed 10-entry) | 24% (76 vs 101) | ~1.5% (130 vs 132 for C/S) or ~23% (111 vs 144 for Adaptive) | Recompute and restate |
| "1,904 simulation runs" | 1,904 | 2,744 (1,904 + 840) | Update if including 5-season runs |
| "six NFL seasons" | 6 (but only 3 for main findings) | 5 for main findings, 6 for weather | Clarify |

### Numbers That Are Unchanged

| Item | Value | Status |
|---|---|---|
| Weather p-value (dome vs outdoor) | 0.511 | Unchanged (same Round 10 data) |
| Divisional avg win rate gap | -2.4pp | Unchanged (same Round 9 data, not retested) |
| Home field avg win rate gap | -0.7pp | Unchanged (same Round 9 data, not retested) |
| Adverse/extreme weather filters | Inert (0 wins, 0 losses, 96 ties) | Unchanged |
| Win probability formula (13.5 SD) | Unchanged | Unchanged |
| Team exhaustion mechanism explanation | Valid | Unchanged (confirmed directionally) |
| Split strategies losing to simple conservative (buyback) | Not retested | Flag as 3-season finding |
| Core/Satellite architectural principle (different scoring functions) | Valid | Unchanged, though magnitude shifted |
| Anti-Overlap = 70/30 Blend null result | Not retested | Likely unchanged |

---

*End of reconciliation report. The white paper's structural logic and explanatory framework are sound. The primary issue is that specific numbers, rankings, and "strongest finding" language are calibrated to 3 seasons and need recalibration to the expanded dataset.*
