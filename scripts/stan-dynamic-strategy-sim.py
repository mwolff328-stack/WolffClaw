#!/usr/bin/env python3
"""
Stan the Scout: Dynamic Strategy Switching Simulation

Research Question: Does dynamically switching pick strategy based on entry state each week
outperform the best static strategy assignment?

Framework: Two-level decision system from Strategy-to-Context Matching research.
  Level 1 (Pool Router): Base strategy by portfolio size + week phase
  Level 2 (Entry Personalizer): Override based on entry's A-tier team inventory

Pool Router:
  n=1-5:   Wk1-7→70/30 Blend | Wk8-14→SP Conservative | Wk15+→Pure WP
  n=6-15:  Wk1-7→Core/Satellite (60%Blend+40%EV) | Wk8-14→SP Production | Wk15+→70/30 Blend
  n=16-30: All weeks→Mixed Portfolio (week-phase weight adjustment)
  n=31-50: Wk1-14→70/30 Blend | Wk15+→Pure WP

Entry Personalizer (inventory override):
  4+ A-tier remaining → use Pool Router strategy as-is
  2-3 A-tier remaining → shift to SP Production or 70/30 Blend
  0-1 A-tier remaining → shift to Pure WP (survival mode)

Core/Satellite roles for n=6-15:
  60% = Core (best pick from assigned strategy)
  30% = Satellite (2nd-best alternative)
  10% = Swing (maximum contrarian)
"""

import json
import os
import sys

# Data directories
DATA_DIR_BACKTESTING = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
DATA_DIR_CMEA = os.path.expanduser("~/Projects/CMEA-Prototype/data")

TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]
A_TIER_WP_THRESHOLD = 0.75  # Teams with future WP >= this are "A-tier"

RESULTS_PATH = os.path.expanduser(
    "~/.openclaw/workspace/scripts/stan-dynamic-strategy-results.json"
)


# ─────────────────────────────────────────────────────────────────────────────
# Data Loading (from stan-10season-sim.py pattern)
# ─────────────────────────────────────────────────────────────────────────────

DIVISIONS = {
    "AFC East":  {"BUF", "MIA", "NE", "NYJ"},
    "AFC North": {"BAL", "CIN", "CLE", "PIT"},
    "AFC South": {"HOU", "IND", "JAX", "TEN"},
    "AFC West":  {"DEN", "KC", "LAC", "LV"},
    "NFC East":  {"DAL", "NYG", "PHI", "WAS"},
    "NFC North": {"CHI", "DET", "GB", "MIN"},
    "NFC South": {"ATL", "CAR", "NO", "TB"},
    "NFC West":  {"ARI", "LAR", "SEA", "SF"},
}
TEAM_DIVISION = {}
for div_name, teams in DIVISIONS.items():
    for t in teams:
        TEAM_DIVISION[t] = div_name


def season_weeks(season: int) -> int:
    return 17 if season <= 2020 else 18


def _normalize_game(g):
    home = g.get('homeTeamId') or g.get('home_team_id')
    away = g.get('awayTeamId') or g.get('away_team_id')
    hwp = float(g.get('homeWinProbability') or g.get('home_win_probability') or 0.5)
    awp = float(g.get('awayWinProbability') or g.get('away_win_probability') or 1.0 - hwp)
    hs = g.get('homeScore') if g.get('homeScore') is not None else g.get('home_score')
    as_ = g.get('awayScore') if g.get('awayScore') is not None else g.get('away_score')
    completed = bool(g.get('completed', False))
    return {
        'homeTeamId': home, 'awayTeamId': away,
        'homeWinProbability': hwp, 'awayWinProbability': awp,
        'homeScore': hs, 'awayScore': as_, 'completed': completed,
        'week': g.get('week'),
    }


def _parse_picks(picks_data):
    pick_by_week = {}
    for wk_str, wk_data in picks_data.get('weeks', {}).items():
        wk = int(wk_str)
        pick_by_week[wk] = {t['teamId']: t.get('average', 0) for t in wk_data.get('teams', [])}
    return pick_by_week


