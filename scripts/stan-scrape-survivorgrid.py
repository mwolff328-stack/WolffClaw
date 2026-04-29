#!/usr/bin/env python3
"""
Stan the Scout: Scrape SurvivorGrid pick popularity data for 2023 and 2024 seasons.

Fetches per-team pick percentages (Yahoo, ESPN, OFP averages) and outcomes
for every week of the 2023 and 2024 NFL regular seasons.

Output: JSON files per season in ~/Projects/CMEA-Prototype/data/
"""

import urllib.request
import json
import re
import sys
import os
import time

OUTPUT_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
SEASONS = [2023, 2024]
TOTAL_WEEKS = 18  # Regular season weeks (18 since 2021)


def fetch_page(url, retries=2):
    """Fetch a web page with retries."""
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


def parse_survivorgrid_picks(html, season, week):
    """
    Parse the SurvivorGrid picks page HTML to extract team pick percentages.
    
    The page structure has rows with: Team (W/L), Yahoo%, ESPN%, OFP%, Avg%
    """
    teams = []
    
    # The data is in a structured format. Let's parse it by looking for team patterns.
    # Team lines look like: "CIN\n  (L)\n\n 42.1%\n\n 29.0%\n\n 33.3%\n\n 37.7%"
    # But since we're getting rendered text, let's use regex on the raw HTML.
    
    # Try to find team data blocks in the HTML
    # Look for 3-letter team codes followed by outcome and percentages
    
    # First, let's try to extract from the text content
    lines = html.split('\n')
    
    # NFL team abbreviations
    nfl_teams = {
        'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
        'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
        'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
        'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS', 'WSH'
    }
    
    # Strategy: find all percentage values near team abbreviations
    # Use regex to find patterns like: >CIN<... (L)... 42.1%... 29.0%... 33.3%... 37.7%
    
    # Look for team rows in table-like HTML structure
    # Pattern: team abbreviation, then outcome (W/L/T), then 4 percentages
    
    # Try extracting from HTML using regex for the structured data
    # SurvivorGrid uses React/Next.js, data might be in script tags
    
    # Look for JSON data in script tags
    json_match = re.search(r'__NEXT_DATA__.*?<\/script>', html, re.DOTALL)
    if json_match:
        try:
            json_str = re.search(r'>({.*?})<', json_match.group(0), re.DOTALL)
            if json_str:
                data = json.loads(json_str.group(1))
                # Navigate the Next.js data structure
                props = data.get('props', {}).get('pageProps', {})
                picks = props.get('picks', props.get('data', []))
                if picks:
                    for pick in picks:
                        team_id = pick.get('team', pick.get('teamId', ''))
                        if team_id == 'WSH':
                            team_id = 'WAS'
                        teams.append({
                            'teamId': team_id,
                            'yahoo': pick.get('yahoo', 0),
                            'espn': pick.get('espn', 0),
                            'ofp': pick.get('ofp', pick.get('officefootballpool', 0)),
                            'average': pick.get('average', pick.get('avg', 0)),
                            'outcome': pick.get('outcome', pick.get('result', None)),
                        })
                    return teams
        except (json.JSONDecodeError, KeyError):
            pass
    
    # Fallback: parse from the rendered text content
    # Extract all percentage values and team codes from the page
    
    # Find all occurrences of team codes in the HTML
    team_pattern = re.compile(
        r'>(' + '|'.join(nfl_teams) + r')<.*?(?:\(([WLT])\))?.*?'
        r'([\d.]+)%.*?([\d.]+)%.*?([\d.]+)%.*?([\d.]+)%',
        re.DOTALL
    )
    
    for match in team_pattern.finditer(html):
        team_id = match.group(1)
        if team_id == 'WSH':
            team_id = 'WAS'
        outcome_letter = match.group(2)
        outcome = None
        if outcome_letter == 'W':
            outcome = 'Win'
        elif outcome_letter == 'L':
            outcome = 'Loss'
        elif outcome_letter == 'T':
            outcome = 'Tie'
            
        teams.append({
            'teamId': team_id,
            'yahoo': float(match.group(3)),
            'espn': float(match.group(4)),
            'ofp': float(match.group(5)),
            'average': float(match.group(6)),
            'outcome': outcome,
        })
    
    # Deduplicate (regex might match same team multiple times)
    seen = set()
    unique_teams = []
    for t in teams:
        if t['teamId'] not in seen:
            seen.add(t['teamId'])
            unique_teams.append(t)
    
    return unique_teams


def scrape_season(season):
    """Scrape all weeks for a season."""
    season_data = {
        'season': season,
        'weeks': {}
    }
    
    for week in range(1, TOTAL_WEEKS + 1):
        url = f"https://www.survivorgrid.com/picks/{season}/{week}"
        sys.stdout.write(f"\r  Fetching {season} Week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()
        
        html = fetch_page(url)
        if not html:
            print(f"\n  WARNING: Could not fetch {season} Week {week}")
            continue
        
        teams = parse_survivorgrid_picks(html, season, week)
        
        if teams:
            season_data['weeks'][str(week)] = {
                'week': week,
                'teams': teams,
                'teamCount': len(teams),
            }
        else:
            print(f"\n  WARNING: No team data parsed for {season} Week {week}")
        
        # Be respectful with rate limiting
        time.sleep(0.5)
    
    print(f"\r  {season}: Scraped {len(season_data['weeks'])} weeks with data.          ")
    return season_data


def scrape_game_results_from_survivorgrid(season):
    """
    Extract game outcomes from SurvivorGrid data.
    Each team has W/L/T outcome per week, which gives us game results.
    """
    # This is already captured in the pick popularity data (outcome field)
    pass


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Stan the Scout: Scraping SurvivorGrid pick popularity data...")
    print()
    
    for season in SEASONS:
        print(f"  Scraping {season} season...")
        season_data = scrape_season(season)
        
        output_file = os.path.join(OUTPUT_DIR, f"survivorgrid_picks_{season}.json")
        with open(output_file, 'w') as f:
            json.dump(season_data, f, indent=2)
        
        # Print summary
        total_teams = 0
        weeks_with_data = 0
        for week_key, week_data in season_data['weeks'].items():
            if week_data['teamCount'] > 0:
                weeks_with_data += 1
                total_teams += week_data['teamCount']
        
        print(f"  Saved to: {output_file}")
        print(f"  Weeks with data: {weeks_with_data}/{TOTAL_WEEKS}")
        print(f"  Total team records: {total_teams}")
        print()
    
    print("Done! Pick popularity data saved.")
    print()
    print("Next steps:")
    print("  1. Get game results + spreads (Pro Football Reference or Spreadspoke)")
    print("  2. Derive win probabilities from spreads")
    print("  3. Load into SurvivorPulse database")


if __name__ == "__main__":
    main()
