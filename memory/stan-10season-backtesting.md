# SurvivorPulse 10-Season Backtesting Report

**Generated:** 2026-04-24  |  **Seasons:** 2016-2025  |  **Rounds:** A-E

**Scope:** 10 NFL seasons (2016-2025), 14 strategies, 4 entry counts, 3 buyback configs, 7 game context filters

**Season lengths:** 2016-2020 = 17 weeks | 2021-2025 = 18 weeks

**Total simulation runs:** ~3,980

**Data sources:**
- 2016-2019: nfl_data_py schedules + quadratic regression pick model (R²=0.46, RMSE=5.7pp)
- 2020: SurvivorPulse cache + synthetic picks
- 2021-2024: SurvivorPulse local cache + SurvivorGrid real pick data
- 2025: SurvivorPulse API cache

---
## Synthetic Pick Model Methodology

For 2016-2020 (pre-SurvivorGrid era), pick shares were modeled as:
```
pick_share = 90.14 × wp² - 66.14 × wp + 11.27  (+ Gaussian noise with σ=4.0%)
```
Fitted from 1,769 (win_prob, pick_share) pairs across 2021-2024 SurvivorGrid data.
R² = 0.46 | RMSE = 5.7 percentage points

**Caveats:** Pick behavior may have evolved over time. Early seasons (2016-2019) likely had:
- Higher chalk concentration (fewer data-driven players)
- Less sophisticated survivor pool culture
- Results for these seasons should be weighted lower in product decisions
- 2021-2025 results carry the most weight (real data)

---
## Season Difficulty Analysis

*Average entry-weeks survived per season at n=10, No Buyback, across all 14 strategies.*

| Season | Avg EW | Max Possible | Survival Rate | Weeks | Difficulty |
|--------|--------|--------------|---------------|-------|------------|
| 2016 | 25 | 170 | 14.5% | 17 | Hard (Synthetic) |
| 2017 | 21 | 170 | 12.1% | 17 | Hard (Synthetic) |
| 2018 | 27 | 170 | 15.7% | 17 | Hard (Synthetic) |
| 2019 | 29 | 170 | 16.9% | 17 | Hard (Synthetic) |
| 2020 | 36 | 170 | 21.1% | 17 | Hard (Synthetic) |
| 2021 | 22 | 180 | 12.2% | 18 | Hard (Real) |
| 2022 | 20 | 180 | 11.2% | 18 | Hard (Real) |
| 2023 | 22 | 180 | 12.1% | 18 | Hard (Real) |
| 2024 | 23 | 180 | 12.8% | 18 | Hard (Real) |
| 2025 | 34 | 180 | 18.7% | 18 | Hard (Real) |

---
## Round A: Strategy × Season Performance (n=5, No Buyback)

*Establishes which strategies work across the full 10-season dataset.*

Note: Totals are not directly comparable across season groups due to 17 vs 18 week seasons.

| Strategy | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Eff% |
|----------|------|------|------|------|------|------|------|------|------|------|-------|------|
| Temporal Diversification | 12 | 15 | 17 | 21 | 16 | 16 | 5 | 25 | 15 | 20 | **162** | 18.5% |
| SP Conservative 65/25/10 | 14 | 12 | 13 | 24 | 13 | 15 | 6 | 14 | 23 | 27 | **161** | 18.4% |
| 70/30 Blend | 13 | 12 | 13 | 16 | 25 | 15 | 10 | 17 | 14 | 26 | **161** | 18.4% |
| Lookahead-5 Exp(0.15) | 16 | 7 | 14 | 19 | 35 | 18 | 8 | 12 | 4 | 27 | **160** | 18.3% |
| Expendable-First 65/25/10 | 21 | 7 | 14 | 14 | 20 | 19 | 11 | 7 | 12 | 32 | **157** | 17.9% |
| SP Balanced 55/25/20 | 11 | 18 | 19 | 21 | 13 | 18 | 6 | 20 | 7 | 22 | **155** | 17.7% |
| Mixed Portfolio | 10 | 14 | 13 | 20 | 9 | 13 | 7 | 19 | 14 | 34 | **153** | 17.5% |
| Adaptive Blend 90/10→50/50 | 13 | 12 | 6 | 16 | 21 | 18 | 7 | 29 | 4 | 25 | **151** | 17.3% |
| Pure Win Probability | 12 | 12 | 6 | 16 | 19 | 21 | 8 | 13 | 3 | 35 | **145** | 16.6% |
| Leverage+60%Floor | 12 | 12 | 6 | 16 | 19 | 21 | 8 | 13 | 3 | 35 | **145** | 16.6% |
| Core/Satellite 60/40 | 12 | 13 | 17 | 17 | 15 | 8 | 8 | 17 | 16 | 11 | **134** | 15.3% |
| 80/20 Blend | 13 | 12 | 6 | 16 | 11 | 17 | 13 | 17 | 4 | 22 | **131** | 15.0% |
| SP Production 70EV+30FV | 5 | 11 | 20 | 14 | 18 | 2 | 6 | 13 | 23 | 9 | **121** | 13.8% |
| Anti-Chalk Top-5 | 5 | 6 | 8 | 5 | 15 | 1 | 19 | 4 | 5 | 11 | **79** | 9.0% |

