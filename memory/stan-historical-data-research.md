# Stan the Scout: Historical Data Research Report
**Date:** 2026-04-13  
**Mission:** Assess feasibility of adding 2021 and 2022 NFL season data to SurvivorPulse production DB for backtesting expansion (3 → 5 seasons).

---

## Executive Summary

**Verdict: Green light. Both seasons are fully acquirable.**

- **Game data (2021 and 2022):** Available via `nfl_data_py`. Complete — 272 and 271 games respectively, all 18 weeks, spread_line and scores 100% populated.
- **Pick popularity (2021 and 2022):** Available via `survivorgrid.com/picks/YYYY/WW`. Server-side rendered HTML, all 32 teams, all 18 weeks. Same format and sources as the 2023–2024 data already in production.

No new tools, no external purchases, no blockers.

---

## Source 1: nfl_data_py (Game Data)

### Confirmed Output

Tested directly against installed version `0.3.3` via `nfl.import_schedules([year])`.

| Season | Regular Season Games | Weeks Covered | spread_line Complete | Scores Complete |
|--------|---------------------|---------------|---------------------|-----------------|
| 2021   | 272                 | 1–18          | 272/272 (100%)       | 272/272 (100%)  |
| 2022   | 271                 | 1–18          | 271/271 (100%)       | 271/271 (100%)  |

**Note on 2022 game count:** 271 instead of 272 because the Bills vs. Bengals game (Week 17) was canceled due to Damar Hamlin's cardiac arrest and not rescheduled as a regular season game. This is accurate, not a data gap.

### Relevant Columns Available

```
game_id, season, week, game_type, away_team, home_team,
away_score, home_score, spread_line, away_spread_odds,
home_spread_odds, total_line, gameday, result
```

### Convention Note

`spread_line` in nfl_data_py: **positive = home team FAVORED** (same as 2023–2024 existing data).

### Data Quality

- Source: nflfastR (Vegas closing lines, sourced from Pinnacle and similar sharp books)
- Accuracy: High — same source used for 2023–2024 already in production
- License: MIT (free for commercial use)

### Sample Verification Script

```python
import nfl_data_py as nfl

for year in [2021, 2022]:
    df = nfl.import_schedules([year])
    reg = df[df['game_type'] == 'REG']
    print(f"{year}: {len(reg)} games, spread_line non-null: {reg['spread_line'].notna().sum()}")
```

---

## Source 2: SurvivorGrid.com (Pick Popularity Data)

### URL Pattern

```
https://www.survivorgrid.com/picks/{YEAR}/{WEEK}
```

Example: `https://www.survivorgrid.com/picks/2021/1`

### Confirmed Coverage

- **2021:** Weeks 1–18 confirmed — all return HTTP 200 with actual pick data
- **2022:** Weeks 1–18 confirmed — all return HTTP 200 with actual pick data
- Pages are **server-side rendered** (no headless browser required — standard HTTP GET works)

### Data Structure Per Page

Each page returns a table with per-team rows, 4 data columns:

| Team | Yahoo | OFP | RunYourPool | Avg |
|------|-------|-----|-------------|-----|
| SF   | 32.1% | 25.4% | 25.4% | 27.6% |
| LAR  | 20.4% | 24.4% | 20.7% | 21.8% |
| ...  | ...   | ...   | ...   | ...   |

**32 teams per week confirmed** (sum of Avg% ≈ 100%, e.g. 99.8% for 2021 Week 1 due to rounding).

### Sample Parsed Data

**2021 Week 1 (top picks):**
- SF: Yahoo=32.1%, OFP=25.4%, RunYourPool=25.4%, Avg=27.6%
- LAR: Yahoo=20.4%, OFP=24.4%, RunYourPool=20.7%, Avg=21.8%
- TB: Yahoo=9.3%, OFP=11.5%, RunYourPool=11.1%, Avg=10.6%

**2022 Week 1 (top picks):**
- BAL: Yahoo=11.5%, OFP=21.5%, RunYourPool=22.0%, Avg=18.3%
- IND: Yahoo=14.1%, OFP=18.5%, RunYourPool=16.9%, Avg=16.5%
- TEN: Yahoo=17.8%, OFP=11.3%, RunYourPool=11.1%, Avg=13.4%

**2021 Week 18 (top picks):**
- TEN: Yahoo=15.3%, OFP=27.8%, RunYourPool=11.4%, Avg=18.2%
- WAS: Yahoo=17.8%, OFP=23.5%, RunYourPool=6.3%, Avg=15.9%
- IND: Yahoo=20.7%, OFP=3.0%, RunYourPool=5.7%, Avg=9.8%

### Data Quality Assessment

