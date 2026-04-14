---
name: Stan's Weather Impact Research — Round 10
description: Full weather impact simulation across 6 NFL seasons (2020-2025). 672 runs: 4 strategies × 7 filter modes × 4 entry counts × 6 seasons.
type: research
date: 2026-04-14
channel: backtesting-research
---

# Round 10: Weather Impact Simulation
**Date:** 2026-04-14
**Analyst:** Stan the Scout
**Script:** `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/scripts/stan-weather-sim.py`
**Results:** `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/scripts/stan-weather-sim-results.json`

---

## Setup and Context

This round expands the weather feasibility study (Round 9.5) to 6 full seasons (2020-2025) with 672 simulation runs. The feasibility study found a +4.2pp dome vs cold-weather upset rate gap in 2023-2024 data, but flagged year-to-year inconsistency as a red flag.

**Key question:** Does a dome preference or adverse-weather avoidance filter improve survivor pool outcomes across 6 seasons of data?

**Data pipeline:**
- 2020-2024: nfl_data_py for game data + weather fields (roof, temp, wind)
- 2023-2024: Real SurvivorGrid pick data (Yahoo/ESPN/OFP averages)
- 2020-2022: Real SurvivorGrid pick data also available (scraped in Round prior)
- 2025: SurvivorPulse API games cache (already built in Round 9)
- 1,615 total game records enriched with weather classification

**Weather classification logic:**
- `weather_neutral`: dome or closed roof
- `weather_mild`: outdoor, temp >= 50°F and wind < 15mph (or warm-climate stadium)
- `weather_adverse`: outdoor, temp 40-49°F or wind 15-24mph, or cold-climate stadium in Dec/Jan with missing data
- `weather_extreme`: outdoor, temp < 32°F or wind >= 25mph

---

## Part 1: Upset Rate Validation — 6 Seasons

### Combined Results (2020-2025, ~1,615 games)

| Category | Games | Upsets | Upset Rate | Fav Win Rate |
|----------|-------|--------|------------|--------------|
| Weather Neutral (Dome/Closed) | 521 | 167 | 32.0% | 68.0% |
| Weather Mild (Outdoor, good conditions) | 703 | 241 | 34.3% | 65.7% |
| Weather Adverse (Cold/Windy outdoor) | 334 | 116 | 34.7% | 65.3% |
| Weather Extreme (Below freezing / gale) | 57 | 16 | 28.1% | 71.9% |

**Surprising finding:** Extreme weather games have FEWER upsets than dome games (28.1% vs 32.0%). This is counter-intuitive and counter to the hypothesis.

### Venue Type Combined

| Venue | Games | Upsets | Upset Rate | Fav Win Rate |
|-------|-------|--------|------------|--------------|
| Dome | 521 | 167 | 32.0% | 68.0% |
| Retractable Open | 32 | 15 | 46.9% | 53.1% |
| Outdoor | 1,062 | 358 | 33.7% | 66.3% |

**Net dome vs outdoor gap: +1.7pp** (outdoor teams upset favorites slightly more). This is well below the +4.2pp found in the 2-year feasibility study. Retractable roof open games show a high 46.9% upset rate but sample size is tiny (32 games — not reliable).

### Year-Over-Year: Dome vs Outdoor

| Season | Dome % | Outdoor % | Gap (pp) | Dome N | Outdoor N |
|--------|--------|-----------|----------|--------|-----------|
| 2020 | 36.3% | 30.9% | -5.3 | 91 | 165 |
| 2021 | 39.2% | 36.3% | -3.0 | 79 | 182 |
| 2022 | 22.6% | 39.0% | +16.4 | 84 | 177 |
| 2023 | 25.9% | 34.4% | +8.5 | 81 | 180 |
| 2024 | 29.8% | 28.1% | -1.7 | 94 | 178 |
| 2025 | 38.0% | 33.3% | -4.7 | 92 | 180 |

**Signal assessment:** INCONSISTENT. In 4 of 6 seasons (2020, 2021, 2024, 2025), dome teams actually had HIGHER upset rates than outdoor teams — meaning dome teams underperformed expectations more. Only 2022 (+16.4pp) and 2023 (+8.5pp) show the expected pattern. The 2-year feasibility study (2023-2024) was misleading: 2023 showed the signal strongly but 2024 already had it reversing (-1.7pp), and adding 2020-2022 shows it reversed in 3 of 4 earlier seasons.