### Round A Findings

- **Overall winner (n=5):** Temporal Diversification with 162 total entry-weeks (18.5% efficiency)
- **Runner-up:** SP Conservative 65/25/10 (161 EW)
- **Bottom performer:** Anti-Chalk Top-5 (79 EW)

#### Real Data Only (2021-2025, 18 weeks/season)

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Eff% |
|----------|------|------|------|------|------|-------|------|
| Mixed Portfolio | 13 | 7 | 19 | 14 | 34 | **87** | 19.3% |
| SP Conservative 65/25/10 | 15 | 6 | 14 | 23 | 27 | **85** | 18.9% |
| Adaptive Blend 90/10→50/50 | 18 | 7 | 29 | 4 | 25 | **83** | 18.4% |
| 70/30 Blend | 15 | 10 | 17 | 14 | 26 | **82** | 18.2% |
| Temporal Diversification | 16 | 5 | 25 | 15 | 20 | **81** | 18.0% |
| Expendable-First 65/25/10 | 19 | 11 | 7 | 12 | 32 | **81** | 18.0% |
| Pure Win Probability | 21 | 8 | 13 | 3 | 35 | **80** | 17.8% |
| Leverage+60%Floor | 21 | 8 | 13 | 3 | 35 | **80** | 17.8% |
| SP Balanced 55/25/20 | 18 | 6 | 20 | 7 | 22 | **73** | 16.2% |
| 80/20 Blend | 17 | 13 | 17 | 4 | 22 | **73** | 16.2% |

---
## Round B: Entry Count Scaling (No Buyback)


### n=5 — Max 875 total entry-weeks

| Strategy | 2016-2020 | 2021-2025 | TOTAL | Avg/Season | SD | Eff% |
|----------|-----------|-----------|-------|------------|----|----- |
| Temporal Diversification | 81 | 81 | **162** | 16.2 | 5.1 | 18.5% |
| SP Conservative 65/25/10 | 76 | 85 | **161** | 16.1 | 6.1 | 18.4% |
| 70/30 Blend | 79 | 82 | **161** | 16.1 | 5.1 | 18.4% |
| Lookahead-5 Exp(0.15) | 91 | 69 | **160** | 16.0 | 9.0 | 18.3% |
| Expendable-First 65/25/10 | 76 | 81 | **157** | 15.7 | 7.2 | 17.9% |
| SP Balanced 55/25/20 | 82 | 73 | **155** | 15.5 | 5.5 | 17.7% |
| Mixed Portfolio | 66 | 87 | **153** | 15.3 | 7.3 | 17.5% |
| Adaptive Blend 90/10→50/50 | 68 | 83 | **151** | 15.1 | 7.9 | 17.3% |
| Pure Win Probability | 65 | 80 | **145** | 14.5 | 8.6 | 16.6% |
| Leverage+60%Floor | 65 | 80 | **145** | 14.5 | 8.6 | 16.6% |
| Core/Satellite 60/40 | 74 | 60 | **134** | 13.4 | 3.4 | 15.3% |
| 80/20 Blend | 58 | 73 | **131** | 13.1 | 5.1 | 15.0% |
| SP Production 70EV+30FV | 68 | 53 | **121** | 12.1 | 6.5 | 13.8% |
| Anti-Chalk Top-5 | 39 | 40 | **79** | 7.9 | 5.2 | 9.0% |

