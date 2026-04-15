# White paper social snippets

**Source:** The Systematic Edge — SurvivorPulse Research, April 2026  
**Usage:** Each block is self-contained. Platform-ready for X, Reddit, LinkedIn.

---

## Snippet 1 — The core finding

Your 10-entry survivor portfolio is probably running the same strategy 10 times.

That's costing you 24% of your survival rate.

We ran 1,904 simulations across 6 NFL seasons and found that a structured Core/Satellite architecture — 60% of entries on a conservative blend, 40% on an EV formula — produces 32% more survival than a single strategy with the lowest variance of any design we tested.

The entries aren't the problem. The architecture is.

---

## Snippet 2 — The 70/30 formula

The simplest thing that actually works in survivor pools:

`score = 0.70 × winProb + 0.30 × (1 − pickShare/100)`

70% win probability + 30% contrarian. Nothing else.

Across 3 NFL seasons, this formula produced 57 entry-weeks vs 38 for pure win-probability picking. That's 50% more survival. The 80/20 blend doesn't work — 30% is the minimum contrarian weight that creates meaningfully different team selection from the chalk crowd.

---

## Snippet 3 — The chalk bust mechanism

Here's why pure "pick the biggest favorite" fails:

Popular teams lose ~25–30% of the time. When they do, everyone who picked them gets eliminated in the same week. That's not variance. That's correlated risk.

By systematically underweighting the most popular picks, the 70/30 Blend sidesteps those spikes. It doesn't pick better teams — it picks the same strong teams while avoiding the ones that will take half the field out with them when they lose.

---

## Snippet 4 — The pool type override

The most important finding in 1,904 simulation runs:

SP Conservative — a strategy that didn't win at any portfolio size without buybacks — wins at ALL four portfolio sizes when buybacks are available.

At n=10: 165 entry-weeks with buybacks vs 101 without. That's a 63% improvement. At n=20: 248 vs 130. That's 90%.

If your pool has buybacks and you're not running SP Conservative, you're leaving 50–100% of your performance on the table.

---

## Snippet 5 — The scale inflection

At 5 entries, the 70/30 Blend is the best strategy.  
At 10 entries, 7 strategies beat it.  
At 50 entries, it's #1 again.

The inflection at 10 entries happens because sophisticated strategies account for future team value in ways that matter more when you're coordinating picks across 10 entries. The reversal at 50 entries happens because team exhaustion collapses all sophisticated strategies — you run out of unique picks, and the clustering kills you.

Portfolio size isn't context. It changes which strategy is optimal.

---

## Snippet 6 — The buyback ROI

At n=10, SP Conservative generates 4.15 additional entry-weeks per buyback used.

In a $100 entry fee pool, a $100 buyback keeps an entry alive for an expected 4+ additional weeks. 30–40% of bought-back entries survive at least 3 more weeks.

The only negative-ROI buyback case we found: Adaptive Blend at n=5. Every other strategy at every other portfolio size: positive ROI.

Always take the buyback.

---

## Snippet 7 — What doesn't work: home field

Home field advantage in survivor-relevant NFL games: not a real edge.

Data from 3 seasons: home teams win at 69.7%, road teams at 70.4%. A 0.7pp gap.

2023: road teams won significantly more. 2024: roughly equal. 2025: home teams had the edge. Net effect: noise.

The home preference filter was harmful at n=5 and n=50. Barely better than random at n=10 (52–58% beneficial swap rate). Strike "prefer home teams" from your checklist.

---

## Snippet 8 — What doesn't work: divisional games

"Avoid divisional matchups — they're more competitive."

Real data across 3 seasons:
- 2023: divisional favorites won 64.1% (vs 69.5% non-div). Hypothesis supported.
- 2024: divisional favorites won 73.6% (vs 70.4% non-div). Opposite.
- 2025: divisional favorites won 76.0% (vs 66.5% non-div). Strongly opposite.
- Average: divisional picks win *more* often on average.

