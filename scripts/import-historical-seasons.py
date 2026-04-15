#!/usr/bin/env python3
"""
Import 2023 and 2024 NFL season data into SurvivorPulse production database.

Creates:
1. Demo pools for 2023 and 2024 (same config as 2025 demo pool)
2. 5 entries per pool
3. Games with scores, spreads, and win probabilities
4. Pick popularity data from SurvivorGrid

Data sources:
- Game data: ~/Projects/CMEA-Prototype/data/nfl_games_{year}.json
- Pick popularity: ~/Projects/CMEA-Prototype/data/survivorgrid_picks_{year}.json

Usage:
    python3 import-historical-seasons.py [--db-url DATABASE_URL] [--dry-run] [--seasons 2021,2022,2023,2024]

    --db-url   Database connection URL (default: production Neon DB)
    --seasons  Comma-separated list of seasons to import (default: 2023,2024)

Examples:
    # Import 2023+2024 into production (default)
    python3 import-historical-seasons.py

    # Import 2021+2022 into Replit dev DB
    python3 import-historical-seasons.py --db-url 'postgresql://postgres:password@helium/heliumdb?sslmode=disable' --seasons 2021,2022

    # Import all 4 seasons into dev DB
    python3 import-historical-seasons.py --db-url 'postgresql://postgres:password@helium/heliumdb?sslmode=disable' --seasons 2021,2022,2023,2024
"""

import psycopg2
import json
import os
import sys
import uuid
import math
from datetime import datetime, timezone

# Default to production DB, override with --db-url
DEFAULT_DB_URL = "postgresql://neondb_owner:npg_uR02UhPfxgXT@ep-orange-bush-afg0m2nx.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require"
DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
if not os.path.isdir(DATA_DIR):
    # Try alternate paths (Replit, BackTesting-Prototype)
    for alt in ['~/Projects/SurvivorPulse-BackTesting-Prototype/data', './data', '../data']:
        alt_path = os.path.expanduser(alt)
        if os.path.isdir(alt_path):
            DATA_DIR = alt_path
            break

def parse_args():
    db_url = DEFAULT_DB_URL
    seasons = [2023, 2024]
    dry_run = '--dry-run' in sys.argv
    for i, arg in enumerate(sys.argv):
        if arg == '--db-url' and i + 1 < len(sys.argv):
            db_url = sys.argv[i + 1]
        if arg == '--seasons' and i + 1 < len(sys.argv):
            seasons = [int(s.strip()) for s in sys.argv[i + 1].split(',')]
    return db_url, seasons, dry_run

# The existing 2025 demo pool to replicate config from
TEMPLATE_POOL_ID = "04e2471b-6498-4a59-8a95-c0dc50221457"
TEMPLATE_USER_ID = "47230349"

# Pre-generated stable IDs for reproducibility (won't create duplicates on re-run)
def get_pool_id(season):
    return f"a1b2c3d4-{season}-4000-8000-0000000000{season % 100:02d}"

def get_entry_ids(season):
    return [f"e1e1e1e1-{season}-4001-8000-00000000000{i}" for i in range(1, 6)]


def log(msg):
    print(f"  {msg}")


def create_pool(cur, season):
    """Create a demo pool for the given season, matching 2025 pool config."""
    pool_id = get_pool_id(season)
    
    cur.execute("SELECT id FROM pools WHERE id = %s", (pool_id,))
    if cur.fetchone():
        log(f"Pool {pool_id} already exists for {season}, skipping")
        return pool_id
    
    cur.execute("""
        INSERT INTO pools (
            id, name, description, created_by, contest_type, total_entries,
            max_entries, max_entries_per_user, pool_type, starting_week, sport,
            pool_provider, entry_fee, pick_objective, picks_per_entry,
            team_use_limit, team_use_limit_scope, allow_buybacks, season,
            is_active, pool_size, pick_requirements, is_test_data
        ) VALUES (
            %s, %s, %s, %s, 'survivor', 5,
            1, 5, 'regular', 1, 'nfl',
            'splash_sports', 25.00, 'pick_winners', 1,
            '1', 'SEASON', false, %s,
            true, 0, '{"mode":"single","default":1,"overrides":{"regular":{},"playoffs":{}}}'::jsonb, false
        )
    """, (
        pool_id,
        f"CMEA Prototype Demo Pool ({season})",
        f"Auto-generated demo pool for the CMEA prototype. Historical {season} season data.",
        TEMPLATE_USER_ID,
        season,
    ))
    log(f"Created pool {pool_id} for {season}")
    return pool_id