### n=10 — Max 1750 total entry-weeks

| Strategy | 2016-2020 | 2021-2025 | TOTAL | Avg/Season | SD | Eff% |
|----------|-----------|-----------|-------|------------|----|----- |
| Adaptive Blend 90/10→50/50 | 152 | 144 | **296** | 29.6 | 6.7 | 16.9% |
| SP Balanced 55/25/20 | 162 | 132 | **294** | 29.4 | 5.6 | 16.8% |
| Core/Satellite 60/40 | 141 | 132 | **273** | 27.3 | 7.4 | 15.6% |
| Pure Win Probability | 135 | 130 | **265** | 26.5 | 8.8 | 15.1% |
| 80/20 Blend | 146 | 117 | **263** | 26.3 | 5.6 | 15.0% |
| Temporal Diversification | 132 | 130 | **262** | 26.2 | 5.3 | 15.0% |
| SP Conservative 65/25/10 | 136 | 126 | **262** | 26.2 | 5.5 | 15.0% |
| Leverage+60%Floor | 131 | 130 | **261** | 26.1 | 8.5 | 14.9% |
| Lookahead-5 Exp(0.15) | 154 | 106 | **260** | 26.0 | 8.8 | 14.9% |
| Expendable-First 65/25/10 | 144 | 112 | **256** | 25.6 | 8.3 | 14.6% |
| 70/30 Blend | 144 | 111 | **255** | 25.5 | 7.8 | 14.6% |
| Mixed Portfolio | 113 | 128 | **241** | 24.1 | 6.8 | 13.8% |
| SP Production 70EV+30FV | 136 | 97 | **233** | 23.3 | 7.2 | 13.3% |
| Anti-Chalk Top-5 | 86 | 93 | **179** | 17.9 | 7.9 | 10.2% |

### n=20 — Max 3500 total entry-weeks

| Strategy | 2016-2020 | 2021-2025 | TOTAL | Avg/Season | SD | Eff% |
|----------|-----------|-----------|-------|------------|----|----- |
| SP Balanced 55/25/20 | 213 | 221 | **434** | 43.4 | 6.8 | 12.4% |
| Adaptive Blend 90/10→50/50 | 218 | 216 | **434** | 43.4 | 10.8 | 12.4% |
| Mixed Portfolio | 211 | 214 | **425** | 42.5 | 7.5 | 12.1% |
| Temporal Diversification | 209 | 213 | **422** | 42.2 | 10.6 | 12.1% |
| 80/20 Blend | 219 | 197 | **416** | 41.6 | 9.1 | 11.9% |
| SP Conservative 65/25/10 | 216 | 194 | **410** | 41.0 | 8.1 | 11.7% |
| Core/Satellite 60/40 | 216 | 194 | **410** | 41.0 | 9.6 | 11.7% |
| 70/30 Blend | 212 | 198 | **410** | 41.0 | 9.1 | 11.7% |
| Pure Win Probability | 214 | 192 | **406** | 40.6 | 11.6 | 11.6% |
| Expendable-First 65/25/10 | 215 | 187 | **402** | 40.2 | 9.2 | 11.5% |
| Lookahead-5 Exp(0.15) | 219 | 177 | **396** | 39.6 | 10.9 | 11.3% |
| Leverage+60%Floor | 200 | 183 | **383** | 38.3 | 11.0 | 10.9% |
| SP Production 70EV+30FV | 203 | 177 | **380** | 38.0 | 6.4 | 10.9% |
| Anti-Chalk Top-5 | 121 | 168 | **289** | 28.9 | 8.0 | 8.3% |

### n=50 — Max 8750 total entry-weeks

