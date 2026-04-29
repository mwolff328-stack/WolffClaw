# SurvivorPulse 5-Season Backtesting Report

**Generated:** 2026-04-13  |  **Seasons:** 2021-2025  |  **Rounds:** 1 unified run

**Scope:** 14 strategies × 4 entry counts × 3 buyback configs × 5 seasons = 840 runs

---
## Season Difficulty (Total Entry-Weeks Survived at n=10, No Buyback)

| Season | Entry-Weeks | Max Possible | Survival Rate | Difficulty |
|--------|-------------|--------------|---------------|------------|
| 2021 | 22 | 180 | 12.2% | Hard |
| 2022 | 20 | 180 | 11.2% | Hard |
| 2023 | 22 | 180 | 12.1% | Hard |
| 2024 | 23 | 180 | 12.8% | Hard |
| 2025 | 34 | 180 | 18.7% | Hard |

---
## Executive Summary

### Key Findings

- **n=5 (No Buyback):** Mixed Portfolio wins with 87 entry-weeks (+5 vs 70/30 Blend)
- **n=10 (No Buyback):** Adaptive Blend 90/10→50/50 wins with 144 entry-weeks (+33 vs 70/30 Blend)
- **n=20 (No Buyback):** SP Balanced 55/25/20 wins with 221 entry-weeks (+23 vs 70/30 Blend)
- **n=50 (No Buyback):** SP Conservative 65/25/10 wins with 441 entry-weeks (+3 vs 70/30 Blend)

- **n=5 (Buyback Wk1-3):** SP Balanced 55/25/20 wins with 128 entry-weeks
- **n=10 (Buyback Wk1-3):** SP Conservative 65/25/10 wins with 239 entry-weeks
- **n=20 (Buyback Wk1-3):** SP Conservative 65/25/10 wins with 357 entry-weeks
- **n=50 (Buyback Wk1-3):** SP Balanced 55/25/20 wins with 736 entry-weeks

---
## Full Results Tables

### No Buyback

#### n=5 | max=90/season | 450 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| Mixed Portfolio | 13 | 7 | 19 | 14 | 34 | **87** | 17.4 | 9.1 | 19.3% |
| SP Conservative 65/25/10 | 15 | 6 | 14 | 23 | 27 | **85** | 17.0 | 7.3 | 18.9% |
| Adaptive Blend 90/10→50/50 | 18 | 7 | 29 | 4 | 25 | **83** | 16.6 | 9.8 | 18.4% |
| 70/30 Blend | 15 | 10 | 17 | 14 | 26 | **82** | 16.4 | 5.3 | 18.2% |
| Expendable-First 65/25/10 | 19 | 11 | 7 | 12 | 32 | **81** | 16.2 | 8.8 | 18.0% |
| Temporal Diversification | 16 | 5 | 25 | 15 | 20 | **81** | 16.2 | 6.6 | 18.0% |
| Pure Win Probability | 21 | 8 | 13 | 3 | 35 | **80** | 16.0 | 11.2 | 17.8% |
| Leverage+60%Floor | 21 | 8 | 13 | 3 | 35 | **80** | 16.0 | 11.2 | 17.8% |
| 80/20 Blend | 17 | 13 | 17 | 4 | 22 | **73** | 14.6 | 6.0 | 16.2% |
| SP Balanced 55/25/20 | 18 | 6 | 20 | 7 | 22 | **73** | 14.6 | 6.7 | 16.2% |
| Lookahead-5 Exp(0.15) | 18 | 8 | 12 | 4 | 27 | **69** | 13.8 | 8.1 | 15.3% |
| Core/Satellite 60/40 | 8 | 8 | 17 | 16 | 11 | **60** | 12.0 | 3.8 | 13.3% |
| SP Production 70EV+30FV | 2 | 6 | 13 | 23 | 9 | **53** | 10.6 | 7.2 | 11.8% |
| Anti-Chalk Top-5 | 1 | 19 | 4 | 5 | 11 | **40** | 8.0 | 6.4 | 8.9% |

#### n=10 | max=180/season | 900 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| Adaptive Blend 90/10→50/50 | 36 | 21 | 34 | 20 | 33 | **144** | 28.8 | 6.9 | 16.0% |
| SP Balanced 55/25/20 | 28 | 22 | 25 | 25 | 32 | **132** | 26.4 | 3.4 | 14.7% |
| Core/Satellite 60/40 | 17 | 14 | 33 | 36 | 32 | **132** | 26.4 | 9.0 | 14.7% |
| Pure Win Probability | 28 | 22 | 23 | 14 | 43 | **130** | 26.0 | 9.6 | 14.4% |
| Leverage+60%Floor | 28 | 22 | 23 | 14 | 43 | **130** | 26.0 | 9.6 | 14.4% |
| Temporal Diversification | 33 | 21 | 20 | 21 | 35 | **130** | 26.0 | 6.6 | 14.4% |
| Mixed Portfolio | 22 | 19 | 25 | 20 | 42 | **128** | 25.6 | 8.5 | 14.2% |
| SP Conservative 65/25/10 | 24 | 20 | 19 | 29 | 34 | **126** | 25.2 | 5.6 | 14.0% |
| 80/20 Blend | 18 | 21 | 24 | 24 | 30 | **117** | 23.4 | 4.0 | 13.0% |
| Expendable-First 65/25/10 | 20 | 24 | 16 | 16 | 36 | **112** | 22.4 | 7.4 | 12.4% |
| 70/30 Blend | 16 | 19 | 20 | 22 | 34 | **111** | 22.2 | 6.2 | 12.3% |
| Lookahead-5 Exp(0.15) | 19 | 19 | 21 | 16 | 31 | **106** | 21.2 | 5.2 | 11.8% |
| SP Production 70EV+30FV | 11 | 15 | 15 | 32 | 24 | **97** | 19.4 | 7.6 | 10.8% |
| Anti-Chalk Top-5 | 7 | 24 | 8 | 33 | 21 | **93** | 18.6 | 9.9 | 10.3% |