def _build_teams_from_games(week_games, week_picks):
    teams = []
    for g in week_games:
        ng = _normalize_game(g)
        home, away = ng['homeTeamId'], ng['awayTeamId']
        hwp, awp = ng['homeWinProbability'], ng['awayWinProbability']
        hs, as_ = ng['homeScore'], ng['awayScore']
        completed = ng['completed']
        ho = ('Win' if hs > as_ else 'Loss') if (completed and hs is not None and as_ is not None) else None
        ao = ('Win' if as_ > hs else 'Loss') if (completed and hs is not None and as_ is not None) else None
        teams.append({'teamId': home, 'winProbability': hwp,
                      'pickShare': week_picks.get(home, 0), 'outcome': ho})
        teams.append({'teamId': away, 'winProbability': awp,
                      'pickShare': week_picks.get(away, 0), 'outcome': ao})
    return teams


def load_season(season: int) -> dict:
    """Load all week data for a given season."""
    total_wks = season_weeks(season)

    if season == 2025:
        # 2025 cache is in normalized format
        cache_path = os.path.join(DATA_DIR_BACKTESTING, "nfl_games_2025_cache.json")
        # Also try CMEA dir
        if not os.path.exists(cache_path):
            cache_path = os.path.join(DATA_DIR_CMEA, "nfl_games_2025_cache.json")
        with open(cache_path) as f:
            raw = json.load(f)
        result = {}
        for wk_str, teams in raw.items():
            wk = int(wk_str)
            result[wk] = [
                {
                    'teamId': t['teamId'],
                    'winProbability': float(t.get('winProbability', 0.5)),
                    'pickShare': float(t.get('pickShare', 0)),
                    'outcome': t.get('outcome'),
                }
                for t in teams
            ]
        return result

    elif season == 2020:
        games_file = "nfl_games_2020_weather.json"
    else:
        games_file = f"nfl_games_{season}.json"

    games_path = os.path.join(DATA_DIR_BACKTESTING, games_file)
    picks_path = os.path.join(DATA_DIR_BACKTESTING, f"survivorgrid_picks_{season}.json")

    with open(games_path) as f:
        raw_games = json.load(f)
    with open(picks_path) as f:
        picks_data = json.load(f)

    pick_by_week = _parse_picks(picks_data)

    result = {}
    for week in range(1, total_wks + 1):
        week_games = [g for g in raw_games if (g.get('week') == week)]
        week_picks = pick_by_week.get(week, {})
        teams = _build_teams_from_games(week_games, week_picks)
        if teams:
            result[week] = teams
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Core Scoring Functions (from stan-entry-scale-sim.py)
# ─────────────────────────────────────────────────────────────────────────────

def compute_expendability(team_id, current_week, all_week_data, lookahead=5, total_weeks=TOTAL_WEEKS):
    max_future_score = 0.0
    for offset in range(1, lookahead + 1):
        fw = current_week + offset
        if fw > total_weeks:
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
    chalk = max(all_teams, key=lambda t: t['pickShare'])
    return team['winProbability'] * (1 - chalk['winProbability']) * (chalk['pickShare'] / 100)


def count_a_tier_remaining(used_set, current_week, all_week_data, threshold=A_TIER_WP_THRESHOLD, total_weeks=TOTAL_WEEKS):
    """Count unique teams with future WP >= threshold available to this entry."""
    seen = set()
    count = 0
    for week in range(current_week, total_weeks + 1):
        for t in all_week_data.get(week, []):
            tid = t['teamId']
            if tid not in used_set and tid not in seen and t['winProbability'] >= threshold:
                seen.add(tid)
                count += 1
    return count


# ─────────────────────────────────────────────────────────────────────────────
# Named Scoring Functions
# ─────────────────────────────────────────────────────────────────────────────