### Statistical Significance Test (All 6 Seasons)

Two-proportion z-test, dome vs outdoor:
- Dome upset rate: 32.1% (n=521)
- Outdoor upset rate: 33.7% (n=1,062)
- Gap: +1.7pp
- Z-score: 0.658
- P-value (approx): 0.511
- Significant at 5%: NO
- Significant at 10%: NO

**Verdict:** The dome vs outdoor gap is NOT statistically significant across 6 seasons. The hypothesis that dome games are safer for picking favorites is REJECTED.

### Extreme Weather Deep Dive

| Season | Extreme N | Extreme Upset % | vs Dome Gap |
|--------|-----------|-----------------|-------------|
| 2020 | 4 | 25.0% | -11.3pp |
| 2021 | 9 | 33.3% | -5.9pp |
| 2022 | 15 | 33.3% | +10.7pp |
| 2023 | 4 | 75.0% | +49.1pp |
| 2024 | 11 | 9.1% | -20.7pp |
| 2025 | 14 | 21.4% | -16.6pp |

**Critical finding:** Extreme weather games are extremely rare (4-15 per season) and their upset rates are wildly volatile: from 9.1% (2024 — barely any upsets at all) to 75.0% (2023 — tiny sample of 4 games). This is noise, not signal. Sample sizes are far too small to draw conclusions.

**Practical note:** In 6 seasons of simulation runs, 0 of 9,054 actual picks were classified as `weather_extreme`. Top-rated teams are virtually never playing in extreme cold — the high-WP matchups in late season are typically at warm-climate or dome venues, or the cold-weather favorites (Buffalo, KC) are so dominant they still lead the board.

### Upset Rates by Month

| Month | Games | Upset Rate |
|-------|-------|------------|
| Sep | 323 | 37.8% |
| Oct | 395 | 33.4% |
| Nov | 375 | 33.6% |
| Dec | 396 | 31.3% |
| Jan | 126 | 28.6% |

**Interesting trend:** Upsets are highest in September and decline through January. This aligns with the opposite of the weather hypothesis: late-season cold games have FEWER upsets, not more. The September warm/mild games show the most chaos. The effect is the opposite of what a dome preference filter would optimize for.

---

## Part 2: Filter Performance

### What the Filters Actually Did

**Critical finding about adverse/extreme filters:** The Avoid Adverse (Soft), Avoid Adverse (Hard), Avoid Extreme (Soft), and Avoid Extreme (Hard) filters produced IDENTICAL results to No Filter in every single simulation run (0 wins, 0 losses, 96 ties). The filters never changed any pick.

**Why:** Top-scoring picks (by any strategy) are virtually never in the `weather_adverse` or `weather_extreme` categories. High-WP teams are typically either dome teams (weather_neutral) or outdoor teams in good conditions (weather_mild). The filter correctly identifies adverse weather games as candidates to avoid, but the base scoring already avoids them implicitly — high-WP teams rarely play in conditions that would be classified as adverse.

Only 3.8% of all No Filter picks fell in `weather_adverse`. Zero fell in `weather_extreme`. The filters targeting these categories are effectively inert.

### Prefer Dome Soft vs No Filter

| Strategy | n=5 | n=10 | n=20 | n=50 | Total | vs No Filter |
|----------|-----|------|------|------|-------|--------------|
| 70/30 Blend | 155 | 310 | 620 | 1,550 | 2,635 | +340 |
| SP Production | 55 | 110 | 220 | 550 | 935 | -425 |
| Core/Satellite | 75 | 130 | 240 | 570 | 1,015 | -389 |
| SP Conservative | 160 | 320 | 640 | 1,600 | 2,720 | +765 |

**Note:** Dome Soft wins big for 70/30 Blend and SP Conservative but badly hurts SP Production and Core/Satellite. This is not a filter effect — it is a team selection effect.

### How Prefer Dome (Soft) Actually Works