#### n=20 | max=360/season | 1800 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Balanced 55/25/20 | 49 | 33 | 44 | 44 | 51 | **221** | 44.2 | 6.2 | 12.3% |
| Adaptive Blend 90/10→50/50 | 57 | 31 | 48 | 29 | 51 | **216** | 43.2 | 11.2 | 12.0% |
| Mixed Portfolio | 50 | 38 | 37 | 37 | 52 | **214** | 42.8 | 6.7 | 11.9% |
| Temporal Diversification | 47 | 32 | 41 | 32 | 61 | **213** | 42.6 | 10.8 | 11.8% |
| 70/30 Blend | 45 | 31 | 38 | 32 | 52 | **198** | 39.6 | 8.0 | 11.0% |
| 80/20 Blend | 47 | 31 | 36 | 35 | 48 | **197** | 39.4 | 6.8 | 10.9% |
| SP Conservative 65/25/10 | 42 | 30 | 28 | 46 | 48 | **194** | 38.8 | 8.3 | 10.8% |
| Core/Satellite 60/40 | 35 | 29 | 47 | 29 | 54 | **194** | 38.8 | 10.0 | 10.8% |
| Pure Win Probability | 51 | 29 | 36 | 22 | 54 | **192** | 38.4 | 12.4 | 10.7% |
| Expendable-First 65/25/10 | 46 | 34 | 31 | 27 | 49 | **187** | 37.4 | 8.6 | 10.4% |
| Leverage+60%Floor | 51 | 27 | 33 | 23 | 49 | **183** | 36.6 | 11.4 | 10.2% |
| SP Production 70EV+30FV | 38 | 26 | 31 | 39 | 43 | **177** | 35.4 | 6.1 | 9.8% |
| Lookahead-5 Exp(0.15) | 38 | 29 | 32 | 27 | 51 | **177** | 35.4 | 8.6 | 9.8% |
| Anti-Chalk Top-5 | 26 | 36 | 35 | 44 | 27 | **168** | 33.6 | 6.6 | 9.3% |

#### n=50 | max=900/season | 4500 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 97 | 56 | 97 | 110 | 81 | **441** | 88.2 | 18.5 | 9.8% |
| 70/30 Blend | 91 | 52 | 101 | 106 | 88 | **438** | 87.6 | 19.0 | 9.7% |
| Core/Satellite 60/40 | 85 | 81 | 97 | 82 | 85 | **430** | 86.0 | 5.7 | 9.6% |
| SP Production 70EV+30FV | 82 | 76 | 93 | 88 | 81 | **420** | 84.0 | 5.9 | 9.3% |
| 80/20 Blend | 92 | 42 | 97 | 102 | 85 | **418** | 83.6 | 21.5 | 9.3% |
| Lookahead-5 Exp(0.15) | 85 | 83 | 78 | 75 | 97 | **418** | 83.6 | 7.6 | 9.3% |
| SP Balanced 55/25/20 | 91 | 40 | 101 | 95 | 85 | **412** | 82.4 | 21.8 | 9.2% |
| Temporal Diversification | 90 | 52 | 97 | 75 | 90 | **404** | 80.8 | 16.1 | 9.0% |
| Mixed Portfolio | 90 | 52 | 95 | 72 | 88 | **397** | 79.4 | 15.7 | 8.8% |
| Expendable-First 65/25/10 | 90 | 45 | 77 | 81 | 94 | **387** | 77.4 | 17.3 | 8.6% |
| Adaptive Blend 90/10→50/50 | 102 | 48 | 108 | 34 | 87 | **379** | 75.8 | 29.6 | 8.4% |
| Pure Win Probability | 95 | 41 | 106 | 26 | 93 | **361** | 72.2 | 32.3 | 8.0% |
| Anti-Chalk Top-5 | 40 | 77 | 48 | 96 | 74 | **335** | 67.0 | 20.4 | 7.4% |
| Leverage+60%Floor | 87 | 38 | 88 | 30 | 90 | **333** | 66.6 | 26.8 | 7.4% |

### Buyback Wk1-3

