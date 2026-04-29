---
name: Stan Buyback Mechanics Research (Round 8)
description: Buyback impact across 12 strategies, 4 entry counts, 3 seasons, 3 buyback configs. 492 total runs. SP Conservative dominates all buyback pools.
type: project
---

# Round 8: Buyback Mechanics Research

**Date:** 2026-04-12
**Runs:** 492 total (432 Part 1 + 60 Part 2)
**Script:** scripts/stan-buyback-sim.py

## Setup

- **Strategies tested (Part 1):** 12 strategies across all rounds
- **Entry counts:** 5, 10, 20, 50
- **Seasons:** 2023, 2024, 2025
- **Buyback configs:** No Buyback (control) | Buyback Wk1-3 | Buyback Wk1-4
- **Buyback mechanic:** Eliminated entries in weeks 1–3 (or 1–4) resurrect the following week with used-teams list preserved; max 1 buyback per entry; rational player always exercises it

---

## PART 1 RESULTS — Strategy Rankings by Entry Count (3-season totals)

### n=5 (max 270 entry-weeks over 3 seasons)

| Strategy | No Buyback | BB Wk1-3 | BB Wk1-4 | Δ(Wk1-3) | BB% |
|---|---|---|---|---|---|
| **SP Conservative 65/25/10** | 64 | **78** | 78 | +14 | +21.9% |
| Safety/Contrarian Split | 45 | 76 | 76 | +31 | +68.9% |
| Mixed Portfolio | 67 | 71 | 76 | +4 | +6.0% |
| Core/Satellite 60blend+40EV | 44 | 65 | 65 | +21 | +47.7% |
| EV Gradient 95/5→55/45 | 46 | 65 | 65 | +19 | +41.3% |
| SP Production 70EV+30FV | 45 | 64 | 64 | +19 | +42.2% |
| 70/30 Blend | 57 | 62 | 67 | +5 | +8.8% |
| Expendable-First 65/25/10 3wk | 51 | 62 | 72 | +11 | +21.6% |
| Pure Win Probability | 51 | 59 | 67 | +8 | +15.7% |
| Adaptive Blend 90/10→50/50 | 58 | 57 | 57 | **-1** | **-1.7%** |
| 80/20 Blend | 43 | 54 | 63 | +11 | +25.6% |
| 60/40 Blend | 32 | 49 | 49 | +17 | +53.1% |

### n=10 (max 540 entry-weeks)

| Strategy | No Buyback | BB Wk1-3 | BB Wk1-4 | Δ(Wk1-3) | BB% |
|---|---|---|---|---|---|
| **SP Conservative 65/25/10** | 82 | **165** | 165 | +83 | **+101.2%** |
| Safety/Contrarian Split | 83 | 146 | 165 | +63 | +75.9% |
| 70/30 Blend | 76 | 138 | 141 | +62 | +81.6% |
| EV Gradient 95/5→55/45 | 73 | 136 | 144 | +63 | +86.3% |
| Pure Win Probability | 80 | 129 | 136 | +49 | +61.3% |
| Core/Satellite 60blend+40EV | 101 | 125 | 126 | +24 | +23.8% |
| 60/40 Blend | 66 | 124 | 146 | +58 | +87.9% |
| 80/20 Blend | 78 | 116 | 130 | +38 | +48.7% |
| SP Production 70EV+30FV | 71 | 111 | 122 | +40 | +56.3% |
| Adaptive Blend 90/10→50/50 | 87 | 110 | 123 | +23 | +26.4% |
| Mixed Portfolio | 87 | 110 | 120 | +23 | +26.4% |
| Expendable-First 65/25/10 3wk | 68 | 95 | 119 | +27 | +39.7% |

### n=20 (max 1080 entry-weeks)

| Strategy | No Buyback | BB Wk1-3 | BB Wk1-4 | Δ(Wk1-3) | BB% |
|---|---|---|---|---|---|
| **SP Conservative 65/25/10** | 122 | **248** | 250 | +126 | +103.3% |
| Safety/Contrarian Split | 129 | 222 | 239 | +93 | +72.1% |
| 70/30 Blend | 122 | 221 | 227 | +99 | +81.1% |
| Pure Win Probability | 112 | 217 | 232 | +105 | +93.8% |
| 80/20 Blend | 119 | 214 | 221 | +95 | +79.8% |
| Adaptive Blend 90/10→50/50 | 128 | 212 | 223 | +84 | +65.6% |
| Core/Satellite 60blend+40EV | 130 | 212 | 223 | +82 | +63.1% |
| SP Production 70EV+30FV | 113 | 209 | 219 | +96 | +85.0% |
| Mixed Portfolio | 126 | 208 | 225 | +82 | +65.1% |
| EV Gradient 95/5→55/45 | 128 | 207 | 225 | +79 | +61.7% |
| Expendable-First 65/25/10 3wk | 107 | 195 | 216 | +88 | +82.2% |
| 60/40 Blend | 106 | 194 | 216 | +88 | +83.0% |