| Strategy | 2016-2020 | 2021-2025 | TOTAL | Avg/Season | SD | Eff% |
|----------|-----------|-----------|-------|------------|----|----- |
| SP Conservative 65/25/10 | 407 | 441 | **848** | 84.8 | 17.0 | 9.7% |
| 70/30 Blend | 405 | 438 | **843** | 84.3 | 18.6 | 9.6% |
| Lookahead-5 Exp(0.15) | 416 | 418 | **834** | 83.4 | 14.0 | 9.5% |
| Core/Satellite 60/40 | 397 | 430 | **827** | 82.7 | 13.9 | 9.5% |
| 80/20 Blend | 396 | 418 | **814** | 81.4 | 17.3 | 9.3% |
| Expendable-First 65/25/10 | 419 | 387 | **806** | 80.6 | 16.6 | 9.2% |
| SP Production 70EV+30FV | 374 | 420 | **794** | 79.4 | 9.5 | 9.1% |
| Mixed Portfolio | 397 | 397 | **794** | 79.4 | 14.1 | 9.1% |
| Adaptive Blend 90/10→50/50 | 399 | 379 | **778** | 77.8 | 22.1 | 8.9% |
| Pure Win Probability | 409 | 361 | **770** | 77.0 | 25.0 | 8.8% |
| SP Balanced 55/25/20 | 353 | 412 | **765** | 76.5 | 20.2 | 8.7% |
| Temporal Diversification | 344 | 404 | **748** | 74.8 | 18.2 | 8.5% |
| Leverage+60%Floor | 402 | 333 | **735** | 73.5 | 22.2 | 8.4% |
| Anti-Chalk Top-5 | 382 | 335 | **717** | 71.7 | 15.8 | 8.2% |

### Round B Winners by Entry Count

| n | Winner | Total EW | Runner-up | Runner-up EW | 70/30 Blend EW |
|---|--------|----------|-----------|--------------|----------------|
| 5 | Temporal Diversification | 162 | 70/30 Blend | 161 | 161 |
| 10 | Adaptive Blend 90/10→50/50 | 296 | SP Balanced 55/25/20 | 294 | 255 |
| 20 | SP Balanced 55/25/20 | 434 | Adaptive Blend 90/10→50/50 | 434 | 410 |
| 50 | SP Conservative 65/25/10 | 848 | 70/30 Blend | 843 | 843 |

---
## Round C: Differentiated Scoring

*Entries must pick different teams each week. Tests whether forced differentiation improves or hurts survival.*


### n=5 | Differentiated Scoring

| Strategy | 10-Season Total | Avg/Season | SD | Eff% | vs Standard |
|----------|-----------------|------------|----|----- |-------------|
| Lookahead-5 Exp(0.15) | 170 | 17.0 | 10.6 | 19.4% | +10 |
| SP Balanced 55/25/20 | 168 | 16.8 | 5.7 | 19.2% | +13 |
| Core/Satellite 60/40 | 165 | 16.5 | 5.2 | 18.9% | +31 |
| 70/30 Blend | 165 | 16.5 | 5.2 | 18.9% | +4 |
| Adaptive Blend 90/10→50/50 | 160 | 16.0 | 8.6 | 18.3% | +9 |
| SP Conservative 65/25/10 | 158 | 15.8 | 5.8 | 18.1% | -3 |
| Expendable-First 65/25/10 | 143 | 14.3 | 5.1 | 16.3% | -14 |
| Anti-Chalk Top-5 | 137 | 13.7 | 7.6 | 15.7% | +58 |
| Pure Win Probability | 136 | 13.6 | 6.7 | 15.5% | -9 |
| Leverage+60%Floor | 136 | 13.6 | 6.7 | 15.5% | -9 |
| 80/20 Blend | 134 | 13.4 | 5.6 | 15.3% | +3 |
| SP Production 70EV+30FV | 126 | 12.6 | 6.8 | 14.4% | +5 |

### n=10 | Differentiated Scoring