#### n=5 | max=90/season | 450 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Balanced 55/25/20 | 28 | 16 | 23 | 33 | 28 | **128** | 25.6 | 5.7 | 28.4% |
| SP Conservative 65/25/10 | 25 | 18 | 18 | 30 | 30 | **121** | 24.2 | 5.4 | 26.9% |
| Mixed Portfolio | 20 | 18 | 21 | 15 | 35 | **109** | 21.8 | 6.9 | 24.2% |
| 70/30 Blend | 24 | 20 | 19 | 16 | 27 | **106** | 21.2 | 3.9 | 23.6% |
| Expendable-First 65/25/10 | 20 | 24 | 16 | 14 | 32 | **106** | 21.2 | 6.4 | 23.6% |
| Pure Win Probability | 27 | 19 | 22 | 14 | 23 | **105** | 21.0 | 4.3 | 23.3% |
| Leverage+60%Floor | 27 | 19 | 22 | 14 | 23 | **105** | 21.0 | 4.3 | 23.3% |
| Anti-Chalk Top-5 | 15 | 23 | 12 | 39 | 16 | **105** | 21.0 | 9.7 | 23.3% |
| Temporal Diversification | 22 | 15 | 18 | 16 | 30 | **101** | 20.2 | 5.5 | 22.4% |
| Adaptive Blend 90/10→50/50 | 25 | 18 | 24 | 7 | 26 | **100** | 20.0 | 7.1 | 22.2% |
| Lookahead-5 Exp(0.15) | 25 | 16 | 18 | 11 | 27 | **97** | 19.4 | 5.9 | 21.6% |
| 80/20 Blend | 22 | 20 | 20 | 7 | 27 | **96** | 19.2 | 6.6 | 21.3% |
| SP Production 70EV+30FV | 21 | 10 | 17 | 30 | 17 | **95** | 19.0 | 6.5 | 21.1% |
| Core/Satellite 60/40 | 16 | 11 | 20 | 22 | 23 | **92** | 18.4 | 4.4 | 20.4% |

#### n=10 | max=180/season | 900 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 41 | 33 | 33 | 91 | 41 | **239** | 47.8 | 21.9 | 26.6% |
| SP Balanced 55/25/20 | 52 | 30 | 39 | 62 | 42 | **225** | 45.0 | 11.0 | 25.0% |
| 70/30 Blend | 37 | 38 | 37 | 53 | 48 | **213** | 42.6 | 6.7 | 23.7% |
| Temporal Diversification | 49 | 30 | 38 | 53 | 40 | **210** | 42.0 | 8.2 | 23.3% |
| Pure Win Probability | 45 | 28 | 43 | 48 | 38 | **202** | 40.4 | 7.0 | 22.4% |
| 80/20 Blend | 45 | 37 | 35 | 39 | 42 | **198** | 39.6 | 3.6 | 22.0% |
| Adaptive Blend 90/10→50/50 | 53 | 33 | 36 | 27 | 47 | **196** | 39.2 | 9.5 | 21.8% |
| Leverage+60%Floor | 45 | 25 | 34 | 47 | 42 | **193** | 38.6 | 8.1 | 21.4% |
| Core/Satellite 60/40 | 34 | 34 | 39 | 42 | 44 | **193** | 38.6 | 4.1 | 21.4% |
| Mixed Portfolio | 49 | 24 | 37 | 29 | 44 | **183** | 36.6 | 9.2 | 20.3% |
| Anti-Chalk Top-5 | 20 | 33 | 38 | 55 | 33 | **179** | 35.8 | 11.3 | 19.9% |
| SP Production 70EV+30FV | 36 | 23 | 28 | 45 | 38 | **170** | 34.0 | 7.7 | 18.9% |
| Lookahead-5 Exp(0.15) | 32 | 28 | 31 | 35 | 42 | **168** | 33.6 | 4.8 | 18.7% |
| Expendable-First 65/25/10 | 37 | 31 | 30 | 25 | 40 | **163** | 32.6 | 5.3 | 18.1% |

#### n=20 | max=360/season | 1800 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 60 | 49 | 70 | 103 | 75 | **357** | 71.4 | 18.1 | 19.8% |
| Temporal Diversification | 62 | 50 | 78 | 89 | 71 | **350** | 70.0 | 13.3 | 19.4% |
| 70/30 Blend | 59 | 61 | 72 | 82 | 67 | **341** | 68.2 | 8.3 | 18.9% |
| Adaptive Blend 90/10→50/50 | 70 | 51 | 68 | 77 | 67 | **333** | 66.6 | 8.5 | 18.5% |
| Core/Satellite 60/40 | 60 | 58 | 68 | 71 | 73 | **330** | 66.0 | 6.0 | 18.3% |
| SP Production 70EV+30FV | 64 | 55 | 68 | 63 | 78 | **328** | 65.6 | 7.5 | 18.2% |
| SP Balanced 55/25/20 | 70 | 49 | 63 | 83 | 62 | **327** | 65.4 | 11.1 | 18.2% |
| 80/20 Blend | 60 | 52 | 66 | 78 | 70 | **326** | 65.2 | 8.8 | 18.1% |
| Pure Win Probability | 63 | 44 | 70 | 86 | 61 | **324** | 64.8 | 13.6 | 18.0% |
| Mixed Portfolio | 71 | 43 | 65 | 72 | 71 | **322** | 64.4 | 11.0 | 17.9% |
| Expendable-First 65/25/10 | 54 | 50 | 54 | 71 | 70 | **299** | 59.8 | 8.9 | 16.6% |
| Lookahead-5 Exp(0.15) | 51 | 53 | 62 | 55 | 71 | **292** | 58.4 | 7.3 | 16.2% |
| Leverage+60%Floor | 57 | 40 | 54 | 68 | 52 | **271** | 54.2 | 9.0 | 15.1% |
| Anti-Chalk Top-5 | 35 | 49 | 53 | 65 | 52 | **254** | 50.8 | 9.6 | 14.1% |

