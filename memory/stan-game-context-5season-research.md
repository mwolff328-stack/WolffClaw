---
name: Stan's Game Context Filter Research — 5-Season Expansion
description: Game context filter simulation across 5 NFL seasons (2021-2025). 560 runs: 4 strategies × 7 filter modes × 4 entry counts × 5 seasons.
type: research
date: 2026-04-23
channel: backtesting-research
---

# Game Context Filter Simulation — 5-Season Expansion
**Date:** 2026-04-23
**Analyst:** Stan the Scout
**Script:** `~/.openclaw/workspace/scripts/stan-game-context-5season-sim.py`
**Results:** `~/.openclaw/workspace/scripts/stan-game-context-5season-results.json`
**Seasons:** 2021, 2022, 2023, 2024, 2025
**Runs:** 560 (4 strategies × 7 filter modes × 4 entry counts × 5 seasons)

---

## Background

This research expands the Round 9 game context filter simulation from 3 seasons (2023-2025, 336 runs) to 5 seasons (2021-2025, 560 runs). The core questions: do divisional game avoidance and home team preference filters improve survivor pool outcomes? Does the verdict change with more data?

---

## Part 1: Hypothesis Validation — Divisional Games

### Overall finding (5 seasons, raw aggregate at n=10, No Filter)

| Category | Picks | Win Rate |
|---|---|---|
| Divisional picks | 145W / 59L | 71.1% |
| Non-divisional picks | 321W / 140L | 69.6% |
| Gap (non-div minus div) | | **-1.4pp** |

**Hypothesis NOT SUPPORTED.** Divisional game favorites win at a slightly *higher* rate than non-divisional favorites in survivor pool pick data. The conventional wisdom (divisional games are traps) is wrong on average across 5 seasons.

### Per-season breakdown

| Season | Div WR | Non-Div WR | Gap | Supports Hypothesis? |
|---|---|---|---|---|
| 2021 | 53.8% | 65.9% | +12.0pp | Yes |
| 2022 | 68.4% | 60.0% | -8.4pp | No |
| 2023 | 61.8% | 71.0% | +9.2pp | Yes |
| 2024 | 81.1% | 73.6% | -7.5pp | No |
| 2025 | 78.3% | 73.7% | -4.6pp | No |
| **5-Season Average** | **71.1%** | **69.6%** | **-1.4pp** | **Not supported** |

The hypothesis holds in only 2 of 5 seasons (2021 and 2023). In the most recent three seasons (2022, 2024, 2025), divisional favorites outperformed non-divisional favorites. The signal flips freely year-to-year. No stable directional edge.

### Comparison to 3-season findings

The 3-season analysis (2023-2025) had already rejected the hypothesis with an average gap of -2.4pp (divisional winning more). The 5-season result confirms and extends this finding: with 2021-2022 data added, the gap narrows to -1.4pp, and we see that 2021 was the one strong year supporting the hypothesis while 2022 already reversed it. The null result is robust across both data windows.

---

## Part 2: Hypothesis Validation — Home Field Advantage

### Overall finding (5 seasons, raw aggregate at n=10, No Filter)

| Category | Picks | Win Rate |
|---|---|---|
| Home picks | 293W / 136L | 68.3% |
| Road picks | 173W / 63L | 73.3% |
| Gap (home minus road) | | **-5.0pp** |

**Hypothesis NOT SUPPORTED.** Road teams win at a *higher* rate than home teams in survivor pool pick data. This is because the strategies tend to select road teams when they have significantly higher win probabilities — meaning the "home team" signal is already priced in by the time picks are assigned.

### Per-season breakdown

| Season | Home WR | Road WR | Gap (H-R) | Supports Hypothesis? |
|---|---|---|---|---|
| 2021 | 59.5% | 70.6% | -11.1pp | No — road wins more |
| 2022 | 67.2% | 57.4% | +9.8pp | Yes |
| 2023 | 62.1% | 82.5% | -20.4pp | No — road wins strongly |
| 2024 | 72.6% | 80.8% | -8.1pp | No |
| 2025 | 76.2% | 74.6% | +1.6pp | Roughly equal |
| **5-Season Average** | **68.3%** | **73.3%** | **-5.0pp** | **Not supported** |

Home field advantage holds in only 1 of 5 seasons (2022). The -5.0pp gap on a 5-season aggregate is meaningfully larger than the -0.7pp found in 3-season data, making the null result stronger with additional data.

### Why road teams outperform in simulation

Survivor pool strategies pick the highest-scoring team available each week. When a road team is favored significantly (e.g., KC at +7 visiting a weak opponent), the strategy picks them — and road favorites win. The home field premium is already baked into win probability calculations. Applying an additional home preference bonus double-counts a factor that market odds have already priced.

### Comparison to 3-season findings

3-season showed a -0.7pp gap. 5-season shows -5.0pp. The additional data from 2021 (strong road advantage) and 2022 (one of the few seasons where home actually helped) shows the pattern is volatile but directionally unfavorable to home preference filtering.

---

## Part 3: Filter Effectiveness

### Avoid Divisional filter — the clear winner

"Avoid Div (Soft)" — a 10% penalty applied to divisional game picks — is the most consistently effective filter across strategies and entry counts:

| Strategy | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| 70/30 Blend | +0.0 | +1.4 | +1.2 | +4.2 |
| SP Production | -3.4 | +2.2 | -2.2 | -1.4 |
| Core/Satellite | -0.2 | -2.8 | +4.6 | +1.2 |
| SP Conservative | +0.4 | +2.8 | +3.4 | +1.2 |

Avg across strategies at n=10: **+0.9 entry-weeks vs control**. Avg at n=50: **+1.3 entry-weeks vs control**.

