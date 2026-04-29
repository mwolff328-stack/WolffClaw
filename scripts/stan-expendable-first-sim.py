#!/usr/bin/env python3
"""
Stan the Scout: Expendable-First + EV Strategy Simulation

Tests the "expendable-first" approach: instead of penalizing high-future-value teams,
reward LOW-future-value (expendable) teams. Also tests the actual SurvivorPulse EV
formula (EV = winProb - pickShare) as a scoring method.

Strategies:
1. Pure Win Probability (baseline)
2. 70/30 Weighted Blend (current best)
3. SurvivorPulse EV (evPick = winProb - pickShare)
4. Expendable-First 60/25/15 (wp/ps/expendability) - 3wk lookahead, exp decay
5. Expendable-First 65/25/10 - 3wk lookahead, exp decay
6. Expendable-First 60/25/15 - 5wk lookahead, exp decay
7. Expendable-First 65/20/15 - 5wk lookahead, exp decay
8. SurvivorPulse Production: 70% EV + 30% Future Utility (matching actual weights)
9. SurvivorPulse Conservative: 65% EV + 25% FV + 10% Leverage
10. SurvivorPulse Balanced: 55% EV + 25% FV + 20% Leverage
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
            home, away = g['homeTeamId'], g['awayTeamId']
            hwp, awp = float(g['homeWinProbability']), float(g['awayWinProbability'])
            completed = g.get('completed', False)
            ho = ao = None
            if completed and g['homeScore'] is not None and g['awayScore'] is not None:
                ho = 'Win' if g['homeScore'] > g['awayScore'] else 'Loss'
                ao = 'Win' if g['awayScore'] > g['homeScore'] else 'Loss'
            teams.append({'teamId': home, 'winProbability': hwp, 'pickShare': pick_shares.get(home, 0), 'outcome': ho})
            teams.append({'teamId': away, 'winProbability': awp, 'pickShare': pick_shares.get(away, 0), 'outcome': ao})
        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025():
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


def compute_expendability(team_id, current_week, all_week_data, lookahead, decay_type='exponential'):
    """
    Compute how "expendable" a team is. HIGH expendability = low future value = use it now.
    Returns 0-1 where 1 = very expendable (no future value), 0 = very valuable (save it).
    """
    max_future_score = 0
    
    for offset in range(1, lookahead + 1):
        future_week = current_week + offset
        if future_week > TOTAL_WEEKS:
            break
        
        future_teams = all_week_data.get(future_week, [])
        future_team = next((t for t in future_teams if t['teamId'] == team_id), None)
        if not future_team:
            continue
        
        wp = future_team['winProbability']
        ps = future_team['pickShare']
        # Future value using the blended score
        future_score = 0.7 * wp + 0.3 * (1 - ps / 100)
        
        if decay_type == 'exponential':
            decay = 0.5 ** (offset - 1)
        else:
            decay = 1.0 - (offset - 1) / lookahead
        
        weighted_score = future_score * decay
        max_future_score = max(max_future_score, weighted_score)
    
    # Invert: high future value -> low expendability, low future value -> high expendability
    expendability = 1.0 - max_future_score
    return max(0, min(1, expendability))


def compute_leverage_vs_chalk(team, all_teams):
    """SurvivorPulse leverage vs chalk: p_team * (1 - p_chalk) * q_chalk"""
    chalk = max(all_teams, key=lambda t: t['pickShare'])
    p_team = team['winProbability']
    p_chalk = chalk['winProbability']
    q_chalk = chalk['pickShare'] / 100  # Convert to 0-1
    return p_team * (1 - p_chalk) * q_chalk


def make_scorer(name, wp_weight=70, ps_weight=30, fv_weight=0, ev_mode=False,
                lookahead=0, decay='exponential', use_leverage=False, lev_weight=0,
                ev_weight=0, fv_real_weight=0):
    """
    Factory for scoring functions.
    
    For expendable-first: score = wp*winProb + ps*(1-pickShare) + fv*expendability
    For EV mode: score = winProb - pickShare (SurvivorPulse evPick formula)
    For SurvivorPulse production: score = ev_weight*(winProb - pickShare) + fv_real_weight*futureUtility + lev_weight*leverage
    """
    def scorer(team, all_teams, all_week_data, available, current_week):
        wp = team['winProbability']
        ps = team['pickShare']
        
        if ev_mode:
            # SurvivorPulse EV formula: evPick = pW - qW
            return wp - (ps / 100)
        
        # Base score components
        base = (wp_weight / 100) * wp + (ps_weight / 100) * (1 - ps / 100)
        
        # Expendability bonus (reward using expendable teams)
        exp_bonus = 0
        if fv_weight > 0 and lookahead > 0:
            expendability = compute_expendability(
                team['teamId'], current_week, all_week_data, lookahead, decay
            )
            exp_bonus = (fv_weight / 100) * expendability
        
        # SurvivorPulse-style: EV + Future Utility + Leverage
        ev_component = 0
        fv_component = 0
        lev_component = 0
        
        if ev_weight > 0:
            ev = wp - (ps / 100)  # evPick formula
            # Normalize EV to 0-1 range (EV ranges from about -0.3 to 0.9)
            ev_normalized = (ev + 0.5) / 1.5  # shift to ~0-1
            ev_normalized = max(0, min(1, ev_normalized))
            ev_component = (ev_weight / 100) * ev_normalized
        
        if fv_real_weight > 0 and lookahead > 0:
            # Future utility = expendability inverted (high FV = save it)
            expendability = compute_expendability(
                team['teamId'], current_week, all_week_data, lookahead, decay
            )
            future_utility = 1 - expendability  # High future value = high utility
            fv_component = (fv_real_weight / 100) * future_utility
        
        if use_leverage and lev_weight > 0:
            lev = compute_leverage_vs_chalk(team, all_teams)
            # Normalize leverage to 0-1 (typically 0-0.2 range)
            lev_normalized = min(1, lev * 5)
            lev_component = (lev_weight / 100) * lev_normalized
        
        return base + exp_bonus + ev_component + fv_component + lev_component
    
    return scorer


STRATEGIES = [
    ("1. Pure Win Probability",
     make_scorer("1", wp_weight=100, ps_weight=0)),
    
    ("2. 70/30 Blend (current best)",
     make_scorer("2", wp_weight=70, ps_weight=30)),
    
    ("3. SP EV (winProb - pickShare)",
     make_scorer("3", ev_mode=True)),
    
    ("4. Expendable 60/25/15 3wk",
     make_scorer("4", wp_weight=60, ps_weight=25, fv_weight=15, lookahead=3)),
    
    ("5. Expendable 65/25/10 3wk",
     make_scorer("5", wp_weight=65, ps_weight=25, fv_weight=10, lookahead=3)),
    
    ("6. Expendable 60/25/15 5wk",
     make_scorer("6", wp_weight=60, ps_weight=25, fv_weight=15, lookahead=5)),
    
    ("7. Expendable 65/20/15 5wk",
     make_scorer("7", wp_weight=65, ps_weight=20, fv_weight=15, lookahead=5)),
    
    ("8. SP Prod: 70% EV + 30% FV",
     make_scorer("8", wp_weight=0, ps_weight=0, ev_weight=70, fv_real_weight=30, lookahead=5)),
    
    ("9. SP Conservative: 65/25/10",
     make_scorer("9", wp_weight=0, ps_weight=0, ev_weight=65, fv_real_weight=25, 
                 use_leverage=True, lev_weight=10, lookahead=5)),
    
    ("10. SP Balanced: 55/25/20",
     make_scorer("10", wp_weight=0, ps_weight=0, ev_weight=55, fv_real_weight=25,
                 use_leverage=True, lev_weight=20, lookahead=5)),
]


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

            scored = [(score_fn(t, teams, week_data, available, week), t) for t in available]
            scored.sort(key=lambda x: x[0], reverse=True)

            if scored:
                best = scored[0][1]
                assigned.add(best['teamId'])
                used_teams[i].add(best['teamId'])
                picks[i] = best
                all_wps.append(best['winProbability'])
                all_owns.append(best['pickShare'])

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

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0
    avg_own = sum(all_owns) / len(all_owns) if all_owns else 0

    return {
        'entry_weeks': entry_weeks_survived,
        'final_elim': final_elim_week,
        'avg_wp': avg_wp,
        'avg_own': avg_own,
    }


def main():
    print("=" * 100)
    print("STAN: EXPENDABLE-FIRST + SURVIVORPULSE EV SIMULATION")
    print("Seasons: 2023, 2024, 2025 | 5 Entries | 10 Strategies")
    print("=" * 100)
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

    # Per-season
    for season in [2023, 2024, 2025]:
        print(f"\n{'=' * 100}")
        print(f"SEASON: {season}")
        print(f"{'=' * 100}")
        print(f"{'Strategy':<42} {'Last Elim':<12} {'Entry-Wks':<12} {'Avg WP':<10} {'Avg Own'}")
        print(f"{'─' * 42} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 10}")
        rows = [(n, results[n][season]) for n, _ in STRATEGIES]
        rows.sort(key=lambda x: x[1]['entry_weeks'], reverse=True)
        for name, r in rows:
            elim = f"Wk {r['final_elim']}" if isinstance(r['final_elim'], int) else r['final_elim']
            print(f"{name:<42} {elim:<12} {r['entry_weeks']:<12} {r['avg_wp']:.1%}{'':>4} {r['avg_own']:.1f}%")

    # Cross-season
    print(f"\n{'=' * 115}")
    print("CROSS-SEASON SUMMARY")
    print(f"{'=' * 115}")
    print(f"{'Strategy':<42} {'2023':<8} {'2024':<8} {'2025':<8} {'TOTAL':<8} {'Avg':<8} {'SD':<8} {'vs 70/30'}")
    print(f"{'─' * 42} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 10}")

    baseline_70 = sum(results["2. 70/30 Blend (current best)"][s]['entry_weeks'] for s in [2023,2024,2025])

    summary = []
    for name, _ in STRATEGIES:
        s23 = results[name][2023]['entry_weeks']
        s24 = results[name][2024]['entry_weeks']
        s25 = results[name][2025]['entry_weeks']
        total = s23 + s24 + s25
        avg = total / 3
        std = ((s23-avg)**2 + (s24-avg)**2 + (s25-avg)**2) ** 0.5 / 3 ** 0.5
        delta = total - baseline_70
        summary.append((name, s23, s24, s25, total, avg, std, delta))

    summary.sort(key=lambda x: x[4], reverse=True)

    for name, s23, s24, s25, total, avg, std, delta in summary:
        delta_str = f"{delta:+d}" if delta != 0 else "="
        print(f"{name:<42} {s23:<8} {s24:<8} {s25:<8} {total:<8} {avg:<8.1f} {std:<8.1f} {delta_str}")

    best = summary[0]
    print(f"\n** BEST: {best[0]} -- {best[4]} total ({best[5]:.1f}/season, SD={best[6]:.1f})")


if __name__ == "__main__":
    main()