#### n=50 | max=900/season | 4500 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Balanced 55/25/20 | 156 | 117 | 141 | 165 | 157 | **736** | 147.2 | 17.0 | 16.4% |
| SP Conservative 65/25/10 | 152 | 118 | 143 | 175 | 145 | **733** | 146.6 | 18.3 | 16.3% |
| 70/30 Blend | 148 | 128 | 146 | 160 | 134 | **716** | 143.2 | 11.2 | 15.9% |
| Mixed Portfolio | 146 | 119 | 150 | 152 | 140 | **707** | 141.4 | 11.9 | 15.7% |
| Expendable-First 65/25/10 | 146 | 113 | 147 | 156 | 143 | **705** | 141.0 | 14.7 | 15.7% |
| Core/Satellite 60/40 | 103 | 145 | 143 | 147 | 144 | **682** | 136.4 | 16.8 | 15.2% |
| Adaptive Blend 90/10→50/50 | 158 | 134 | 152 | 89 | 149 | **682** | 136.4 | 25.0 | 15.2% |
| SP Production 70EV+30FV | 103 | 141 | 142 | 141 | 154 | **681** | 136.2 | 17.3 | 15.1% |
| 80/20 Blend | 141 | 127 | 142 | 120 | 147 | **677** | 135.4 | 10.2 | 15.0% |
| Lookahead-5 Exp(0.15) | 151 | 129 | 145 | 114 | 135 | **674** | 134.8 | 12.9 | 15.0% |
| Temporal Diversification | 145 | 116 | 144 | 123 | 133 | **661** | 132.2 | 11.4 | 14.7% |
| Pure Win Probability | 144 | 100 | 142 | 103 | 130 | **619** | 123.8 | 18.9 | 13.8% |
| Leverage+60%Floor | 137 | 97 | 141 | 80 | 132 | **587** | 117.4 | 24.4 | 13.0% |
| Anti-Chalk Top-5 | 66 | 132 | 110 | 138 | 127 | **573** | 114.6 | 26.0 | 12.7% |

### Buyback Wk1-4

#### n=5 | max=90/season | 450 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Balanced 55/25/20 | 28 | 16 | 23 | 33 | 28 | **128** | 25.6 | 5.7 | 28.4% |
| SP Conservative 65/25/10 | 25 | 18 | 18 | 30 | 30 | **121** | 24.2 | 5.4 | 26.9% |
| 70/30 Blend | 24 | 29 | 19 | 16 | 32 | **120** | 24.0 | 6.0 | 26.7% |
| Mixed Portfolio | 25 | 18 | 21 | 15 | 40 | **119** | 23.8 | 8.7 | 26.4% |
| Expendable-First 65/25/10 | 20 | 24 | 16 | 14 | 42 | **116** | 23.2 | 10.0 | 25.8% |
| Lookahead-5 Exp(0.15) | 25 | 19 | 18 | 11 | 42 | **115** | 23.0 | 10.5 | 25.6% |
| Pure Win Probability | 28 | 19 | 22 | 14 | 31 | **114** | 22.8 | 6.1 | 25.3% |
| Leverage+60%Floor | 28 | 19 | 22 | 14 | 31 | **114** | 22.8 | 6.1 | 25.3% |
| Temporal Diversification | 22 | 15 | 18 | 28 | 30 | **113** | 22.6 | 5.7 | 25.1% |
| 80/20 Blend | 27 | 21 | 20 | 7 | 36 | **111** | 22.2 | 9.5 | 24.7% |
| Anti-Chalk Top-5 | 15 | 20 | 12 | 39 | 21 | **107** | 21.4 | 9.4 | 23.8% |
| Adaptive Blend 90/10→50/50 | 27 | 18 | 24 | 7 | 26 | **102** | 20.4 | 7.4 | 22.7% |
| SP Production 70EV+30FV | 21 | 10 | 17 | 30 | 17 | **95** | 19.0 | 6.5 | 21.1% |
| Core/Satellite 60/40 | 16 | 12 | 20 | 22 | 23 | **93** | 18.6 | 4.1 | 20.7% |

