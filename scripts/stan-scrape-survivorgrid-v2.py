#!/usr/bin/env python3
"""
Stan the Scout: Scrape SurvivorGrid pick popularity data for 2023 and 2024 seasons.
V2: Fixed HTML parser for Laravel/PHP rendered tables.
"""

import urllib.request
import json
import re
import sys
import os
import time

OUTPUT_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
SEASONS = [2023, 2024]
TOTAL_WEEKS = 18


def fetch_page(url, retries=2):
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            print(f"  FAILED: {url} - {e}", file=sys.stderr)
            return None


def parse_picks_page(html):
    """Parse SurvivorGrid picks page HTML table."""
    teams = []
    
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if not cells or not any('%' in c for c in cells):
            continue
        
        # Clean HTML tags from cells
        clean_cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        
        if len(clean_cells) < 5:
            continue
        
        # First cell: "CIN\n...&nbsp;(L)" or "CIN (W)"
        first = clean_cells[0].replace('&nbsp;', ' ').replace('\n', ' ').strip()
        
        # Extract team ID and outcome
        team_match = re.match(r'^([A-Z]{2,3})\s*\(([WLT])\)', first)
        if not team_match:
            # Try without outcome
            team_match = re.match(r'^([A-Z]{2,3})', first)
            if not team_match:
                continue
            team_id = team_match.group(1)
            outcome = None
        else:
            team_id = team_match.group(1)
            outcome_letter = team_match.group(2)
            outcome = 'Win' if outcome_letter == 'W' else ('Loss' if outcome_letter == 'L' else 'Tie')
        
        # Normalize team ID
        if team_id == 'WSH':
            team_id = 'WAS'
        
        # Parse percentages (Yahoo, ESPN, OFP, Average)
        def parse_pct(s):
            s = s.replace('%', '').strip()
            try:
                return float(s)
            except ValueError:
                return 0.0
        
        yahoo = parse_pct(clean_cells[1])
        espn = parse_pct(clean_cells[2])
        ofp = parse_pct(clean_cells[3])
        average = parse_pct(clean_cells[4])
        
        teams.append({
            'teamId': team_id,
            'yahoo': yahoo,
            'espn': espn,
            'ofp': ofp,
            'average': average,
            'outcome': outcome,
        })
    
    return teams


def scrape_season(season):
    season_data = {'season': season, 'weeks': {}}
    
    for week in range(1, TOTAL_WEEKS + 1):
        url = f"https://www.survivorgrid.com/picks/{season}/{week}"
        sys.stdout.write(f"\r  Fetching {season} Week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()
        
        html = fetch_page(url)
        if not html:
            print(f"\n  WARNING: Could not fetch {season} Week {week}")
            continue
        
        teams = parse_picks_page(html)
        
        if teams:
            season_data['weeks'][str(week)] = {
                'week': week,
                'teams': teams,
                'teamCount': len(teams),
            }
        else:
            print(f"\n  WARNING: No team data parsed for {season} Week {week}")
        
        time.sleep(0.5)
    
    print(f"\r  {season}: Scraped {len(season_data['weeks'])} weeks with data.          ")
    return season_data


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Stan the Scout: Scraping SurvivorGrid pick popularity data (v2)...")
    print()
    
    for season in SEASONS:
        print(f"  Scraping {season} season...")
        season_data = scrape_season(season)
        
        output_file = os.path.join(OUTPUT_DIR, f"survivorgrid_picks_{season}.json")
        with open(output_file, 'w') as f:
            json.dump(season_data, f, indent=2)
        
        total_teams = 0
        weeks_with_data = 0
        for week_key, week_data in season_data['weeks'].items():
            if week_data['teamCount'] > 0:
                weeks_with_data += 1
                total_teams += week_data['teamCount']
        
        print(f"  Saved to: {output_file}")
        print(f"  Weeks with data: {weeks_with_data}/{TOTAL_WEEKS}")
        print(f"  Total team records: {total_teams}")
        
        # Show Week 1 sample
        w1 = season_data['weeks'].get('1', {}).get('teams', [])
        if w1:
            print(f"  Week 1 sample (top 5 by avg):")
            for t in sorted(w1, key=lambda x: x['average'], reverse=True)[:5]:
                print(f"    {t['teamId']:4s} avg={t['average']:5.1f}% yahoo={t['yahoo']:.1f}% outcome={t['outcome']}")
        print()
    
    print("Done!")


if __name__ == "__main__":
    main()
