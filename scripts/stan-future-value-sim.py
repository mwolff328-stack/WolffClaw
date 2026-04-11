#!/usr/bin/env python3
"""
Stan the Scout: Future Value Lookahead Strategy Simulation

Tests multiple lookahead strategies with time-decay weighting against 3 NFL seasons.
Core idea: penalize using a team now if it has high value in upcoming weeks,
with nearer-term future value weighted more heavily than distant future value.

Strategies tested:
1. Pure Win Probability (baseline)
2. 70/30 Weighted Blend (current best)
3. Lookahead-3: 70/30 blend with 3-week lookahead, linear decay
4. Lookahead-5: 70/30 blend with 5-week lookahead, linear decay
5. Lookahead-5 Exponential: 70/30 blend with 5-week lookahead, exponential decay
6. Lookahead-3 Aggressive: stronger future value penalty
7. Lookahead-5 with floor: only penalize teams above 65% future win prob
8. Lookahead-5 + contrarian bonus: future value considers both win prob AND low ownership
"""

import urllib.request
import json
import math
import sys
import os

DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
NUM_ENTRIES = 5


def fetch_json(url, timeout=20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except:
        return None


def load_local_season(season):
    """Load combined game + pick data for 2023/2024 from local files."""
    with open(os.path.join(DATA_DIR, f"nfl_games_{season}.json")) as f:
        games = json.load(f)
    with open(os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data = {}
    for week in range(1, TOTAL_WEEKS + 1):
        week_games = [g for g in games if g['week'] == week]
        week_picks = picks_data.get('weeks', {}).get(str(week), {}).get('teams', [])
        pick_shares = {p['teamId']: p.get('average', 0) for p in week_picks}

        teams = []
        for g in week_games:
            home = g['homeTeamId']
            away = g['awayTeamId']
            hwp = float(g['homeWinProbability'])
            awp = float(g['awayWinProbability'])
            completed = g.get('completed', False)
            home_outcome = None
            away_outcome = None
            if completed and g['homeScore'] is not None and g['awayScore'] is not None:
                home_outcome = 'Win' if g['homeScore'] > g['awayScore'] else 'Loss'
                away_outcome = 'Win' if g['awayScore'] > g['homeScore'] else 'Loss'

            teams.append({'teamId': home, 'winProbability': hwp, 'pickShare': pick_shares.get(home, 0), 'outcome': home_outcome})
            teams.append({'teamId': away, 'winProbability': awp, 'pickShare': pick_shares.get(away, 0), 'outcome': away_outcome})

        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025():
    """Load 2025 data from API."""
    all_week_data = {}
    for week in range(1, TOTAL_WEEKS + 1):
        sys.stdout.write(f"\r  Fetching 2025 Week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()
        games = fetch_json(f"{BASE_URL}/api/games?season=2025&scheduleType=regular&week={week}")
        dynamics = fetch_json(f"{BASE_URL}/api/pools/{POOL_ID_2025}/dynamics/comprehensive?week={week}&season=2025&scheduleType=regular")
        if not games or not dynamics:
            continue
        pick_shares = {t['teamId']: t.get('pickShare', 0) for t in dynamics.get('teamDynamics', [])}
        teams = []
        for g in games:
            hwp = float(g['homeWinProbability']) if g.get('homeWinProbability') else 0
            awp = float(g['awayWinProbability']) if g.get('awayWinProbability') else 0
            completed = g.get('completed', False)
            hs, as_ = g.get('homeScore'), g.get('awayScore')
            ho = ('Win' if hs > as_ else 'Loss') if completed and hs is not None and as_ is not None else None
            ao = ('Win' if as_ > hs else 'Loss') if completed and hs is not None and as_ is not None else None
            home, away = g['homeTeamId'], g['awayTeamId']
            teams.append({'teamId': home, 'winProbability': hwp, 'pickShare': pick_shares.get(home, 0), 'outcome': ho})
            teams.append({'teamId': away, 'winProbability': awp, 'pickShare': pick_shares.get(away, 0), 'outcome': ao})
        if teams:
            all_week_data[week] = teams
    print(f"\r  2025: Loaded {len(all_week_data)} weeks.          ")
    return all_week_data


def compute_future_value(team_id, current_week, all_week_data, lookahead, decay_type, 
                         wp_weight=0.7, ps_weight=0.3, min_future_wp=0.0):
    """
    Compute the future value of a team over the next N weeks.
    
    Returns a score representing how valuable this team will be in upcoming weeks.
    Higher = more valuable to save for later.
    
    decay_type: 'linear' or 'exponential'
    - linear: weight = 1 - (offset / lookahead)  [week+1 gets full weight, week+N gets ~0]
    - exponential: weight = 0.5^(offset-1)  [week+1 gets 1.0, week+2 gets 0.5, week+3 gets 0.25...]
    """
    future_value = 0
    for offset in range(1, lookahead + 1):
        future_week = current_week + offset
        if future_week > TOTAL_WEEKS:
            break
        
        future_teams = all_week_data.get(future_week, [])
        future_team = next((t for t in future_teams if t['teamId'] == team_id), None)
        if not future_team:
            continue
        
        wp = future_team['winProbability']
        if wp < min_future_wp:
            continue
            
        ps = future_team['pickShare']
        
        # Score this future week's value
        week_score = wp_weight * wp + ps_weight * (1 - ps / 100)
        
        # Apply time decay
        if decay_type == 'linear':
            decay = 1.0 - (offset - 1) / lookahead
        elif decay_type == 'exponential':
            decay = 0.5 ** (offset - 1)
        else:
            decay = 1.0
        
        future_value += week_score * decay
    
    return future_value


# ─── Strategy Definitions ───────────────────────────────────────────────────

def make_scorer(wp_weight, ps_weight, lookahead=0, decay_type='linear', 
                penalty_factor=0.15, min_future_wp=0.0, future_includes_ps=True):
    """
    Factory function that creates a scoring function with the given parameters.
    
    Base score = wp_weight * winProb + ps_weight * (1 - pickShare/100)
    Future penalty = penalty_factor * future_value (weighted by decay)
    Final score = base_score - future_penalty
    
    penalty_factor controls how much to penalize using a high-future-value team now.
    A value of 0.15 means "I'll accept 15% less current value to save this team."
    """
    def scorer(team, all_teams, all_week_data, available, current_week):
        wp = team['winProbability']
        ps = team['pickShare']
        
        base_score = (wp_weight / 100) * wp + (ps_weight / 100) * (1 - ps / 100)
        
        if lookahead == 0:
            return base_score
        
        fv_wp = wp_weight / 100 if future_includes_ps else 1.0
        fv_ps = ps_weight / 100 if future_includes_ps else 0.0
        
        future_val = compute_future_value(
            team['teamId'], current_week, all_week_data,
            lookahead, decay_type, fv_wp, fv_ps, min_future_wp
        )
        
        # Normalize future value by lookahead window to keep penalty scale consistent
        if lookahead > 0:
            future_val /= lookahead
        
        return base_score - penalty_factor * future_val
    
    return scorer


STRATEGIES = [
    ("1. Pure Win Probability",
     make_scorer(100, 0)),
    
    ("2. 70/30 Blend (current best)",
     make_scorer(70, 30)),
    
    ("3. Lookahead-3 Linear (penalty=0.10)",
     make_scorer(70, 30, lookahead=3, decay_type='linear', penalty_factor=0.10)),
    
    ("4. Lookahead-5 Linear (penalty=0.10)",
     make_scorer(70, 30, lookahead=5, decay_type='linear', penalty_factor=0.10)),
    
    ("5. Lookahead-5 Exponential (penalty=0.10)",
     make_scorer(70, 30, lookahead=5, decay_type='exponential', penalty_factor=0.10)),
    
    ("6. Lookahead-3 Aggressive (penalty=0.20)",
     make_scorer(70, 30, lookahead=3, decay_type='linear', penalty_factor=0.20)),
    
    ("7. Lookahead-5 + 65% floor (penalty=0.10)",
     make_scorer(70, 30, lookahead=5, decay_type='exponential', penalty_factor=0.10, min_future_wp=0.65)),
    
    ("8. Lookahead-5 Exp (penalty=0.15)",
     make_scorer(70, 30, lookahead=5, decay_type='exponential', penalty_factor=0.15)),
    
    ("9. Lookahead-3 Exp (penalty=0.15)",
     make_scorer(70, 30, lookahead=3, decay_type='exponential', penalty_factor=0.15)),
    
    ("10. Lookahead-5 Linear (penalty=0.15)",
     make_scorer(70, 30, lookahead=5, decay_type='linear', penalty_factor=0.15)),
]


# ─── Simulation ─────────────────────────────────────────────────────────────

def simulate(strategy_name, score_fn, week_data):
    alive = set(range(NUM_ENTRIES))
    used_teams = [set() for _ in range(NUM_ENTRIES)]
    entry_weeks_survived = 0
    final_elim_week = None
    all_wps = []
    all_owns = []

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

            scored = []
            for t in available:
                s = score_fn(t, teams, week_data, available, week)
                scored.append((s, t))
            scored.sort(key=lambda x: x[0], reverse=True)

            if scored:
                best = scored[0][1]
                assigned.add(best['teamId'])
                used_teams[i].add(best['teamId'])
                picks[i] = best

        for i in sorted(alive):
            p = picks.get(i)
            if p:
                all_wps.append(p['winProbability'])
                all_owns.append(p['pickShare'])
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks_survived += 1

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = f"18+" if alive else 18

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0
    avg_own = sum(all_owns) / len(all_owns) if all_owns else 0

    return {
        'entry_weeks': entry_weeks_survived,
        'final_elim': final_elim_week,
        'avg_wp': avg_wp,
        'avg_own': avg_own,
    }


def main():
    print("=" * 95)
    print("STAN THE SCOUT: FUTURE VALUE LOOKAHEAD SIMULATION")
    print("Seasons: 2023, 2024, 2025 | 5 Entries | 10 Strategies")
    print("=" * 95)
    print()

    print("Loading data...")
    season_data = {}
    print("  Loading 2023...")
    season_data[2023] = load_local_season(2023)
    print(f"  2023: {len(season_data[2023])} weeks")
    print("  Loading 2024...")
    season_data[2024] = load_local_season(2024)
    print(f"  2024: {len(season_data[2024])} weeks")
    print("  Loading 2025...")
    season_data[2025] = load_2025()
    print()

    results = {}
    for strat_name, strat_fn in STRATEGIES:
        results[strat_name] = {}
        for season in [2023, 2024, 2025]:
            r = simulate(strat_name, strat_fn, season_data[season])
            results[strat_name][season] = r

    # Per-season results
    for season in [2023, 2024, 2025]:
        print(f"\n{'=' * 95}")
        print(f"SEASON: {season}")
        print(f"{'=' * 95}")
        print(f"{'Strategy':<45} {'Last Elim':<12} {'Entry-Wks':<12} {'Avg WP':<10} {'Avg Own'}")
        print(f"{'─' * 45} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 10}")

        rows = [(name, results[name][season]) for name, _ in STRATEGIES]
        rows.sort(key=lambda x: x[1]['entry_weeks'], reverse=True)

        for name, r in rows:
            elim = f"Wk {r['final_elim']}" if isinstance(r['final_elim'], int) else r['final_elim']
            print(f"{name:<45} {elim:<12} {r['entry_weeks']:<12} {r['avg_wp']:.1%}{'':>4} {r['avg_own']:.1f}%")

    # Cross-season summary
    print(f"\n{'=' * 110}")
    print("CROSS-SEASON SUMMARY")
    print(f"{'=' * 110}")
    print(f"{'Strategy':<45} {'2023':<8} {'2024':<8} {'2025':<8} {'TOTAL':<8} {'Avg':<8} {'SD':<8} {'Best In'}")
    print(f"{'─' * 45} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 10}")

    summary = []
    for name, _ in STRATEGIES:
        s23 = results[name][2023]['entry_weeks']
        s24 = results[name][2024]['entry_weeks']
        s25 = results[name][2025]['entry_weeks']
        total = s23 + s24 + s25
        avg = total / 3
        std = ((s23 - avg)**2 + (s24 - avg)**2 + (s25 - avg)**2) ** 0.5 / 3 ** 0.5
        
        # Count how many seasons this strategy was #1
        best_count = 0
        for season in [2023, 2024, 2025]:
            season_best = max(results[n][season]['entry_weeks'] for n, _ in STRATEGIES)
            if results[name][season]['entry_weeks'] == season_best:
                best_count += 1
        
        summary.append((name, s23, s24, s25, total, avg, std, best_count))

    summary.sort(key=lambda x: x[4], reverse=True)

    for name, s23, s24, s25, total, avg, std, best_count in summary:
        best_str = f"{best_count}/3" if best_count > 0 else "-"
        print(f"{name:<45} {s23:<8} {s24:<8} {s25:<8} {total:<8} {avg:<8.1f} {std:<8.1f} {best_str}")

    best = summary[0]
    print(f"\n** BEST OVERALL: {best[0]} -- {best[4]} total entry-weeks ({best[5]:.1f}/season, SD={best[6]:.1f})")
    
    # Compare to baselines
    baseline_wp = next(s for s in summary if '1. Pure' in s[0])
    baseline_70 = next(s for s in summary if '2. 70/30' in s[0])
    print(f"   vs Pure Win Prob: +{best[4] - baseline_wp[4]} entry-weeks ({(best[4]/baseline_wp[4]-1)*100:+.0f}%)")
    print(f"   vs 70/30 Blend:   +{best[4] - baseline_70[4]} entry-weeks ({(best[4]/baseline_70[4]-1)*100:+.0f}%)")


if __name__ == "__main__":
    main()