#### n=10 | max=180/season | 900 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 41 | 33 | 33 | 91 | 41 | **239** | 47.8 | 21.9 | 26.6% |
| SP Balanced 55/25/20 | 52 | 34 | 39 | 64 | 42 | **231** | 46.2 | 10.7 | 25.7% |
| 70/30 Blend | 41 | 38 | 37 | 56 | 48 | **220** | 44.0 | 7.1 | 24.4% |
| Temporal Diversification | 46 | 31 | 38 | 53 | 45 | **213** | 42.6 | 7.5 | 23.7% |
| Pure Win Probability | 44 | 28 | 43 | 48 | 45 | **208** | 41.6 | 7.0 | 23.1% |
| 80/20 Blend | 43 | 34 | 35 | 44 | 51 | **207** | 41.4 | 6.3 | 23.0% |
| Adaptive Blend 90/10→50/50 | 42 | 42 | 36 | 41 | 46 | **207** | 41.4 | 3.2 | 23.0% |
| Core/Satellite 60/40 | 38 | 42 | 39 | 42 | 45 | **206** | 41.2 | 2.5 | 22.9% |
| Anti-Chalk Top-5 | 22 | 35 | 38 | 56 | 45 | **196** | 39.2 | 11.2 | 21.8% |
| Leverage+60%Floor | 44 | 25 | 34 | 47 | 45 | **195** | 39.0 | 8.3 | 21.7% |
| Lookahead-5 Exp(0.15) | 32 | 35 | 31 | 35 | 57 | **190** | 38.0 | 9.6 | 21.1% |
| Expendable-First 65/25/10 | 37 | 31 | 30 | 31 | 58 | **187** | 37.4 | 10.6 | 20.8% |
| Mixed Portfolio | 43 | 24 | 37 | 29 | 54 | **187** | 37.4 | 10.6 | 20.8% |
| SP Production 70EV+30FV | 36 | 28 | 28 | 45 | 49 | **186** | 37.2 | 8.6 | 20.7% |

#### n=20 | max=360/season | 1800 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 60 | 59 | 70 | 103 | 77 | **369** | 73.8 | 16.0 | 20.5% |
| 70/30 Blend | 70 | 65 | 72 | 83 | 72 | **362** | 72.4 | 5.9 | 20.1% |
| SP Balanced 55/25/20 | 70 | 53 | 65 | 91 | 80 | **359** | 71.8 | 13.0 | 19.9% |
| Temporal Diversification | 64 | 42 | 78 | 89 | 80 | **353** | 70.6 | 16.4 | 19.6% |
| Pure Win Probability | 66 | 53 | 70 | 90 | 72 | **351** | 70.2 | 11.9 | 19.5% |
| Core/Satellite 60/40 | 60 | 66 | 68 | 73 | 82 | **349** | 69.8 | 7.4 | 19.4% |
| Adaptive Blend 90/10→50/50 | 64 | 59 | 68 | 79 | 76 | **346** | 69.2 | 7.4 | 19.2% |
| SP Production 70EV+30FV | 68 | 50 | 68 | 66 | 85 | **337** | 67.4 | 11.1 | 18.7% |
| 80/20 Blend | 66 | 49 | 65 | 80 | 76 | **336** | 67.2 | 10.8 | 18.7% |
| Mixed Portfolio | 64 | 43 | 65 | 72 | 88 | **332** | 66.4 | 14.5 | 18.4% |
| Expendable-First 65/25/10 | 54 | 51 | 55 | 80 | 81 | **321** | 64.2 | 13.4 | 17.8% |
| Lookahead-5 Exp(0.15) | 51 | 54 | 62 | 61 | 84 | **312** | 62.4 | 11.6 | 17.3% |
| Leverage+60%Floor | 63 | 41 | 54 | 71 | 55 | **284** | 56.8 | 10.0 | 15.8% |
| Anti-Chalk Top-5 | 39 | 53 | 53 | 66 | 59 | **270** | 54.0 | 8.9 | 15.0% |

#### n=50 | max=900/season | 4500 total

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |
|----------|------|------|------|------|------|-------|-----|----|------|
| SP Conservative 65/25/10 | 156 | 128 | 156 | 175 | 164 | **779** | 155.8 | 15.5 | 17.3% |
| Lookahead-5 Exp(0.15) | 158 | 157 | 158 | 124 | 167 | **764** | 152.8 | 14.9 | 17.0% |
| SP Balanced 55/25/20 | 159 | 119 | 152 | 165 | 167 | **762** | 152.4 | 17.5 | 16.9% |
| 70/30 Blend | 164 | 128 | 153 | 162 | 144 | **751** | 150.2 | 13.2 | 16.7% |
| Expendable-First 65/25/10 | 153 | 114 | 159 | 150 | 175 | **751** | 150.2 | 20.1 | 16.7% |
| Mixed Portfolio | 142 | 123 | 150 | 139 | 171 | **725** | 145.0 | 15.7 | 16.1% |
| Temporal Diversification | 153 | 129 | 153 | 131 | 156 | **722** | 144.4 | 11.8 | 16.0% |
| Core/Satellite 60/40 | 116 | 150 | 154 | 155 | 143 | **718** | 143.6 | 14.4 | 16.0% |
| Adaptive Blend 90/10→50/50 | 150 | 125 | 170 | 107 | 165 | **717** | 143.4 | 24.0 | 15.9% |
| 80/20 Blend | 145 | 124 | 157 | 134 | 156 | **716** | 143.2 | 12.7 | 15.9% |
| SP Production 70EV+30FV | 107 | 145 | 153 | 147 | 159 | **711** | 142.2 | 18.3 | 15.8% |
| Pure Win Probability | 152 | 104 | 153 | 104 | 163 | **676** | 135.2 | 25.8 | 15.0% |
| Leverage+60%Floor | 147 | 92 | 149 | 83 | 161 | **632** | 126.4 | 32.2 | 14.0% |
| Anti-Chalk Top-5 | 68 | 144 | 122 | 139 | 145 | **618** | 123.6 | 29.0 | 13.7% |