| Strategy | 10-Season Total | Avg/Season | SD | Eff% | vs Standard |
|----------|-----------------|------------|----|----- |-------------|
| SP Balanced 55/25/20 | 306 | 30.6 | 7.1 | 17.5% | +12 |
| Adaptive Blend 90/10→50/50 | 289 | 28.9 | 6.9 | 16.5% | -7 |
| 80/20 Blend | 286 | 28.6 | 6.0 | 16.3% | +23 |
| SP Conservative 65/25/10 | 268 | 26.8 | 6.5 | 15.3% | +6 |
| Core/Satellite 60/40 | 265 | 26.5 | 6.9 | 15.1% | -8 |
| 70/30 Blend | 265 | 26.5 | 6.9 | 15.1% | +10 |
| Pure Win Probability | 258 | 25.8 | 7.2 | 14.7% | -7 |
| SP Production 70EV+30FV | 257 | 25.7 | 7.8 | 14.7% | +24 |
| Lookahead-5 Exp(0.15) | 256 | 25.6 | 6.5 | 14.6% | -4 |
| Leverage+60%Floor | 255 | 25.5 | 7.4 | 14.6% | -6 |
| Expendable-First 65/25/10 | 246 | 24.6 | 6.8 | 14.1% | -10 |
| Anti-Chalk Top-5 | 209 | 20.9 | 7.3 | 11.9% | +30 |

### n=20 | Differentiated Scoring

| Strategy | 10-Season Total | Avg/Season | SD | Eff% | vs Standard |
|----------|-----------------|------------|----|----- |-------------|
| Core/Satellite 60/40 | 443 | 44.3 | 13.2 | 12.7% | +33 |
| 70/30 Blend | 443 | 44.3 | 13.2 | 12.7% | +33 |
| SP Balanced 55/25/20 | 441 | 44.1 | 7.2 | 12.6% | +7 |
| 80/20 Blend | 424 | 42.4 | 9.3 | 12.1% | +8 |
| Adaptive Blend 90/10→50/50 | 421 | 42.1 | 10.7 | 12.0% | -13 |
| SP Conservative 65/25/10 | 416 | 41.6 | 6.6 | 11.9% | +6 |
| Expendable-First 65/25/10 | 413 | 41.3 | 10.7 | 11.8% | +11 |
| Pure Win Probability | 394 | 39.4 | 9.3 | 11.3% | -12 |
| Lookahead-5 Exp(0.15) | 387 | 38.7 | 9.7 | 11.1% | -9 |
| SP Production 70EV+30FV | 380 | 38.0 | 7.0 | 10.9% | +0 |
| Leverage+60%Floor | 364 | 36.4 | 9.6 | 10.4% | -19 |
| Anti-Chalk Top-5 | 312 | 31.2 | 9.5 | 8.9% | +23 |

### n=50 | Differentiated Scoring

| Strategy | 10-Season Total | Avg/Season | SD | Eff% | vs Standard |
|----------|-----------------|------------|----|----- |-------------|
| Expendable-First 65/25/10 | 724 | 72.4 | 8.8 | 8.3% | -82 |
| Core/Satellite 60/40 | 724 | 72.4 | 9.8 | 8.3% | -103 |
| 70/30 Blend | 724 | 72.4 | 9.8 | 8.3% | -119 |
| SP Conservative 65/25/10 | 692 | 69.2 | 9.4 | 7.9% | -156 |
| 80/20 Blend | 692 | 69.2 | 8.2 | 7.9% | -122 |
| Pure Win Probability | 685 | 68.5 | 9.0 | 7.8% | -85 |
| Lookahead-5 Exp(0.15) | 683 | 68.3 | 7.3 | 7.8% | -151 |
| Adaptive Blend 90/10→50/50 | 682 | 68.2 | 8.3 | 7.8% | -96 |
| SP Balanced 55/25/20 | 670 | 67.0 | 8.3 | 7.7% | -95 |
| SP Production 70EV+30FV | 664 | 66.4 | 8.7 | 7.6% | -130 |
| Leverage+60%Floor | 659 | 65.9 | 8.8 | 7.5% | -76 |
| Anti-Chalk Top-5 | 629 | 62.9 | 5.9 | 7.2% | -88 |

---
## Round D: Buyback Mechanics

*Does adding a buyback window materially improve survival?*

### Winner by Entry Count × Buyback Config (10-season totals)

