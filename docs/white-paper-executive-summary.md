# The systematic edge: executive summary

**Research by SurvivorPulse | April 2026 | 1,904 simulations | 6 NFL seasons**

---

## What we found

We ran 10 rounds of backtesting across six NFL seasons to answer the question serious multi-entry survivor pool players have never had a clean answer to: what strategy actually maximizes survival when you're running 10, 20, or 50 entries?

Three headline findings:

**1. A simple contrarian-blended formula beats pure win-probability picking by 50%**

Weighting win probability at 70% and contrarian appeal (inverse of pick share) at 30% produces 57 entry-weeks across three seasons vs 38 for pure win-probability picking. This isn't complicated — it just says: pick safe teams, and among teams of similar safety, prefer the ones fewer people are on. The 80/20 blend doesn't work; 30% contrarian weight is the minimum that creates meaningfully different team selection.

**2. Portfolio size changes which strategy is optimal — dramatically**

At 1–5 entries, the 70/30 Blend is the clear best. At 10 entries, seven strategies beat it. At 50 entries, it wins again because sophisticated strategies self-destruct under team exhaustion. The most important finding: at 10 entries, a Core/Satellite architecture (60% of entries on the 70/30 Blend, 40% on a higher-EV formula) produces **32% more survival than a single strategy with the lowest variance of any design tested.**

**3. Pool type overrides everything**

When buybacks are available, the optimal strategy reverses completely at every portfolio size. SP Conservative — which doesn't win at any entry count without buybacks — wins at all four entry counts with buybacks. At n=10, it produces 63% more entry-weeks than the best no-buyback strategy. Using the wrong strategy for your pool type leaves 50–100% performance on the table.

---

## What doesn't work

Three pieces of conventional wisdom were tested empirically and rejected:

- **Avoid divisional games:** Divisional favorites actually win at a slightly *higher* rate on average across three seasons. Not a reliable filter.
- **Prefer home teams:** Home vs road win rate difference is -0.7 percentage points across three seasons. Negligible and inconsistent.
- **Avoid bad weather:** Not statistically significant (p=0.511). Adverse weather filters change zero picks in simulation because the base scoring function already avoids those games.

---

## The decision framework

| Pool type | Portfolio size | Strategy | Avg entry-weeks/season |
|---|---|---|---|
| No buyback | 1–5 | 70/30 Blend | ~19 |
| **No buyback** | **6–15** | **Core/Satellite (60/40)** | **33.7** |
| No buyback | 16–30 | Mixed Portfolio | ~44 |
| No buyback | 31–50+ | 70/30 Blend | 98.3 |
| **Buyback (any window)** | **Any** | **SP Conservative** | **26–154** |

**Three questions before you pick:**
1. Does my pool have buybacks? → Yes: SP Conservative, always.
2. How many entries am I running? → Match to the table above.
3. Any strong conviction about game types? → Divisional avoidance is defensible as an optional toggle at n=10-20. Home field and weather filters are not.

---

*Full methodology, all data tables, and round-by-round findings: docs/white-paper-final.md*