---
## Winner Tables Per Dimension

### Winner by Entry Count × Buyback Config

| n | No Buyback | Buyback Wk1-3 | Buyback Wk1-4 |
|---|------------|---------------|---------------|
| **5** | Mixed Portfolio (87) | SP Balanced 55/25/20 (128) | SP Balanced 55/25/20 (128) |
| **10** | Adaptive Blend 90/10→50/50 (144) | SP Conservative 65/25/10 (239) | SP Conservative 65/25/10 (239) |
| **20** | SP Balanced 55/25/20 (221) | SP Conservative 65/25/10 (357) | SP Conservative 65/25/10 (369) |
| **50** | SP Conservative 65/25/10 (441) | SP Balanced 55/25/20 (736) | SP Conservative 65/25/10 (779) |

---
## Consistency Analysis (SD across 5 seasons)

*Lower SD = more consistent. Consistency matters more than peak for product recs.*

### n=5 | No Buyback

| Rank | Strategy | 5-Season Total | Avg/Season | SD | CV (SD/Avg) |
|------|----------|----------------|------------|----|-------------|
| 1 | Core/Satellite 60/40 | 60 | 12.0 | 3.8 | 0.321 |
| 2 | 70/30 Blend | 82 | 16.4 | 5.3 | 0.324 |
| 3 | 80/20 Blend | 73 | 14.6 | 6.0 | 0.412 |
| 4 | Anti-Chalk Top-5 | 40 | 8.0 | 6.4 | 0.798 |
| 5 | Temporal Diversification | 81 | 16.2 | 6.6 | 0.408 |
| 6 | SP Balanced 55/25/20 | 73 | 14.6 | 6.7 | 0.462 |
| 7 | SP Production 70EV+30FV | 53 | 10.6 | 7.2 | 0.677 |
| 8 | SP Conservative 65/25/10 | 85 | 17.0 | 7.3 | 0.432 |
| 9 | Lookahead-5 Exp(0.15) | 69 | 13.8 | 8.1 | 0.584 |
| 10 | Expendable-First 65/25/10 | 81 | 16.2 | 8.8 | 0.543 |
| 11 | Mixed Portfolio | 87 | 17.4 | 9.1 | 0.525 |
| 12 | Adaptive Blend 90/10→50/50 | 83 | 16.6 | 9.8 | 0.589 |
| 13 | Pure Win Probability | 80 | 16.0 | 11.2 | 0.700 |
| 14 | Leverage+60%Floor | 80 | 16.0 | 11.2 | 0.700 |

### n=10 | No Buyback

| Rank | Strategy | 5-Season Total | Avg/Season | SD | CV (SD/Avg) |
|------|----------|----------------|------------|----|-------------|
| 1 | SP Balanced 55/25/20 | 132 | 26.4 | 3.4 | 0.128 |
| 2 | 80/20 Blend | 117 | 23.4 | 4.0 | 0.170 |
| 3 | Lookahead-5 Exp(0.15) | 106 | 21.2 | 5.2 | 0.243 |
| 4 | SP Conservative 65/25/10 | 126 | 25.2 | 5.6 | 0.224 |
| 5 | 70/30 Blend | 111 | 22.2 | 6.2 | 0.280 |
| 6 | Temporal Diversification | 130 | 26.0 | 6.6 | 0.253 |
| 7 | Adaptive Blend 90/10→50/50 | 144 | 28.8 | 6.9 | 0.238 |
| 8 | Expendable-First 65/25/10 | 112 | 22.4 | 7.4 | 0.331 |
| 9 | SP Production 70EV+30FV | 97 | 19.4 | 7.6 | 0.392 |
| 10 | Mixed Portfolio | 128 | 25.6 | 8.5 | 0.330 |
| 11 | Core/Satellite 60/40 | 132 | 26.4 | 9.0 | 0.343 |
| 12 | Pure Win Probability | 130 | 26.0 | 9.6 | 0.370 |
| 13 | Leverage+60%Floor | 130 | 26.0 | 9.6 | 0.370 |
| 14 | Anti-Chalk Top-5 | 93 | 18.6 | 9.9 | 0.532 |

### n=20 | No Buyback

