#!/usr/bin/env python3
"""
Stan the Scout: Multi-Season Strategy Simulation (2023, 2024, 2025)

Tests all 7 strategies across 3 NFL seasons using:
- 2023/2024: Local JSON files (game data from nfl_data_py, pick popularity from SurvivorGrid)
- 2025: Live SurvivorPulse API (game data + dynamics)
"""

import urllib.request
import json
import math
import sys
import os

DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
BASE_URL = "https://survivorpulse.com"
POOL_ID = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
NUM_ENTRIES = 5


# ─── Data Loading ───────────────────────────────────────────────────────────

def load_local_season(season):
    """Load game data and pick popularity from local JSON files for 2023/2024."""
    games_file = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
    picks_file = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")

    with open(games_file) as f:
        games = json.load(f)
    with open(picks_file) as f:
        picks_data = json.load(f)

    all_week_data = {}
    for week in range(1, TOTAL_WEEKS + 1):
        week_games = [g for g in games if g['week'] == week]
        week_picks = picks_data.get('weeks', {}).get(str(week), {}).get('teams', [])

        # Build pick share lookup from SurvivorGrid average
        pick_shares = {}
        outcomes_from_picks = {}
        for p in week_picks:
            tid = p['teamId']
            pick_shares[tid] = p.get('average', 0)
            if p.get('outcome'):
                outcomes_from_picks[tid] = p['outcome']

        teams = []
        for g in week_games:
            home = g['homeTeamId']
            away = g['awayTeamId']
            hwp = float(g['homeWinProbability'])
            awp = float(g['awayWinProbability'])

            # Determine outcomes from game scores
            completed = g.get('completed', False)
            home_outcome = None
            away_outcome = None
            if completed and g['homeScore'] is not None and g['awayScore'] is not None:
                home_outcome = 'Win' if g['homeScore'] > g['awayScore'] else 'Loss'
                away_outcome = 'Win' if g['awayScore'] > g['homeScore'] else 'Loss'

            # Cross-check with SurvivorGrid outcomes if available
            if not home_outcome and home in outcomes_from_picks:
                home_outcome = outcomes_from_picks[home]
            if not away_outcome and away in outcomes_from_picks:
                away_outcome = outcomes_from_picks[away]

            teams.append({
                'teamId': home,
                'winProbability': hwp,
                'pickShare': pick_shares.get(home, 0),
                'outcome': home_outcome,
            })
            teams.append({
                'teamId': away,
                'winProbability': awp,
                'pickShare': pick_shares.get(away, 0),
                'outcome': away_outcome,
            })

        if teams:
            all_week_data[week] = teams

    return all_week_data


def fetch_json(url, timeout=20):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return None