def create_entries(cur, season, pool_id):
    """Create 5 entries for the pool."""
    for i, entry_id in enumerate(get_entry_ids(season)):
        cur.execute("SELECT id FROM entries WHERE id = %s", (entry_id,))
        if cur.fetchone():
            continue
        
        cur.execute("""
            INSERT INTO entries (id, pool_id, user_id, name, is_alive, strikes, used_teams)
            VALUES (%s, %s, %s, %s, true, 0, '[]'::jsonb)
        """, (entry_id, pool_id, TEMPLATE_USER_ID, f"Entry {i + 1}"))
    
    log(f"Created 5 entries for {season} pool")


def load_games(cur, season):
    """Load game data from local JSON files."""
    games_file = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
    with open(games_file) as f:
        games = json.load(f)
    
    # Filter to regular season only (weeks 1-18)
    regular = [g for g in games if 1 <= g["week"] <= 18]
    
    inserted = 0
    skipped = 0
    
    for g in regular:
        home = g["homeTeamId"]
        away = g["awayTeamId"]
        week = g["week"]
        
        # Game ID format matching existing: {season}-{week:02d}-{away}-{home}
        game_id = f"{season}-{week:02d}-{away}-{home}"
        
        # Check if exists
        cur.execute("SELECT id FROM games WHERE id = %s", (game_id,))
        if cur.fetchone():
            skipped += 1
            continue
        
        # Parse values
        home_spread = float(g["homeSpread"]) if g.get("homeSpread") else None
        home_wp = float(g["homeWinProbability"]) if g.get("homeWinProbability") else None
        away_wp = float(g["awayWinProbability"]) if g.get("awayWinProbability") else None
        
        # Generate a plausible game_time (Sunday 1pm ET for most games)
        from datetime import timedelta
        sept_1 = datetime(season, 9, 1)
        # Find first Thursday of September
        days_to_thu = (3 - sept_1.weekday()) % 7
        first_thu = sept_1 + timedelta(days=days_to_thu)
        # Week N Sunday = first_thu + (week-1)*7 + 3 days
        game_date = first_thu + timedelta(days=(week - 1) * 7 + 3)
        game_time = game_date.replace(hour=13, minute=0, second=0, tzinfo=timezone.utc)
        
        cur.execute("""
            INSERT INTO games (
                id, week, season, home_team_id, away_team_id, game_time,
                home_spread, home_win_probability, away_win_probability,
                completed, home_score, away_score,
                period_type, period_index, schedule_type
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                'WEEK', %s, 'regular_season'
            )
        """, (
            game_id, week, season, home, away, game_time,
            home_spread, home_wp, away_wp,
            g.get("completed", True), g.get("homeScore"), g.get("awayScore"),
            week,
        ))
        inserted += 1
    
    log(f"Games {season}: {inserted} inserted, {skipped} skipped (already exist)")