The +10% dome bonus effectively lowers the WP threshold for picking a dome-team favorite. When a dome team is at 0.62 WP and an outdoor team is at 0.70 WP, the dome team's adjusted score becomes 0.62 × 1.10 = 0.682 — close to or beating the outdoor favorite. This changes which teams are picked, not just which weather conditions are avoided.

**Season-by-season dome filter impact (Dome Soft vs No Filter, 70/30 Blend n=10):**

| Season | No Filter EW | Dome Soft EW | Delta |
|--------|-------------|--------------|-------|
| 2020 | 40 | 100 | +60 |
| 2021 | 50 | 30 | -20 |
| 2022 | 0 | 80 | +80 |
| 2023 | 40 | 60 | +20 |
| 2024 | 110 | 10 | -100 |
| 2025 | 30 | 30 | 0 |

**2024 is catastrophic for dome preference:** 70/30 Blend No Filter survived to 110 entry-weeks at n=10 in 2024. The same strategy with Dome Soft collapsed to 10 entry-weeks. This is because 2024 dome teams had a 29.8% upset rate — picks directed toward dome teams missed the actual best picks (outdoor teams won more predictably in 2024).

The filter wins in 2020 and 2022 but loses badly in 2021, 2024, and 2025. Net positive only because 2020 and 2022 gains (+60, +80) dwarf 2021 and 2024 losses (-20, -100) across different n configurations.

### Prefer Dome Hard vs No Filter

Total delta across all runs: -935 (heavily negative). Hard dome preference is worse than soft because it overrides the scoring more aggressively and loses the smoothing benefit.

### Overall Champions Per Entry Count

| n | Strategy | Filter | Total EW (6 seasons) | vs No Filter Best |
|---|----------|--------|---------------------|-------------------|
| 5 | SP Conservative | Prefer Dome (Soft) | 160 | +45 |
| 10 | SP Conservative | Prefer Dome (Soft) | 320 | +90 |
| 20 | SP Conservative | Prefer Dome (Soft) | 640 | +180 |
| 50 | SP Conservative | Prefer Dome (Soft) | 1,600 | +450 |

**But context matters enormously:** SP Conservative + Dome Soft wins the headline because it happened to align with dome-team performance in certain seasons. Broken down by season, this strategy destroys value in 2024 (dome teams had high upset rates that year) and 2021.

### Filter Win/Loss Record vs No Filter (All 96 combos)

| Filter Mode | Wins | Losses | Ties | Total Delta |
|-------------|------|--------|------|-------------|
| Avoid Adverse (Soft) | 0 | 0 | 96 | 0 |
| Avoid Adverse (Hard) | 0 | 0 | 96 | 0 |
| Avoid Extreme (Soft) | 0 | 0 | 96 | 0 |
| Avoid Extreme (Hard) | 0 | 0 | 96 | 0 |
| Prefer Dome (Soft) | 33 | 47 | 16 | +291 |
| Prefer Dome (Hard) | 24 | 56 | 16 | -935 |

**Prefer Dome (Soft) has a losing win rate** (33 wins, 47 losses = 41.3% win rate) but positive total delta because it wins very big in the seasons it wins. This is a high-variance bet.

---

## Part 3: Statistical Confidence Assessment

### Sample Sizes and Power

| Category | N (games) | Needed for 80% power at 3pp gap* |
|----------|-----------|----------------------------------|
| Dome (all 6 seasons) | 521 | ~1,700 each arm |
| Outdoor (all 6 seasons) | 1,062 | ~1,700 each arm |
| Weather Extreme (all 6 seasons) | 57 | ~8,800 each arm |

*At α=0.05, β=0.20, for detecting 3pp difference in two proportions near 30%.

We are dramatically underpowered to detect a 3pp signal. With 521 dome games and 1,062 outdoor games, we need roughly 3x more data to draw firm conclusions at standard significance levels.

### Does the Signal Stabilize With More Data?

No. Adding seasons 2020-2022 to the 2023-2024 dataset moved the dome vs outdoor gap from +4.2pp to +1.7pp and made it even less consistent. The 6-season variance range is -5.3pp to +16.4pp. True stabilization toward a reliable signal would show year-over-year gaps clustering toward a consistent positive value. Instead they flip sign freely.