**Recommended use:** Defensible as a soft overlay, especially for SP Conservative and 70/30 Blend at n=10 and above. Avoid Div (Hard) — the force-swap variant — is slightly weaker but still positive for these strategies. Both provide ~60-62% beneficial swap rates.

### Prefer Home filter — consistently harmful

"Prefer Home" filters hurt outcomes at nearly every configuration:

| Strategy | n=5 | n=10 | n=20 | n=50 |
|---|---|---|---|---|
| 70/30 Blend | -0.2 | 0.0 | -1.4 | -4.2 |
| SP Production | -2.8 | -4.0 | -2.0 | -16.2 |
| Core/Satellite | +0.8 | -4.4 | -4.6 | -14.8 |
| SP Conservative | +1.0 | -0.2 | +3.2 | -6.0 |

The soft variant produces a beneficial swap rate of only 50-58%. That's barely above random chance — and since many swaps are costly, the filter is net negative. Prefer Home (Hard) is worse, with SP Production and Core/Satellite taking hits of -4 to -21 entry-weeks at larger N.

**Verdict: Discard the home preference filter at n=10 and above.**

### "Both" combined filters — generally negative

Combining divisional avoidance and home preference (soft or hard) produces net-negative results for most strategies at most entry counts. The two filters compete and cancel each other, and the home penalty drag dominates at high N.

Exception: Both (Soft) at 70/30 Blend n=20 (+0.2) and Core/Satellite n=50 (+0.4). Too marginal to recommend.

### Filter swap opportunity cost (% of swaps where new pick won)

| Filter | Avg beneficial swap % |
|---|---|
| Avoid Div (Soft) | 61.5% |
| Avoid Div (Hard) | 61.3% |
| Both (Soft) | 59.8% |
| Both (Hard) | 58.3% |
| Prefer Home (Soft) | 53.9% |
| Prefer Home (Hard) | 53.6% |

Divisional avoidance filters direct to winners most of the time. Home preference filters are barely above coin-flip.

---

## Part 4: Champion Table (5-Season Baseline)

| Entry Count | Best Strategy+Filter | Avg Entry-Weeks | Lift vs No Filter |
|---|---|---|---|
| n=5 | SP Conservative + Prefer Home (Soft) | 18.0 | +1.0 |
| n=10 | SP Conservative + Avoid Div (Soft) | 28.0 | +2.8 |
| n=20 | Core/Satellite + Avoid Div (Soft) | 43.4 | +4.6 |
| n=50 | 70/30 Blend + Avoid Div (Soft) | 91.8 | +4.2 |

**Key observation:** Avoid Div (Soft) wins or is competitive at n=10, n=20, and n=50. The filter provides the most consistent lift at larger entry counts where avoiding correlated divisional game risk matters more.

At n=5, SP Conservative + Prefer Home (Soft) wins narrowly (+1.0), but SP Conservative alone at 17.0 is nearly identical. The home preference benefit at n=5 is marginal and not robust across seasons.

---

## Part 5: Comparison to 3-Season Findings — What Changed

### What stayed the same
- Both core hypotheses are rejected
- Avoid Div (Soft) remains the best-performing filter
- Prefer Home filters remain harmful at n=10 and above
- The combined "Both" filters are net negative
- "No Filter" is competitive or best at n=5 for most strategies

### What changed or became clearer
1. **Divisional hypothesis gap narrowed:** From -2.4pp (3-season) to -1.4pp (5-season). Still rejects hypothesis, but the margin is smaller. The addition of 2021 (which supports the hypothesis strongly) moderated the overall average.

2. **Home hypothesis gap widened:** From -0.7pp (3-season) to -5.0pp (5-season). The 5-season data strengthens the anti-home-filter conclusion. The 2021 season shows road teams dominating heavily (-11.1pp), which wasn't in the original 3-season window.

3. **SP Conservative emerges as filter champion:** The 3-season data showed 70/30 Blend as filter champion at n=10. With 5 seasons, SP Conservative + Avoid Div (Soft) at n=10 wins outright (28.0 vs 70/30 Blend's 23.6).

4. **Core/Satellite shines at n=20:** Core/Satellite + Avoid Div (Soft) at n=20 (43.4) edges out SP Conservative (42.2) as the n=20 champion with filter applied.

---

## Part 6: Weather Research Cross-Check

The weather research (Round 10, 6-season study) showed:
- Dome vs outdoor gap: +1.7pp (outdoor teams upset slightly more)
- Not statistically significant (z=0.658, p=0.511)
- Adverse/extreme weather filters were operationally inert — 0 picks changed

These numbers are already in the white paper and accurately represent the 6-season data. No discrepancies found between the research file and the white paper's weather section.

The white paper correctly cites 672 weather runs (4 strategies × 7 filter modes × 4 entry counts × 6 seasons).

---

## Summary Verdicts

| Filter | Verdict | Best use case |
|---|---|---|
| Avoid Div (Soft) | **Defensible** — soft overlay that adds ~1-5 entry-weeks for Conservative/Blend strategies | n=10, n=20, n=50 with SP Conservative or 70/30 Blend |
| Avoid Div (Hard) | **Marginally useful** — slightly weaker than soft, similar direction | Same as above |
| Prefer Home (Soft) | **Discard** — barely above chance, harmful at scale | No default use |
| Prefer Home (Hard) | **Discard** — consistently the worst filter mode | No default use |
| Both (Soft) | **Avoid** — home drag cancels divisional benefit | No default use |
| Both (Hard) | **Avoid** — worst combined outcome at most configurations | No default use |

---

*Research conducted by Stan the Scout — SurvivorPulse Intelligence Layer*
*Script: `~/.openclaw/workspace/scripts/stan-game-context-5season-sim.py`*
*Seasons: 2021-2025 | Runs: 560*
