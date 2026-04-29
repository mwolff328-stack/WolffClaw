#!/usr/bin/env python3
"""
Stan the Scout: Simulation 3 — Per-Entry Week-of-Death with Inventory State Tracking

Research Question: Do entries die from bad luck (high-WP pick that lost) or inventory
depletion (forced into low-WP pick because good teams are exhausted)?

This separates the two causes of elimination to sharpen Entry Personalizer logic.

Death Classification:
  "Bad luck"      — WP >= 0.60 at death (reasonable pick, unlucky outcome)
  "Moderate risk" — WP 0.50–0.60 at death (gray zone)
  "Forced low-WP" — WP < 0.50 at death (inventory depleted, no good options)

Also tracks:
  - A-tier inventory at time of death (teams with future WP >= 0.75 remaining)
  - Whether the fatal pick was the best available option
  - Inventory trajectory (A-tier count by week per strategy)
"""

import json
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]
A_TIER_WP = 0.75   # teams with future WP >= this are "A-tier"
B_TIER_WP = 0.60   # B-tier: 0.60–0.74
# C-tier: < 0.60

# Death classification thresholds
BAD_LUCK_WP   = 0.60   # WP >= this → bad luck
MODERATE_WP   = 0.50   # WP 0.50–0.60 → moderate risk
# WP < 0.50 → forced low-WP

RESULTS_PATH = os.path.expanduser(
    "~/.openclaw/workspace/scripts/stan-inventory-death-results.json"
)

# ─────────────────────────────────────────────────────────────────────────────
# Data Loading (inherited from stan-dynamic-strategy-sim.py pattern)
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
    total_wks = season_weeks(season)

    if season == 2025:
        cache_path = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
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

    games_path = os.path.join(DATA_DIR, games_file)
    picks_path = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")

    with open(games_path) as f:
        raw_games = json.load(f)
    with open(picks_path) as f:
        picks_data = json.load(f)

    pick_by_week = _parse_picks(picks_data)

    result = {}
    for week in range(1, total_wks + 1):
        week_games = [g for g in raw_games if g.get('week') == week]
        week_picks = pick_by_week.get(week, {})
        teams = _build_teams_from_games(week_games, week_picks)
        if teams:
            result[week] = teams
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Inventory Counting
# ─────────────────────────────────────────────────────────────────────────────

def count_tier_teams(used_set, current_week, all_week_data, min_wp, max_wp=1.1, total_weeks=TOTAL_WEEKS):
    """Count unique available teams in a WP tier (future games from current_week onward)."""
    seen = set()
    count = 0
    for week in range(current_week, total_weeks + 1):
        for t in all_week_data.get(week, []):
            tid = t['teamId']
            if tid not in used_set and tid not in seen:
                wp = t['winProbability']
                if min_wp <= wp < max_wp:
                    seen.add(tid)
                    count += 1
    return count


def get_inventory(used_set, current_week, all_week_data, total_weeks=TOTAL_WEEKS):
    """Return dict with a_tier, b_tier, c_tier counts."""
    a = count_tier_teams(used_set, current_week, all_week_data, A_TIER_WP, 1.1, total_weeks)
    b = count_tier_teams(used_set, current_week, all_week_data, B_TIER_WP, A_TIER_WP, total_weeks)
    c = count_tier_teams(used_set, current_week, all_week_data, 0.0, B_TIER_WP, total_weeks)
    return {'a_tier': a, 'b_tier': b, 'c_tier': c}


# ─────────────────────────────────────────────────────────────────────────────
# Scoring Functions
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