| Rank | Strategy | 5-Season Total | Avg/Season | SD | CV (SD/Avg) |
|------|----------|----------------|------------|----|-------------|
| 1 | SP Production 70EV+30FV | 177 | 35.4 | 6.1 | 0.172 |
| 2 | SP Balanced 55/25/20 | 221 | 44.2 | 6.2 | 0.141 |
| 3 | Anti-Chalk Top-5 | 168 | 33.6 | 6.6 | 0.196 |
| 4 | Mixed Portfolio | 214 | 42.8 | 6.7 | 0.157 |
| 5 | 80/20 Blend | 197 | 39.4 | 6.8 | 0.173 |
| 6 | 70/30 Blend | 198 | 39.6 | 8.0 | 0.201 |
| 7 | SP Conservative 65/25/10 | 194 | 38.8 | 8.3 | 0.213 |
| 8 | Expendable-First 65/25/10 | 187 | 37.4 | 8.6 | 0.230 |
| 9 | Lookahead-5 Exp(0.15) | 177 | 35.4 | 8.6 | 0.244 |
| 10 | Core/Satellite 60/40 | 194 | 38.8 | 10.0 | 0.259 |
| 11 | Temporal Diversification | 213 | 42.6 | 10.8 | 0.254 |
| 12 | Adaptive Blend 90/10→50/50 | 216 | 43.2 | 11.2 | 0.259 |
| 13 | Leverage+60%Floor | 183 | 36.6 | 11.4 | 0.312 |
| 14 | Pure Win Probability | 192 | 38.4 | 12.4 | 0.322 |

### n=50 | No Buyback

| Rank | Strategy | 5-Season Total | Avg/Season | SD | CV (SD/Avg) |
|------|----------|----------------|------------|----|-------------|
| 1 | Core/Satellite 60/40 | 430 | 86.0 | 5.7 | 0.067 |
| 2 | SP Production 70EV+30FV | 420 | 84.0 | 5.9 | 0.070 |
| 3 | Lookahead-5 Exp(0.15) | 418 | 83.6 | 7.6 | 0.091 |
| 4 | Mixed Portfolio | 397 | 79.4 | 15.7 | 0.198 |
| 5 | Temporal Diversification | 404 | 80.8 | 16.1 | 0.199 |
| 6 | Expendable-First 65/25/10 | 387 | 77.4 | 17.3 | 0.224 |
| 7 | SP Conservative 65/25/10 | 441 | 88.2 | 18.5 | 0.210 |
| 8 | 70/30 Blend | 438 | 87.6 | 19.0 | 0.216 |
| 9 | Anti-Chalk Top-5 | 335 | 67.0 | 20.4 | 0.304 |
| 10 | 80/20 Blend | 418 | 83.6 | 21.5 | 0.258 |
| 11 | SP Balanced 55/25/20 | 412 | 82.4 | 21.8 | 0.265 |
| 12 | Leverage+60%Floor | 333 | 66.6 | 26.8 | 0.402 |
| 13 | Adaptive Blend 90/10→50/50 | 379 | 75.8 | 29.6 | 0.390 |
| 14 | Pure Win Probability | 361 | 72.2 | 32.3 | 0.447 |

---
## Regime Analysis: 2021-2022 vs 2023-2025

*Are there strategies that dominated early but faded, or vice versa?*

### n=5 | No Buyback — Early (2021-2022) vs Late (2023-2025)

| Strategy | 2021-2022 Avg | 2023-2025 Avg | Δ Late-Early | Regime |
|----------|---------------|---------------|--------------|--------|
| Mixed Portfolio | 10.0 | 22.3 | +12.3 | Improved |
| SP Production 70EV+30FV | 4.0 | 15.0 | +11.0 | Improved |
| SP Conservative 65/25/10 | 10.5 | 21.3 | +10.8 | Improved |
| Temporal Diversification | 10.5 | 20.0 | +9.5 | Improved |
| Adaptive Blend 90/10→50/50 | 12.5 | 19.3 | +6.8 | Improved |
| Core/Satellite 60/40 | 8.0 | 14.7 | +6.7 | Improved |
| 70/30 Blend | 12.5 | 19.0 | +6.5 | Improved |
| SP Balanced 55/25/20 | 12.0 | 16.3 | +4.3 | Improved |
| Anti-Chalk Top-5 | 10.0 | 6.7 | -3.3 | Declined |
| Pure Win Probability | 14.5 | 17.0 | +2.5 | Improved |
| Leverage+60%Floor | 14.5 | 17.0 | +2.5 | Improved |
| Expendable-First 65/25/10 | 15.0 | 17.0 | +2.0 | Stable |
| Lookahead-5 Exp(0.15) | 13.0 | 14.3 | +1.3 | Stable |
| 80/20 Blend | 15.0 | 14.3 | -0.7 | Stable |

### n=10 | No Buyback — Early (2021-2022) vs Late (2023-2025)