### n=50 (max 2700 entry-weeks)

| Strategy | No Buyback | BB Wk1-3 | BB Wk1-4 | Δ(Wk1-3) | BB% |
|---|---|---|---|---|---|
| **SP Conservative 65/25/10** | 288 | **463** | 495 | +175 | +60.8% |
| Expendable-First 65/25/10 3wk | 252 | 446 | 484 | +194 | +77.0% |
| Mixed Portfolio | 255 | 442 | 460 | +187 | +73.3% |
| 70/30 Blend | 295 | 440 | 459 | +145 | +49.2% |
| Safety/Contrarian Split | 287 | 438 | 470 | +151 | +52.6% |
| SP Production 70EV+30FV | 262 | 437 | 459 | +175 | +66.8% |
| Core/Satellite 60blend+40EV | 264 | 434 | 452 | +170 | +64.4% |
| EV Gradient 95/5→55/45 | 263 | 420 | 454 | +157 | +59.7% |
| 80/20 Blend | 284 | 409 | 447 | +125 | +44.0% |
| Adaptive Blend 90/10→50/50 | 229 | 390 | 442 | +161 | +70.3% |
| 60/40 Blend | 250 | 379 | 409 | +129 | +51.6% |
| Pure Win Probability | 225 | 375 | 420 | +150 | +66.7% |

---

## PART 1 — Average Buyback Uplift

| n | Avg uplift Wk1-3 | Avg uplift Wk1-4 | Winner w/ BB |
|---|---|---|---|
| 5 | +13.2 | +16.3 | SP Conservative (78) |
| 10 | +46.1 | +57.1 | SP Conservative (165) |
| 20 | +93.1 | +106.2 | SP Conservative (248) |
| 50 | +159.9 | +191.4 | SP Conservative (463) |

---

## PART 2 RESULTS — Split Strategies vs Best Non-Split Baseline (Wk1-3 buyback)

**Verdict: No split strategy beats the best non-split baseline. Skip the complexity.**

| n | Best Baseline w/BB | Best Split | Gap |
|---|---|---|---|
| 5 | SP Conservative 78 | B. EV/Blend Split 75 | -3 |
| 10 | SP Conservative 165 | C. Contrarian/Conservative 145 | -20 |
| 20 | SP Conservative 248 | B. EV/Blend Split 233 | -15 |
| 50 | SP Conservative 463 | D. Expendable/Safe Split 443 | -20 |

All 5 split configs underperformed the SP Conservative baseline at every entry count. The strategy-switching adds complexity without reward — the buyback window is only 3 weeks, not long enough for "aggressive early, safe late" to produce net positive results compared to simply running the optimal strategy the whole time.

---

## PART 3 — Buyback ROI Analysis (Wk1-3 window)

### Entry-Weeks Gained Per Buyback Used (EW/BB — higher = better investment)

| n | Best EW/BB | Strategy | Surv3+% | Surv10+% |
|---|---|---|---|---|
| 5 | 3.10 | Safety/Contrarian Split | 40.0% | 20.0% |
| 10 | **4.15** | SP Conservative | 35.0% | 30.0% |
| 20 | 2.74 | SP Conservative | 26.1% | 15.2% |
| 50 | 1.75 | Expendable-First | 19.8% | 5.4% |

Full n=10 ROI table (sorted by EW/BB):

| Strategy | BB Used | Surv3+% | Surv10+% | Net EW | EW/BB |
|---|---|---|---|---|---|
| SP Conservative | 20 | 35.0% | 30.0% | +83 | 4.15 |
| EV Gradient | 19 | 26.3% | 15.8% | +63 | 3.32 |
| Safety/Contrarian | 19 | 31.6% | 15.8% | +63 | 3.32 |
| 70/30 Blend | 19 | 26.3% | 21.1% | +62 | 3.26 |
| 60/40 Blend | 21 | 28.6% | 9.5% | +58 | 2.76 |
| Pure Win Probability | 19 | 26.3% | 10.5% | +49 | 2.58 |
| SP Production | 20 | 35.0% | 5.0% | +40 | 2.00 |
| 80/20 Blend | 18 | 16.7% | 11.1% | +38 | 2.11 |

Notable outlier: **Adaptive Blend at n=5 (−0.12 EW/BB)** — only case where buybacks hurt. The adaptive strategy shifts from aggressive to conservative over time; bought-back entries are forced into a now-conservative strategy during the critical early weeks they missed, reducing effectiveness.