def score_pure_wp(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    return team['winProbability']


def score_blend_70_30(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    return 0.70 * team['winProbability'] + 0.30 * (1 - team['pickShare'] / 100)


def score_sp_production(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    wp = team['winProbability']
    ps = team['pickShare']
    ev = wp - (ps / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], current_week, all_week_data, 5, total_weeks)
    future_utility = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * future_utility


def score_sp_conservative(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
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
    return team['winProbability'] - (team['pickShare'] / 100)


def score_contrarian(team, all_teams, all_week_data, current_week, total_weeks=TOTAL_WEEKS):
    return 0.40 * team['winProbability'] + 0.60 * (1 - team['pickShare'] / 100)


def score_adaptive_blend(week, total_weeks=TOTAL_WEEKS):
    """
    Adaptive Blend 90/10→50/50:
    Early weeks: 90% WP + 10% contrarian
    Late weeks:  50% WP + 50% contrarian
    Linearly interpolated between week 1 and total_weeks.
    """
    progress = (week - 1) / max(total_weeks - 1, 1)  # 0.0 to 1.0
    wp_weight = 0.90 - 0.40 * progress    # 0.90 → 0.50
    ct_weight = 0.10 + 0.40 * progress    # 0.10 → 0.50

    def scorer(team, all_teams, all_week_data, current_week, total_weeks_inner=TOTAL_WEEKS):
        return wp_weight * team['winProbability'] + ct_weight * (1 - team['pickShare'] / 100)

    return scorer


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Strategy Logic (from sim 1)
# ─────────────────────────────────────────────────────────────────────────────

def get_week_phase(week):
    if week <= 7:
        return 'early'
    elif week <= 14:
        return 'mid'
    return 'late'


def select_dynamic_strategy(n, week, a_tier_count, role):
    phase = get_week_phase(week)
    if a_tier_count <= 1:
        return 'pure_wp'
    elif a_tier_count <= 3:
        if phase == 'late':
            return 'pure_wp'
        return 'blend_70_30'

    if n <= 5:
        if phase == 'early':
            return 'blend_70_30'
        elif phase == 'mid':
            return 'sp_conservative'
        return 'pure_wp'
    elif n <= 15:
        if phase == 'early':
            if role == 'swing':
                return 'contrarian'
            elif role == 'satellite':
                return 'ev_pure'
            return 'blend_70_30'
        elif phase == 'mid':
            if role == 'swing':
                return 'ev_pure'
            return 'sp_production'
        return 'blend_70_30'
    elif n <= 30:
        role_strategies = {'core': 'blend_70_30', 'satellite': 'sp_production', 'swing': 'ev_pure'}
        if phase == 'late':
            return 'pure_wp'
        return role_strategies.get(role, 'blend_70_30')
    else:
        if phase == 'late':
            return 'pure_wp'
        return 'blend_70_30'


SCORER_MAP = {
    'pure_wp':        score_pure_wp,
    'blend_70_30':    score_blend_70_30,
    'sp_production':  score_sp_production,
    'sp_conservative': score_sp_conservative,
    'ev_pure':        score_ev_pure,
    'contrarian':     score_contrarian,
}


def assign_roles(num_entries):
    n_swing = max(1, round(num_entries * 0.10))
    n_satellite = max(1, round(num_entries * 0.30))
    n_core = num_entries - n_swing - n_satellite
    return (['core'] * n_core + ['satellite'] * n_satellite + ['swing'] * n_swing)[:num_entries]


# ─────────────────────────────────────────────────────────────────────────────
# Death Classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_death(wp, was_best_available):
    """
    Classify the cause of death:
    - bad_luck: WP >= 0.60 (reasonable pick, unlucky)
    - moderate: 0.50 <= WP < 0.60 (gray zone)
    - forced_low_wp: WP < 0.50 (no good options left)
    """
    if wp >= BAD_LUCK_WP:
        return 'bad_luck'
    elif wp >= MODERATE_WP:
        return 'moderate'
    return 'forced_low_wp'


# ─────────────────────────────────────────────────────────────────────────────
# Core Simulation Engine with Inventory Tracking
# ─────────────────────────────────────────────────────────────────────────────

def simulate_with_inventory_tracking(strategy_name, scorer_fn_factory, week_data, num_entries,
                                      is_core_satellite=False, is_mixed=False, is_dynamic=False):
    """
    Simulate a season with per-entry, per-week inventory and death tracking.

    Returns:
      deaths: list of death records (one per eliminated entry)
      inventory_by_week: dict {week: [a_tier_count_per_alive_entry]}
      weekly_survivor_count: list of alive count per week
      entry_weeks: total entry-weeks survived
    """
    total_weeks = max(week_data.keys()) if week_data else TOTAL_WEEKS

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0

    deaths = []  # list of death records
    # inventory_by_week[week] = list of a_tier counts from alive entries BEFORE pick
    inventory_by_week = {w: [] for w in range(1, total_weeks + 1)}
    weekly_survivor_count = []

    # For role-based strategies
    roles = assign_roles(num_entries)
    # For mixed portfolio: cycle scorers
    base_scorers_list = [score_blend_70_30, score_sp_production, score_pure_wp,
                         score_sp_conservative, score_ev_pure]
    entry_scorers_mixed = [base_scorers_list[i % len(base_scorers_list)] for i in range(num_entries)]

    for week in range(1, total_weeks + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            weekly_survivor_count.append(len(alive))
            continue

        assigned = set()  # teams already assigned this week
        picks = {}        # entry_id → chosen team dict

        for i in sorted(alive):
            # ─── Inventory snapshot BEFORE pick ─────────────────────────────
            inv = get_inventory(used_teams[i], week, week_data, total_weeks)
            a_tier = inv['a_tier']
            inventory_by_week[week].append(a_tier)

            # ─── Determine scorer ────────────────────────────────────────────
            if is_dynamic:
                role = roles[i] if i < len(roles) else 'core'
                strat_name = select_dynamic_strategy(num_entries, week, a_tier, role)
                scorer = SCORER_MAP[strat_name]
            elif is_mixed:
                scorer = entry_scorers_mixed[i]
                role = roles[i] if i < len(roles) else 'core'
            elif is_core_satellite:
                role = roles[i] if i < len(roles) else 'core'
                scorer = scorer_fn_factory  # base scorer for core/satellite
            else:
                scorer = scorer_fn_factory  # static scorer
                role = 'core'

            # ─── Adaptive blend scorer (week-aware) ─────────────────────────
            if strategy_name == 'Adaptive Blend 90/10→50/50':
                scorer = score_adaptive_blend(week, total_weeks)

            # ─── Build available teams ───────────────────────────────────────
            available = [t for t in teams
                         if t['teamId'] not in assigned
                         and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            # ─── Score and rank ──────────────────────────────────────────────
            scored = sorted(
                [(scorer(t, teams, week_data, week, total_weeks), t) for t in available],
                key=lambda x: x[0],
                reverse=True
            )

            # ─── Pick selection based on role ────────────────────────────────
            if is_core_satellite or is_dynamic:
                if role == 'satellite' and len(scored) >= 2:
                    pick_rank = 1  # 0-indexed 2nd best
                    pick = scored[1][1]
                elif role == 'swing' and len(scored) >= 3:
                    pick_rank = 2
                    pick = scored[2][1]
                else:
                    pick_rank = 0
                    pick = scored[0][1]
            else:
                pick_rank = 0
                pick = scored[0][1]

            assigned.add(pick['teamId'])
            used_teams[i].add(pick['teamId'])
            picks[i] = {
                'team': pick,
                'a_tier_before': a_tier,
                'b_tier_before': inv['b_tier'],
                'c_tier_before': inv['c_tier'],
                'pick_rank': pick_rank,       # 0 = best available, 1 = 2nd, etc.
                'was_best_available': (pick_rank == 0),
            }

        # ─── Resolve outcomes ────────────────────────────────────────────────
        newly_dead = []
        for i in sorted(alive):
            p = picks.get(i)
            if p:
                pick_wp = p['team']['winProbability']
                if p['team']['outcome'] == 'Loss':
                    newly_dead.append((i, p, week, pick_wp))
                else:
                    entry_weeks += 1

        for (i, p, wk, pick_wp) in newly_dead:
            alive.discard(i)
            cause = classify_death(pick_wp, p['was_best_available'])
            deaths.append({
                'entry_id': i,
                'week': wk,
                'pick_wp': round(pick_wp, 4),
                'a_tier_before': p['a_tier_before'],
                'b_tier_before': p['b_tier_before'],
                'c_tier_before': p['c_tier_before'],
                'pick_rank': p['pick_rank'],
                'was_best_available': p['was_best_available'],
                'cause': cause,
            })

        weekly_survivor_count.append(len(alive))

    return {
        'deaths': deaths,
        'inventory_by_week': inventory_by_week,
        'weekly_survivor_count': weekly_survivor_count,
        'entry_weeks': entry_weeks,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Strategy Registry
# ─────────────────────────────────────────────────────────────────────────────

STRATEGIES = [
    {
        'name': '70/30 Blend',
        'scorer': score_blend_70_30,
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': False,
    },
    {
        'name': 'Pure WP',
        'scorer': score_pure_wp,
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': False,
    },
    {
        'name': 'SP Production 70%EV+30%FV',
        'scorer': score_sp_production,
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': False,
    },
    {
        'name': 'SP Conservative 65%EV/25%FV/10%Lev',
        'scorer': score_sp_conservative,
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': False,
    },
    {
        'name': 'Core/Satellite',
        'scorer': score_blend_70_30,  # base scorer; role differentiation applied
        'is_core_satellite': True,
        'is_mixed': False,
        'is_dynamic': False,
    },
    {
        'name': 'Mixed Portfolio',
        'scorer': None,
        'is_core_satellite': False,
        'is_mixed': True,
        'is_dynamic': False,
    },
    {
        'name': 'Dynamic Strategy Switching',
        'scorer': None,
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': True,
    },
    {
        'name': 'Adaptive Blend 90/10→50/50',
        'scorer': score_blend_70_30,  # placeholder; week-aware scorer applied in sim
        'is_core_satellite': False,
        'is_mixed': False,
        'is_dynamic': False,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Aggregation Helpers
# ─────────────────────────────────────────────────────────────────────────────

def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def stdev(vals):
    if len(vals) < 2:
        return 0.0
    avg = mean(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


def aggregate_deaths(deaths_list):
    """deaths_list: list of death records across all seasons/runs."""
    if not deaths_list:
        return {
            'total': 0,
            'bad_luck_pct': 0.0,
            'moderate_pct': 0.0,
            'forced_low_wp_pct': 0.0,
            'avg_a_tier_at_death': 0.0,
            'avg_wp_fatal_pick': 0.0,
            'pct_best_available': 0.0,
            'week_of_death_dist': {},
        }
    total = len(deaths_list)
    bad_luck = sum(1 for d in deaths_list if d['cause'] == 'bad_luck')
    moderate = sum(1 for d in deaths_list if d['cause'] == 'moderate')
    forced = sum(1 for d in deaths_list if d['cause'] == 'forced_low_wp')

    avg_a_tier = mean([d['a_tier_before'] for d in deaths_list])
    avg_wp = mean([d['pick_wp'] for d in deaths_list])
    pct_best = sum(1 for d in deaths_list if d['was_best_available']) / total * 100

    week_dist = {}
    for d in deaths_list:
        w = d['week']
        week_dist[w] = week_dist.get(w, 0) + 1

    return {
        'total': total,
        'bad_luck_pct': round(bad_luck / total * 100, 1),
        'moderate_pct': round(moderate / total * 100, 1),
        'forced_low_wp_pct': round(forced / total * 100, 1),
        'avg_a_tier_at_death': round(avg_a_tier, 2),
        'avg_wp_fatal_pick': round(avg_wp, 4),
        'pct_best_available': round(pct_best, 1),
        'week_of_death_dist': week_dist,
    }


def aggregate_inventory_curves(inv_by_week_list, total_weeks=18):
    """
    inv_by_week_list: list of inventory_by_week dicts (one per season run).
    Returns avg A-tier count by week.
    """
    curve = {}
    for week in range(1, total_weeks + 1):
        all_counts = []
        for inv_dict in inv_by_week_list:
            counts = inv_dict.get(week, [])
            all_counts.extend(counts)
        curve[week] = round(mean(all_counts), 2) if all_counts else 0.0
    return curve


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 120)
    print("STAN: SIMULATION 3 — PER-ENTRY WEEK-OF-DEATH WITH INVENTORY STATE TRACKING")
    print("Research Question: Do entries die from bad luck or inventory depletion?")
    print("=" * 120)
    print()

    # Discover available seasons
    all_seasons = []
    for season in [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
        if season == 2025:
            p = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
        elif season == 2020:
            p = os.path.join(DATA_DIR, "nfl_games_2020_weather.json")
        else:
            p = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
        p2 = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json") if season != 2025 else p
        if os.path.exists(p) and (season == 2025 or os.path.exists(p2)):
            all_seasons.append(season)

    primary_seasons = [s for s in all_seasons if s >= 2023]
    extended_seasons = [s for s in all_seasons if s < 2023]

    print(f"Available seasons:  {all_seasons}")
    print(f"Primary (2023+):    {primary_seasons}")
    print(f"Extended (2018-22): {extended_seasons}")
    print()

    if not all_seasons:
        print("ERROR: No season data found.")
        sys.exit(1)

    # Load data
    print("Loading season data...")
    season_data = {}
    for season in all_seasons:
        try:
            season_data[season] = load_season(season)
            print(f"  {season}: {len(season_data[season])} weeks")
        except Exception as e:
            print(f"  {season}: ERROR — {e}")
    print()

    # ─── Run all simulations ──────────────────────────────────────────────────
    # Structure: results[num_entries][strategy_name] = {
    #   'deaths_agg': aggregate_deaths(),
    #   'inventory_curve': {week: avg_a_tier},
    #   'entry_weeks': total,
    #   'per_season': {season: {...}},
    # }

    all_results = {}

    total_runs = len(ENTRY_COUNTS) * len(STRATEGIES) * len(all_seasons)
    run_num = 0

    for num_entries in ENTRY_COUNTS:
        all_results[num_entries] = {}
        for strat in STRATEGIES:
            sname = strat['name']
            all_results[num_entries][sname] = {
                'deaths': [],          # accumulated deaths across all seasons
                'inv_curves': [],      # list of inventory_by_week dicts
                'entry_weeks': 0,
                'per_season': {},
            }

            for season in all_seasons:
                if season not in season_data:
                    continue
                run_num += 1
                sys.stdout.write(
                    f"\r  [{run_num:3d}/{total_runs}] n={num_entries:2d} | {sname:<40} | {season}  "
                )
                sys.stdout.flush()

                wdata = season_data[season]
                sim_result = simulate_with_inventory_tracking(
                    strategy_name=sname,
                    scorer_fn_factory=strat['scorer'],
                    week_data=wdata,
                    num_entries=num_entries,
                    is_core_satellite=strat['is_core_satellite'],
                    is_mixed=strat['is_mixed'],
                    is_dynamic=strat['is_dynamic'],
                )

                all_results[num_entries][sname]['deaths'].extend(sim_result['deaths'])
                all_results[num_entries][sname]['inv_curves'].append(sim_result['inventory_by_week'])
                all_results[num_entries][sname]['entry_weeks'] += sim_result['entry_weeks']
                all_results[num_entries][sname]['per_season'][season] = {
                    'entry_weeks': sim_result['entry_weeks'],
                    'deaths_agg': aggregate_deaths(sim_result['deaths']),
                }

    print(f"\r  All {total_runs} simulation runs complete.{' ':60}")
    print()

    # ─── Aggregate across seasons ────────────────────────────────────────────
    for num_entries in ENTRY_COUNTS:
        for strat in STRATEGIES:
            sname = strat['name']
            r = all_results[num_entries][sname]
            r['deaths_agg'] = aggregate_deaths(r['deaths'])
            total_weeks = max((max(inv.keys()) for inv in r['inv_curves'] if inv), default=18)
            r['inventory_curve'] = aggregate_inventory_curves(r['inv_curves'], total_weeks)

    # ─── Print Results ────────────────────────────────────────────────────────

    for num_entries in ENTRY_COUNTS:
        print("=" * 120)
        print(f"RESULTS FOR n={num_entries} ENTRIES")
        print("=" * 120)

        # Table 1: Death Cause Breakdown
        print()
        print(f"  {'Strategy':<42}  {'Total Deaths':>12}  {'Bad Luck%':>9}  {'Moderate%':>9}  {'ForcedLowWP%':>12}  {'Avg A@Death':>11}  {'Avg WP Fatal':>12}  {'% Best Pick':>11}")
        print(f"  {'-'*42}  {'-'*12}  {'-'*9}  {'-'*9}  {'-'*12}  {'-'*11}  {'-'*12}  {'-'*11}")
        for strat in STRATEGIES:
            sname = strat['name']
            agg = all_results[num_entries][sname]['deaths_agg']
            ew = all_results[num_entries][sname]['entry_weeks']
            print(
                f"  {sname:<42}  {agg['total']:>12}  "
                f"{agg['bad_luck_pct']:>8.1f}%  {agg['moderate_pct']:>8.1f}%  "
                f"{agg['forced_low_wp_pct']:>11.1f}%  "
                f"{agg['avg_a_tier_at_death']:>11.2f}  {agg['avg_wp_fatal_pick']:>12.4f}  "
                f"{agg['pct_best_available']:>10.1f}%"
            )

        # Table 2: Inventory Depletion Curves (A-tier by week)
        print()
        print(f"  INVENTORY DEPLETION CURVES: avg A-tier teams remaining (WP >= 0.75) per week")
        total_weeks_avail = max((max(all_results[num_entries][s]['inventory_curve'].keys(), default=0)
                                 for s in all_results[num_entries]), default=18)
        week_header = "".join(f"  W{w:02d}" for w in range(1, min(total_weeks_avail + 1, 19)))
        print(f"  {'Strategy':<42}{week_header}")
        print(f"  {'-'*42}" + "".join("  ----" for _ in range(min(total_weeks_avail, 18))))
        for strat in STRATEGIES:
            sname = strat['name']
            curve = all_results[num_entries][sname]['inventory_curve']
            values = "".join(f"  {curve.get(w, 0.0):>4.1f}" for w in range(1, min(total_weeks_avail + 1, 19)))
            print(f"  {sname:<42}{values}")

        # Table 3: Week-of-Death Heatmap by Cause
        print()
        print(f"  WEEK-OF-DEATH HEATMAP (total deaths per week, across all seasons)")
        weeks_with_deaths = set()
        for strat in STRATEGIES:
            sname = strat['name']
            for d in all_results[num_entries][sname]['deaths']:
                weeks_with_deaths.add(d['week'])
        sorted_weeks = sorted(weeks_with_deaths)
        wk_header = "".join(f"  W{w:02d}" for w in sorted_weeks)
        print(f"  {'Strategy':<42}{wk_header}")
        print(f"  {'-'*42}" + "".join("  ----" for _ in sorted_weeks))
        for strat in STRATEGIES:
            sname = strat['name']
            wod = all_results[num_entries][sname]['deaths_agg']['week_of_death_dist']
            row = "".join(f"  {wod.get(w, 0):>4d}" for w in sorted_weeks)
            print(f"  {sname:<42}{row}")

        print()

    # ─── Key Findings ─────────────────────────────────────────────────────────

    print("=" * 120)
    print("KEY FINDINGS: Inventory Depletion vs. Bad Luck")
    print("=" * 120)
    print()

    for num_entries in ENTRY_COUNTS:
        print(f"  n={num_entries}:")
        # Compare Pure WP vs SP Conservative forced_low_wp rates
        pure_wp_agg = all_results[num_entries]['Pure WP']['deaths_agg']
        sp_cons_agg = all_results[num_entries]['SP Conservative 65%EV/25%FV/10%Lev']['deaths_agg']
        sp_prod_agg = all_results[num_entries]['SP Production 70%EV+30%FV']['deaths_agg']
        blend_agg   = all_results[num_entries]['70/30 Blend']['deaths_agg']
        dyn_agg     = all_results[num_entries]['Dynamic Strategy Switching']['deaths_agg']

        print(f"    Pure WP forced-low-WP deaths:      {pure_wp_agg['forced_low_wp_pct']:>5.1f}%  (bad luck: {pure_wp_agg['bad_luck_pct']:.1f}%)")
        print(f"    SP Conservative forced-low-WP:     {sp_cons_agg['forced_low_wp_pct']:>5.1f}%  (bad luck: {sp_cons_agg['bad_luck_pct']:.1f}%)")
        print(f"    SP Production forced-low-WP:       {sp_prod_agg['forced_low_wp_pct']:>5.1f}%  (bad luck: {sp_prod_agg['bad_luck_pct']:.1f}%)")
        print(f"    70/30 Blend forced-low-WP:         {blend_agg['forced_low_wp_pct']:>5.1f}%  (bad luck: {blend_agg['bad_luck_pct']:.1f}%)")
        print(f"    Dynamic Switching forced-low-WP:   {dyn_agg['forced_low_wp_pct']:>5.1f}%  (bad luck: {dyn_agg['bad_luck_pct']:.1f}%)")

        # Detect A-tier cliff: find week where avg A-tier drops below 2 for Pure WP
        pw_curve = all_results[num_entries]['Pure WP']['inventory_curve']
        cliff_week = next((w for w in range(1, 19) if pw_curve.get(w, 99) < 2.0), None)
        sc_curve = all_results[num_entries]['SP Conservative 65%EV/25%FV/10%Lev']['inventory_curve']
        cliff_week_sc = next((w for w in range(1, 19) if sc_curve.get(w, 99) < 2.0), None)

        print(f"    Pure WP A-tier depletes below 2.0 at week: {cliff_week or 'never'}")
        print(f"    SP Conservative A-tier < 2.0 at week:      {cliff_week_sc or 'never'}")

        # Suggest inventory warning threshold
        # Find week where forced_low_wp rate spikes: if we had per-week cause data
        # (use avg a_tier at death as proxy)
        avg_a_death_pw = pure_wp_agg['avg_a_tier_at_death']
        print(f"    Suggested Personalizer trigger: warn when A-tier <= {max(1, round(avg_a_death_pw))}")
        print()

    # ─── Product Implications ─────────────────────────────────────────────────
    print("=" * 120)
    print("PRODUCT IMPLICATIONS")
    print("=" * 120)
    print()

    # Overall average forced_low_wp across all strategies and n
    all_forced = []
    all_bad_luck = []
    for num_entries in ENTRY_COUNTS:
        for strat in STRATEGIES:
            sname = strat['name']
            agg = all_results[num_entries][sname]['deaths_agg']
            if agg['total'] > 0:
                all_forced.append(agg['forced_low_wp_pct'])
                all_bad_luck.append(agg['bad_luck_pct'])

    avg_forced = mean(all_forced)
    avg_bad_luck = mean(all_bad_luck)

    print(f"  Overall avg forced-low-WP deaths:  {avg_forced:.1f}%")
    print(f"  Overall avg bad-luck deaths:        {avg_bad_luck:.1f}%")
    print()

    if avg_forced > 25:
        print("  ⚠️  High inventory depletion mortality (>25%): Entry Personalizer is CRITICAL.")
        print("      Future-value preserving strategies (SP Conservative/Production) meaningfully")
        print("      reduce forced eliminations — a strong product differentiator.")
    elif avg_forced > 10:
        print("  ⚠️  Moderate inventory depletion mortality (10–25%): Entry Personalizer adds value.")
        print("      SP Conservative/Production reduce forced eliminations but bad luck dominates.")
    else:
        print("  ✓  Low inventory depletion mortality (<10%): Bad luck is the primary cause.")
        print("      Inventory management is helpful at margins but not critical for survival.")

    print()
    print("  Inventory Health Indicator recommendation:")
    # Find median avg_a_tier at death across all Pure WP scenarios (high stress)
    thresholds = []
    for num_entries in ENTRY_COUNTS:
        agg = all_results[num_entries]['Pure WP']['deaths_agg']
        if agg['total'] > 0:
            thresholds.append(agg['avg_a_tier_at_death'])
    med_threshold = sorted(thresholds)[len(thresholds)//2] if thresholds else 2.0
    print(f"    - Show 'inventory health' indicator when A-tier count <= {max(2, round(med_threshold + 1))}")
    print(f"    - Show 'danger zone' warning when A-tier count <= {max(1, round(med_threshold))}")
    print(f"    - Typical avg A-tier at death: {med_threshold:.1f} teams")
    print()

    # ─── Save Results to JSON ─────────────────────────────────────────────────
    print(f"Saving results to {RESULTS_PATH}...")

    save_data = {}
    for num_entries in ENTRY_COUNTS:
        save_data[str(num_entries)] = {}
        for strat in STRATEGIES:
            sname = strat['name']
            r = all_results[num_entries][sname]
            save_data[str(num_entries)][sname] = {
                'deaths_agg': r['deaths_agg'],
                'inventory_curve': {str(k): v for k, v in r['inventory_curve'].items()},
                'entry_weeks': r['entry_weeks'],
                'per_season': {
                    str(s): {
                        'entry_weeks': v['entry_weeks'],
                        'deaths_agg': v['deaths_agg'],
                    }
                    for s, v in r['per_season'].items()
                },
            }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"  ✓ Results saved.")
    print()
    print("Simulation 3 complete.")


if __name__ == '__main__':
    main()
