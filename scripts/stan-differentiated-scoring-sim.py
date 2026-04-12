#!/usr/bin/env python3
"""
Stan the Scout: Per-Entry Differentiated Scoring Simulation (Round 7)

12 strategies × 4 entry counts (5, 10, 20, 50) × 3 seasons (2023, 2024, 2025) = 144 runs.

Research question: Does intentional role assignment beat random strategy diversity
(Mixed Portfolio, the Round 6 winner at n=20)?

Baselines (from Round 6):
  1. 70/30 Blend
  2. Mixed Portfolio (random strategy cycling)

New intentional portfolio configs:
  3.  Safety/Contrarian Split
  4.  Core/Satellite
  5.  Temporal Diversification
  6.  Role-Based Portfolio (5 roles)
  7.  Adaptive Role Portfolio (role weights shift by phase)
  8.  Anti-Overlap Portfolio (global greedy, hard uniqueness constraint)
  9.  Correlated Pairs + Hedges
  10. Ownership-Bucket Spread
  11. EV Gradient
  12. Dynamic Rebalancing
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
SEASONS = [2023, 2024, 2025]


# ── Data Loading (identical to Round 6) ──────────────────────────────────────

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


# ── Scoring Primitives ────────────────────────────────────────────────────────

def blend_score(team, wp_w, ps_w):
    """Linear blend of win probability and anti-chalk."""
    return (wp_w / 100) * team['winProbability'] + (ps_w / 100) * (1 - team['pickShare'] / 100)


def compute_expendability(team_id, current_week, all_week_data, lookahead=5):
    """HIGH expendability = low future value = safe to use now. Returns 0-1."""
    max_future_score = 0.0
    for offset in range(1, lookahead + 1):
        fw = current_week + offset
        if fw > TOTAL_WEEKS:
            break
        ft = next((t for t in all_week_data.get(fw, []) if t['teamId'] == team_id), None)
        if not ft:
            continue
        fs = 0.7 * ft['winProbability'] + 0.3 * (1 - ft['pickShare'] / 100)
        decay = 0.5 ** (offset - 1)
        max_future_score = max(max_future_score, fs * decay)
    return max(0.0, min(1.0, 1.0 - max_future_score))


def sp_production_score(team, all_week_data, week, lookahead=5):
    """SP Production: 70% EV (normalized) + 30% FV."""
    ev = team['winProbability'] - (team['pickShare'] / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
    fv = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * fv


def fv_preserver_score(team, all_week_data, week, wp_w=60, ps_w=10, fv_w=30, lookahead=5):
    """60/10/30 WP/ownership/FV — uses high-FV teams now, saves optionality."""
    base = blend_score(team, wp_w, ps_w)
    exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
    fv = 1.0 - exp
    return base + (fv_w / 100) * fv


# ── Scorer Factories ──────────────────────────────────────────────────────────

def make_blend_scorer(wp_w=70, ps_w=30):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return blend_score(team, wp_w, ps_w)
    return scorer


def make_pure_wp_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return team['winProbability']
    return scorer


def make_sp_production_scorer(lookahead=5):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return sp_production_score(team, all_week_data, week, lookahead)
    return scorer


def make_fv_preserver_scorer(wp_w=60, ps_w=10, fv_w=30, lookahead=5):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return fv_preserver_score(team, all_week_data, week, wp_w, ps_w, fv_w, lookahead)
    return scorer


# ── Portfolio Builder Helpers ─────────────────────────────────────────────────

_FIVE_BASE_SCORERS = [
    make_blend_scorer(70, 30),
    make_sp_production_scorer(),
    make_fv_preserver_scorer(65, 25, 10, 3),
    make_fv_preserver_scorer(70, 20, 10, 5),
    make_pure_wp_scorer(),
]

_ROLE_SCORERS = [
    make_blend_scorer(90, 10),        # Safety anchor
    make_blend_scorer(70, 30),        # Blend optimizer
    make_blend_scorer(50, 50),        # Contrarian hunter
    make_fv_preserver_scorer(),       # Future value preserver (60/10/30)
    make_sp_production_scorer(),      # EV maximizer
]

_ROLE_NAMES = ['safety', 'blend', 'contrarian', 'fv', 'ev']

_ROLE_SCORER_MAP = dict(zip(_ROLE_NAMES, _ROLE_SCORERS))


def make_mixed_scorers(num_entries):
    """Cycle through 5 base strategies — same as Round 6."""
    return [_FIVE_BASE_SCORERS[i % 5] for i in range(num_entries)]


def make_safety_contrarian_scorers(num_entries):
    """Half high-safety (85/15), half high-contrarian (55/45)."""
    n_safe = num_entries // 2
    n_cont = num_entries - n_safe
    return [make_blend_scorer(85, 15)] * n_safe + [make_blend_scorer(55, 45)] * n_cont


def make_core_satellite_scorers(num_entries):
    """60% core (70/30), 40% satellite (SP Production EV)."""
    n_core = round(num_entries * 0.6)
    n_sat = num_entries - n_core
    return [make_blend_scorer(70, 30)] * n_core + [make_sp_production_scorer()] * n_sat


def make_temporal_scorers(num_entries):
    """1/3 pure WP, 1/3 70/30 blend, 1/3 heavy FV (60/10/30 5wk)."""
    n_wp = num_entries // 3
    n_bl = num_entries // 3
    n_fv = num_entries - n_wp - n_bl
    return (
        [make_pure_wp_scorer()] * n_wp
        + [make_blend_scorer(70, 30)] * n_bl
        + [make_fv_preserver_scorer(60, 10, 30, 5)] * n_fv
    )


def make_role_based_scorers(num_entries):
    """5 roles distributed proportionally: safety, blend, contrarian, fv, ev."""
    per_role = max(1, num_entries // 5)
    scorers = []
    for s in _ROLE_SCORERS:
        scorers.extend([s] * per_role)
    # Fill remainder with blend
    while len(scorers) < num_entries:
        scorers.append(make_blend_scorer(70, 30))
    return scorers[:num_entries]


def make_ev_gradient_scorers(num_entries):
    """5-level gradient from 95/5 to 55/45. Entry count / 5 entries per level."""
    gradient = [(95, 5), (85, 15), (75, 25), (65, 35), (55, 45)]
    per_level = max(1, num_entries // 5)
    scorers = []
    for wp_w, ps_w in gradient:
        scorers.extend([make_blend_scorer(wp_w, ps_w)] * per_level)
    # Fill remainder with the middle level (75/25)
    while len(scorers) < num_entries:
        scorers.append(make_blend_scorer(75, 25))
    return scorers[:num_entries]


def _assign_roles_by_distribution(num_entries, distribution):
    """
    Given a distribution dict {role: fraction}, return a list of role keys
    of length num_entries. Last role absorbs rounding remainder.
    """
    roles = list(distribution.keys())
    counts = {}
    remaining = num_entries
    for i, role in enumerate(roles[:-1]):
        n = round(num_entries * distribution[role])
        counts[role] = n
        remaining -= n
    counts[roles[-1]] = remaining

    role_list = []
    for role in roles:
        role_list.extend([role] * max(0, counts[role]))
    # Safety pad
    while len(role_list) < num_entries:
        role_list.append('blend')
    return role_list[:num_entries]


# ── Standard Simulation Engine ────────────────────────────────────────────────

def simulate(scorer_or_list, week_data, num_entries):
    """
    Sequential greedy: entries pick in order, no duplicate teams per week.
    Falls back to duplicates when entries > unique teams available.
    scorer_or_list: single callable or list of callables (one per entry).
    """
    if callable(scorer_or_list):
        scorers = [scorer_or_list] * num_entries
    else:
        scorers = list(scorer_or_list)
        while len(scorers) < num_entries:
            scorers.append(scorers[len(scorers) % len(scorers)])

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned = set()
        picks = {}

        for i in sorted(alive):
            scorer = scorers[i]
            available = [t for t in teams
                         if t['teamId'] not in assigned and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            scored = [(scorer(t, teams, week_data, available, week, i, used_teams), t)
                      for t in available]
            scored.sort(key=lambda x: x[0], reverse=True)
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

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Custom Simulation: Anti-Overlap (Global Greedy) ──────────────────────────

def simulate_anti_overlap(week_data, num_entries):
    """
    Strategy 8: Anti-Overlap Portfolio.
    Each entry uses 70/30 blend. Assignment uses global greedy to maximize
    unique teams across all entries each week (hard uniqueness constraint).
    Unlike sequential greedy where entry order determines who gets best picks,
    global greedy gives the highest-value (entry, team) pairs regardless of ordering.
    """
    scorer = make_blend_scorer(70, 30)

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        alive_list = sorted(alive)

        # Build all (score, entry, teamId, team) pairs for unique picks
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

        # Global greedy: best (entry, team) pair with no repeats
        for s, i, tid, t in candidates:
            if i in assigned_entries or tid in assigned_teams:
                continue
            picks[i] = t
            assigned_entries.add(i)
            assigned_teams.add(tid)
            used_teams[i].add(tid)
            if len(assigned_entries) == len(alive_list):
                break

        # Fallback for overflow (more entries than unique teams this week)
        for i in alive_list:
            if i not in picks:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
                if not available:
                    continue
                best = max(available, key=lambda t: scorer(
                    t, teams, week_data, available, week, i, used_teams))
                picks[i] = best
                used_teams[i].add(best['teamId'])

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

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Custom Simulation: Adaptive Role Portfolio ───────────────────────────────

def simulate_adaptive_role(week_data, num_entries):
    """
    Strategy 7: Adaptive Role Portfolio.
    Roles shift across 3 phases:
      Weeks  1-6:  40% safety, 20% blend, 20% contrarian, 10% FV, 10% EV
      Weeks  7-12: 20% each
      Weeks 13-18: 10% safety, 20% blend, 30% contrarian, 20% FV, 20% EV
    """
    PHASE_DISTS = [
        {'safety': 0.40, 'blend': 0.20, 'contrarian': 0.20, 'fv': 0.10, 'ev': 0.10},
        {'safety': 0.20, 'blend': 0.20, 'contrarian': 0.20, 'fv': 0.20, 'ev': 0.20},
        {'safety': 0.10, 'blend': 0.20, 'contrarian': 0.30, 'fv': 0.20, 'ev': 0.20},
    ]
    phase_roles = [_assign_roles_by_distribution(num_entries, d) for d in PHASE_DISTS]

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        # Select phase
        if week <= 6:
            role_assignment = phase_roles[0]
        elif week <= 12:
            role_assignment = phase_roles[1]
        else:
            role_assignment = phase_roles[2]

        assigned = set()
        picks = {}

        for i in sorted(alive):
            role = role_assignment[i]
            scorer = _ROLE_SCORER_MAP[role]
            available = [t for t in teams
                         if t['teamId'] not in assigned and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            scored = [(scorer(t, teams, week_data, available, week, i, used_teams), t)
                      for t in available]
            scored.sort(key=lambda x: x[0], reverse=True)
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

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Custom Simulation: Correlated Pairs + Hedges ─────────────────────────────

def simulate_correlated_pairs(week_data, num_entries):
    """
    Strategy 9: Correlated Pairs + Hedges.
    Entries in pairs: lead picks highest WP (consensus), hedge picks best
    non-consensus team (70/30 score from teams with pickShare < 10%).
    Remainder entries use 70/30 as wild cards.
    """
    n_pairs = num_entries // 2

    def entry_role(i):
        if i < n_pairs * 2:
            return 'lead' if i % 2 == 0 else 'hedge'
        return 'wild'

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned = set()
        picks = {}

        for i in sorted(alive):
            role = entry_role(i)
            available = [t for t in teams
                         if t['teamId'] not in assigned and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            if role == 'lead':
                best = max(available, key=lambda t: t['winProbability'])
            elif role == 'hedge':
                non_chalk = [t for t in available if t['pickShare'] < 10]
                pool = non_chalk if non_chalk else available
                best = max(pool, key=lambda t: blend_score(t, 70, 30))
            else:
                best = max(available, key=lambda t: blend_score(t, 70, 30))

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

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Custom Simulation: Ownership-Bucket Spread ───────────────────────────────

def simulate_ownership_bucket(week_data, num_entries):
    """
    Strategy 10: Ownership-Bucket Spread.
    50% entries pick from high-ownership teams (>15%), by WP.
    30% entries pick from medium-ownership teams (5-15%), by WP.
    20% entries pick from low-ownership teams (<5%), by WP.
    Fallback: if bucket is empty, pick from all available by WP.
    """
    n_high = max(1, round(num_entries * 0.5))
    n_med = max(0, round(num_entries * 0.3))
    n_low = num_entries - n_high - n_med

    buckets = (
        ['high'] * n_high
        + ['medium'] * n_med
        + ['low'] * max(0, n_low)
    )
    while len(buckets) < num_entries:
        buckets.append('medium')
    buckets = buckets[:num_entries]

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned = set()
        picks = {}

        for i in sorted(alive):
            bucket = buckets[i]
            available = [t for t in teams
                         if t['teamId'] not in assigned and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            if bucket == 'high':
                pool = [t for t in available if t['pickShare'] >= 15]
            elif bucket == 'medium':
                pool = [t for t in available if 5 <= t['pickShare'] < 15]
            else:
                pool = [t for t in available if t['pickShare'] < 5]

            pool = pool if pool else available
            best = max(pool, key=lambda t: t['winProbability'])

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

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Custom Simulation: Dynamic Rebalancing ────────────────────────────────────

def simulate_dynamic_rebalancing(week_data, num_entries):
    """
    Strategy 12: Dynamic Rebalancing.
    Start at 70/30 blend. After each week:
    - >30% eliminated: shift toward conservative (+10pp WP, cap at 90/10)
    - 0 eliminated: shift toward aggressive (-10pp WP, floor at 50/50)
    - Otherwise: no change
    """
    wp_weight = 70
    ps_weight = 30

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned = set()
        picks = {}

        for i in sorted(alive):
            available = [t for t in teams
                         if t['teamId'] not in assigned and t['teamId'] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t['teamId'] not in used_teams[i]]
            if not available:
                continue

            scored = [(blend_score(t, wp_weight, ps_weight), t) for t in available]
            scored.sort(key=lambda x: x[0], reverse=True)
            best = scored[0][1]

            assigned.add(best['teamId'])
            used_teams[i].add(best['teamId'])
            picks[i] = best

        n_alive_before = len(alive)
        n_eliminated = 0
        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    alive.discard(i)
                    n_eliminated += 1
                else:
                    entry_weeks += 1

        if not alive and final_elim_week is None:
            final_elim_week = week

        # Rebalance weights for next week
        if n_alive_before > 0:
            frac = n_eliminated / n_alive_before
            if frac > 0.30:
                wp_weight = min(90, wp_weight + 10)
                ps_weight = max(10, ps_weight - 10)
            elif n_eliminated == 0:
                wp_weight = max(50, wp_weight - 10)
                ps_weight = min(50, ps_weight + 10)

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {'entry_weeks': entry_weeks, 'final_elim': final_elim_week}


# ── Strategy Registry ─────────────────────────────────────────────────────────

STRATEGIES = [
    # (name, run_fn_or_tag)
    # run_fn_or_tag is either a function(week_data, num_entries)->result
    # or a scorer (callable) to be passed into simulate()
    # or a list-builder function(num_entries)->list_of_scorers

    ("1.  70/30 Blend [baseline]",
     lambda wd, n: simulate(make_blend_scorer(70, 30), wd, n)),

    ("2.  Mixed Portfolio [Round6 winner@n=20]",
     lambda wd, n: simulate(make_mixed_scorers(n), wd, n)),

    ("3.  Safety/Contrarian Split",
     lambda wd, n: simulate(make_safety_contrarian_scorers(n), wd, n)),

    ("4.  Core/Satellite [60%blend+40%EV]",
     lambda wd, n: simulate(make_core_satellite_scorers(n), wd, n)),

    ("5.  Temporal Diversification",
     lambda wd, n: simulate(make_temporal_scorers(n), wd, n)),

    ("6.  Role-Based Portfolio [5 roles]",
     lambda wd, n: simulate(make_role_based_scorers(n), wd, n)),

    ("7.  Adaptive Role Portfolio",
     lambda wd, n: simulate_adaptive_role(wd, n)),

    ("8.  Anti-Overlap [global assign]",
     lambda wd, n: simulate_anti_overlap(wd, n)),

    ("9.  Correlated Pairs + Hedges",
     lambda wd, n: simulate_correlated_pairs(wd, n)),

    ("10. Ownership-Bucket Spread",
     lambda wd, n: simulate_ownership_bucket(wd, n)),

    ("11. EV Gradient [95/5→55/45]",
     lambda wd, n: simulate(make_ev_gradient_scorers(n), wd, n)),

    ("12. Dynamic Rebalancing",
     lambda wd, n: simulate_dynamic_rebalancing(wd, n)),
]


# ── Output Helpers ────────────────────────────────────────────────────────────

def std(vals):
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 120)
    print("STAN: PER-ENTRY DIFFERENTIATED SCORING SIMULATION — Round 7")
    print("12 strategies × 4 entry counts (5, 10, 20, 50) × 3 seasons = 144 runs")
    print("=" * 120)
    print()

    # Load season data
    print("Loading season data...")
    season_data = {}
    for season in [2023, 2024]:
        print(f"  Loading {season}...")
        season_data[season] = load_local_season(season)
        print(f"  {season}: {len(season_data[season])} weeks loaded")
    print("  Loading 2025...")
    season_data[2025] = load_2025()
    print()

    strat_names = [n for n, _ in STRATEGIES]
    results = {n: {} for n in strat_names}

    total_runs = len(STRATEGIES) * len(ENTRY_COUNTS) * len(SEASONS)
    run_num = 0

    for strat_name, run_fn in STRATEGIES:
        results[strat_name] = {}
        for num_entries in ENTRY_COUNTS:
            results[strat_name][num_entries] = {}
            for season in SEASONS:
                run_num += 1
                sys.stdout.write(
                    f"\r  [{run_num:3d}/{total_runs}] {strat_name[:40]:<40} "
                    f"n={num_entries:2d}  {season}"
                )
                sys.stdout.flush()
                r = run_fn(season_data[season], num_entries)
                results[strat_name][num_entries][season] = r

    print(f"\r  All {total_runs} runs complete.{'':60}")
    print()

    # ── Per entry-count tables ──────────────────────────────────────────────
    # Baselines for comparison
    blend_name = strat_names[0]
    mixed_name = strat_names[1]

    for num_entries in ENTRY_COUNTS:
        max_possible = num_entries * TOTAL_WEEKS
        blend_total = sum(results[blend_name][num_entries][s]['entry_weeks'] for s in SEASONS)
        mixed_total = sum(results[mixed_name][num_entries][s]['entry_weeks'] for s in SEASONS)

        print("=" * 130)
        print(f"ENTRY COUNT: n={num_entries}  (max possible entry-weeks/season: {max_possible})")
        print(f"  Baselines: 70/30 Blend = {blend_total}  |  Mixed Portfolio = {mixed_total}")
        print("=" * 130)
        print(f"{'Strategy':<44} {'2023':>6} {'2024':>6} {'2025':>6} {'TOTAL':>7} "
              f"{'SD':>5} {'Eff%':>6} {'vs Blend':>9} {'vs Mixed':>9}")
        print(f"{'─' * 44} {'─' * 6} {'─' * 6} {'─' * 6} {'─' * 7} "
              f"{'─' * 5} {'─' * 6} {'─' * 9} {'─' * 9}")

        rows = []
        for name in strat_names:
            s23 = results[name][num_entries][2023]['entry_weeks']
            s24 = results[name][num_entries][2024]['entry_weeks']
            s25 = results[name][num_entries][2025]['entry_weeks']
            total = s23 + s24 + s25
            sd = std([s23, s24, s25])
            eff = total / (max_possible * 3) * 100
            d_blend = total - blend_total
            d_mixed = total - mixed_total
            rows.append((name, s23, s24, s25, total, sd, eff, d_blend, d_mixed))

        rows.sort(key=lambda x: x[4], reverse=True)

        for name, s23, s24, s25, total, sd, eff, db, dm in rows:
            db_str = f"{db:+d}" if db != 0 else "="
            dm_str = f"{dm:+d}" if dm != 0 else "="
            print(f"{name:<44} {s23:>6} {s24:>6} {s25:>6} {total:>7} "
                  f"{sd:>5.1f} {eff:>5.1f}% {db_str:>9} {dm_str:>9}")
        print()

    # ── Scaling table ───────────────────────────────────────────────────────
    print("=" * 120)
    print("SCALING ANALYSIS — Total entry-weeks across 3 seasons by entry count")
    print("=" * 120)
    print(f"{'Strategy':<44} {'n=5':>7} {'n=10':>7} {'n=20':>7} {'n=50':>7} "
          f"{'Scale5→50':>10} {'BestAt':>8}")
    print(f"{'─' * 44} {'─' * 7} {'─' * 7} {'─' * 7} {'─' * 7} "
          f"{'─' * 10} {'─' * 8}")

    blend_totals_by_n = {
        n: sum(results[blend_name][n][s]['entry_weeks'] for s in SEASONS)
        for n in ENTRY_COUNTS
    }

    scaling_rows = []
    for name in strat_names:
        tots = {n: sum(results[name][n][s]['entry_weeks'] for s in SEASONS) for n in ENTRY_COUNTS}
        scale_ratio = tots[50] / tots[5] if tots[5] > 0 else 0
        best_at = max(ENTRY_COUNTS, key=lambda n: tots[n] / blend_totals_by_n[n])
        scaling_rows.append((name, tots[5], tots[10], tots[20], tots[50], scale_ratio, best_at))

    scaling_rows.sort(key=lambda x: x[4], reverse=True)

    for name, t5, t10, t20, t50, sr, best_at in scaling_rows:
        print(f"{name:<44} {t5:>7} {t10:>7} {t20:>7} {t50:>7} "
              f"   {sr:>7.2f}x   n={best_at:>2}")
    print()

    # ── Efficiency table ────────────────────────────────────────────────────
    print("=" * 120)
    print("EFFICIENCY — Entry-week survival rate (total / (n × 18 × 3 seasons))")
    print("=" * 120)
    print(f"{'Strategy':<44} {'n=5':>7} {'n=10':>7} {'n=20':>7} {'n=50':>7} {'Δ 5→50':>8}")
    print(f"{'─' * 44} {'─' * 7} {'─' * 7} {'─' * 7} {'─' * 7} {'─' * 8}")

    eff_rows = []
    for name in strat_names:
        effs = {n: sum(results[name][n][s]['entry_weeks'] for s in SEASONS) / (n * TOTAL_WEEKS * 3) * 100
                for n in ENTRY_COUNTS}
        delta = effs[50] - effs[5]
        eff_rows.append((name, effs[5], effs[10], effs[20], effs[50], delta))

    eff_rows.sort(key=lambda x: x[4], reverse=True)

    for name, e5, e10, e20, e50, delta in eff_rows:
        print(f"{name:<44} {e5:>6.1f}%  {e10:>6.1f}%   {e20:>6.1f}%   {e50:>6.1f}%   {delta:>+.1f}pp")
    print()

    # ── Winners ─────────────────────────────────────────────────────────────
    print("=" * 120)
    print("WINNERS PER ENTRY COUNT")
    print("=" * 120)
    for num_entries in ENTRY_COUNTS:
        best_name = max(strat_names, key=lambda n: sum(
            results[n][num_entries][s]['entry_weeks'] for s in SEASONS))
        best_total = sum(results[best_name][num_entries][s]['entry_weeks'] for s in SEASONS)
        blend_total = blend_totals_by_n[num_entries]
        delta = best_total - blend_total
        eff = best_total / (num_entries * TOTAL_WEEKS * 3) * 100
        print(f"  n={num_entries:2d}: {best_name:<44}  total={best_total}  vs_blend={delta:+d}  eff={eff:.1f}%")
    print()

    # ── Blend challenger analysis ────────────────────────────────────────────
    print("=" * 120)
    print("BLEND CHALLENGER ANALYSIS — Intentional configs vs 70/30 Blend")
    print("=" * 120)
    for num_entries in ENTRY_COUNTS:
        blend_total = blend_totals_by_n[num_entries]
        challengers = []
        for name in strat_names:
            if name == blend_name:
                continue
            total = sum(results[name][num_entries][s]['entry_weeks'] for s in SEASONS)
            if total > blend_total:
                challengers.append((name, total, total - blend_total))
        challengers.sort(key=lambda x: x[2], reverse=True)

        if challengers:
            print(f"  n={num_entries:2d}: Blend BEATEN by {len(challengers)} configs:")
            for cname, ctotal, cdelta in challengers:
                mixed_total = sum(results[mixed_name][num_entries][s]['entry_weeks'] for s in SEASONS)
                beats_mixed = "★ BEATS MIXED" if ctotal > mixed_total else ""
                print(f"         {cname:<44} total={ctotal}  vs_blend={cdelta:+d}  {beats_mixed}")
        else:
            print(f"  n={num_entries:2d}: Blend HOLDS LEAD (total={blend_total})")
    print()

    # ── Mixed Portfolio vs Intentional configs ────────────────────────────────
    print("=" * 120)
    print("KEY QUESTION: Do intentional portfolio configs beat Mixed Portfolio (random)?")
    print("=" * 120)
    for num_entries in ENTRY_COUNTS:
        mixed_total = sum(results[mixed_name][num_entries][s]['entry_weeks'] for s in SEASONS)
        intentional_winners = []
        for name in strat_names:
            if name in (blend_name, mixed_name):
                continue
            total = sum(results[name][num_entries][s]['entry_weeks'] for s in SEASONS)
            if total > mixed_total:
                intentional_winners.append((name, total, total - mixed_total))
        intentional_winners.sort(key=lambda x: x[2], reverse=True)
        if intentional_winners:
            print(f"  n={num_entries:2d}: Mixed Portfolio ({mixed_total}) BEATEN by {len(intentional_winners)} intentional configs:")
            for cname, ctotal, cdelta in intentional_winners:
                print(f"         {cname:<44} total={ctotal}  vs_mixed={cdelta:+d}")
        else:
            print(f"  n={num_entries:2d}: Mixed Portfolio ({mixed_total}) HOLDS — no intentional config beats it")
    print()

    print("=" * 120)
    print("SIMULATION COMPLETE")
    print("=" * 120)

    # Save JSON
    output_path = os.path.join(
        os.path.expanduser("~/.openclaw/workspace"),
        "scripts/stan-differentiated-scoring-results.json"
    )
    serializable = {}
    for name in strat_names:
        serializable[name] = {}
        for n in ENTRY_COUNTS:
            serializable[name][str(n)] = {}
            for season in SEASONS:
                r = results[name][n][season]
                serializable[name][str(n)][str(season)] = {
                    'entry_weeks': r['entry_weeks'],
                    'final_elim': str(r['final_elim']),
                }
    with open(output_path, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nRaw results saved to: {output_path}")


if __name__ == "__main__":
    main()