| n | No Buyback | BB Wk1-3 | BB Wk1-4 |
|---|------------|----------|---------|
| **5** | Temporal Diversification (162) | SP Conservative 65/25/10 (244) | SP Conservative 65/25/10 (261) |
| **10** | Adaptive Blend 90/10→50/50 (296) | SP Conservative 65/25/10 (463) | SP Conservative 65/25/10 (473) |
| **20** | SP Balanced 55/25/20 (434) | SP Conservative 65/25/10 (705) | 70/30 Blend (741) |
| **50** | SP Conservative 65/25/10 (848) | SP Conservative 65/25/10 (1461) | SP Conservative 65/25/10 (1540) |

### Buyback Lift Analysis (n=10)

| Strategy | No BB | BB Wk1-3 | Δ(3) | BB Wk1-4 | Δ(4) |
|----------|-------|----------|------|----------|------|
| SP Conservative 65/25/10 | 262 | 463 | +201 | 473 | +211 |
| SP Balanced 55/25/20 | 294 | 438 | +144 | 450 | +156 |
| 70/30 Blend | 255 | 426 | +171 | 458 | +203 |
| Temporal Diversification | 262 | 422 | +160 | 453 | +191 |
| Core/Satellite 60/40 | 273 | 411 | +138 | 433 | +160 |
| Pure Win Probability | 265 | 410 | +145 | 446 | +181 |
| Leverage+60%Floor | 261 | 408 | +147 | 418 | +157 |
| Adaptive Blend 90/10→50/50 | 296 | 402 | +106 | 432 | +136 |
| 80/20 Blend | 263 | 395 | +132 | 418 | +155 |
| Mixed Portfolio | 241 | 386 | +145 | 409 | +168 |
| Lookahead-5 Exp(0.15) | 260 | 386 | +126 | 420 | +160 |
| Expendable-First 65/25/10 | 256 | 374 | +118 | 406 | +150 |
| SP Production 70EV+30FV | 233 | 356 | +123 | 388 | +155 |
| Anti-Chalk Top-5 | 179 | 333 | +154 | 345 | +166 |

---
## Round E: Game Context Filters

*Do divisional avoidance or home-field preference filters improve survival?*

**Note:** 2016-2019 divisional data derived from team division lookup table. 2025 divisional flags unavailable (cache format limitation).


### 70/30 Blend — Filter Comparison

| Filter | n=5 | n=10 | n=20 | n=50 | Best n |
|--------|-----|------|------|------|--------|
| No Filter | 161 | 255 | 410 | 843 | n=50 |
| Avoid Div (Soft -10%) | 183 | 267 | 407 | 849 | n=50 ◄ |
| Avoid Div (Hard swap) | 181 | 257 | 386 | 844 | n=50 ◄ |
| Prefer Home (Soft +10%) | 163 | 244 | 406 | 794 | n=50 |
| Prefer Home (Hard swap) | 155 | 232 | 356 | 776 | n=50 |
| Both Soft | 137 | 220 | 368 | 756 | n=50 |
| Both Hard | 135 | 202 | 312 | 731 | n=50 |

### SP Production 70EV+30FV — Filter Comparison

| Filter | n=5 | n=10 | n=20 | n=50 | Best n |
|--------|-----|------|------|------|--------|
| No Filter | 121 | 233 | 380 | 794 | n=50 |
| Avoid Div (Soft -10%) | 101 | 194 | 332 | 755 | n=50 |
| Avoid Div (Hard swap) | 105 | 189 | 319 | 762 | n=50 |
| Prefer Home (Soft +10%) | 110 | 188 | 350 | 623 | n=50 |
| Prefer Home (Hard swap) | 110 | 189 | 331 | 607 | n=50 |
| Both Soft | 113 | 190 | 335 | 708 | n=50 |
| Both Hard | 108 | 185 | 311 | 705 | n=50 |

### Core/Satellite 60/40 — Filter Comparison