def load_2025_season():
    """Load 2025 data from SurvivorPulse API."""
    all_week_data = {}
    for week in range(1, TOTAL_WEEKS + 1):
        sys.stdout.write(f"\r  Fetching 2025 Week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()

        games = fetch_json(f"{BASE_URL}/api/games?season=2025&scheduleType=regular&week={week}")
        dynamics = fetch_json(
            f"{BASE_URL}/api/pools/{POOL_ID}/dynamics/comprehensive?week={week}&season=2025&scheduleType=regular"
        )

        if not games or not dynamics:
            continue

        pick_shares = {}
        for t in dynamics.get('teamDynamics', []):
            pick_shares[t['teamId']] = t.get('pickShare', 0)

        teams = []
        for g in games:
            hwp = float(g['homeWinProbability']) if g.get('homeWinProbability') else 0
            awp = float(g['awayWinProbability']) if g.get('awayWinProbability') else 0
            completed = g.get('completed', False)
            hs = g.get('homeScore')
            as_ = g.get('awayScore')

            home_outcome = None
            away_outcome = None
            if completed and hs is not None and as_ is not None:
                home_outcome = 'Win' if hs > as_ else 'Loss'
                away_outcome = 'Win' if as_ > hs else 'Loss'

            home = g['homeTeamId']
            away = g['awayTeamId']

            teams.append({
                'teamId': home,
                'winProbability': hwp,
                'pickShare': pick_shares.get(home, 0),
                'outcome': home_outcome,
            })
            teams.append({
                'teamId': away,
                'winProbability': awp,
                'pickShare': pick_shares.get(away, 0),
                'outcome': away_outcome,
            })

        if teams:
            all_week_data[week] = teams

    print(f"\r  2025: Loaded {len(all_week_data)} weeks from API.          ")
    return all_week_data


# ─── Scoring Functions ──────────────────────────────────────────────────────

def score_pure_win_prob(team, _all, _future, _avail):
    return team['winProbability']

def score_leverage_floor_60(team, _all, _future, _avail):
    if team['winProbability'] < 0.60:
        return -1
    ps = max(team['pickShare'], 0.1)
    return team['winProbability'] / (ps / 100)

def score_leverage_floor_55(team, _all, _future, _avail):
    if team['winProbability'] < 0.55:
        return -1
    ps = max(team['pickShare'], 0.1)
    return team['winProbability'] / (ps / 100)

def score_weighted_70_30(team, _all, _future, _avail):
    return 0.7 * team['winProbability'] + 0.3 * (1 - team['pickShare'] / 100)

def score_weighted_80_20(team, _all, _future, _avail):
    return 0.8 * team['winProbability'] + 0.2 * (1 - team['pickShare'] / 100)

def score_tiered_top10(team, _all, _future, available):
    sorted_avail = sorted(available, key=lambda t: t['winProbability'], reverse=True)
    top10_ids = set(t['teamId'] for t in sorted_avail[:10])
    if team['teamId'] not in top10_ids:
        return -1
    return team['winProbability'] * 0.01 + (1 - team['pickShare'] / 100)

def score_antichalk_top5(team, _all, _future, available):
    sorted_avail = sorted(available, key=lambda t: t['winProbability'], reverse=True)
    top5_ids = set(t['teamId'] for t in sorted_avail[:5])
    if team['teamId'] not in top5_ids:
        return -1
    return team['winProbability'] * 0.001 + (1 - team['pickShare'] / 100)


STRATEGIES = [
    ("1. Pure Win Probability", score_pure_win_prob),
    ("2a. Leverage + 60% Floor", score_leverage_floor_60),
    ("2b. Weighted Blend (70/30)", score_weighted_70_30),
    ("2c. Tiered Top-10", score_tiered_top10),
    ("2d. Leverage + 55% Floor", score_leverage_floor_55),
    ("2e. Weighted Blend (80/20)", score_weighted_80_20),
    ("2f. Anti-Chalk Top-5", score_antichalk_top5),
]


# ─── Simulation ─────────────────────────────────────────────────────────────

def simulate(strategy_name, score_fn, week_data):
    alive = set(range(NUM_ENTRIES))
    used_teams = [set() for _ in range(NUM_ENTRIES)]
    entry_weeks_survived = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned = set()
        picks = {}

        for i in sorted(alive):
            available = [t for t in teams
                        if t['teamId'] not in assigned
                        and t['teamId'] not in used_teams[i]]

            for t in available:
                t['_score'] = score_fn(t, teams, {}, available)

            viable = sorted([t for t in available if t.get('_score', -1) >= 0],
                          key=lambda t: t['_score'], reverse=True)

            if not viable:
                viable = sorted(available, key=lambda t: t['winProbability'], reverse=True)

            if viable:
                best = viable[0]
                assigned.add(best['teamId'])
                used_teams[i].add(best['teamId'])
                picks[i] = best

        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks_survived += 1

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    # Calculate avg win prob and ownership of all picks made
    all_wps = []
    all_owns = []
    # Re-run to collect pick stats (simpler than tracking in main loop)
    alive2 = set(range(NUM_ENTRIES))
    used2 = [set() for _ in range(NUM_ENTRIES)]
    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive2:
            continue
        assigned = set()
        for i in sorted(alive2):
            available = [t for t in teams
                        if t['teamId'] not in assigned
                        and t['teamId'] not in used2[i]]
            for t in available:
                t['_score'] = score_fn(t, teams, {}, available)
            viable = sorted([t for t in available if t.get('_score', -1) >= 0],
                          key=lambda t: t['_score'], reverse=True)
            if not viable:
                viable = sorted(available, key=lambda t: t['winProbability'], reverse=True)
            if viable:
                best = viable[0]
                assigned.add(best['teamId'])
                used2[i].add(best['teamId'])
                all_wps.append(best['winProbability'])
                all_owns.append(best['pickShare'])
                if best['outcome'] == 'Loss':
                    alive2.discard(i)

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0
    avg_own = sum(all_owns) / len(all_owns) if all_owns else 0

    return {
        'entry_weeks': entry_weeks_survived,
        'final_elim': final_elim_week,
        'avg_wp': avg_wp,
        'avg_own': avg_own,
    }


def main():
    print("=" * 90)
    print("STAN THE SCOUT: MULTI-SEASON STRATEGY SIMULATION")
    print("Seasons: 2023, 2024, 2025 | 5 Entries | 7 Strategies")
    print("=" * 90)
    print()

    # Load data
    print("Loading data...")
    season_data = {}

    print("  Loading 2023 (local files)...")
    season_data[2023] = load_local_season(2023)
    print(f"  2023: {len(season_data[2023])} weeks loaded")

    print("  Loading 2024 (local files)...")
    season_data[2024] = load_local_season(2024)
    print(f"  2024: {len(season_data[2024])} weeks loaded")

    print("  Loading 2025 (API)...")
    season_data[2025] = load_2025_season()
    print()

    # Run simulations
    results = {}  # strategy -> {season -> result}

    for strat_name, strat_fn in STRATEGIES:
        results[strat_name] = {}
        for season in [2023, 2024, 2025]:
            r = simulate(strat_name, strat_fn, season_data[season])
            results[strat_name][season] = r

    # Print per-season results
    for season in [2023, 2024, 2025]:
        print(f"\n{'=' * 90}")
        print(f"SEASON: {season}")
        print(f"{'=' * 90}")
        print(f"{'Strategy':<35} {'Last Elim':<12} {'Entry-Wks':<12} {'Avg WP':<10} {'Avg Own'}")
        print(f"{'─' * 35} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 10}")

        rows = []
        for strat_name, _ in STRATEGIES:
            r = results[strat_name][season]
            rows.append((strat_name, r))

        # Sort by entry_weeks descending
        rows.sort(key=lambda x: x[1]['entry_weeks'], reverse=True)

        for strat_name, r in rows:
            elim = f"Wk {r['final_elim']}" if isinstance(r['final_elim'], int) else r['final_elim']
            print(f"{strat_name:<35} {elim:<12} {r['entry_weeks']:<12} {r['avg_wp']:.1%}{'':>4} {r['avg_own']:.1f}%")

    # Print cross-season summary
    print(f"\n{'=' * 90}")
    print("CROSS-SEASON SUMMARY (Total Entry-Weeks Survived Across All 3 Seasons)")
    print(f"{'=' * 90}")
    print(f"{'Strategy':<35} {'2023':<10} {'2024':<10} {'2025':<10} {'TOTAL':<10} {'Avg/Season':<12} {'Consistency'}")
    print(f"{'─' * 35} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 12} {'─' * 12}")

    summary_rows = []
    for strat_name, _ in STRATEGIES:
        s23 = results[strat_name][2023]['entry_weeks']
        s24 = results[strat_name][2024]['entry_weeks']
        s25 = results[strat_name][2025]['entry_weeks']
        total = s23 + s24 + s25
        avg = total / 3
        # Consistency: standard deviation of the 3 season values
        mean = avg
        variance = ((s23 - mean)**2 + (s24 - mean)**2 + (s25 - mean)**2) / 3
        std = variance ** 0.5
        summary_rows.append((strat_name, s23, s24, s25, total, avg, std))

    summary_rows.sort(key=lambda x: x[4], reverse=True)

    for name, s23, s24, s25, total, avg, std in summary_rows:
        consistency = f"SD={std:.1f}"
        print(f"{name:<35} {s23:<10} {s24:<10} {s25:<10} {total:<10} {avg:<12.1f} {consistency}")

    # Print the winner
    best = summary_rows[0]
    print(f"\n** BEST OVERALL: {best[0]} — {best[4]} total entry-weeks ({best[5]:.1f}/season)")


if __name__ == "__main__":
    main()
