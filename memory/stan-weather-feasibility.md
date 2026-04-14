---
name: Weather Impact Feasibility Study
description: Stan's feasibility study on weather as a filter for NFL survivor pool backtesting
type: project
---

# Weather Impact Feasibility Study
**Date:** 2026-04-14  
**Requested by:** Luigi  
**Analyst:** Stan the Scout

---

## Part 1: Data Availability

### 1A. nfl_data_py Weather Fields

`nfl_data_py.import_schedules()` includes the following weather/venue columns:

| Field | Coverage | Notes |
|-------|----------|-------|
| `roof` | 100% | Values: `outdoors`, `dome`, `closed`, `open` (retractable) |
| `surface` | Partial | grass, fieldturf, matrixturf, sportturf, a_turf, astroturf |
| `temp` | 55.4% (158/285) | Missing for dome/indoor games; degrees Fahrenheit |
| `wind` | 55.4% (158/285) | Missing for dome/indoor games; mph |
| `stadium` | 100% | Full stadium name |
| `stadium_id` | 100% | Unique ID per venue |

**Conclusion:** `roof` field is complete and reliable for dome/outdoor classification. Actual temp/wind data is only populated for ~55% of games (outdoor only), which is actually correct behavior — indoor games have no weather.

### 1B. Existing Local Game Data (SurvivorPulse-BackTesting-Prototype)

Files: `data/nfl_games_2021-2024.json` and `data/nfl_games_2025_cache.json`

**Fields available:**
```json
{"week", "season", "homeTeamId", "awayTeamId", "homeSpread", 
 "homeWinProbability", "awayWinProbability", "homeScore", "awayScore", "completed"}
```

**No weather or stadium fields.** These files only have spread/probability/score data.

The 2025 games cache (`nfl_games_2025_games_cache.json`) is keyed by week and contains team-level data with `{teamId, winProbability, pickShare, outcome, is_home, opponent_id, is_divisional}`. Also **no weather fields**.

### 1C. SurvivorPulse API (2025 Data)

No weather or venue fields present in any cached API data. The API is focused on survivor pool metrics (win probability, pick share, outcome) — not game conditions.

**Data Availability Verdict:** nfl_data_py is the only source with venue/weather data. It's free, well-maintained, and the `roof` field alone is sufficient for dome vs outdoor classification without needing real-time weather.

---

## Part 2: Stadium Classification

### Dome / Weather-Neutral (8 teams)
| Team | Stadium | Roof Type |
|------|---------|-----------|
| ARI | State Farm Stadium | closed/retractable |
| ATL | Mercedes-Benz Stadium | closed |
| DET | Ford Field | dome |
| IND | Lucas Oil Stadium | closed |
| LAC/LAR | SoFi Stadium | dome |
| LV | Allegiant Stadium | dome |
| MIN | U.S. Bank Stadium | dome |
| NO | Mercedes-Benz Superdome | dome |

### Retractable Roof (situational — 2 teams)
| Team | Stadium | Notes |
|------|---------|-------|
| DAL | AT&T Stadium | Open = outdoor; Closed = dome |
| HOU | NRG Stadium | Open = outdoor; Closed = dome |

nfl_data_py `roof` field captures actual game-day state (`open` vs `closed`) where available.

### Outdoor Cold-Weather (18+ teams)
BAL, BUF, CHI, CIN, CLE, DEN, GB, KC, NE, NYG, NYJ, PHI, PIT, SEA, TEN, WAS

### Outdoor Warm-Weather
CAR, JAX, MIA, SF, TB

Note: LAR plays at SoFi (dome). International games (London, Munich) appear in data with home team's stadium classification.

---

## Part 3: Historical Weather via Open-Meteo

**API:** `https://archive-api.open-meteo.com/v1/archive`  
**Cost:** Free, no API key required  
**Coverage:** Full historical data back to 1940

### Sample Test — Buffalo NY, Dec 17 2023 (Bills vs Cowboys)
```
Location: 42.77°N, 78.79°W (Buffalo/Orchard Park area)
1PM ET conditions:
  Temperature: 46.8°F
  Precipitation: 0.0 in
  Wind speed: 15.0 mph
  Wind gusts: 29.8 mph
```

### Fields Available
- `temperature_2m` (°F or °C configurable)
- `precipitation` (inches or mm)
- `wind_speed_10m` (mph or km/h)
- `wind_gusts_10m` (mph or km/h)
- Hourly resolution — can target game-time window (e.g. 1PM-4PM ET)