| Filter | n=5 | n=10 | n=20 | n=50 | Best n |
|--------|-----|------|------|------|--------|
| No Filter | 161 | 255 | 410 | 843 | n=50 |
| Avoid Div (Soft -10%) | 183 | 267 | 407 | 849 | n=50 ◄ |
| Avoid Div (Hard swap) | 181 | 257 | 386 | 844 | n=50 ◄ |
| Prefer Home (Soft +10%) | 163 | 244 | 406 | 794 | n=50 |
| Prefer Home (Hard swap) | 155 | 232 | 356 | 776 | n=50 |
| Both Soft | 137 | 220 | 368 | 756 | n=50 |
| Both Hard | 135 | 202 | 312 | 731 | n=50 |

### SP Conservative 65/25/10 — Filter Comparison

| Filter | n=5 | n=10 | n=20 | n=50 | Best n |
|--------|-----|------|------|------|--------|
| No Filter | 161 | 262 | 410 | 848 | n=50 |
| Avoid Div (Soft -10%) | 164 | 279 | 395 | 829 | n=50 ◄ |
| Avoid Div (Hard swap) | 166 | 273 | 365 | 825 | n=50 ◄ |
| Prefer Home (Soft +10%) | 175 | 251 | 396 | 771 | n=50 |
| Prefer Home (Hard swap) | 167 | 244 | 349 | 739 | n=50 |
| Both Soft | 141 | 244 | 365 | 784 | n=50 |
| Both Hard | 140 | 208 | 310 | 752 | n=50 |

---
## Regime Analysis: Historical vs Modern

*2016-2020 (synthetic picks + shorter seasons) vs 2021-2025 (real data)*

*⚠ Historical results carry lower confidence due to synthetic pick data*


### n=10, No Buyback — Synthetic Era (2016-2020) vs Real Data Era (2021-2025)

| Strategy | Hist Avg/Season | Real Avg/Season | Δ | Signal |
|----------|-----------------|-----------------|---|--------|
| Lookahead-5 Exp(0.15) | 1.81 EW/wk | 1.18 EW/wk | -0.63 | Declined |
| SP Production 70EV+30FV | 1.60 EW/wk | 1.08 EW/wk | -0.52 | Declined |
| 70/30 Blend | 1.69 EW/wk | 1.23 EW/wk | -0.46 | Declined |
| Expendable-First 65/25/10 | 1.69 EW/wk | 1.24 EW/wk | -0.45 | Declined |
| SP Balanced 55/25/20 | 1.91 EW/wk | 1.47 EW/wk | -0.44 | Declined |
| 80/20 Blend | 1.72 EW/wk | 1.30 EW/wk | -0.42 | Declined |
| SP Conservative 65/25/10 | 1.60 EW/wk | 1.40 EW/wk | -0.20 | Declined |
| Core/Satellite 60/40 | 1.66 EW/wk | 1.47 EW/wk | -0.19 | Declined |
| Adaptive Blend 90/10→50/50 | 1.79 EW/wk | 1.60 EW/wk | -0.19 | Declined |
| Pure Win Probability | 1.59 EW/wk | 1.44 EW/wk | -0.14 | Declined |
| Temporal Diversification | 1.55 EW/wk | 1.44 EW/wk | -0.11 | Declined |
| Leverage+60%Floor | 1.54 EW/wk | 1.44 EW/wk | -0.10 | Declined |
| Mixed Portfolio | 1.33 EW/wk | 1.42 EW/wk | +0.09 | Improved |
| Anti-Chalk Top-5 | 1.01 EW/wk | 1.03 EW/wk | +0.02 | Stable |

---
## Consistency Analysis (SD across 10 seasons)

*Lower SD = more predictable across seasons. Key for product recommendations.*


### n=10, No Buyback — All 10 Seasons