---

## Part 4: What the Simulation Actually Found

The headline result (SP Conservative + Prefer Dome Soft wins) is technically correct in aggregate but misleading as a product recommendation because:

1. The dome preference filter changes team selection, not weather avoidance. It is a de facto "tilt toward dome-team favorites" strategy, not a weather risk management tool.

2. The filter has a losing record in head-to-head comparisons (41.3% win rate across all combos).

3. Its net-positive total delta is driven by 2020 and 2022 — two seasons where dome teams happened to outperform their win probabilities. In 2021, 2024, and 2025, dome teams underperformed and the filter destroyed value.

4. The adverse weather filters are inert: the 4 adverse-weather filters produced zero picks different from the no-filter baseline. Weather avoidance as a signal-based filter is non-operational because top picks never land in adverse conditions.

---

## Product Implications

### Weather as a Filter Feature

**Recommendation: DO NOT implement weather filters as a default or core feature.**

Evidence:
- Dome vs outdoor gap: 1.7pp, p=0.511 — not statistically significant
- Adverse weather filters: literally inert (never change picks)
- Dome preference: 41.3% win rate in head-to-head, high variance, season-dependent

A filter that fails to fire is not useful. A filter with 41.3% win rate and high season-to-season variance is harmful more often than helpful.

### What WOULD Be Useful

If weather data is surfaced at all in SurvivorPulse:

1. **Display only, no filter:** Show the venue type (dome/outdoor) and game conditions as contextual information for users making manual overrides. Let the user decide — don't bake it into the algorithm.

2. **Seasonal volatility warning:** Flag when a top pick is a dome team whose WP is boosted by the dome premium assumption. (The data suggests dome teams don't consistently outperform their spread-derived WP.)

3. **September caution flag:** Sep games have a 37.8% upset rate vs 28.6% in January. A "early-season volatility" warning might be more useful than a weather filter.

4. **Retractable roof transparency:** The 46.9% upset rate for retractable-open games is notable (though sample is tiny at 32 games). Flagging "this stadium has a retractable roof and it is reported open today" could be informative.

### Revised Strategy Defaults (incorporating Round 10)

Weather filters should NOT be added to the default strategy stack. The Round 9 defaults stand:

- Non-buyback, n=5: SP Conservative + No Filter
- Non-buyback, n=10: Core/Satellite + No Filter
- Non-buyback, n=20: Core/Satellite + Avoid Div Soft (or No Filter)
- Non-buyback, n=50: 70/30 Blend + No Filter
- Buyback pools: SP Conservative + No Filter at all entry counts

---

## Data Assets Generated

- `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/data/nfl_games_2020_weather.json` — 256 games, 2020 season (camelCase format for simulation)
- `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/data/weather_classification_2020_2025.json` — Weather category lookup (season/week/home_team → category)
- `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/data/weather_raw_records_2020_2025.json` — Full game-level weather records for all 1,615 games
- `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/data/weather_upset_rates_2020_2025.json` — Upset rates by category, season, and venue
- `/Users/mrwolff/Projects/SurvivorPulse-BackTesting-Prototype/scripts/stan-weather-sim-results.json` — Full 672-run simulation results

---

## Summary: Signal Verdict

| Hypothesis | Status |
|------------|--------|
| Dome games produce fewer upsets than outdoor | REJECTED (not significant, p=0.51) |
| Cold/adverse weather games produce more upsets | NOT SUPPORTED (2020-2022 actually reversed) |
| Extreme weather significantly spikes upset rates | NOT SUPPORTED (too few games, extreme variance) |
| Avoiding adverse weather improves survivor outcomes | NOT APPLICABLE (filter never fires) |
| Preferring dome games improves survivor outcomes | MIXED (positive in aggregate, losing head-to-head record, driven by 2 seasons) |
| Signal stable across 6 seasons | NO (gap ranges from -5.3pp to +16.4pp year-over-year) |

**Final recommendation:** Close this research thread. Weather is not a reliable filter signal for NFL survivor pools with the available data. Shelf as potential long-term enhancement only if weather data coverage expands substantially (e.g., Open-Meteo integration with per-game conditions and 10+ seasons of data).