def load_pick_popularity(cur, season):
    """Load pick popularity data from SurvivorGrid JSON files."""
    picks_file = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")
    with open(picks_file) as f:
        picks_data = json.load(f)
    
    inserted = 0
    skipped = 0
    
    weeks = picks_data.get("weeks", {})
    for week_str, week_data in weeks.items():
        week = int(week_str)
        teams = week_data.get("teams", [])
        
        for team in teams:
            team_id = team["teamId"]
            avg_pct = team.get("average", 0)
            
            if avg_pct <= 0:
                continue
            
            # Find the game_id for this team in this week
            # Game ID format: {season}-{week:02d}-{away}-{home}
            # We need to find which game this team played in
            cur.execute("""
                SELECT id FROM games 
                WHERE season = %s AND week = %s 
                AND (home_team_id = %s OR away_team_id = %s)
                LIMIT 1
            """, (season, week, team_id, team_id))
            game_row = cur.fetchone()
            
            if not game_row:
                # Game might not be loaded yet (bye week or missing data)
                continue
            
            game_id = game_row[0]
            
            # Use a deterministic ID to allow re-runs
            pp_id = f"sg-{season}-{week:02d}-{team_id}"
            
            cur.execute("SELECT id FROM pick_popularity WHERE id = %s", (pp_id,))
            if cur.fetchone():
                skipped += 1
                continue
            
            cur.execute("""
                INSERT INTO pick_popularity (
                    id, game_id, team_id, week, season,
                    popularity_percentage, source,
                    period_type, period_index, schedule_type
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, 'survivorgrid',
                    'WEEK', %s, 'regular_season'
                )
            """, (
                pp_id, game_id, team_id, week, season,
                avg_pct, week,
            ))
            inserted += 1
    
    log(f"Pick popularity {season}: {inserted} inserted, {skipped} skipped")


def verify(cur, season):
    """Verify the data was loaded correctly."""
    pool_id = get_pool_id(season)
    
    cur.execute("SELECT name FROM pools WHERE id = %s", (pool_id,))
    pool = cur.fetchone()
    
    cur.execute("SELECT COUNT(*) FROM entries WHERE pool_id = %s", (pool_id,))
    entry_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM games WHERE season = %s AND schedule_type = 'regular_season'", (season,))
    game_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM pick_popularity WHERE season = %s AND source = 'survivorgrid'", (season,))
    pp_count = cur.fetchone()[0]
    
    cur.execute("""
        SELECT team_id, popularity_percentage 
        FROM pick_popularity 
        WHERE season = %s AND week = 1 AND source = 'survivorgrid'
        ORDER BY popularity_percentage DESC LIMIT 3
    """, (season,))
    top_picks = cur.fetchall()
    
    print(f"\n  Verification for {season}:")
    print(f"    Pool: {pool[0] if pool else 'MISSING'}")
    print(f"    Entries: {entry_count}")
    print(f"    Games: {game_count}")
    print(f"    Pick popularity records: {pp_count}")
    print(f"    Week 1 top picks: {[(t[0], float(t[1])) for t in top_picks]}")


def main():
    db_url, seasons, dry_run = parse_args()
    
    if dry_run:
        print("=" * 60)
        print("DRY RUN — no changes will be committed")
        print("=" * 60)
    
    print(f"Connecting to database...")
    print(f"  URL: {db_url[:50]}...")
    print(f"  Seasons: {seasons}")
    print(f"  Data dir: {DATA_DIR}")
    conn = psycopg2.connect(db_url)
    
    if dry_run:
        conn.autocommit = False
    
    cur = conn.cursor()
    
    for season in seasons:
        print(f"\n{'=' * 60}")
        print(f"Importing {season} season data")
        print(f"{'=' * 60}")
        
        create_pool(cur, season)
        create_entries(cur, season, get_pool_id(season))
        load_games(cur, season)
        load_pick_popularity(cur, season)
        verify(cur, season)
    
    if dry_run:
        print("\n\nDRY RUN — rolling back all changes")
        conn.rollback()
    else:
        print("\n\nCommitting changes...")
        conn.commit()
        print("Done!")
    
    # Print pool IDs for reference
    print(f"\nPool IDs for prototype:")
    for s in seasons:
        print(f"  {s}: {get_pool_id(s)}")
    print(f"  2025: {TEMPLATE_POOL_ID}")
    
    conn.close()


if __name__ == "__main__":
    main()