The heuristic holds one year out of three. That's not a signal. That's coin flipping.

---

## Snippet 9 — What doesn't work: weather

The weather filter study: 1,615 games across 6 NFL seasons.

Extreme weather games had fewer upsets than dome games. 28.1% upset rate in extreme weather vs 32.0% in dome games. The opposite of the hypothesis.

The dome advantage held in 2 of 6 seasons. It flipped in 4.

Statistical test result: p-value of 0.511. Not significant at any conventional threshold.

And the practical kicker: adverse/extreme weather filters changed zero picks in simulation. The base scoring function already avoids these games implicitly. Weather filters are operationally inert.

---

## Snippet 10 — The team exhaustion problem

Why do sophisticated strategies fail at 50 entries?

With 50 entries and ~30 teams playing per week, roughly 20 entries can't get unique picks. They share teams — perfectly correlated. Same team wins or loses, both entries go together.

Sophisticated strategies cluster toward the single best team. At n=50, entries 1–20 get great picks; entries 21–50 get leftovers — often low-probability teams that eliminate fast.

The 70/30 Blend's 30% contrarian weighting naturally distributes entries across teams. No clustering. Entries 21–50 still get solid picks.

The strategy that wins at 10 entries actively destroys a 50-entry portfolio.

---

## Snippet 11 — The variance finding

The most consistent strategy across all 1,904 simulation runs:

Core/Satellite at n=10. Standard deviation of 1.7. Season breakdown: 33/36/32 across 2023, 2024, 2025.

For context: Pure Win Probability had SD of 7.8. It went 13 → 3 → 22 across the same seasons. The 3-entry-week 2024 season would have wiped out most of that portfolio by Week 2.

In survivor pools, consistency isn't a consolation prize. It's the strategy. One catastrophic season undoes multiple good ones.

---

## Snippet 12 — The split strategy trap

Buyback pool intuition: play aggressively during weeks 1–3 (you can buy back in), then go conservative.

We tested 5 split strategy configurations. Every single one lost to simple SP Conservative run from Week 1.

At n=10: SP Conservative = 165 entry-weeks. Best split strategy = 145. That's a -20 gap.

The buyback window is 3 weeks. By the time you switch to conservative mode, the compounding advantage of starting conservative is already gone.

If your pool has buybacks: run SP Conservative from game 1, week 1. Do not deviate.

---

## Snippet 13 — The framework in one tweet

Survivor pool strategy in 3 questions:

1. Buybacks available? → YES: SP Conservative, everything else is noise. / NO: continue.
2. How many entries? → 1-5: 70/30 Blend. 6-15: Core/Satellite. 16-30: Mixed Portfolio. 31+: 70/30 Blend.
3. Strong game-type conviction? → Divisional avoidance is defensible at n=10-20. Home field and weather filters are not.

That's 1,904 simulations and 6 seasons compressed into a decision tree.

---

## Snippet 14 — The null results are the point

Survivor pool research usually only reports what works.

We're reporting what doesn't:
- Home field preference filter: harmful at most portfolio sizes, noise at others
- Divisional avoidance: marginal gains at one scale, harmful at two others
- Weather avoidance: statistically insignificant (p=0.511), operationally inert, contradicted by extreme weather data

These aren't failures. They're scope reduction. Three conventional wisdom filters tested and rejected means the decision framework is cleaner, faster, and less prone to overthinking.

Know what to ignore. It's worth as much as knowing what to do.

---

## Snippet 15 — The portfolio as a system

Most players think about each entry individually.

The data says think about the portfolio as a system with intentional roles.

Core entries (60%): 70/30 Blend. Consistent survival, sidestep chalk busts.
Satellite entries (40%): EV formula. Exploit contrarian opportunities when they appear.

When safe weeks happen, cores capture them. When contrarian upside appears, satellites capture it. The portfolio adapts to seasonal variation automatically because the two scoring functions diverge.

32% more survival than running 10 copies of the same strategy. Lowest variance of any design tested. That's what intentional role design produces.
