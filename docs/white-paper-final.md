# The systematic edge: what 1,904 survivor pool simulations taught us about strategy, scale, and pool type

**Research team:** SurvivorPulse  
**Date:** April 2026  
**Simulation runs:** 1,904  
**Seasons covered:** 2020–2025  
**Rounds of backtesting:** 10

---

## Table of contents

1. [The uncomfortable truth about your portfolio](#1-the-uncomfortable-truth-about-your-portfolio)
2. [The real problem serious players haven't solved](#2-the-real-problem-serious-players-havent-solved)
3. [What we did](#3-what-we-did)
4. [The baseline: why picking favorites isn't enough](#4-the-baseline-why-picking-favorites-isnt-enough)
5. [The inflection point: how scale changes everything](#5-the-inflection-point-how-scale-changes-everything)
6. [Portfolio architecture: the Core/Satellite advantage](#6-portfolio-architecture-the-coresatellite-advantage)
7. [The buyback reversal: when pool type overrides strategy](#7-the-buyback-reversal-when-pool-type-overrides-strategy)
8. [What doesn't work: three myths the data killed](#8-what-doesnt-work-three-myths-the-data-killed)
9. [The decision framework](#9-the-decision-framework)
10. [What's next](#10-whats-next)
11. [Methodology appendix](#11-methodology-appendix)

---

## 1. The uncomfortable truth about your portfolio

Here is a scenario that probably sounds familiar.

You enter 10 pools in Week 1. You spend an hour researching picks. You settle on Kansas City because they're favored by 7 at home. You look at your portfolio and realize seven of your ten entries are taking Kansas City. You tell yourself that's fine — KC is the right pick. You move on.

KC wins. You feel smart.

Three weeks later, KC is favored again. You're still on them with five entries (because a couple died already). Same story. Then in Week 8, they lose to a 6.5-point underdog on a Thursday night, and half your portfolio disappears overnight.

That's not bad luck. That's a structural portfolio problem that 1,904 simulation runs across six NFL seasons helped us understand precisely.

**The finding:** a 10-entry portfolio where every entry runs the same pick-the-biggest-favorite strategy produces 24% fewer entry-weeks than a portfolio built with intentional role design. Across the length of a season, that's the difference between a live portfolio and a graveyard.

The rest of this paper explains why, and what to do about it.

---

## 2. The real problem serious players haven't solved

The chalk-avoidance principle is not news. If you've played survivor pools seriously for more than a year, you know that concentrating your entries on the most-picked teams creates correlated risk. When the chalk busts, everyone dies at once.

But knowing the problem and solving it are different things.

The survivor pool community has developed rough heuristics: avoid the top-2 most-picked teams, pick teams with fewer than 15% ownership when possible, look for value in the 70–75% win probability range. These intuitions are roughly correct. They're just not systematic.

What hasn't been answered rigorously:

- What is the mathematically optimal weighting between win probability and pick popularity?
- Does that optimal weighting change with portfolio size — and if so, by how much?
- Should different entries in your portfolio run different strategies?
- Do pool mechanics (buybacks) change the calculus entirely?
- Do the conventional wisdom filters (avoid divisional games, prefer home teams, avoid bad weather) actually improve outcomes?

We built a simulator and ran 1,904 combinations to find out. Some answers confirmed intuition. Others reversed it completely.

---

## 3. What we did

### The simulator

Our simulator runs NFL survivor pool mechanics for a full 18-week regular season. Each entry picks one team per week, cannot reuse teams, and is eliminated when its pick loses. The key metric is **entry-weeks survived** — the sum of weeks each entry remained alive across all entries. A 10-entry portfolio surviving an average of 12 weeks produces 120 entry-weeks.

We use entry-weeks rather than "wins" because winner-take-all outcomes are too noisy at small sample sizes. Entry-weeks provide a continuous, strategy-sensitive signal that correlates directly with long-run expected value.

### The data

- **Game results and win probabilities:** nfl_data_py Python package (2020–2024) and live data for 2025. Win probabilities derived from point spreads using the standard normal CDF formula with a 13.5-point historical standard deviation constant.
- **Pick popularity:** SurvivorGrid.com scraped historical percentages (2023–2025), weighted across Yahoo, ESPN, and OfficeFootballPool.
- **Total game data:** 1,615 games across 6 seasons for weather analysis (Round 10).

### The strategies

The core strategies referenced throughout this paper:

| Label | Formula |
|---|---|
| Pure Win Probability | Select team with highest win probability |
| 70/30 Blend | `0.70 × winProb + 0.30 × (1 − pickShare/100)` |
| SP Production | `0.70 × EVPick + 0.30 × futureUtility` |
| SP Conservative | `0.65 × EVPick + 0.25 × futureUtility + 0.10 × leverageScore` |
| Core/Satellite | 60% of entries use 70/30 Blend; 40% use SP Production EV |
| Mixed Portfolio | Entries cycle through multiple strategy classes |

### Scale of the research

| Round | Focus | Runs |
|---|---|---|
| 1–2 | Initial strategy baseline (2025 only) | 11 |
| 3–5 | Multi-season validation, lookahead, EV variants | 81 |
| 6 | Entry-count scaling across portfolio sizes | 168 |
| 7 | Differentiated scoring per entry | 144 |
| 8 | Buyback mechanics | 492 |
| 9 | Game context filters (divisional, home/away) | 336 |
| 10 | Weather impact (6 seasons) | 672 |
| **Total** | | **1,904** |

---

## 4. The baseline: why picking favorites isn't enough

### The first simulation

Our first test was straightforward: run four strategies for the 2025 season and see what breaks.

Two strategies self-destructed immediately. Raw leverage scoring (win probability divided by pick ownership) and future-value preservation without win probability floors both picked teams with near-zero ownership — and those teams lost. Heavily. Both portfolios were essentially eliminated by Week 2.

The lesson came fast: **contrarianism without a safety floor is a death sentence.** Any strategy that overweights unpopularity without requiring a baseline win probability will pick the wrong kind of undervalued team — the kind that loses.

Pure Win Probability survived until Week 10 (22 entry-weeks for a single entry). That was the floor.

### The 70/30 discovery

The second round of testing introduced a blended approach: weight win probability at 70% and contrarian appeal (inverse of pick share) at 30%.

The result was not marginal. The 70/30 Blend survived until Week 14 — **four weeks longer than Pure Win Probability** and 18% more entry-weeks.

The formula is simple: `score = 0.70 × winProb + 0.30 × (1 − pickShare/100)`. Pick safe teams. Among teams of similar safety, prefer the ones fewer people are on.

Why does four extra weeks matter? Because in survivor pools, elimination is not a smooth curve. It happens in spikes. When a heavily-picked team loses, everyone who picked them dies in the same week. By systematically underweighting the most popular picks, the 70/30 Blend sidesteps those spikes and keeps entries alive through the chaos.

We also tested an 80/20 Blend. It produced identical results to Pure Win Probability. **The contrarian weight needs to be at least 30% to create meaningfully different team selection.** At 20%, you still end up on the same teams as the chalk crowd.

### Three-season validation

A single-season result might be noise. So we ran the same strategies across 2023, 2024, and 2025.

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev |
|---|---|---|---|---|---|
| **70/30 Blend** | **17** | **14** | **26** | **57** | **5.1** |
| 80/20 Blend | 17 | 4 | 22 | 43 | 8.8 |
| Pure Win Probability | 13 | 3 | 22 | 38 | 7.8 |

**57 entry-weeks vs 38 for Pure Win Probability — 50% more survival across three seasons.** The 70/30 Blend also had the lowest standard deviation (5.1), meaning it's more consistent season over season.

The 2024 season makes the case most clearly. Pure Win Probability collapsed to just 3 entry-weeks — it got wiped out in the first few weeks by chalk busts. The 70/30 Blend produced 14 in the same season because it had stepped off the teams that crashed the field.

> **The 70/30 Blend's primary virtue is that it never has a catastrophic season. In a pool game where catastrophe is always one upset away, that matters more than ceiling.**

This is the foundation. The blended contrarian-aware formula beats the naive approach by 50% at small entry counts. But this is where the easy part ends.

---

## 5. The inflection point: how scale changes everything

### The question

Does the 70/30 Blend still dominate when you're running 10, 20, or 50 entries? Or do the dynamics change?

Round 6 tested 14 strategies across four portfolio sizes (n=5, 10, 20, 50) over three seasons. 168 simulation runs.

### n=5: 70/30 holds

At five entries, the 70/30 Blend ties for best on a risk-adjusted basis. Mixed Portfolio and Adaptive Blend produce one additional entry-week in aggregate but with dramatically higher standard deviation (10.5 and 11.0 vs 5.1). For a small portfolio, consistency wins.

### n=10: the inflection point

This is where the research got interesting.

| Strategy | 2023 | 2024 | 2025 | Total | Efficiency | vs 70/30 |
|---|---|---|---|---|---|---|
| **SP Production** | **25** | **32** | **37** | **94** | **17.4%** | **+18** |
| SP Conservative | 25 | 33 | 29 | 87 | 16.1% | +11 |
| Adaptive Blend | 34 | 20 | 33 | 87 | 16.1% | +11 |
| Mixed Portfolio | 19 | 21 | 41 | 81 | 15.0% | +5 |
| **70/30 Blend** | **20** | **22** | **34** | **76** | **14.1%** | **=** |

**Seven strategies beat the 70/30 Blend at n=10.** SP Production leads by 24%. The 70/30 Blend's efficiency drops from 21.1% at n=5 to 14.1% at n=10. More sophisticated strategies retain efficiency better because they account for future team value and EV dynamics that matter more when you're coordinating picks across 10 entries.

### n=50: simplicity reclaims the top

By the time you reach 50 entries, the picture flips again.

| Strategy | 2023 | 2024 | 2025 | Total | vs 70/30 |
|---|---|---|---|---|---|
| **70/30 Blend** | **101** | **106** | **88** | **295** | **=** |
| 80/20 Blend | 97 | 102 | 85 | 284 | -11 |
| SP Conservative | 99 | 98 | 81 | 278 | -17 |
| Adaptive Blend | 108 | 34 | 87 | 229 | -66 |
| Pure Win Probability | 106 | 26 | 93 | 225 | -70 |

The 70/30 Blend wins again. Sophisticated strategies collapse. Why?

### The team exhaustion problem

With 50 entries and roughly 30 teams playing per week, about 20 entries cannot get unique team assignments. They share picks with other entries — meaning they're perfectly correlated. Same team wins or loses, both entries survive or die.

Sophisticated strategies cluster heavily toward the single best team each week. At n=50, entries 1–20 get those preferred picks; entries 21–50 get whatever's left — often low-WP teams that get eliminated quickly.

The 70/30 Blend's 30% contrarian weighting distributes entries across teams naturally. Entries 21–50 still get solid fallback picks because the strategy doesn't push 30 entries onto a single team.

**Adaptive Blend's 2024 season was the worst collapse in the entire study:** standard deviation of 31.1, only 34 entry-weeks. Late-season contrarian weighting shifted entries toward risky teams, and at 50 entries in weeks 13–18, a single bad week killed dozens simultaneously.

> **The same sophistication that helps a 10-entry portfolio destroys a 50-entry portfolio. Portfolio size isn't just a context factor — it changes which strategy is optimal.**

---

## 6. Portfolio architecture: the Core/Satellite advantage

### The question

Round 6 showed that mixing strategies (Mixed Portfolio) beats single-strategy approaches at n=20. Round 7 asked a sharper question: does **intentional role design** beat random strategy mixing? Does it matter if you give each entry a specific purpose, or is any diversification good enough?

144 simulation runs across 12 strategies, 4 entry counts, 3 seasons.

### The Core/Satellite architecture

The standout design from Round 7: **60% of entries run 70/30 Blend (core), 40% run SP Production EV formula (satellites).**

Core entries capture safe weeks. Satellite entries exploit contrarian opportunities when they appear. The architecture is simple to describe but produces genuinely different behavior from different entries because the scoring functions diverge.

### The results at n=10

| Strategy | 2023 | 2024 | 2025 | Total | Std Dev | vs 70/30 | vs Mixed |
|---|---|---|---|---|---|---|---|
| **Core/Satellite** | **33** | **36** | **32** | **101** | **1.7** | **+25** | **+17** |
| Role-Based Portfolio | 32 | 25 | 28 | 85 | 2.9 | +9 | +1 |
| Mixed Portfolio | 32 | 20 | 32 | 84 | 5.7 | +8 | = |
| **70/30 Blend** | **20** | **22** | **34** | **76** | **6.2** | **=** | — |

Core/Satellite at n=10 is the strongest finding in the entire study:

- **101 total entry-weeks vs 76 for 70/30 Blend — 32% more survival**
- **+17 entry-weeks vs Mixed Portfolio**, which was the previous best
- **Standard deviation of 1.7** — the lowest variance of any strategy tested across all 10 rounds
- Season breakdown of 33/36/32 — nearly identical results in every season tested

This is not a lucky result from one good year. The 33/36/32 consistency across 2023, 2024, and 2025 tells you the structural advantage is real. When cores capture safe weeks and satellites capture contrarian upside, the portfolio adapts to seasonal variation automatically.

> **A structured Core/Satellite architecture produces 32% more survival than a single-strategy approach at 10 entries — with the lowest variance of any design we tested.**

### A notable null result

Anti-Overlap Portfolio — global greedy assignment with 70/30 scoring — produced **identical results to the 70/30 Blend at every entry count**.

This confirms something important: changing the assignment algorithm doesn't help. Meaningful entry differentiation requires fundamentally different scoring functions per entry, not just smarter assignment of the same scores. The Core/Satellite design works because the scoring functions diverge, not because of how picks are allocated.

### What works and what doesn't by scale

| Entry count | Does intentional design beat random mixing? | Best approach |
|---|---|---|
| n=5 | No | Mixed Portfolio or 70/30 Blend |
| **n=10** | **Yes — 3 designs beat Mixed** | **Core/Satellite (+17 over Mixed)** |
| n=20 | No — Mixed holds | Core/Satellite close at -4 |
| **n=50** | **Yes — 8 designs beat Mixed** | **Role-Based Portfolio (+30 over Mixed)** |

Intentional design matters most at the scale where serious multi-entry players actually operate: 10 entries. That's not a coincidence — it's the sweet spot where portfolio coordination creates genuine option value without the team exhaustion problem that breaks sophisticated strategies at higher counts.

---

## 7. The buyback reversal: when pool type overrides strategy

### The question

Buyback pools — where eliminated entries can pay to re-enter during the first few weeks — are increasingly common. The research question: does optimal strategy change when buybacks are available?

The answer was the most dramatic finding in the entire study.

492 simulation runs across 12 strategies, 4 entry counts, 3 buyback configurations, 3 seasons.

### SP Conservative wins everything — with buybacks

| Entry count | Best no-buyback strategy | Score | Best buyback strategy | Score | Uplift |
|---|---|---|---|---|---|
| n=5 | Mixed Portfolio | 67 | **SP Conservative** | **78** | +16.4% |
| n=10 | Core/Satellite | 101 | **SP Conservative** | **165** | +63.4% |
| n=20 | Core/Satellite | 130 | **SP Conservative** | **248** | +90.8% |
| n=50 | 70/30 Blend | 295 | **SP Conservative** | **463** | +57.0% |

SP Conservative (65% EV + 25% future value + 10% leverage score) did not win at any entry count without buybacks. With buybacks, it wins at all four.

The winner completely reverses at every portfolio size. This is not a marginal shift — at n=20, SP Conservative with buybacks produces 90.8% more entry-weeks than the best no-buyback strategy.

### Why conservative strategies exploit buybacks

Here's the mechanism. Conservative strategies tolerate more early-game losses. Their moderate win probability threshold means some entries get eliminated in weeks 1–3 more frequently than aggressive strategies.

In a no-buyback pool, this is a penalty. You're losing entries early.

In a buyback pool, **those early eliminations become refundable.** Conservative strategies get multiple second chances to showcase their late-season survival advantages. Aggressive strategies (Core/Satellite, SP Production) lose fewer entries early — so they exercise fewer buybacks and capture less of the mechanic's structural value.

The result: buybacks convert early losses from a liability into a structural advantage.

### The buyback ROI question

Is the buyback worth the cost (typically the same as your initial entry fee)?

| Portfolio size | Entry-weeks per buyback | Strategy | 3+ week survival rate |
|---|---|---|---|
| n=5 | 3.10 | Safety/Contrarian Split | 40.0% |
| **n=10** | **4.15** | **SP Conservative** | **35.0%** |
| n=20 | 2.74 | SP Conservative | 26.1% |
| n=50 | 1.75 | Expendable-First | 19.8% |

At n=10, SP Conservative generates 4.15 additional entry-weeks per buyback used. In a $100 entry fee pool, a $100 buyback keeps an entry alive for an expected 4+ additional weeks. 30–40% of bought-back entries survive at least 3 more weeks.

The only negative-ROI case in the study was Adaptive Blend at n=5 (-0.12 EW/BB). That's the exception — every other strategy at every portfolio size produced positive buyback ROI.

### Don't overcomplicate it

An intuitive hypothesis: play aggressively during the buyback window (weeks 1–3), then switch to conservative after. Get the upside early, then batten down the hatches.

We tested five split strategy configurations. None beat simple SP Conservative.

| Portfolio size | Best non-split w/BB | Best split w/BB | Gap |
|---|---|---|---|
| n=10 | SP Conservative (165) | Contrarian/Conservative (145) | -20 |
| n=20 | SP Conservative (248) | EV/Blend Split (233) | -15 |
| n=50 | SP Conservative (463) | Expendable/Safe Split (443) | -20 |

The 3-week buyback window is too short for strategy switching to pay off. The compounding advantage of early conservative picks has already been foregone by the time the strategy shifts. The conclusion: don't overthink it. If your pool has buybacks, run SP Conservative from Week 1.

> **Pool type overrides strategy. Using the wrong approach for your pool mechanic leaves 50–100% performance on the table.**

---

## 8. What doesn't work: three myths the data killed

This section is worth reading carefully. Null results are underreported in sports analytics because they're less exciting than positive findings. But for serious players, knowing what *doesn't* work is as valuable as knowing what does — and far more credibility-building than showing only wins.

We killed three pieces of conventional wisdom empirically. Here they are.

---

### Myth 1: Avoid divisional games

The intuition: divisional matchups are more competitive than non-divisional games. Familiar opponents, late-season stakes, the idea that divisional games are "trap games" for favorites. Therefore, when picking survivor pool teams, avoid picking favorites in divisional contests.

**What we tested:** 7 filter modes for the divisional avoidance hypothesis (no filter, soft 10% penalty, hard swap if within 15% score gap, and combinations), across 4 strategies × 4 entry counts × 3 seasons = 336 runs.

**The actual data:**

| Season | Divisional favorite win rate | Non-divisional favorite win rate | Gap | Supports hypothesis? |
|---|---|---|---|---|
| 2023 | 64.1% | 69.5% | +5.4pp | Yes |
| 2024 | 73.6% | 70.4% | -3.2pp | No |
| 2025 | 76.0% | 66.5% | -9.5pp | Strongly No |
| **Average** | **71.2%** | **68.8%** | **-2.4pp** | **Not supported** |

The hypothesis holds in 2023. In 2024 and 2025, divisional favorites won at a *higher* rate than non-divisional favorites. Averaged across three seasons, divisional picks win slightly more often than non-divisional picks — the opposite direction of the heuristic.

The divisional avoidance filter showed marginal gains at n=10 and n=20 for SP Conservative (+5.3 and +7.0 entry-weeks per season). But at n=5 and n=50, it's harmful. And the year-to-year variance is substantial enough that a filter gaining +5 in one season can lose -10 in the next.

**Verdict:** Not a default. Maximum a personal conviction toggle.

---

### Myth 2: Prefer home teams

The intuition: home field advantage is real in the NFL. Noise, travel, familiar surroundings — home teams win more often. Therefore, prefer home team picks in survivor pools.

**The actual data:**

| Season | Home team win rate | Road team win rate | Gap | Supports hypothesis? |
|---|---|---|---|---|
| 2023 | 62.9% | 74.6% | -11.7pp | Road wins more |
| 2024 | 71.4% | 72.3% | -0.9pp | Roughly equal |
| 2025 | 74.9% | 64.4% | +10.5pp | Yes |
| **Average** | **69.7%** | **70.4%** | **-0.7pp** | **Not supported** |

In survivor-relevant matchups (where one team is a significant favorite), home field advantage effectively doesn't exist in recent NFL data. In 2023, road teams in high-probability matchups won significantly more often. In 2025 the pattern flipped. Net effect across three seasons: a negligible -0.7 percentage points.

The home preference filter was harmful at every portfolio size except n=20 for specific strategies. Hard home preference (force swaps to home teams) was consistently the worst performer.

**Verdict:** Discard. The home filter is barely above random chance (52–58% beneficial swap rate), and harmful at the entry counts most players actually use.

---

### Myth 3: Avoid bad weather games

The intuition: cold temperatures and high winds increase variance in NFL games, favoring the run game and reducing the aerial advantage that high-powered offenses typically hold. Survivor pool favorites often rely on their passing game. Therefore, avoid picking favorites in extreme weather.

We ran the most extensive weather analysis in the study: 1,615 games across 6 seasons (2020–2025), enriched with dome/outdoor classification and weather conditions from venue data.

**The actual upset rates:**

| Weather category | Games | Upset rate | Favorite win rate |
|---|---|---|---|
| Dome/Closed | 521 | 32.0% | 68.0% |
| Outdoor Mild | 703 | 34.3% | 65.7% |
| Outdoor Adverse | 334 | 34.7% | 65.3% |
| **Outdoor Extreme** | **57** | **28.1%** | **71.9%** |

**Extreme weather games have fewer upsets than dome games** (28.1% vs 32.0%). This is the direct opposite of the hypothesis.

The overall dome-vs-outdoor gap is +1.7 percentage points. That sounds like it might mean something until you look at the year-by-year breakdown:

| Season | Dome advantage? |
|---|---|
| 2020 | No (dome teams had 5.3pp *higher* upset rate) |
| 2021 | No (dome teams had 3.0pp *higher* upset rate) |
| 2022 | Yes (+16.4pp dome advantage) |
| 2023 | Yes (+8.5pp dome advantage) |
| 2024 | No (-1.7pp) |
| 2025 | No (-4.7pp) |

The dome advantage holds in exactly 2 of 6 seasons. The signal flips freely. A formal statistical test confirms it: the dome vs outdoor gap is not statistically significant at any conventional threshold (z-score: 0.658, p-value: 0.511).

There's also a practical problem: the adverse and extreme weather filters produced **identical results to no filter in every single simulation run** — 0 wins, 0 losses, 96 ties. Top-scoring picks virtually never fall in the adverse or extreme weather categories because the base scoring function already avoids them. Only 3.8% of No Filter picks were in adverse weather. Zero were in extreme weather.

The weather avoidance filter is operationally inert. The scoring function has already done this work.

**Verdict:** Don't build weather into the algorithm. Surface weather information for player context — let them make manual overrides if they want — but weather is not a reliable algorithmic signal.

> **The null results aren't failures. They're scope reduction. Three conventional wisdom filters tested and rejected means the decision framework is cleaner, not weaker.**

---

## 9. The decision framework

This is what 1,904 simulation runs, 6 NFL seasons, and 10 rounds of backtesting actually recommend.

### The master decision tree

```
Is this a buyback pool?
├── YES: Run SP Conservative (65% EV + 25% future value + 10% leverage)
│   at all entry counts. Always exercise the buyback — positive ROI
│   at every portfolio size tested.
│
└── NO: How many entries are you running?
    ├── 1–5 entries:   Mixed Portfolio or 70/30 Blend
    │                  No filter applied
    ├── 6–15 entries:  Core/Satellite (60% blend + 40% EV formula)
    │                  No filter (optional: Avoid Divisional Soft)
    ├── 16–30 entries: Mixed Portfolio
    │                  No filter (or Avoid Divisional Soft for n=20)
    ├── 31–50 entries: 70/30 Blend or Role-Based Portfolio
    │                  No filter
    └── 50+ entries:   70/30 Blend
                       No filter
```

### Strategy performance by configuration

| Pool type | Portfolio size | Strategy | Filter | Avg entry-weeks/season |
|---|---|---|---|---|
| Non-buyback | 5 | SP Conservative | None | 21.3 |
| Non-buyback | 10 | Core/Satellite | None | 33.7 |
| Non-buyback | 20 | Core/Satellite | Avoid Div Soft | 49.0 |
| Non-buyback | 50 | 70/30 Blend | None | 98.3 |
| Buyback (Wk1-3) | 5 | SP Conservative | None | 26.0 |
| Buyback (Wk1-3) | 10 | SP Conservative | None | 55.0 |
| Buyback (Wk1-3) | 20 | SP Conservative | None | 82.7 |
| Buyback (Wk1-3) | 50 | SP Conservative | None | 154.3 |

### What each strategy profile means in practice

**Single-entry or very small portfolio (1–5 entries):** You want consistency above everything else. The 70/30 Blend never has a catastrophic season. Mixed Portfolio adds slight upside with higher variance. Pick based on your risk tolerance, but don't reach for sophistication you don't need.

**The serious player's sweet spot (6–15 entries):** This is where intentional portfolio architecture pays off. Run Core/Satellite: 60% of your entries on the safe, contrarian-aware strategy; 40% on the higher-EV formula. You get 32% more survival than a single strategy and the lowest variance of any design in the study. This is the recommendation for anyone playing multiple pools seriously.

**Large-scale operations (16–30 entries):** Mixed Portfolio holds up well here. True diversification across strategy classes creates genuine option value. When one strategy collapses in a given season, others buffer the loss.

**Very high entry counts (31–50+):** Team exhaustion is the binding constraint. At this scale, you're running more entries than available unique team assignments. The 70/30 Blend's natural distribution across teams handles this without clustering. Sophisticated strategies self-destruct.

**Buyback pools (any size):** Ignore everything else. SP Conservative. From Week 1. Don't try to time a strategy switch — the 3-week buyback window is too short for it to pay off.

### The three questions before you pick

1. Does my pool have buybacks?
   - Yes: SP Conservative, always.
   - No: proceed to question 2.

2. How many entries am I running?
   - Use the table above to match portfolio size to strategy.

3. Do I have strong conviction about any game type?
   - Divisional game avoidance is defensible as a personal override at n=10-20.
   - Home field preference and weather avoidance are not.
   - Treat filters as conviction toggles, not algorithmic defaults.

---

## 10. What's next

This research was built to answer the question that nobody had answered systematically: what actually maximizes survival in a multi-entry NFL survivor pool?

The answers are cleaner than expected in some ways (one formula dominates small portfolios; pool type overrides everything), and more nuanced in others (the scale inflection at 10 entries, the complete reversal when buybacks are introduced).

The findings are also directly implementable. They're not dependent on information that's hard to get or calculations that require advanced infrastructure. Win probabilities, pick share percentages, a defined weighting formula, and a clear decision tree based on your pool type and portfolio size.

That implementation is what we built. **SurvivorPulse** is the product that runs this research as a live system for the 2026 NFL season: real-time pick recommendations calibrated to your portfolio size and pool type, portfolio coordination tools for multi-entry players, and the buyback ROI tracking that tells you whether each buyback is worth taking.

The research stands on its own regardless of the tool. If you take nothing else from this paper, take the decision framework table and the three questions before you pick. That alone will outperform gut feel and spreadsheet management by a margin the data makes quantifiable.

---

## 11. Methodology appendix

### Win probability derivation

For 2020–2024 historical seasons, win probabilities were derived from point spreads using:

```
P(win) = 0.5 × (1 + erf(spread / (13.5 × √2)))
```

The 13.5 constant represents the historical standard deviation of NFL score differentials. This formula matches implied win probabilities from moneylines within approximately 1 percentage point for most matchups.

Important note: `nfl_data_py` uses a positive `spread_line` to indicate the home team is favored — the opposite convention from some betting platforms. This was verified and handled consistently throughout.

### Pick share data

- 2023–2025: SurvivorGrid.com per-team percentages from Yahoo, ESPN, and OfficeFootballPool, weighted-averaged across sources.
- 2020–2022: Real historical SurvivorGrid data scraped for available seasons.
- For Rounds 1–5 (2025 season only), 2020–2022 pick shares were not yet integrated. Rounds 6 onward used real historical pick data for all seasons.

### Simulation mechanics

- 18-week regular season per simulation.
- Per-entry pick assignment: sequential-greedy by default. Each week, each live entry scores all eligible teams and selects the top-scored team.
- Efficiency metric: entry-weeks survived divided by theoretical maximum (N entries × 18 weeks × seasons tested).
- Buyback mechanics: eliminated entries within the buyback window (Weeks 1–3 or 1–4) re-enter with a full team history reset for the re-entering entry.

### Limitations

**Sample size:** Rounds 1–8 cover 3 NFL seasons (2023–2025). Small sample. A single anomalous season can move aggregate results significantly. Season-to-season variance is substantial: Pure Win Probability produced 3 entry-weeks in 2024 and 22 in 2025 from the same strategy. Any recommendation is a bet on distributional consistency, not a guarantee.

**Entry-weeks vs real-money EV:** All simulations optimize for entry-weeks survived — a proxy that correlates with long-run EV but doesn't model entry fee structures, prize pool sizes, or winner-take-all dynamics. A complete dollar-value EV simulation would require pool-size-specific survivor math that was intentionally deferred to keep strategy research clean.

**Real player behavior:** Real survivor pool players are not fully rational. They're influenced by narrative, media, and personal bias. The research identifies optimal strategies under idealized conditions; real-world implementation will see some degradation from simulated results.

**Future research priorities:**
1. Prize structure modeling — compute actual EV in dollars for a realistic pool scenario.
2. Extended historical data — 10+ seasons would meaningfully reduce variance in per-strategy estimates.
3. Live-season adaptive strategies — adjusting weights based on observed eliminations in a running pool.

---

*Research conducted April 2026. All data from publicly available sources: nfl_data_py, SurvivorGrid.com, Odds API.*
