#!/usr/bin/env python3
"""
Stan the Scout: Entry-Count Scaling Simulation (Round 6)

14 strategies x 4 entry counts (5, 10, 20, 50) x 3 seasons (2023, 2024, 2025) = 168 runs.

Research question: Does the 70/30 Blend still dominate at higher entry counts,
or do coordination/diversification/scarcity-aware strategies prove the CMEA thesis?
"""

import urllib.request
import json
import sys
import os

DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
CACHE_FILE = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]


# --------------------------------------------------------------------------
# Data Loading
# --------------------------------------------------------------------------

def fetch_json(url, timeout=20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
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
            hwp = float(g['homeWinProbability'])
            awp = float(g['awayWinProbability'])
            completed = g.get('completed', False)
            ho = ao = None
            if completed and g['homeScore'] is not None and g['awayScore'] is not None:
                ho = 'Win' if g['homeScore'] > g['awayScore'] else 'Loss'
                ao = 'Win' if g['awayScore'] > g['homeScore'] else 'Loss'
            teams.append({
                'teamId': home, 'winProbability': hwp,
                'pickShare': pick_shares.get(home, 0), 'outcome': ho
            })
            teams.append({
                'teamId': away, 'winProbability': awp,
                'pickShare': pick_shares.get(away, 0), 'outcome': ao
            })
        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025():
    if os.path.exists(CACHE_FILE):
        print("  2025: Loading from cache...")
        with open(CACHE_FILE) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}

    all_week_data = {}
    for week in range(1, TOTAL_WEEKS + 1):
        sys.stdout.write(f"\r  Fetching 2025 Week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()
        games = fetch_json(
            f"{BASE_URL}/api/games?season=2025&scheduleType=regular&week={week}"
        )
        dynamics = fetch_json(
            f"{BASE_URL}/api/pools/{POOL_ID_2025}/dynamics/comprehensive"
            f"?week={week}&season=2025&scheduleType=regular"
        )
        if not games or not dynamics:
            continue
        pick_shares = {
            t['teamId']: t.get('pickShare', 0)
            for t in dynamics.get('teamDynamics', [])
        }
        teams = []
        for g in games:
            hwp = float(g['homeWinProbability']) if g.get('homeWinProbability') else 0
            awp = float(g['awayWinProbability']) if g.get('awayWinProbability') else 0
            completed = g.get('completed', False)
            hs, as_ = g.get('homeScore'), g.get('awayScore')
            ho = ('Win' if hs > as_ else 'Loss') if (completed and hs is not None and as_ is not None) else None
            ao = ('Win' if as_ > hs else 'Loss') if (completed and hs is not None and as_ is not None) else None
            home, away = g['homeTeamId'], g['awayTeamId']
            teams.append({'teamId': home, 'winProbability': hwp,
                          'pickShare': pick_shares.get(home, 0), 'outcome': ho})
            teams.append({'teamId': away, 'winProbability': awp,
                          'pickShare': pick_shares.get(away, 0), 'outcome': ao})
        if teams:
            all_week_data[week] = teams

    print(f"\r  2025: Loaded {len(all_week_data)} weeks.          ")
    with open(CACHE_FILE, 'w') as f:
        json.dump(all_week_data, f)
    print(f"  2025: Cached to {CACHE_FILE}")
    return all_week_data


# --------------------------------------------------------------------------
# Scoring Helpers
# --------------------------------------------------------------------------

def compute_expendability(team_id, current_week, all_week_data, lookahead):
    """HIGH expendability = low future value = safe to use now. Returns 0-1."""
    max_future_score = 0.0
    for offset in range(1, lookahead + 1):
        fw = current_week + offset
        if fw > TOTAL_WEEKS:
            break
        future_teams = all_week_data.get(fw, [])
        ft = next((t for t in future_teams if t['teamId'] == team_id), None)
        if not ft:
            continue
        future_score = 0.7 * ft['winProbability'] + 0.3 * (1 - ft['pickShare'] / 100)
        decay = 0.5 ** (offset - 1)
        max_future_score = max(max_future_score, future_score * decay)
    return max(0.0, min(1.0, 1.0 - max_future_score))


def compute_leverage(team, all_teams):
    """SurvivorPulse leverage vs chalk: p_team * (1 - p_chalk) * q_chalk."""
    chalk = max(all_teams, key=lambda t: t['pickShare'])
    return team['winProbability'] * (1 - chalk['winProbability']) * (chalk['pickShare'] / 100)


def count_quality_teams_remaining(used_set, current_week, all_week_data, min_wp=0.60):
    """Count unique teams with WP >= min_wp available to this entry in future weeks."""
    seen = set()
    count = 0
    for week in range(current_week, TOTAL_WEEKS + 1):
        for t in all_week_data.get(week, []):
            tid = t['teamId']
            if tid not in used_set and tid not in seen and t['winProbability'] >= min_wp:
                seen.add(tid)
                count += 1
    return count


# --------------------------------------------------------------------------
# Scorer Factory
# --------------------------------------------------------------------------

def make_scorer(wp_weight=70, ps_weight=30, fv_exp_weight=0, fv_save_weight=0,
                ev_weight=0, lev_weight=0, lookahead=0,
                adaptive=False, scarcity_aware=False, anti_corr_weight=0,
                min_wp_floor=0.0, ev_mode=False):
    """
    General scorer factory. Extended signature supports per-entry context.

    Scorer(team, all_teams, all_week_data, available, current_week, entry_idx, all_used_teams)

    fv_exp_weight: reward EXPENDABLE teams (low future value) — use them up
    fv_save_weight: reward high-FUTURE-VALUE teams in the score (SP Production style)
    ev_weight: SurvivorPulse EV component (normalized)
    lev_weight: leverage vs chalk component
    adaptive: shift 90/10 → 50/50 over 18 weeks
    scarcity_aware: boost FV save weight when entry's quality team count drops below 8
    anti_corr_weight: penalize teams previously used by OTHER entries
    min_wp_floor: hard floor on win probability (returns -999 if below)
    ev_mode: pure SP EV formula (winProb - pickShare), ignores other weights
    """
    def scorer(team, all_teams, all_week_data, available, current_week,
               entry_idx=0, all_used_teams=None):
        wp = team['winProbability']
        ps = team['pickShare']

        if min_wp_floor > 0 and wp < min_wp_floor:
            return -999.0

        if ev_mode:
            return wp - (ps / 100)

        # Base: win-prob / pick-share blend
        if adaptive:
            progress = (current_week - 1) / max(1, TOTAL_WEEKS - 1)
            eff_wp = 90 - 40 * progress   # 90 -> 50
            eff_ps = 10 + 40 * progress   # 10 -> 50
            base = (eff_wp / 100) * wp + (eff_ps / 100) * (1 - ps / 100)
        else:
            base = (wp_weight / 100) * wp + (ps_weight / 100) * (1 - ps / 100)

        # Expendable-first: reward teams with low future value
        if fv_exp_weight > 0 and lookahead > 0:
            exp = compute_expendability(team['teamId'], current_week, all_week_data, lookahead)
            base += (fv_exp_weight / 100) * exp

        # Future-save: reward teams with high future value (SP Production style)
        if fv_save_weight > 0 and lookahead > 0:
            exp = compute_expendability(team['teamId'], current_week, all_week_data, lookahead)
            future_utility = 1.0 - exp
            base += (fv_save_weight / 100) * future_utility

        # SP EV component (normalized winProb - pickShare)
        if ev_weight > 0:
            ev = wp - (ps / 100)
            ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
            base += (ev_weight / 100) * ev_norm

        # Leverage vs chalk
        if lev_weight > 0:
            lev = compute_leverage(team, all_teams)
            lev_norm = min(1.0, lev * 5)
            base += (lev_weight / 100) * lev_norm

        # Scarcity-aware: boost future-save weight when running low on quality teams
        if scarcity_aware and all_used_teams is not None:
            my_used = all_used_teams[entry_idx] if entry_idx < len(all_used_teams) else set()
            quality_remaining = count_quality_teams_remaining(my_used, current_week, all_week_data)
            if quality_remaining < 8:
                exp = compute_expendability(team['teamId'], current_week, all_week_data, 5)
                future_utility = 1.0 - exp
                scarcity_boost = max(0.0, (8 - quality_remaining) / 8) * 0.30
                base += scarcity_boost * future_utility

        # Anti-correlation: penalize teams used by other entries in prior weeks
        if anti_corr_weight > 0 and all_used_teams is not None:
            tid = team['teamId']
            n_others = len(all_used_teams) - 1
            if n_others > 0:
                times_used = sum(
                    1 for idx, used in enumerate(all_used_teams)
                    if idx != entry_idx and tid in used
                )
                penalty = (anti_corr_weight / 100) * (times_used / n_others)
                base -= penalty

        return base

    return scorer


# --------------------------------------------------------------------------
# Standalone Scorers
# --------------------------------------------------------------------------

def leverage_60_floor(team, all_teams, all_week_data, available, current_week,
                      entry_idx=0, all_used_teams=None):
    """Strategy 5: require WP >= 60%, then score by leverage vs chalk."""
    if team['winProbability'] < 0.60:
        return -999.0
    return compute_leverage(team, all_teams)


# --------------------------------------------------------------------------
# Mixed Portfolio Scorer Builder
# --------------------------------------------------------------------------

_PORTFOLIO_BASE_SCORERS = [
    make_scorer(wp_weight=70, ps_weight=30),                              # 70/30 blend
    make_scorer(ev_weight=70, fv_save_weight=30, lookahead=5),            # SP Production
    make_scorer(wp_weight=65, ps_weight=25, fv_exp_weight=10, lookahead=3),  # Expendable
    make_scorer(wp_weight=70, ps_weight=20, fv_exp_weight=10, lookahead=5),  # Lookahead-5
    make_scorer(wp_weight=100, ps_weight=0),                              # Pure WP
]


def make_mixed_scorers(num_entries):
    """Cycle through 5 base strategies across all entries."""
    return [_PORTFOLIO_BASE_SCORERS[i % len(_PORTFOLIO_BASE_SCORERS)] for i in range(num_entries)]


# --------------------------------------------------------------------------
# Simulation Engine
# --------------------------------------------------------------------------

def simulate(scorer_or_list, week_data, num_entries):
    """
    Sequential greedy assignment: entries pick in order, no duplicate teams per week.
    Falls back to duplicate picks when entries exceed available teams.

    scorer_or_list: single scorer callable, or list of scorers (one per entry).
    """
    if callable(scorer_or_list):
        scorers = [scorer_or_list] * num_entries
    else:
        scorers = list(scorer_or_list)
        # Safety: extend if needed
        while len(scorers) < num_entries:
            scorers.append(scorers[len(scorers) % len(scorers)])

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
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
            scorer = scorers[i]
            # Try unique team first
            available = [t for t in teams
                         if t['teamId'] not in assigned
                         and t['teamId'] not in used_teams[i]]
            # Fallback: allow duplicate picks (entry count > available teams)
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue  # Entry truly exhausted all teams — extremely rare

            scored = [
                (scorer(t, teams, week_data, available, week, i, used_teams), t)
                for t in available
            ]
            scored.sort(key=lambda x: x[0], reverse=True)
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
                    entry_weeks += 1

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0.0
    avg_own = sum(all_owns) / len(all_owns) if all_owns else 0.0
    return {
        'entry_weeks': entry_weeks,
        'final_elim': final_elim_week,
        'avg_wp': avg_wp,
        'avg_own': avg_own,
    }


def simulate_global_assign(scorer, week_data, num_entries):
    """
    Strategy 10: Global greedy assignment.
    Instead of entries picking in order, find the highest-scoring (entry, team)
    pair globally at each step, assign it, then find the next best, etc.
    This ensures the highest-value picks go to the entries that value them most,
    rather than rigidly giving entry 0 the first pick.
    """
    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None
    all_wps = []
    all_owns = []

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        alive_list = sorted(alive)

        # Build full (entry, team) score matrix for unique picks
        candidates = []
        for i in alive_list:
            for t in teams:
                if t['teamId'] not in used_teams[i]:
                    s = scorer(t, teams, week_data, teams, week, i, used_teams)
                    candidates.append((s, i, t['teamId'], t))

        candidates.sort(key=lambda x: x[0], reverse=True)

        assigned_entries = set()
        assigned_teams = set()
        picks = {}

        for s, i, tid, t in candidates:
            if i in assigned_entries or tid in assigned_teams:
                continue
            picks[i] = t
            assigned_entries.add(i)
            assigned_teams.add(tid)
            used_teams[i].add(tid)
            all_wps.append(t['winProbability'])
            all_owns.append(t['pickShare'])
            if len(assigned_entries) == len(alive_list):
                break

        # Fallback for entries that couldn't get a unique pick (50-entry overflow)
        for i in alive_list:
            if i not in picks:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
                if not available:
                    continue
                best = max(available, key=lambda t: scorer(t, teams, week_data, available, week, i, used_teams))
                picks[i] = best
                used_teams[i].add(best['teamId'])
                all_wps.append(best['winProbability'])
                all_owns.append(best['pickShare'])

        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks += 1

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0.0
    avg_own = sum(all_owns) / len(all_owns) if all_owns else 0.0
    return {
        'entry_weeks': entry_weeks,
        'final_elim': final_elim_week,
        'avg_wp': avg_wp,
        'avg_own': avg_own,
    }


# --------------------------------------------------------------------------
# Strategy Registry
# --------------------------------------------------------------------------

# (name, scorer_or_special)
# Special values: "leverage_60_floor", "global_assign", "mixed_portfolio"
STRATEGIES = [
    ("1.  Pure WinProb",
     make_scorer(wp_weight=100, ps_weight=0)),

    ("2.  70/30 Blend [champion]",
     make_scorer(wp_weight=70, ps_weight=30)),

    ("3.  80/20 Blend",
     make_scorer(wp_weight=80, ps_weight=20)),

    ("4.  60/40 Blend [contrarian]",
     make_scorer(wp_weight=60, ps_weight=40)),

    ("5.  Leverage+60%Floor",
     "leverage_60_floor"),

    ("6.  Lookahead-5 Exp [best FV]",
     make_scorer(wp_weight=70, ps_weight=20, fv_exp_weight=10, lookahead=5)),

    ("7.  SP Prod 70%EV+30%FV",
     make_scorer(ev_weight=70, fv_save_weight=30, lookahead=5)),

    ("8.  SP Conservative 65/25/10",
     make_scorer(ev_weight=65, fv_save_weight=25, lev_weight=10, lookahead=5)),

    ("9.  Expendable 65/25/10 3wk",
     make_scorer(wp_weight=65, ps_weight=25, fv_exp_weight=10, lookahead=3)),

    ("10. Coord Diversification [global]",
     "global_assign"),      # Uses global greedy assignment with 70/30 blend

    ("11. Adaptive Blend [90/10→50/50]",
     make_scorer(adaptive=True)),

    ("12. Scarcity-Aware",
     make_scorer(wp_weight=65, ps_weight=25, scarcity_aware=True)),

    ("13. Anti-Correlation",
     make_scorer(wp_weight=70, ps_weight=30, anti_corr_weight=20)),

    ("14. Mixed Portfolio",
     "mixed_portfolio"),    # Each entry uses a different base strategy
]

# 70/30 blend scorer reused for global-assign strategy
_BLEND_SCORER = make_scorer(wp_weight=70, ps_weight=30)


def run_strategy(strat_name, strat_val, week_data, num_entries):
    if strat_val == "leverage_60_floor":
        return simulate(leverage_60_floor, week_data, num_entries)
    elif strat_val == "global_assign":
        return simulate_global_assign(_BLEND_SCORER, week_data, num_entries)
    elif strat_val == "mixed_portfolio":
        scorers = make_mixed_scorers(num_entries)
        return simulate(scorers, week_data, num_entries)
    else:
        return simulate(strat_val, week_data, num_entries)


# --------------------------------------------------------------------------
# Output Helpers
# --------------------------------------------------------------------------

def fmt_elim(v):
    if isinstance(v, int):
        return f"Wk{v:2d}"
    return str(v)


def std(vals, avg):
    if len(vals) < 2:
        return 0.0
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    print("=" * 110)
    print("STAN: ENTRY-COUNT SCALING SIMULATION — Round 6")
    print("14 strategies × 4 entry counts (5, 10, 20, 50) × 3 seasons = 168 runs")
    print("=" * 110)
    print()

    # Load data
    print("Loading season data...")
    season_data = {}
    for season in [2023, 2024]:
        print(f"  Loading {season}...")
        season_data[season] = load_local_season(season)
        print(f"  {season}: {len(season_data[season])} weeks")
    print("  Loading 2025...")
    season_data[2025] = load_2025()
    print()

    seasons = [2023, 2024, 2025]
    strat_names = [n for n, _ in STRATEGIES]

    # Run all 168 simulations
    # results[strat_name][num_entries][season] = {entry_weeks, final_elim, avg_wp, avg_own}
    results = {n: {} for n in strat_names}

    total_runs = len(STRATEGIES) * len(ENTRY_COUNTS) * len(seasons)
    run_num = 0

    for strat_name, strat_val in STRATEGIES:
        results[strat_name] = {}
        for num_entries in ENTRY_COUNTS:
            results[strat_name][num_entries] = {}
            for season in seasons:
                run_num += 1
                sys.stdout.write(
                    f"\r  [{run_num:3d}/{total_runs}] {strat_name[:35]:<35} "
                    f"n={num_entries:2d} {season}"
                )
                sys.stdout.flush()
                r = run_strategy(strat_name, strat_val, season_data[season], num_entries)
                results[strat_name][num_entries][season] = r

    print(f"\r  All {total_runs} runs complete.{'':50}")
    print()

    # --------------------------------------------------------------------------
    # Output: Per Entry Count — all strategies, 3 seasons + totals
    # --------------------------------------------------------------------------
    for num_entries in ENTRY_COUNTS:
        max_possible = num_entries * TOTAL_WEEKS
        print("=" * 120)
        print(f"ENTRY COUNT: {num_entries} entries  (max possible entry-weeks: {max_possible})")
        print("=" * 120)
        print(f"{'Strategy':<40} {'2023':>6} {'2024':>6} {'2025':>6} {'TOTAL':>7} "
              f"{'Avg':>6} {'SD':>5} {'Eff%':>6} {'vs Blend':>8}")
        print(f"{'─' * 40} {'─' * 6} {'─' * 6} {'─' * 6} {'─' * 7} "
              f"{'─' * 6} {'─' * 5} {'─' * 6} {'─' * 8}")

        blend_total = sum(
            results["2.  70/30 Blend [champion]"][num_entries][s]['entry_weeks']
            for s in seasons
        )

        rows = []
        for name in strat_names:
            s23 = results[name][num_entries][2023]['entry_weeks']
            s24 = results[name][num_entries][2024]['entry_weeks']
            s25 = results[name][num_entries][2025]['entry_weeks']
            total = s23 + s24 + s25
            avg = total / 3
            sd = std([s23, s24, s25], avg)
            eff = total / (max_possible * 3) * 100
            delta = total - blend_total
            rows.append((name, s23, s24, s25, total, avg, sd, eff, delta))

        rows.sort(key=lambda x: x[4], reverse=True)

        for name, s23, s24, s25, total, avg, sd, eff, delta in rows:
            delta_str = f"{delta:+d}" if delta != 0 else "="
            print(f"{name:<40} {s23:>6} {s24:>6} {s25:>6} {total:>7} "
                  f"{avg:>6.1f} {sd:>5.1f} {eff:>5.1f}% {delta_str:>8}")

        print()

    # --------------------------------------------------------------------------
    # Output: Scaling Analysis — how each strategy scales with entry count
    # --------------------------------------------------------------------------
    print("=" * 120)
    print("SCALING ANALYSIS — Total entry-weeks across 3 seasons by entry count")
    print("(Shows whether strategies improve relative to 70/30 at higher entry counts)")
    print("=" * 120)
    print(f"{'Strategy':<40} {'n=5':>7} {'n=10':>7} {'n=20':>7} {'n=50':>7} "
          f"{'ScaleRatio':>11} {'BestAt':>8}")
    print(f"{'─' * 40} {'─' * 7} {'─' * 7} {'─' * 7} {'─' * 7} "
          f"{'─' * 11} {'─' * 8}")

    # Compute blend reference for each entry count
    blend_totals = {
        n: sum(results["2.  70/30 Blend [champion]"][n][s]['entry_weeks'] for s in seasons)
        for n in ENTRY_COUNTS
    }

    scaling_rows = []
    for name in strat_names:
        counts_totals = {
            n: sum(results[name][n][s]['entry_weeks'] for s in seasons)
            for n in ENTRY_COUNTS
        }
        t5  = counts_totals[5]
        t10 = counts_totals[10]
        t20 = counts_totals[20]
        t50 = counts_totals[50]

        # Scale ratio: how much does it grow relative to the 10x entry increase (5->50)?
        # Perfect linear scaling = 10x. Better than 10x means diminishing losses at scale.
        # Efficiency at n=5 vs n=50
        eff5  = t5  / (5  * TOTAL_WEEKS * 3) * 100
        eff50 = t50 / (50 * TOTAL_WEEKS * 3) * 100
        scale_ratio = t50 / t5 if t5 > 0 else 0  # should be ~10x if perfectly linear

        best_at = max(ENTRY_COUNTS, key=lambda n: counts_totals[n] / blend_totals[n])

        scaling_rows.append((name, t5, t10, t20, t50, scale_ratio, best_at,
                              eff5, eff50))

    scaling_rows.sort(key=lambda x: x[4], reverse=True)

    for name, t5, t10, t20, t50, sr, best_at, eff5, eff50 in scaling_rows:
        print(f"{name:<40} {t5:>7} {t10:>7} {t20:>7} {t50:>7} "
              f"  {sr:>8.2f}x   n={best_at:>2}")

    print()

    # --------------------------------------------------------------------------
    # Output: Efficiency comparison (normalized per entry-week)
    # --------------------------------------------------------------------------
    print("=" * 120)
    print("EFFICIENCY ANALYSIS — Entry-week survival rate (higher = better strategy per entry)")
    print("(Total / (num_entries × 18 weeks × 3 seasons) — removes scale inflation)")
    print("=" * 120)
    print(f"{'Strategy':<40} {'n=5 Eff':>8} {'n=10 Eff':>9} {'n=20 Eff':>9} {'n=50 Eff':>9} {'Δ 5→50':>8}")
    print(f"{'─' * 40} {'─' * 8} {'─' * 9} {'─' * 9} {'─' * 9} {'─' * 8}")

    eff_rows = []
    for name in strat_names:
        effs = {}
        for n in ENTRY_COUNTS:
            total = sum(results[name][n][s]['entry_weeks'] for s in seasons)
            effs[n] = total / (n * TOTAL_WEEKS * 3) * 100
        delta = effs[50] - effs[5]
        eff_rows.append((name, effs[5], effs[10], effs[20], effs[50], delta))

    eff_rows.sort(key=lambda x: x[4], reverse=True)

    for name, e5, e10, e20, e50, delta in eff_rows:
        delta_str = f"{delta:+.1f}pp"
        print(f"{name:<40} {e5:>7.1f}%  {e10:>7.1f}%   {e20:>7.1f}%   {e50:>7.1f}%   {delta_str:>8}")

    print()

    # --------------------------------------------------------------------------
    # Output: Strategy class winners per entry count
    # --------------------------------------------------------------------------
    print("=" * 120)
    print("WINNERS PER ENTRY COUNT")
    print("=" * 120)
    for num_entries in ENTRY_COUNTS:
        max_total = -1
        max_name = ""
        for name in strat_names:
            total = sum(results[name][num_entries][s]['entry_weeks'] for s in seasons)
            if total > max_total:
                max_total = total
                max_name = name
        eff = max_total / (num_entries * TOTAL_WEEKS * 3) * 100
        print(f"  n={num_entries:2d}: {max_name:<40}  total={max_total}  efficiency={eff:.1f}%")

    print()

    # --------------------------------------------------------------------------
    # Output: 70/30 Blend vs Champion at each entry count
    # --------------------------------------------------------------------------
    print("=" * 120)
    print("BLEND CHALLENGER ANALYSIS — At what entry count does 70/30 lose its crown?")
    print("=" * 120)
    for num_entries in ENTRY_COUNTS:
        blend_total = blend_totals[num_entries]
        challengers = []
        for name in strat_names:
            if "70/30 Blend" in name:
                continue
            total = sum(results[name][num_entries][s]['entry_weeks'] for s in seasons)
            if total > blend_total:
                challengers.append((name, total, total - blend_total))
        challengers.sort(key=lambda x: x[2], reverse=True)

        if challengers:
            print(f"  n={num_entries:2d}: 70/30 Blend BEATEN by {len(challengers)} strategies:")
            for cname, ctotal, cdelta in challengers[:5]:
                print(f"         {cname:<40} total={ctotal}  +{cdelta}")
        else:
            print(f"  n={num_entries:2d}: 70/30 Blend HOLDS LEAD (total={blend_total})")

    print()
    print("=" * 120)
    print("SIMULATION COMPLETE")
    print("=" * 120)

    # Save raw results for analysis
    output_path = os.path.join(
        os.path.expanduser("~/.openclaw/workspace"),
        "scripts/stan-entry-scale-results.json"
    )
    serializable = {}
    for name in strat_names:
        serializable[name] = {}
        for n in ENTRY_COUNTS:
            serializable[name][str(n)] = {}
            for season in seasons:
                r = results[name][n][season]
                serializable[name][str(n)][str(season)] = {
                    'entry_weeks': r['entry_weeks'],
                    'final_elim': str(r['final_elim']),
                    'avg_wp': round(r['avg_wp'], 4),
                    'avg_own': round(r['avg_own'], 4),
                }
    with open(output_path, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nRaw results saved to: {output_path}")


if __name__ == "__main__":
    main()