| Strategy | 2021-2022 Avg | 2023-2025 Avg | Δ Late-Early | Regime |
|----------|---------------|---------------|--------------|--------|
| Core/Satellite 60/40 | 15.5 | 33.7 | +18.2 | Improved |
| SP Production 70EV+30FV | 13.0 | 23.7 | +10.7 | Improved |
| Mixed Portfolio | 20.5 | 29.0 | +8.5 | Improved |
| 70/30 Blend | 17.5 | 25.3 | +7.8 | Improved |
| 80/20 Blend | 19.5 | 26.0 | +6.5 | Improved |
| SP Conservative 65/25/10 | 22.0 | 27.3 | +5.3 | Improved |
| Anti-Chalk Top-5 | 15.5 | 20.7 | +5.2 | Improved |
| Lookahead-5 Exp(0.15) | 19.0 | 22.7 | +3.7 | Improved |
| SP Balanced 55/25/20 | 25.0 | 27.3 | +2.3 | Improved |
| Pure Win Probability | 25.0 | 26.7 | +1.7 | Stable |
| Leverage+60%Floor | 25.0 | 26.7 | +1.7 | Stable |
| Temporal Diversification | 27.0 | 25.3 | -1.7 | Stable |
| Expendable-First 65/25/10 | 22.0 | 22.7 | +0.7 | Stable |
| Adaptive Blend 90/10→50/50 | 28.5 | 29.0 | +0.5 | Stable |

---
## Product Recommendation Matrix

*Based on 5-season performance + consistency. Primary ICP is n=10.*

| Pool Size | No Buyback Rec | Buyback Rec |
|-----------|----------------|-------------|
| **n=5** | 70/30 Blend (82 total, SD=5.3) | SP Balanced 55/25/20 (128 total, SD=5.7) |
| **n=10** | Adaptive Blend 90/10→50/50 (144 total, SD=6.9) | SP Balanced 55/25/20 (225 total, SD=11.0) |
| **n=20** | SP Balanced 55/25/20 (221 total, SD=6.2) | 70/30 Blend (341 total, SD=8.3) |
| **n=50** | Core/Satellite 60/40 (430 total, SD=5.7) | SP Balanced 55/25/20 (736 total, SD=17.0) |

### Recommendation Narrative

**n=5:** No buyback → **70/30 Blend**. With buyback → **SP Balanced 55/25/20**.
**n=10:** No buyback → **Adaptive Blend 90/10→50/50**. With buyback → **SP Balanced 55/25/20**.
**n=20:** No buyback → **SP Balanced 55/25/20**. With buyback → **70/30 Blend**.
**n=50:** No buyback → **Core/Satellite 60/40**. With buyback → **SP Balanced 55/25/20**.

---
## Notable Findings from 2021-2022 Data

### Per-Season Breakdown (n=10, No Buyback)

| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL |
|----------|------|------|------|------|------|-------|
| Adaptive Blend 90/10→50/50 | 36 | 21 | 34 | 20 | 33 | 144 |
| SP Balanced 55/25/20 | 28 | 22 | 25 | 25 | 32 | 132 |
| Core/Satellite 60/40 | 17 | 14 | 33 | 36 | 32 | 132 |
| Temporal Diversification | 33 | 21 | 20 | 21 | 35 | 130 |
| Pure Win Probability | 28 | 22 | 23 | 14 | 43 | 130 |
| Leverage+60%Floor | 28 | 22 | 23 | 14 | 43 | 130 |
| Mixed Portfolio | 22 | 19 | 25 | 20 | 42 | 128 |
| SP Conservative 65/25/10 | 24 | 20 | 19 | 29 | 34 | 126 |
| 80/20 Blend | 18 | 21 | 24 | 24 | 30 | 117 |
| Expendable-First 65/25/10 | 20 | 24 | 16 | 16 | 36 | 112 |
| 70/30 Blend | 16 | 19 | 20 | 22 | 34 | 111 |
| Lookahead-5 Exp(0.15) | 19 | 19 | 21 | 16 | 31 | 106 |
| SP Production 70EV+30FV | 11 | 15 | 15 | 32 | 24 | 97 |
| Anti-Chalk Top-5 | 7 | 24 | 8 | 33 | 21 | 93 |

### Best and Worst Season per Strategy (n=10, No Buyback)

| Strategy | Best Season | Worst Season | Range |
|----------|-------------|--------------|-------|
| Pure Win Probability | 2025 (43) | 2024 (14) | 29 |
| 70/30 Blend | 2025 (34) | 2021 (16) | 18 |
| 80/20 Blend | 2025 (30) | 2021 (18) | 12 |
| SP Production 70EV+30FV | 2024 (32) | 2021 (11) | 21 |
| SP Conservative 65/25/10 | 2025 (34) | 2023 (19) | 15 |
| SP Balanced 55/25/20 | 2025 (32) | 2022 (22) | 10 |
| Leverage+60%Floor | 2025 (43) | 2024 (14) | 29 |
| Anti-Chalk Top-5 | 2024 (33) | 2021 (7) | 26 |
| Expendable-First 65/25/10 | 2025 (36) | 2023 (16) | 20 |
| Core/Satellite 60/40 | 2024 (36) | 2022 (14) | 22 |
| Mixed Portfolio | 2025 (42) | 2022 (19) | 23 |
| Temporal Diversification | 2025 (35) | 2023 (20) | 15 |
| Adaptive Blend 90/10→50/50 | 2021 (36) | 2024 (20) | 16 |
| Lookahead-5 Exp(0.15) | 2025 (31) | 2024 (16) | 15 |

---
*Report generated by Stan the Scout — SurvivorPulse Intelligence Layer*