| Rank | Strategy | Total EW | Avg/Season | SD | CV |
|------|----------|----------|------------|----|----|
| 1 | Temporal Diversification | 262 | 26.2 | 5.3 | 0.202 |
| 2 | SP Conservative 65/25/10 | 262 | 26.2 | 5.5 | 0.210 |
| 3 | 80/20 Blend | 263 | 26.3 | 5.6 | 0.212 |
| 4 | SP Balanced 55/25/20 | 294 | 29.4 | 5.6 | 0.191 |
| 5 | Adaptive Blend 90/10→50/50 | 296 | 29.6 | 6.7 | 0.228 |
| 6 | Mixed Portfolio | 241 | 24.1 | 6.8 | 0.284 |
| 7 | SP Production 70EV+30FV | 233 | 23.3 | 7.2 | 0.309 |
| 8 | Core/Satellite 60/40 | 273 | 27.3 | 7.4 | 0.273 |
| 9 | 70/30 Blend | 255 | 25.5 | 7.8 | 0.306 |
| 10 | Anti-Chalk Top-5 | 179 | 17.9 | 7.9 | 0.442 |
| 11 | Expendable-First 65/25/10 | 256 | 25.6 | 8.3 | 0.323 |
| 12 | Leverage+60%Floor | 261 | 26.1 | 8.5 | 0.324 |
| 13 | Pure Win Probability | 265 | 26.5 | 8.8 | 0.331 |
| 14 | Lookahead-5 Exp(0.15) | 260 | 26.0 | 8.8 | 0.338 |

---
## Product Recommendation Matrix

*Based on 10-season performance + consistency. Primary ICP: n=10.*

*Risk-adjusted score = avg_per_season - 0.5 × SD (penalizes volatility)*


### No Buyback Recommendations

| Pool Size | Recommended Strategy | 10-Season Total | SD | Risk-Adj Score |
|-----------|----------------------|-----------------|----| ---------------|
| n=5 | **Temporal Diversification** | 162 | 5.1 | 13.6 |
| n=10 | **SP Balanced 55/25/20** | 294 | 5.6 | 26.6 |
| n=20 | **SP Balanced 55/25/20** | 434 | 6.8 | 40.0 |
| n=50 | **Lookahead-5 Exp(0.15)** | 834 | 14.0 | 76.4 |

### Buyback Recommendations (Wk1-3 window)

| Pool Size | Recommended Strategy | 10-Season Total | SD | Risk-Adj Score |
|-----------|----------------------|-----------------|----| ---------------|
| n=5 | **SP Conservative 65/25/10** | 244 | 5.2 | 21.8 |
| n=10 | **SP Balanced 55/25/20** | 438 | 9.2 | 39.2 |
| n=20 | **70/30 Blend** | 692 | 9.1 | 64.6 |
| n=50 | **70/30 Blend** | 1456 | 12.4 | 139.4 |

---
## Comparison: 3-Season vs 5-Season vs 10-Season Findings

| Finding | 3-Season (2022-2025) | 5-Season (2021-2025) | 10-Season (2016-2025) | Verdict |
|---------|---------------------|---------------------|----------------------|---------|
| n=5 champion | 70/30 Blend | TBD from 5-season | See Round A | Confirm/Update |
| n=10 champion | SP Production | TBD | See Round B | Confirm/Update |
| Buyback lift | Yes, +20-40% | TBD | See Round D | Confirm/Update |
| Game filters | Marginal/Neutral | TBD | See Round E | Confirm/Update |
| Best BB strategy | SP Conservative | TBD | See Round D | Confirm/Update |

*Note: Fill in 3-season/5-season columns from prior research docs for direct comparison.*

---
## Statistical Confidence Improvement

| Metric | 3 Seasons | 5 Seasons | 10 Seasons |
|--------|-----------|-----------|------------|
| Season sample size | 3 | 5 | 10 |
| Real pick data | 3 years | 4 years | 4 years (2021-2024) |
| Total entry-weeks (n=10) | 3×18×10=540 | 5×18×10=900 | 5×17×10+5×18×10=1750 |
| SE of mean (est.) | ±33% | ±22% | ±16% |
| NFL regime coverage | 2022-2025 (recent) | 2021-2025 | 2016-2025 (full modern era) |

**Key confidence gains:**
- 10 seasons covers pre-COVID, COVID, and post-COVID NFL eras
- Better representation of 'hard' years (e.g., 2017 had many upsets)
- Strategy rankings that hold across 10 seasons have ~3× more confidence than 3-season findings
- Still limited by synthetic picks for 2016-2020; treat those seasons as directional signals

---
*Report generated by Stan the Scout — SurvivorPulse Intelligence Layer*

*Run date: 2026-04-24 | Script: stan-10season-sim.py*