- **Coverage:** All 32 teams, all 18 weeks — complete
- **Accuracy:** Actual pick distribution data from live survivor pools (Yahoo, OfficeFootballPool, RunYourPool) — not modeled or estimated
- **Same sources as 2023–2024** already in production (Yahoo, OFP, RunYourPool — weighted average used)
- **Licensing:** Public data, same approach used for 2023–2024; fair use for internal analytics. Scraping at reasonable rate (per-week, not bulk) is non-abusive.
- **Format:** Simple HTML table, trivially parseable with Python HTMLParser or BeautifulSoup

---

## Source 3: ESPN Eliminator Challenge (Historical)

- **Status:** Not usable. ESPN's historical pick availability pages for 2021–2022 are JavaScript-rendered and require authenticated sessions. Only summary/leaderboard stats are accessible (e.g., "391 of 387,836 entries survived").
- **Verdict:** Not needed — SurvivorGrid covers the same ground.

---

## Source 4: Yahoo Survivor Pool (Direct)

- No historical public archive of Yahoo's raw pick percentages for 2021–2022 was found.
- Yahoo picks **are captured** inside SurvivorGrid as one of the three component sources.
- **Verdict:** Not needed as standalone — SurvivorGrid provides the data.

---

## Source 5: 4for4.com

- 4for4 was confirmed in Google Drive for 2025 season (weekly CSV files with spread/schedule data for survivor optimization).
- For pick popularity specifically, 4for4 is a survivor strategy tool, not a pick distribution aggregator. It does not appear to publish historical per-team pick percentages for 2021–2022.
- **Verdict:** Not a source for pick popularity. Potentially useful for spread validation only.

---

## Source 6: nfl_data_py Pick Popularity

- `nfl_data_py` does not contain any pick popularity or survivor pool distribution data.
- It covers: play-by-play, schedules, rosters, team stats, contracts, injuries, combine, depth charts.
- **Verdict:** Not applicable.

---

## Source 7: Wayback Machine (SurvivorGrid Archives)

- Wayback Machine has 8 snapshots of survivorgrid.com from the 2021 season (Sept–Nov 2021).
- However, the live site already serves the 2021 and 2022 pick data via SSR — no archive scraping needed.
- **Verdict:** Not needed (live site works).

---

## Feasibility Verdict

| Season | Game Data | Pick Popularity | Overall |
|--------|-----------|-----------------|---------|
| 2021   | ✅ nfl_data_py — 272 games, 100% spreads | ✅ SurvivorGrid — 32 teams × 18 weeks | **FEASIBLE** |
| 2022   | ✅ nfl_data_py — 271 games (1 canceled), 100% spreads | ✅ SurvivorGrid — 32 teams × 18 weeks | **FEASIBLE** |

---

## Data Acquisition Plan

### Step 1: Verify Game Data (5 min)

```python
import nfl_data_py as nfl

for year in [2021, 2022]:
    df = nfl.import_schedules([year])
    reg = df[df['game_type'] == 'REG']
    print(f"\n{year} Regular Season:")
    print(f"  Games: {len(reg)}")
    print(f"  Spread non-null: {reg['spread_line'].notna().sum()}")
    print(f"  Score non-null: {reg['home_score'].notna().sum()}")
    print(f"  Weeks: {sorted(reg['week'].unique().tolist())}")
    print(f"  Sample: {reg[['week','away_team','home_team','spread_line','away_score','home_score']].head(3).to_string()}")
```

### Step 2: Write SurvivorGrid Scraper

The following script fetches and parses pick data for any season/week:

```python
import urllib.request
import re
import time
from html.parser import HTMLParser

class SGTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.cells = []
        self.current = ''
    
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
            self.current = ''
    
    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
            self.cells.append(self.current.strip())
    
    def handle_data(self, data):
        if self.in_td:
            self.current += data.strip()

def scrape_survivorgrid_picks(year, week):
    """Returns list of {team, yahoo_pct, ofp_pct, ryp_pct, avg_pct} for given year/week."""
    url = f"https://www.survivorgrid.com/picks/{year}/{week}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 SurvivorPulse/1.0'})
    response = urllib.request.urlopen(req, timeout=15)
    content = response.read().decode('utf-8', errors='ignore')
    
    parser = SGTableParser()
    parser.feed(content)
    cells = [c for c in parser.cells if c]
    
    picks = []
    i = 0
    while i < len(cells):
        cell = cells[i]
        if re.match(r'^[A-Z]{2,3}\([WLTa-z]+\)$', cell):
            team = re.match(r'^([A-Z]{2,3})', cell).group(1)
            if i + 4 < len(cells):
                try:
                    yahoo = float(cells[i+1].rstrip('%'))
                    ofp   = float(cells[i+2].rstrip('%'))
                    ryp   = float(cells[i+3].rstrip('%'))
                    avg   = float(cells[i+4].rstrip('%'))
                    picks.append({
                        'team': team, 'week': week, 'year': year,
                        'yahoo_pct': yahoo, 'ofp_pct': ofp, 'ryp_pct': ryp,
                        'pick_pct': avg  # avg = weighted consensus
                    })
                    i += 5
                    continue
                except (ValueError, IndexError):
                    pass
        i += 1
    return picks

def scrape_all_weeks(year, delay=0.5):
    """Scrape all 18 weeks for a season."""
    all_picks = []
    for week in range(1, 19):
        picks = scrape_survivorgrid_picks(year, week)
        print(f"  {year} Week {week}: {len(picks)} teams")
        all_picks.extend(picks)
        time.sleep(delay)  # Be polite
    return all_picks

# Usage:
# picks_2021 = scrape_all_weeks(2021)
# picks_2022 = scrape_all_weeks(2022)
```