def score_pure_wp(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    return team['winProbability']


def score_blend_70_30(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    return 0.70 * team['winProbability'] + 0.30 * (1 - team['pickShare'] / 100)


def score_sp_production(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    """SP Production: 70% EV + 30% FV save."""
    wp = team['winProbability']
    ps = team['pickShare']
    ev = wp - (ps / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], current_week, all_week_data, 5, total_weeks)
    future_utility = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * future_utility


def score_sp_conservative(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    """SP Conservative: 65% EV + 25% FV + 10% leverage."""
    wp = team['winProbability']
    ps = team['pickShare']
    ev = wp - (ps / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], current_week, all_week_data, 5, total_weeks)
    future_utility = 1.0 - exp
    lev = compute_leverage(team, all_teams)
    lev_norm = min(1.0, lev * 5)
    return 0.65 * ev_norm + 0.25 * future_utility + 0.10 * lev_norm


def score_ev_pure(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    """Pure EV: winProb - pickShare."""
    return team['winProbability'] - (team['pickShare'] / 100)


def score_contrarian(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    """Maximum contrarian: invert pick share heavily."""
    return 0.40 * team['winProbability'] + 0.60 * (1 - team['pickShare'] / 100)


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Strategy Selector
# ─────────────────────────────────────────────────────────────────────────────

def get_week_phase(week):
    """Return 'early', 'mid', or 'late'."""
    if week <= 7:
        return 'early'
    elif week <= 14:
        return 'mid'
    else:
        return 'late'


def select_strategy(n, week, a_tier_count, role):
    """
    Returns a strategy name based on:
    - n: portfolio size
    - week: current week
    - a_tier_count: A-tier teams remaining for this entry
    - role: 'core', 'satellite', or 'swing' (only relevant for n=6-15)

    Returns one of: 'pure_wp', 'blend_70_30', 'sp_production',
                    'sp_conservative', 'ev_pure', 'contrarian'
    """
    phase = get_week_phase(week)

    # ─── Entry Personalizer Override (takes precedence) ─────────────────────
    # 0-1 A-tier remaining → survival mode
    if a_tier_count <= 1:
        return 'pure_wp'
    # 2-3 A-tier remaining → reduce FV weighting
    elif a_tier_count <= 3:
        if phase == 'late':
            return 'pure_wp'
        else:
            return 'blend_70_30'  # SP Production-like but simpler

    # ─── Pool Router (4+ A-tier remaining) ──────────────────────────────────

    if n <= 5:
        # n=1-5 regime
        if phase == 'early':
            return 'blend_70_30'
        elif phase == 'mid':
            return 'sp_conservative'
        else:  # late
            return 'pure_wp'

    elif n <= 15:
        # n=6-15 regime with Core/Satellite/Swing roles
        if phase == 'early':
            # Core/Satellite strategy: 60% blend + 40% EV split
            if role == 'swing':
                return 'contrarian'
            elif role == 'satellite':
                return 'ev_pure'
            else:  # core
                return 'blend_70_30'
        elif phase == 'mid':
            # SP Production for all roles, but satellite/swing get more aggressive
            if role == 'swing':
                return 'ev_pure'
            elif role == 'satellite':
                return 'sp_production'
            else:  # core
                return 'sp_production'
        else:  # late
            return 'blend_70_30'

    elif n <= 30:
        # n=16-30 regime → Mixed Portfolio (cycle through strategies)
        # Role determines which base strategy in the mix
        role_strategies = {
            'core': 'blend_70_30',
            'satellite': 'sp_production',
            'swing': 'ev_pure',
        }
        if phase == 'late':
            return 'pure_wp'
        return role_strategies.get(role, 'blend_70_30')

    else:
        # n=31-50 regime
        if phase == 'late':  # week 15+
            return 'pure_wp'
        else:
            return 'blend_70_30'


SCORER_MAP = {
    'pure_wp': score_pure_wp,
    'blend_70_30': score_blend_70_30,
    'sp_production': score_sp_production,
    'sp_conservative': score_sp_conservative,
    'ev_pure': score_ev_pure,
    'contrarian': score_contrarian,
}


# ─────────────────────────────────────────────────────────────────────────────
# Role Assignment for n=6-15
# ─────────────────────────────────────────────────────────────────────────────

def assign_roles(num_entries):
    """
    60% Core, 30% Satellite, 10% Swing.
    Returns list of roles indexed by entry number.
    """
    n_swing = max(1, round(num_entries * 0.10))
    n_satellite = max(1, round(num_entries * 0.30))
    n_core = num_entries - n_swing - n_satellite

    roles = ['core'] * n_core + ['satellite'] * n_satellite + ['swing'] * n_swing
    # Distribute evenly: core first, satellite middle, swing last
    return roles[:num_entries]


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Simulation Engine
# ─────────────────────────────────────────────────────────────────────────────

def simulate_dynamic(week_data, num_entries):
    """
    Dynamic strategy switching simulation.
    Each entry selects a pick strategy based on its current state each week.

    Returns:
      entry_weeks, late_survival (entries alive at week 14+),
      strategy_usage (dict of strategy→count),
      weekly_survivors (list of alive count per week)
    """
    total_weeks = max(week_data.keys()) if week_data else TOTAL_WEEKS

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    late_survival_entries = 0  # entries still alive at week 14+
    strategy_usage = {}
    weekly_survivors = []

    # Assign roles once at season start (for n=6-15 regime)
    roles = assign_roles(num_entries)

    for week in range(1, total_weeks + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            weekly_survivors.append(len(alive))
            continue

        # Track late-season entries (surviving into week 14+)
        if week == 14:
            late_survival_entries = len(alive)

        assigned = set()
        picks = {}
        strategies_this_week = {}

        for i in sorted(alive):
            # Compute A-tier remaining for this entry
            a_tier = count_a_tier_remaining(
                used_teams[i], week, week_data, A_TIER_WP_THRESHOLD, total_weeks
            )

            # Get role for this entry
            role = roles[i] if i < len(roles) else 'core'

            # Select strategy
            strat_name = select_strategy(num_entries, week, a_tier, role)
            scorer = SCORER_MAP[strat_name]
            strategies_this_week[i] = strat_name
            strategy_usage[strat_name] = strategy_usage.get(strat_name, 0) + 1

            # Find best available team (no duplicate picks per week)
            available = [t for t in teams
                         if t['teamId'] not in assigned
                         and t['teamId'] not in used_teams[i]]
            if not available:
                # Fallback: allow picking used-by-others teams
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            # For satellite role: take the 2nd-best pick to reduce correlation
            scored = sorted(
                [(scorer(t, teams, week_data, week, total_weeks), t) for t in available],
                key=lambda x: x[0],
                reverse=True
            )

            if role == 'satellite' and len(scored) >= 2:
                best = scored[1][1]  # 2nd best to reduce correlation
            elif role == 'swing' and len(scored) >= 3:
                best = scored[2][1]  # 3rd best for maximum contrarian
            else:
                best = scored[0][1]  # best pick

            assigned.add(best['teamId'])
            used_teams[i].add(best['teamId'])
            picks[i] = best

        # Resolve outcomes
        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks += 1

        weekly_survivors.append(len(alive))

    return {
        'entry_weeks': entry_weeks,
        'late_survival': late_survival_entries,
        'strategy_usage': strategy_usage,
        'weekly_survivors': weekly_survivors,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Static Strategy Simulations (for baseline comparison)
# ─────────────────────────────────────────────────────────────────────────────

def simulate_static(scorer_fn, week_data, num_entries):
    """
    Static strategy simulation using a single scorer for all entries all season.
    Sequential greedy assignment.
    """
    total_weeks = max(week_data.keys()) if week_data else TOTAL_WEEKS
    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    late_survival_entries = 0

    for week in range(1, total_weeks + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        if week == 14:
            late_survival_entries = len(alive)

        assigned = set()
        picks = {}

        for i in sorted(alive):
            available = [t for t in teams
                         if t['teamId'] not in assigned
                         and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            scored = sorted(
                [(scorer_fn(t, teams, week_data, week, total_weeks), t) for t in available],
                key=lambda x: x[0],
                reverse=True
            )
            best = scored[0][1]
            assigned.add(best['teamId'])
            used_teams[i].add(best['teamId'])
            picks[i] = best

        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks += 1

    return {'entry_weeks': entry_weeks, 'late_survival': late_survival_entries}


def simulate_mixed_portfolio(week_data, num_entries):
    """Mixed Portfolio: cycle through 5 base strategies across entries."""
    total_weeks = max(week_data.keys()) if week_data else TOTAL_WEEKS
    base_scorers = [
        score_blend_70_30,
        score_sp_production,
        score_pure_wp,
        score_sp_conservative,
        score_ev_pure,
    ]
    entry_scorers = [base_scorers[i % len(base_scorers)] for i in range(num_entries)]

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    late_survival_entries = 0

    for week in range(1, total_weeks + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        if week == 14:
            late_survival_entries = len(alive)

        assigned = set()
        picks = {}

        for i in sorted(alive):
            scorer = entry_scorers[i]
            available = [t for t in teams
                         if t['teamId'] not in assigned
                         and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            scored = sorted(
                [(scorer(t, teams, week_data, week, total_weeks), t) for t in available],
                key=lambda x: x[0],
                reverse=True
            )
            best = scored[0][1]
            assigned.add(best['teamId'])
            used_teams[i].add(best['teamId'])
            picks[i] = best

        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                else:
                    entry_weeks += 1

    return {'entry_weeks': entry_weeks, 'late_survival': late_survival_entries}


# ─────────────────────────────────────────────────────────────────────────────
# Static Baseline Registry
# ─────────────────────────────────────────────────────────────────────────────

# Best static strategy per entry count regime (from Round 6 results)
STATIC_BASELINES = {
    5:  [
        ("Adaptive Blend / Mixed Portfolio", None, 'mixed'),  # tied at 58
        ("70/30 Blend", score_blend_70_30, 'static'),
        ("SP Conservative", score_sp_conservative, 'static'),
    ],
    10: [
        ("SP Production", score_sp_production, 'static'),
        ("SP Conservative", score_sp_conservative, 'static'),
        ("70/30 Blend", score_blend_70_30, 'static'),
    ],
    20: [
        ("Mixed Portfolio", None, 'mixed'),
        ("SP Production", score_sp_production, 'static'),
        ("70/30 Blend", score_blend_70_30, 'static'),
    ],
    50: [
        ("70/30 Blend", score_blend_70_30, 'static'),
        ("SP Production", score_sp_production, 'static'),
        ("Pure WP", score_pure_wp, 'static'),
    ],
}


def run_baseline(name, scorer_fn, kind, week_data, num_entries):
    if kind == 'mixed':
        return simulate_mixed_portfolio(week_data, num_entries)
    else:
        return simulate_static(scorer_fn, week_data, num_entries)


# ─────────────────────────────────────────────────────────────────────────────
# Standard Deviation Helper
# ─────────────────────────────────────────────────────────────────────────────

def stdev(vals):
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 110)
    print("STAN: DYNAMIC STRATEGY SWITCHING SIMULATION")
    print("Validation: Does per-entry context-aware strategy selection beat best static assignment?")
    print("=" * 110)
    print()

    # Determine available seasons
    all_seasons = []
    for season in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
        games_file = "nfl_games_2020_weather.json" if season == 2020 else f"nfl_games_{season}.json"
        games_path = os.path.join(DATA_DIR_BACKTESTING, games_file)
        picks_path = os.path.join(DATA_DIR_BACKTESTING, f"survivorgrid_picks_{season}.json")
        cache_path = os.path.join(DATA_DIR_BACKTESTING, "nfl_games_2025_cache.json")

        if season == 2025:
            if os.path.exists(cache_path):
                all_seasons.append(season)
        elif os.path.exists(games_path) and os.path.exists(picks_path):
            all_seasons.append(season)

    # Primary seasons: 2023-2025
    primary_seasons = [s for s in all_seasons if s >= 2023]
    # Extended seasons: 2018-2022 if available
    extended_seasons = [s for s in all_seasons if s < 2023]

    seasons_to_run = primary_seasons if primary_seasons else all_seasons
    print(f"Available seasons: {all_seasons}")
    print(f"Primary seasons (2023-2025): {primary_seasons}")
    print(f"Extended seasons (2018-2022): {extended_seasons}")
    print()

    if not seasons_to_run:
        print("ERROR: No season data found. Check DATA_DIR path.")
        sys.exit(1)

    # Load season data
    print("Loading season data...")
    season_data = {}
    for season in all_seasons:
        sys.stdout.write(f"\r  Loading {season}...")
        sys.stdout.flush()
        try:
            season_data[season] = load_season(season)
            print(f"\r  {season}: {len(season_data[season])} weeks loaded          ")
        except Exception as e:
            print(f"\r  {season}: ERROR - {e}          ")
    print()

    # ─── Run Simulations ──────────────────────────────────────────────────────
    # For each entry count × season:
    #   - Dynamic strategy switching result
    #   - Best static baselines (top 3)

    results = {}

    total_runs = len(ENTRY_COUNTS) * len(all_seasons) * (1 + 3)  # 1 dynamic + 3 baselines
    run_num = 0

    for num_entries in ENTRY_COUNTS:
        results[num_entries] = {}
        for season in all_seasons:
            if season not in season_data:
                continue
            wdata = season_data[season]

            results[num_entries][season] = {}

            # Dynamic
            run_num += 1
            sys.stdout.write(f"\r  [{run_num:3d}/{total_runs}] Dynamic n={num_entries} {season}     ")
            sys.stdout.flush()
            dyn_result = simulate_dynamic(wdata, num_entries)
            results[num_entries][season]['dynamic'] = dyn_result

            # Static baselines
            for bname, bscorer, bkind in STATIC_BASELINES[num_entries]:
                run_num += 1
                sys.stdout.write(f"\r  [{run_num:3d}/{total_runs}] {bname[:25]} n={num_entries} {season}  ")
                sys.stdout.flush()
                br = run_baseline(bname, bscorer, bkind, wdata, num_entries)
                results[num_entries][season][bname] = br

    print(f"\r  All runs complete.{'':60}")
    print()

    # ─── Primary Analysis: 2023-2025 ─────────────────────────────────────────

    if primary_seasons:
        print("=" * 110)
        print("PRIMARY RESULTS: 2023-2025 (3 seasons)")
        print("=" * 110)
        print()

        for num_entries in ENTRY_COUNTS:
            max_possible = num_entries * 18
            print(f"┌{'─' * 108}┐")
            print(f"│ ENTRY COUNT: n={num_entries}  (max possible: {max_possible} EW/season) {'':63}│")
            print(f"├{'─' * 108}┤")

            # Collect results
            rows = []

            # Dynamic
            dyn_ews = [results[num_entries][s]['dynamic']['entry_weeks']
                       for s in primary_seasons if s in results[num_entries]]
            dyn_late = [results[num_entries][s]['dynamic']['late_survival']
                        for s in primary_seasons if s in results[num_entries]]
            dyn_total = sum(dyn_ews)
            dyn_avg = dyn_total / len(dyn_ews) if dyn_ews else 0
            dyn_sd = stdev(dyn_ews)
            dyn_late_avg = sum(dyn_late) / len(dyn_late) if dyn_late else 0
            rows.append(('*** DYNAMIC (Context-Aware) ***', dyn_ews, dyn_total, dyn_avg, dyn_sd, dyn_late_avg))

            # Baselines
            for bname, _, _ in STATIC_BASELINES[num_entries]:
                bews = [results[num_entries][s][bname]['entry_weeks']
                        for s in primary_seasons if s in results[num_entries] and bname in results[num_entries][s]]
                blate = [results[num_entries][s][bname]['late_survival']
                         for s in primary_seasons if s in results[num_entries] and bname in results[num_entries][s]]
                if not bews:
                    continue
                btotal = sum(bews)
                bavg = btotal / len(bews)
                bsd = stdev(bews)
                blate_avg = sum(blate) / len(blate) if blate else 0
                rows.append((bname, bews, btotal, bavg, bsd, blate_avg))

            # Best static baseline
            static_rows = rows[1:]
            best_static_total = max((r[2] for r in static_rows), default=0)
            best_static_name = next((r[0] for r in static_rows if r[2] == best_static_total), "N/A")

            # Print header
            seasons_header = "  ".join(f"{s}" for s in primary_seasons[:3])
            print(f"│ {'Strategy':<35} {seasons_header}   {'TOTAL':>6}  {'AVG':>6}  {'SD':>5}  {'Wk14+':>5}  {'vs.Best':>7} │")
            print(f"├{'─' * 108}┤")

            for rname, rews, rtotal, ravg, rsd, rlate in rows:
                ew_parts = "  ".join(f"{e:>6}" for e in rews[:3])
                if rtotal == dyn_total:
                    vs_best = "  ---"
                else:
                    delta = rtotal - best_static_total if 'DYNAMIC' in rname else rtotal - best_static_total
                    if 'DYNAMIC' in rname:
                        delta = rtotal - best_static_total
                        vs_str = f"{delta:+d}" if delta != 0 else "  tied"
                    else:
                        vs_str = ""
                    vs_best = vs_str if 'DYNAMIC' in rname else ""
                marker = ">>>" if 'DYNAMIC' in rname else "   "
                print(f"│ {marker} {rname:<32} {ew_parts}   {rtotal:>6}  {ravg:>6.1f}  {rsd:>5.1f}  {rlate:>5.1f}  {vs_best:>7} │")

            # Summary
            dyn_vs_best = dyn_total - best_static_total
            pct_improvement = (dyn_vs_best / best_static_total * 100) if best_static_total > 0 else 0
            validation = "✓ VALIDATED (≥5%)" if pct_improvement >= 5 else ("≈ TIES" if abs(pct_improvement) < 2 else "✗ UNDERPERFORMS")
            print(f"├{'─' * 108}┤")
            print(f"│  Best static: {best_static_name:<35} Dynamic gain: {dyn_vs_best:+d} EW  ({pct_improvement:+.1f}%)  {validation:<25} │")
            print(f"└{'─' * 108}┘")
            print()

    # ─── Extended Analysis: 2018-2022 ────────────────────────────────────────

    if extended_seasons:
        ext_seasons_available = [s for s in extended_seasons if s in season_data]
        if ext_seasons_available:
            print("=" * 110)
            print(f"EXTENDED RESULTS: {ext_seasons_available} ({len(ext_seasons_available)} seasons)")
            print("=" * 110)
            print()

            for num_entries in ENTRY_COUNTS:
                print(f"n={num_entries}:")
                dyn_ews = [results[num_entries][s]['dynamic']['entry_weeks']
                           for s in ext_seasons_available if s in results[num_entries]]
                dyn_total = sum(dyn_ews)

                for bname, _, _ in STATIC_BASELINES[num_entries]:
                    bews = [results[num_entries][s][bname]['entry_weeks']
                            for s in ext_seasons_available
                            if s in results[num_entries] and bname in results[num_entries][s]]
                    if not bews:
                        continue
                    btotal = sum(bews)
                    delta = dyn_total - btotal
                    pct = (delta / btotal * 100) if btotal > 0 else 0
                    print(f"  Dynamic={dyn_total} vs {bname}={btotal}  ({delta:+d}, {pct:+.1f}%)")
                print()

    # ─── Strategy Usage Analysis ─────────────────────────────────────────────

    print("=" * 110)
    print("STRATEGY USAGE — Which strategies does dynamic switching select most often?")
    print("=" * 110)
    print()

    for num_entries in ENTRY_COUNTS:
        combined_usage = {}
        for season in all_seasons:
            if season not in results[num_entries]:
                continue
            usage = results[num_entries][season]['dynamic'].get('strategy_usage', {})
            for strat, cnt in usage.items():
                combined_usage[strat] = combined_usage.get(strat, 0) + cnt

        total_picks = sum(combined_usage.values())
        print(f"  n={num_entries} — strategy usage distribution:")
        for strat, cnt in sorted(combined_usage.items(), key=lambda x: x[1], reverse=True):
            pct = cnt / total_picks * 100 if total_picks > 0 else 0
            print(f"    {strat:<20}: {cnt:5d} picks ({pct:5.1f}%)")
        print()

    # ─── Late Season Survival Deep Dive ──────────────────────────────────────

    print("=" * 110)
    print("LATE-SEASON SURVIVAL (Week 14+ entries still alive)")
    print("=" * 110)
    print()
    print(f"  {'Entry Count':<14} {'Dynamic':>9} {'Best Static':>12} {'Delta':>7}")
    print(f"  {'─' * 14} {'─' * 9} {'─' * 12} {'─' * 7}")

    for num_entries in ENTRY_COUNTS:
        if not primary_seasons:
            continue
        dyn_late = [results[num_entries][s]['dynamic']['late_survival']
                    for s in primary_seasons if s in results[num_entries]]
        dyn_late_avg = sum(dyn_late) / len(dyn_late) if dyn_late else 0

        best_static_late = 0
        best_static_late_name = ""
        for bname, _, _ in STATIC_BASELINES[num_entries]:
            blate = [results[num_entries][s][bname]['late_survival']
                     for s in primary_seasons
                     if s in results[num_entries] and bname in results[num_entries][s]]
            if blate:
                bavg = sum(blate) / len(blate)
                if bavg > best_static_late:
                    best_static_late = bavg
                    best_static_late_name = bname

        delta = dyn_late_avg - best_static_late
        print(f"  n={num_entries:<11} {dyn_late_avg:>9.1f}  {best_static_late:>9.1f} ({best_static_late_name[:15]:<15})  {delta:>+.1f}")
    print()

    # ─── Season-to-Season SD (Consistency) ───────────────────────────────────

    if len(primary_seasons) >= 2:
        print("=" * 110)
        print("CONSISTENCY (Season-to-Season Standard Deviation — lower is more reliable)")
        print("=" * 110)
        print()
        print(f"  {'Entry Count':<14} {'Dynamic SD':>11} {'Best Static SD':>15} {'Better?':>9}")
        print(f"  {'─' * 14} {'─' * 11} {'─' * 15} {'─' * 9}")

        for num_entries in ENTRY_COUNTS:
            dyn_ews = [results[num_entries][s]['dynamic']['entry_weeks']
                       for s in primary_seasons if s in results[num_entries]]
            dyn_sd = stdev(dyn_ews)

            best_static_sd = None
            for bname, _, _ in STATIC_BASELINES[num_entries]:
                bews = [results[num_entries][s][bname]['entry_weeks']
                        for s in primary_seasons
                        if s in results[num_entries] and bname in results[num_entries][s]]
                if bews:
                    bsd = stdev(bews)
                    if best_static_sd is None or bsd < best_static_sd:
                        best_static_sd = bsd

            if best_static_sd is not None:
                better = "Dynamic" if dyn_sd < best_static_sd else "Static"
                print(f"  n={num_entries:<11}  {dyn_sd:>9.1f}   {best_static_sd:>12.1f}   {better:>9}")
        print()

    # ─── Validation Summary ───────────────────────────────────────────────────

    print("=" * 110)
    print("VALIDATION SUMMARY — Does dynamic switching meet the ≥5% threshold?")
    print("=" * 110)
    print()

    validated_regimes = []
    for num_entries in ENTRY_COUNTS:
        if not primary_seasons:
            continue
        dyn_ews = [results[num_entries][s]['dynamic']['entry_weeks']
                   for s in primary_seasons if s in results[num_entries]]
        dyn_total = sum(dyn_ews)

        best_static_total = 0
        best_static_name = ""
        for bname, _, _ in STATIC_BASELINES[num_entries]:
            bews = [results[num_entries][s][bname]['entry_weeks']
                    for s in primary_seasons
                    if s in results[num_entries] and bname in results[num_entries][s]]
            if bews:
                btotal = sum(bews)
                if btotal > best_static_total:
                    best_static_total = btotal
                    best_static_name = bname

        if best_static_total > 0:
            delta = dyn_total - best_static_total
            pct = delta / best_static_total * 100
            if pct >= 5:
                status = "✓ VALIDATED"
                validated_regimes.append(f"n={num_entries}")
            elif abs(pct) < 2:
                status = "≈ TIES"
            else:
                status = "✗ UNDERPERFORMS"
            print(f"  n={num_entries:2d}: Dynamic={dyn_total}  Best Static={best_static_total} ({best_static_name[:25]})  "
                  f"Δ={delta:+d} ({pct:+.1f}%)  {status}")
        else:
            print(f"  n={num_entries:2d}: Insufficient data")

    print()
    if validated_regimes:
        print(f"  Framework VALIDATED at: {', '.join(validated_regimes)}")
    else:
        print("  Framework NOT validated at ≥5% threshold at any entry count.")
        print("  See analysis below for static strategy optimality findings.")

    print()
    print("=" * 110)
    print("SIMULATION COMPLETE")
    print("=" * 110)

    # ─── Save Results ─────────────────────────────────────────────────────────
    serializable = {}
    for n in ENTRY_COUNTS:
        serializable[str(n)] = {}
        for season in all_seasons:
            if season not in results[n]:
                continue
            serializable[str(n)][str(season)] = {}
            for key, val in results[n][season].items():
                if isinstance(val, dict):
                    # Convert sets/non-serializable to serializable
                    safe_val = {}
                    for k2, v2 in val.items():
                        if isinstance(v2, (int, float, str, list)):
                            safe_val[k2] = v2
                        else:
                            safe_val[k2] = str(v2)
                    serializable[str(n)][str(season)][key] = safe_val
                else:
                    serializable[str(n)][str(season)][key] = val

    with open(RESULTS_PATH, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nRaw results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