### Stadium Coordinates Needed
Would need a lat/lon lookup table for each outdoor stadium (~25 stadiums). Easy to build.

**Open-Meteo Verdict:** Fully viable. Free, reliable, historical. Could enrich the dataset with actual game-day conditions for all outdoor games going back to 2020+.

---

## Part 4: Proxy Analysis — Dome vs Outdoor Upset Rates

**Data:** 544 regular season games, 2023-2024 (excluding pick'em spreads <1.0)  
**Method:** Games classified by venue type + calendar month. Upset = favorite loses SU (spread used to identify favorite only).

### Two-Year Combined Results (2023 + 2024)

| Category | Games | Upsets | Upset Rate | Fav Win Rate |
|----------|-------|--------|------------|--------------|
| Outdoor Transitional (Nov) | 76 | 19 | **25.0%** | 75.0% |
| **Dome** | **175** | **49** | **28.0%** | **72.0%** |
| Outdoor Cold (Dec/Jan) | 121 | 39 | **32.2%** | 67.8% |
| Outdoor Warm (Sep/Oct) | 172 | 58 | **33.7%** | 66.3% |

### Key Signal
- **Dome upset rate: 28.0%**
- **Outdoor cold upset rate: 32.2%**
- **Difference: +4.2pp** (cold-weather games have MORE upsets than dome)
- **Threshold: 3pp** → **EXCEEDS threshold** ✓

### Year-by-Year Breakdown

| Category | 2023 Upset% | 2024 Upset% |
|----------|-------------|-------------|
| Dome | 25.9% | 29.8% |
| Outdoor Cold | **39.7%** | **24.1%** |
| Outdoor Transitional | 23.7% | 26.3% |
| Outdoor Warm | 35.6% | 31.7% |

**⚠ Yellow Flag:** The cold-weather signal is NOT consistent year-to-year. In 2023, cold games had a massive 39.7% upset rate (vs 25.9% dome = +13.8pp). In 2024, cold games had *fewer* upsets than dome (24.1% vs 29.8% = -5.7pp). High variance with small samples (~60-63 games per year per category).

### Warm Weather Surprise
Outdoor warm (Sep/Oct) also shows higher upset rates than dome in both years. This is counterintuitive — warm games shouldn't have more chaos than dome. Possible explanation: Sep/Oct has more competitive matchups (parity early in season) or this is just noise.

---

## Recommendations

### Signal Verdict: PROCEED (with caveats)
The 2-year average exceeds the 3pp threshold (+4.2pp dome vs cold gap). **Recommend proceeding with a full weather simulation** but with realistic expectations:

1. **Use `roof` field from nfl_data_py as the primary filter** — it's complete, free, and reliable. No need for Open-Meteo for basic dome/outdoor split.

2. **Add Open-Meteo for granular filters** — wind speed and temp thresholds (e.g., wind > 20mph, temp < 25°F) may capture the truly extreme weather games where upsets spike. This requires ~25 stadium coordinate lookups.

3. **Expand to 2020-2024** (5 years, ~1,350 games) before drawing firm conclusions. Two years (544 games) split ~60-120 games per category is too noisy for reliable inference.

4. **Specific hypothesis to test in full simulation:**
   - Games at outdoor cold stadiums in Dec/Jan with wind > 20mph → upset rate vs dome baseline
   - Games at outdoor stadiums with temp < 32°F → does freezing temp spike upset rate further?
   - Filter: avoid picking strong favorites in these conditions

5. **Year-to-year variance is a red flag** — if the signal doesn't hold across 5 years, it's not reliable enough to use as a strategy filter.

---

## Implementation Notes

If proceeding:
```python
# Easy dome classification using nfl_data_py
import nfl_data_py as nfl
sched = nfl.import_schedules([2020, 2021, 2022, 2023, 2024])
sched['is_dome'] = sched['roof'].isin(['dome', 'closed'])
sched['is_outdoor'] = sched['roof'] == 'outdoors'
# retractable ('open') = outdoor that day
```

Stadium coordinates for Open-Meteo (25 outdoor stadiums):
- Would be a small static lookup table in the codebase
- API call per game: `archive-api.open-meteo.com/v1/archive?lat=X&lon=Y&date=YYYY-MM-DD&hourly=temperature_2m,precipitation,wind_speed_10m`
- Target game-time window: hours 13-16 (1PM-4PM local time) for most games; adjust for primetime