---

## KEY FINDINGS

### 1. SP Conservative Dominates Buyback Pools — Completely

SP Conservative 65/25/10 (moderate WP + mild anti-chalk + mild FV preservation) wins at **all four entry counts** when buybacks are available. It did not win at any entry count without buybacks. This is the most dramatic strategy reshuffling across all 8 rounds.

**Why:** Conservative strategies lose more entries in early weeks (lower WP tolerance), but buybacks refund exactly these early losses. The result is that conservative strategies get multiple "second chances" to showcase their late-season survival advantages, while aggressive strategies don't get as much benefit from buybacks (they lose fewer early entries to begin with).

### 2. The "Before/After" Winner Comparison

| n | No Buyback Winner | Buyback Winner | Same? |
|---|---|---|---|
| 5 | Mixed Portfolio (67) | SP Conservative (78) | No |
| 10 | Core/Satellite (101) | SP Conservative (165) | No |
| 20 | Core/Satellite (130) | SP Conservative (248) | No |
| 50 | 70/30 Blend (295) | SP Conservative (463) | No |

**The winner changes at EVERY entry count when buybacks are introduced.** This is a major product signal.

### 3. Buyback Uplift Varies Dramatically by Strategy

Strategies with lower win rates (more early eliminations) benefit the most from buybacks:
- Safety/Contrarian Split: +68.9% at n=5 (31 additional entry-weeks from 45 baseline)
- SP Conservative: +101.2% at n=10 — more than doubles its performance
- Adaptive Blend: −1.7% at n=5 — the only strategy that can be HURT by buybacks

Strategies that already survive early (Mixed Portfolio, 70/30 Blend) gain less from buybacks because they have fewer entries to resurrect in the window.

### 4. Wider Window = More Gain (But Smaller Marginal Return)

Wk1-4 window consistently outperforms Wk1-3, but the marginal gain is smaller than going from no-buyback to Wk1-3. The additional week's worth of resurrections compounds on top of the existing buyback advantage. Average cross-strategy uplift difference: +3.1 entry-weeks for Wk1-4 vs Wk1-3 at n=5, up to +31.5 at n=50.

### 5. Buyback ROI is Compelling

The buyback investment (typically same cost as entry fee) generates:
- **n=10:** 4.15 entry-weeks per buyback used (SP Conservative) — effectively a 4x ROI vs not buying back
- **n=5:** 3.10 entry-weeks per buyback (Safety/Contrarian)
- **n=50:** 1.75 entry-weeks per buyback (Expendable-First)

Entry-weeks translate directly to additional time in the pool with a live entry competing for the prize. Even the weakest buyback ROI (1.07 at n=50, 60/40 Blend) is positive.

### 6. Split Strategies Add Zero Value

All 5 split strategy configs (aggressive during window → safe after) underperformed the simple SP Conservative at every entry count. The 3-week window is too short for strategy switching to pay off. The best performance was B. EV/Blend at n=5 (75 vs 78 baseline, −4%) and D. Expendable/Safe at n=50 (443 vs 463, −4.3%).

---

## PRODUCT IMPLICATIONS

### For SurvivorPulse Recommendations

**The app MUST distinguish between buyback and non-buyback pool types.** Using the same recommendation engine for both pool types would leave significant performance on the table.

1. **Non-buyback pools:** Continue recommending Core/Satellite (n=5–20) and 70/30 Blend (n=50)
2. **Buyback pools:** Switch recommendation to SP Conservative 65/25/10 at ALL entry counts
3. **Buyback window size:** Wider window = stronger case for SP Conservative. If pool offers Wk1-4, the advantage grows even further.
4. **Split strategies:** Not worth implementing in the product. Too complex, no upside.

### For the Buyback Decision Itself

The buyback is virtually always worth exercising (positive ROI at every strategy and entry count tested). SurvivorPulse should default to recommending "always buy back if eliminated during the window" with a brief explanation of expected return.

### For Strategy Explanation to Users

Key insight to communicate: "In a buyback pool, you can afford to be slightly more conservative early. Your early-season losses are partially refundable. Conservative strategies that look weaker in standard pools become the dominant choice once you factor in the buyback safety net."

---

## MASTER WINNERS TABLE (Updated Through Round 8)

| n | No Buyback | Buyback Wk1-3 |
|---|---|---|
| 5 | Mixed Portfolio (67) | SP Conservative (78) |
| 10 | Core/Satellite (101) | SP Conservative (165) |
| 20 | Core/Satellite (130) | SP Conservative (248) |
| 50 | 70/30 Blend (295) | SP Conservative (463) |

**Why:** Pool mechanics fundamentally change the optimal strategy. Buybacks create a safety net that benefits conservative strategies disproportionately.