### Step 3: Extend import-historical-seasons.py

The existing script used for 2023–2024 should be extended to:
1. Add `year` loop for 2021 and 2022
2. Assign pool IDs:
   - `a1b2c3d4-2021-4000-8000-000000000021`
   - `a1b2c3d4-2022-4000-8000-000000000022`
3. Integrate the `scrape_survivorgrid_picks()` function above
4. Compute win probabilities from spread: `P = 0.5 * (1 + erf(spread / (13.5 * sqrt(2))))`

**Note:** If the original `import-historical-seasons.py` no longer exists at `~/Projects/CMEA-Prototype/`, it may need to be reconstructed from scratch. The 2023–2024 data files in `~/Projects/CMEA-Prototype/data/` also appear to no longer be present. Check if the script/data live elsewhere or if it must be rebuilt.

### Step 4: Run Import

```bash
# Verify DB connectivity first
psql $NEON_DATABASE_URL -c "SELECT season, COUNT(*) FROM games GROUP BY season ORDER BY season;"

# Run extended import script
python3 import-historical-seasons.py --years 2021 2022

# Verify loaded data
psql $NEON_DATABASE_URL -c "
  SELECT season, COUNT(*) as games, 
         SUM(CASE WHEN spread IS NOT NULL THEN 1 ELSE 0 END) as with_spread
  FROM games 
  WHERE season IN (2021, 2022) 
  GROUP BY season;"
```

---

## Season Structure Note

- **2021:** First 17-game regular season → 18 weeks (each team has 1 bye)
  - ~272 regular season games ✅ (confirmed: exactly 272)
  - Weeks 1–18 all populated
- **2022:** Second 17-game season → 18 weeks
  - ~272 games, but 271 due to Bills vs. Bengals cancellation (Week 17, Damar Hamlin)
  - Weeks 1–18 all populated in SurvivorGrid
  - The missing game had minimal survivor pool impact (occurred late in the week)

---

## Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| SurvivorGrid changes URL structure or takes down historical pages | Low | Scrape and save all 2021–2022 pick data to JSON files immediately, before proceeding with DB import |
| SurvivorGrid blocks scraping (rate limit / IP ban) | Low | Use 0.5s delay between requests; 36 total pages (18 weeks × 2 seasons) — very low volume |
| nfl_data_py source data changes or package breaks | Very Low | Cache raw schedule data locally; package is stable at v0.3.3 |
| Import script lost (not found at expected path) | Confirmed | Script must be reconstructed; SurvivorGrid scraper above is functional; nfl_data_py calls are straightforward |
| 2022 missing game causes DB issues | Very Low | Simply omit that game from game table; it's an accurate representation |

---

## Alternative if SurvivorGrid Pick Data Becomes Unavailable

If the SurvivorGrid historical pages go down, alternatives in priority order:

1. **Synthetic pick data from spreads:** Model pick% as a function of win probability. Historical analysis of 2023–2024 shows pick concentration is heavily correlated with spread. Could use a fitted curve (e.g., exponential or sigmoid) as an approximation. This would reduce backtesting realism but is better than no data.

2. **PoolCrunch (via SurvivorGrid):** PoolCrunch references consensus pick numbers and has knockout data. Same underlying sources, likely same data — but no direct historical URL pattern found.

3. **Wayback Machine archive:** Survivorgrid.com had snapshots during 2021 season (Sept 9, Sept 17, Sept 24, Nov 10). Limited to those dates only, so would only recover a subset of weeks.

4. **Contact SurvivorGrid directly:** Site appears actively maintained. Possible to request historical data export or licensing arrangement.

---

## Recommended Next Action

Delegate to **Rita the Relay** or **Felix the Forge** with these exact instructions:

1. Run the SurvivorGrid scraper for 2021 and 2022 (all 18 weeks each) and save JSON files locally
2. Extend or reconstruct the import script to process 2021–2022 game data via nfl_data_py
3. Load into production Neon DB with pool IDs `a1b2c3d4-2021-...` and `a1b2c3d4-2022-...`
4. Verify row counts match expectations: ~272 games per season, ~576 pick records per season

**Inputs needed:** Neon DB connection string, existing import script (or instruction to reconstruct), column schema from current `games` and `pick_popularity` tables.

**Estimated effort:** 2–4 hours dev time to implement and verify.
