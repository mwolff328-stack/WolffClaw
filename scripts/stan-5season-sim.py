#!/usr/bin/env python3
"""
Stan the Scout: 5-Season Comprehensive Backtesting Simulation

14 strategies × 4 entry counts × 3 buyback configs × 5 seasons = 840 runs

Seasons: 2021, 2022, 2023, 2024, 2025
Entry counts: 5, 10, 20, 50
Buyback configs: No buyback, Buyback Wk1-3, Buyback Wk1-4

Research questions:
  1. Does 70/30 Blend still dominate at n=5 across 5 seasons?
  2. Does Core/Satellite still win at n=10?
  3. Does SP Conservative still dominate all buyback scenarios?
  4. Which strategies are most consistent (lowest SD) across 5 seasons?
  5. Are there regime changes between 2021-2022 and 2023-2025?
  6. Updated product recommendation matrix for SurvivorPulse.
"""

import json
import math
import os
import sys
import urllib.request

# ── Config ────────────────────────────────────────────────────────────────────

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
CACHE_FILE_2025 = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
# Fallback to old path if needed
ALT_DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
ALT_CACHE_2025 = os.path.join(ALT_DATA_DIR, "nfl_games_2025_cache.json")

BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"

TOTAL_WEEKS = 18
SEASONS = [2021, 2022, 2023, 2024, 2025]
ENTRY_COUNTS = [5, 10, 20, 50]
BUYBACK_CONFIGS = [
    ("No Buyback", 0),
    ("Buyback Wk1-3", 3),
    ("Buyback Wk1-4", 4),
]

RESULTS_PATH = os.path.expanduser("~/.openclaw/workspace/scripts/stan-5season-results.json")
REPORT_PATH = os.path.expanduser("~/.openclaw/workspace/memory/stan-5season-backtesting.md")


# ── Data Loading ──────────────────────────────────────────────────────────────

def _resolve_data_dir():
    if os.path.exists(DATA_DIR):
        return DATA_DIR
    if os.path.exists(ALT_DATA_DIR):
        return ALT_DATA_DIR
    raise FileNotFoundError(f"Data dir not found: {DATA_DIR}")


def fetch_json(url, timeout=20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _normalize_game(g: dict) -> dict:
    """Normalize snake_case (2021/2022) or camelCase (2023/2024) game records."""
    return {
        'homeTeamId': g.get('homeTeamId') or g.get('home_team_id'),
        'awayTeamId': g.get('awayTeamId') or g.get('away_team_id'),
        'homeWinProbability': float(g.get('homeWinProbability') or g.get('home_win_probability') or 0),
        'awayWinProbability': float(g.get('awayWinProbability') or g.get('away_win_probability') or 0),
        'homeScore': g.get('homeScore') if g.get('homeScore') is not None else g.get('home_score'),
        'awayScore': g.get('awayScore') if g.get('awayScore') is not None else g.get('away_score'),
        'completed': bool(g.get('completed', False)),
        'week': g.get('week'),
    }


def load_local_season(season: int, data_dir: str) -> dict:
    """Load games + pick shares for a local season (2021-2024)."""
    with open(os.path.join(data_dir, f"nfl_games_{season}.json")) as f:
        raw_games = json.load(f)
    with open(os.path.join(data_dir, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data: dict = {}
    for week in range(1, TOTAL_WEEKS + 1):
        week_games = [_normalize_game(g) for g in raw_games if g.get('week') == week]
        week_picks = picks_data.get('weeks', {}).get(str(week), {}).get('teams', [])
        pick_shares = {p['teamId']: p.get('average', 0) for p in week_picks}

        teams = []
        for g in week_games:
            home, away = g['homeTeamId'], g['awayTeamId']
            hwp, awp = g['homeWinProbability'], g['awayWinProbability']
            completed = g['completed']
            hs, as_ = g['homeScore'], g['awayScore']
            ho = ('Win' if hs > as_ else 'Loss') if (completed and hs is not None and as_ is not None) else None
            ao = ('Win' if as_ > hs else 'Loss') if (completed and hs is not None and as_ is not None) else None
            teams.append({'teamId': home, 'winProbability': hwp,
                          'pickShare': pick_shares.get(home, 0), 'outcome': ho})
            teams.append({'teamId': away, 'winProbability': awp,
                          'pickShare': pick_shares.get(away, 0), 'outcome': ao})
        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025(data_dir: str) -> dict:
    """Load 2025 season — from cache file (pre-processed format)."""
    cache_path = os.path.join(data_dir, "nfl_games_2025_cache.json")
    if not os.path.exists(cache_path):
        cache_path = ALT_CACHE_2025

    if os.path.exists(cache_path):
        print("  2025: Loading from cache...")
        with open(cache_path) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}

    # Fetch from API
    print("  2025: Cache not found — fetching from API...")
    all_week_data: dict = {}
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
    with open(cache_path, 'w') as f:
        json.dump(all_week_data, f)
    print(f"  2025: Cached to {cache_path}")
    return all_week_data


def load_all_seasons() -> dict:
    data_dir = _resolve_data_dir()
    season_data = {}
    for season in SEASONS:
        print(f"  Loading {season}...")
        if season == 2025:
            season_data[season] = load_2025(data_dir)
        else:
            season_data[season] = load_local_season(season, data_dir)
        print(f"  {season}: {len(season_data[season])} weeks loaded")
    return season_data


# ── Scoring Primitives ────────────────────────────────────────────────────────

def blend_score(team: dict, wp_w: float, ps_w: float) -> float:
    return (wp_w / 100) * team['winProbability'] + (ps_w / 100) * (1 - team['pickShare'] / 100)


def compute_expendability(team_id: str, current_week: int, all_week_data: dict,
                          lookahead: int = 5) -> float:
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


def sp_production_score(team: dict, all_week_data: dict, week: int,
                        lookahead: int = 5) -> float:
    """SP Production: 70% EV (normalized) + 30% FV."""
    ev = team['winProbability'] - (team['pickShare'] / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
    fv = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * fv


def compute_leverage(team: dict, all_teams: list) -> float:
    """Leverage vs chalk: p_team * (1 - p_chalk) * q_chalk."""
    chalk = max(all_teams, key=lambda t: t['pickShare'])
    return team['winProbability'] * (1 - chalk['winProbability']) * (chalk['pickShare'] / 100)


# ── Scorer Factories ──────────────────────────────────────────────────────────

def make_blend_scorer(wp_w: float = 70, ps_w: float = 30):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return blend_score(team, wp_w, ps_w)
    return scorer


def make_pure_wp_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return team['winProbability']
    return scorer


def make_sp_production_scorer(lookahead: int = 5):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return sp_production_score(team, all_week_data, week, lookahead)
    return scorer


def make_sp_conservative_scorer():
    """SP Conservative: 65% EV + 25% anti-chalk + 10% FV."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 65, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.10 * fv
    return scorer


def make_sp_balanced_scorer():
    """SP Balanced: 55% WP + 25% anti-chalk + 20% FV."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 55, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.20 * fv
    return scorer


def make_leverage_60_floor_scorer():
    """Leverage + 60% floor: require WP >= 60%, then pick by leverage vs chalk."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        if team['winProbability'] < 0.60:
            return -999.0
        return compute_leverage(team, all_teams)
    return scorer


def make_anti_chalk_top5_scorer():
    """Anti-Chalk Top-5: pick from top 5 win-prob teams, maximize anti-chalk score."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        # Rank team by win probability among all available this week
        sorted_teams = sorted(available, key=lambda t: t['winProbability'], reverse=True)
        top5_ids = {t['teamId'] for t in sorted_teams[:5]}
        if team['teamId'] not in top5_ids:
            return -999.0
        return 1.0 - (team['pickShare'] / 100)  # pure anti-chalk within top 5
    return scorer


def make_expendable_first_scorer(lookahead: int = 3):
    """Expendable-First: 65% WP + 25% anti-chalk + 10% expendability."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 65, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
        return base + 0.10 * exp
    return scorer


def make_adaptive_scorer():
    """Adaptive Blend: 90/10 week 1 → 50/50 week 18."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        progress = (week - 1) / max(1, TOTAL_WEEKS - 1)
        eff_wp = 90 - 40 * progress
        eff_ps = 10 + 40 * progress
        return blend_score(team, eff_wp, eff_ps)
    return scorer


def make_lookahead5_scorer(exp_coeff: float = 0.15):
    """Lookahead-5 Expendability: 70/20 blend + exp_coeff × expendability (5-week)."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 70, 20)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        return base + exp_coeff * exp
    return scorer


# ── Portfolio Builder Helpers ─────────────────────────────────────────────────

_FIVE_BASE_SCORERS = [
    make_blend_scorer(70, 30),
    make_sp_production_scorer(),
    make_expendable_first_scorer(3),
    make_blend_scorer(80, 20),
    make_pure_wp_scorer(),
]


def make_mixed_portfolio_scorers(num_entries: int) -> list:
    """Cycle through 5 base strategies across entries."""
    return [_FIVE_BASE_SCORERS[i % 5] for i in range(num_entries)]


def make_core_satellite_scorers(num_entries: int) -> list:
    """60% core (70/30 blend) + 40% satellite (SP Production EV)."""
    n_core = round(num_entries * 0.6)
    n_sat = num_entries - n_core
    return [make_blend_scorer(70, 30)] * n_core + [make_sp_production_scorer()] * n_sat


def make_temporal_scorers(num_entries: int) -> list:
    """1/3 pure WP + 1/3 70/30 blend + 1/3 heavy FV (60/10/30 5wk)."""
    n_wp = num_entries // 3
    n_bl = num_entries // 3
    n_fv = num_entries - n_wp - n_bl

    def fv_scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 60, 10)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.30 * fv

    return (
        [make_pure_wp_scorer()] * n_wp
        + [make_blend_scorer(70, 30)] * n_bl
        + [fv_scorer] * n_fv
    )


# ── Core Simulation Engine (with Buyback) ─────────────────────────────────────

def simulate_with_buyback(
    scorer_or_list,
    week_data: dict,
    num_entries: int,
    buyback_window_end: int = 0,
) -> dict:
    """
    Sequential greedy survivor simulation with optional buyback mechanics.

    Returns:
      entry_weeks: total accumulated entry-weeks survived
      final_elim: week when last entry died (or "18+")
      buyback_count: number of buyback events used
      avg_wp: average win probability of all picks
      avg_pick_share: average pick share of all picks
    """
    if callable(scorer_or_list):
        scorers = [scorer_or_list] * num_entries
    else:
        scorers = list(scorer_or_list)
        while len(scorers) < num_entries:
            scorers.append(scorers[len(scorers) % len(scorers)])

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    buyback_used = [False] * num_entries
    entry_weeks = 0
    final_elim_week = None
    all_wps = []
    all_ps = []

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned: set = set()
        picks: dict = {}

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
            all_wps.append(best['winProbability'])
            all_ps.append(best['pickShare'])

        newly_eliminated = set()
        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    newly_eliminated.add(i)
                else:
                    entry_weeks += 1

        for i in newly_eliminated:
            alive.discard(i)
            if buyback_window_end > 0 and week <= buyback_window_end and not buyback_used[i]:
                buyback_used[i] = True
                alive.add(i)  # Resurrect

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    avg_wp = sum(all_wps) / len(all_wps) if all_wps else 0.0
    avg_ps = sum(all_ps) / len(all_ps) if all_ps else 0.0

    return {
        'entry_weeks': entry_weeks,
        'final_elim': str(final_elim_week),
        'buyback_count': sum(buyback_used),
        'avg_wp': round(avg_wp, 4),
        'avg_pick_share': round(avg_ps, 4),
    }


# ── Strategy Registry ─────────────────────────────────────────────────────────

def build_strategies():
    return [
        ("Pure Win Probability",
         lambda wd, n, bb: simulate_with_buyback(make_pure_wp_scorer(), wd, n, bb)),

        ("70/30 Blend",
         lambda wd, n, bb: simulate_with_buyback(make_blend_scorer(70, 30), wd, n, bb)),

        ("80/20 Blend",
         lambda wd, n, bb: simulate_with_buyback(make_blend_scorer(80, 20), wd, n, bb)),

        ("SP Production 70EV+30FV",
         lambda wd, n, bb: simulate_with_buyback(make_sp_production_scorer(), wd, n, bb)),

        ("SP Conservative 65/25/10",
         lambda wd, n, bb: simulate_with_buyback(make_sp_conservative_scorer(), wd, n, bb)),

        ("SP Balanced 55/25/20",
         lambda wd, n, bb: simulate_with_buyback(make_sp_balanced_scorer(), wd, n, bb)),

        ("Leverage+60%Floor",
         lambda wd, n, bb: simulate_with_buyback(make_leverage_60_floor_scorer(), wd, n, bb)),

        ("Anti-Chalk Top-5",
         lambda wd, n, bb: simulate_with_buyback(make_anti_chalk_top5_scorer(), wd, n, bb)),

        ("Expendable-First 65/25/10",
         lambda wd, n, bb: simulate_with_buyback(make_expendable_first_scorer(3), wd, n, bb)),

        ("Core/Satellite 60/40",
         lambda wd, n, bb: simulate_with_buyback(make_core_satellite_scorers(n), wd, n, bb)),

        ("Mixed Portfolio",
         lambda wd, n, bb: simulate_with_buyback(make_mixed_portfolio_scorers(n), wd, n, bb)),

        ("Temporal Diversification",
         lambda wd, n, bb: simulate_with_buyback(make_temporal_scorers(n), wd, n, bb)),

        ("Adaptive Blend 90/10→50/50",
         lambda wd, n, bb: simulate_with_buyback(make_adaptive_scorer(), wd, n, bb)),

        ("Lookahead-5 Exp(0.15)",
         lambda wd, n, bb: simulate_with_buyback(make_lookahead5_scorer(0.15), wd, n, bb)),
    ]


# ── Analysis Helpers ──────────────────────────────────────────────────────────

def std_dev(vals: list) -> float:
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


def pct_of_max(entry_weeks: int, num_entries: int) -> float:
    return entry_weeks / (num_entries * TOTAL_WEEKS) * 100


# ── Report Generator ──────────────────────────────────────────────────────────

def generate_report(results: dict, strategies: list) -> str:
    strat_names = [n for n, _ in strategies]
    lines = []

    lines.append("# SurvivorPulse 5-Season Backtesting Report")
    lines.append(f"\n**Generated:** 2026-04-13  |  **Seasons:** 2021-2025  |  **Rounds:** 1 unified run")
    lines.append(f"\n**Scope:** 14 strategies × 4 entry counts × 3 buyback configs × 5 seasons = 840 runs")

    # ── Season difficulty ──────────────────────────────────────────────────
    lines.append("\n---\n## Season Difficulty (Total Entry-Weeks Survived at n=10, No Buyback)\n")
    lines.append("| Season | Entry-Weeks | Max Possible | Survival Rate | Difficulty |")
    lines.append("|--------|-------------|--------------|---------------|------------|")
    season_totals = {}
    for season in SEASONS:
        total_ew = sum(
            results[n][10][season]["No Buyback"]['entry_weeks']
            for n in strat_names
        ) / len(strat_names)
        max_ew = 10 * TOTAL_WEEKS
        pct = total_ew / max_ew * 100
        difficulty = "Easy" if pct >= 55 else ("Medium" if pct >= 40 else "Hard")
        season_totals[season] = total_ew
        lines.append(f"| {season} | {total_ew:.0f} | {max_ew} | {pct:.1f}% | {difficulty} |")

    # ── Executive Summary ──────────────────────────────────────────────────
    lines.append("\n---\n## Executive Summary\n")

    # Find winners per entry count, no buyback
    winners_no_bb = {}
    for n in ENTRY_COUNTS:
        best = max(strat_names, key=lambda nm: sum(
            results[nm][n][s]["No Buyback"]['entry_weeks'] for s in SEASONS))
        best_val = sum(results[best][n][s]["No Buyback"]['entry_weeks'] for s in SEASONS)
        blend_val = sum(results["70/30 Blend"][n][s]["No Buyback"]['entry_weeks'] for s in SEASONS)
        winners_no_bb[n] = (best, best_val, blend_val)

    # Find winners with buyback
    winners_bb3 = {}
    for n in ENTRY_COUNTS:
        best = max(strat_names, key=lambda nm: sum(
            results[nm][n][s]["Buyback Wk1-3"]['entry_weeks'] for s in SEASONS))
        best_val = sum(results[best][n][s]["Buyback Wk1-3"]['entry_weeks'] for s in SEASONS)
        winners_bb3[n] = (best, best_val)

    lines.append("### Key Findings\n")
    for n in ENTRY_COUNTS:
        winner, val, blend_val = winners_no_bb[n]
        delta = val - blend_val
        lines.append(f"- **n={n} (No Buyback):** {winner} wins with {val} entry-weeks "
                     f"({delta:+d} vs 70/30 Blend)")
    lines.append("")
    for n in ENTRY_COUNTS:
        winner, val = winners_bb3[n]
        lines.append(f"- **n={n} (Buyback Wk1-3):** {winner} wins with {val} entry-weeks")

    # ── Full results tables ────────────────────────────────────────────────
    lines.append("\n---\n## Full Results Tables\n")

    for bb_label, bb_end in BUYBACK_CONFIGS:
        lines.append(f"### {bb_label}\n")
        for n in ENTRY_COUNTS:
            max_per_season = n * TOTAL_WEEKS
            max_5season = max_per_season * 5
            lines.append(f"#### n={n} | max={max_per_season}/season | {max_5season} total\n")
            lines.append(
                "| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL | Avg | SD | Eff% |"
            )
            lines.append(
                "|----------|------|------|------|------|------|-------|-----|----|------|"
            )

            rows = []
            for nm in strat_names:
                vals = [results[nm][n][s][bb_label]['entry_weeks'] for s in SEASONS]
                total = sum(vals)
                avg = total / 5
                sd = std_dev(vals)
                eff = total / max_5season * 100
                rows.append((total, nm, vals, avg, sd, eff))
            rows.sort(key=lambda x: x[0], reverse=True)

            for total, nm, vals, avg, sd, eff in rows:
                v_str = " | ".join(str(v) for v in vals)
                lines.append(
                    f"| {nm} | {v_str} | **{total}** | {avg:.1f} | {sd:.1f} | {eff:.1f}% |"
                )
            lines.append("")

    # ── Winner tables ──────────────────────────────────────────────────────
    lines.append("---\n## Winner Tables Per Dimension\n")
    lines.append("### Winner by Entry Count × Buyback Config\n")
    lines.append("| n | No Buyback | Buyback Wk1-3 | Buyback Wk1-4 |")
    lines.append("|---|------------|---------------|---------------|")
    for n in ENTRY_COUNTS:
        row = [f"**{n}**"]
        for bb_label, _ in BUYBACK_CONFIGS:
            best = max(strat_names, key=lambda nm: sum(
                results[nm][n][s][bb_label]['entry_weeks'] for s in SEASONS))
            best_val = sum(results[best][n][s][bb_label]['entry_weeks'] for s in SEASONS)
            row.append(f"{best} ({best_val})")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # ── Consistency Analysis ───────────────────────────────────────────────
    lines.append("---\n## Consistency Analysis (SD across 5 seasons)\n")
    lines.append("*Lower SD = more consistent. Consistency matters more than peak for product recs.*\n")

    for n in ENTRY_COUNTS:
        lines.append(f"### n={n} | No Buyback\n")
        lines.append("| Rank | Strategy | 5-Season Total | Avg/Season | SD | CV (SD/Avg) |")
        lines.append("|------|----------|----------------|------------|----|-------------|")

        rows = []
        for nm in strat_names:
            vals = [results[nm][n][s]["No Buyback"]['entry_weeks'] for s in SEASONS]
            total = sum(vals)
            avg = total / 5
            sd = std_dev(vals)
            cv = sd / avg if avg > 0 else 0
            rows.append((sd, nm, total, avg, cv))
        rows.sort(key=lambda x: x[0])  # sort by SD ascending

        for rank, (sd, nm, total, avg, cv) in enumerate(rows, 1):
            lines.append(f"| {rank} | {nm} | {total} | {avg:.1f} | {sd:.1f} | {cv:.3f} |")
        lines.append("")

    # ── Regime Analysis ────────────────────────────────────────────────────
    lines.append("---\n## Regime Analysis: 2021-2022 vs 2023-2025\n")
    lines.append("*Are there strategies that dominated early but faded, or vice versa?*\n")

    for n in [5, 10]:
        lines.append(f"### n={n} | No Buyback — Early (2021-2022) vs Late (2023-2025)\n")
        lines.append("| Strategy | 2021-2022 Avg | 2023-2025 Avg | Δ Late-Early | Regime |")
        lines.append("|----------|---------------|---------------|--------------|--------|")

        rows = []
        for nm in strat_names:
            early = [results[nm][n][s]["No Buyback"]['entry_weeks'] for s in [2021, 2022]]
            late = [results[nm][n][s]["No Buyback"]['entry_weeks'] for s in [2023, 2024, 2025]]
            early_avg = sum(early) / len(early)
            late_avg = sum(late) / len(late)
            delta = late_avg - early_avg
            regime = "Improved" if delta > 2 else ("Declined" if delta < -2 else "Stable")
            rows.append((abs(delta), nm, early_avg, late_avg, delta, regime))
        rows.sort(key=lambda x: x[0], reverse=True)

        for _, nm, ea, la, d, regime in rows:
            d_str = f"{d:+.1f}"
            lines.append(f"| {nm} | {ea:.1f} | {la:.1f} | {d_str} | {regime} |")
        lines.append("")

    # ── Product Recommendation Matrix ──────────────────────────────────────
    lines.append("---\n## Product Recommendation Matrix\n")
    lines.append("*Based on 5-season performance + consistency. Primary ICP is n=10.*\n")

    rec_matrix = {
        (5, "No Buyback"): None, (5, "Buyback"): None,
        (10, "No Buyback"): None, (10, "Buyback"): None,
        (20, "No Buyback"): None, (20, "Buyback"): None,
        (50, "No Buyback"): None, (50, "Buyback"): None,
    }

    for n in ENTRY_COUNTS:
        # No buyback: best by total + penalize high SD
        rows_nb = []
        for nm in strat_names:
            vals = [results[nm][n][s]["No Buyback"]['entry_weeks'] for s in SEASONS]
            total = sum(vals)
            sd = std_dev(vals)
            avg = total / 5
            score = avg - 0.5 * sd  # risk-adjusted
            rows_nb.append((score, nm, total, sd))
        rows_nb.sort(reverse=True)
        rec_matrix[(n, "No Buyback")] = (rows_nb[0][1], rows_nb[0][2], rows_nb[0][3])

        # With buyback: use Wk1-3
        rows_bb = []
        for nm in strat_names:
            vals = [results[nm][n][s]["Buyback Wk1-3"]['entry_weeks'] for s in SEASONS]
            total = sum(vals)
            sd = std_dev(vals)
            avg = total / 5
            score = avg - 0.5 * sd
            rows_bb.append((score, nm, total, sd))
        rows_bb.sort(reverse=True)
        rec_matrix[(n, "Buyback")] = (rows_bb[0][1], rows_bb[0][2], rows_bb[0][3])

    lines.append("| Pool Size | No Buyback Rec | Buyback Rec |")
    lines.append("|-----------|----------------|-------------|")
    for n in ENTRY_COUNTS:
        nb_name, nb_total, nb_sd = rec_matrix[(n, "No Buyback")]
        bb_name, bb_total, bb_sd = rec_matrix[(n, "Buyback")]
        lines.append(f"| **n={n}** | {nb_name} ({nb_total} total, SD={nb_sd:.1f}) "
                     f"| {bb_name} ({bb_total} total, SD={bb_sd:.1f}) |")
    lines.append("")

    lines.append("### Recommendation Narrative\n")
    for n in ENTRY_COUNTS:
        nb_name, nb_total, _ = rec_matrix[(n, "No Buyback")]
        bb_name, bb_total, _ = rec_matrix[(n, "Buyback")]
        lines.append(f"**n={n}:** No buyback → **{nb_name}**. With buyback → **{bb_name}**.")
    lines.append("")

    # ── Surprising Findings ────────────────────────────────────────────────
    lines.append("---\n## Notable Findings from 2021-2022 Data\n")

    lines.append("### Per-Season Breakdown (n=10, No Buyback)\n")
    lines.append("| Strategy | 2021 | 2022 | 2023 | 2024 | 2025 | TOTAL |")
    lines.append("|----------|------|------|------|------|------|-------|")
    rows = []
    for nm in strat_names:
        vals = [results[nm][10][s]["No Buyback"]['entry_weeks'] for s in SEASONS]
        rows.append((sum(vals), nm, vals))
    rows.sort(reverse=True)
    for total, nm, vals in rows:
        v_str = " | ".join(str(v) for v in vals)
        lines.append(f"| {nm} | {v_str} | {total} |")
    lines.append("")

    # Best season per strategy
    lines.append("### Best and Worst Season per Strategy (n=10, No Buyback)\n")
    lines.append("| Strategy | Best Season | Worst Season | Range |")
    lines.append("|----------|-------------|--------------|-------|")
    for nm in strat_names:
        vals = {s: results[nm][10][s]["No Buyback"]['entry_weeks'] for s in SEASONS}
        best_s = max(vals, key=vals.get)
        worst_s = min(vals, key=vals.get)
        rng = vals[best_s] - vals[worst_s]
        lines.append(f"| {nm} | {best_s} ({vals[best_s]}) | {worst_s} ({vals[worst_s]}) | {rng} |")
    lines.append("")

    lines.append("---\n*Report generated by Stan the Scout — SurvivorPulse Intelligence Layer*")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 120)
    print("STAN: 5-SEASON COMPREHENSIVE BACKTESTING SIMULATION")
    print("14 strategies × 4 entry counts × 3 buyback configs × 5 seasons = 840 runs")
    print("=" * 120)
    print()

    # Load all season data
    print("Loading season data...")
    season_data = load_all_seasons()
    print()

    strategies = build_strategies()
    strat_names = [n for n, _ in strategies]

    # results[strat_name][num_entries][season][bb_label] = sim_result
    results: dict = {nm: {} for nm in strat_names}

    total_runs = len(strategies) * len(ENTRY_COUNTS) * len(SEASONS) * len(BUYBACK_CONFIGS)
    run_num = 0

    for strat_name, run_fn in strategies:
        results[strat_name] = {}
        for num_entries in ENTRY_COUNTS:
            results[strat_name][num_entries] = {}
            for season in SEASONS:
                results[strat_name][num_entries][season] = {}
                for bb_label, bb_end in BUYBACK_CONFIGS:
                    run_num += 1
                    sys.stdout.write(
                        f"\r  [{run_num:3d}/{total_runs}] {strat_name[:32]:<32} "
                        f"n={num_entries:2d} {season} {bb_label}"
                    )
                    sys.stdout.flush()
                    r = run_fn(season_data[season], num_entries, bb_end)
                    results[strat_name][num_entries][season][bb_label] = r

    print(f"\r  All {total_runs} runs complete.{'':60}")
    print()

    # ── Console Output ─────────────────────────────────────────────────────
    print("=" * 120)
    print("RESULTS SUMMARY — No Buyback, All Entry Counts")
    print("=" * 120)

    for num_entries in ENTRY_COUNTS:
        max_5 = num_entries * TOTAL_WEEKS * 5
        print(f"\n--- n={num_entries} (max {max_5} entry-weeks across 5 seasons) ---")
        print(f"{'Strategy':<35} {'2021':>6} {'2022':>6} {'2023':>6} {'2024':>6} {'2025':>6} "
              f"{'TOTAL':>7} {'SD':>5} {'Eff%':>6}")
        print("-" * 95)

        rows = []
        for nm in strat_names:
            vals = [results[nm][num_entries][s]["No Buyback"]['entry_weeks'] for s in SEASONS]
            total = sum(vals)
            sd = std_dev(vals)
            eff = total / max_5 * 100
            rows.append((total, nm, vals, sd, eff))
        rows.sort(reverse=True)

        blend_total = sum(results["70/30 Blend"][num_entries][s]["No Buyback"]['entry_weeks']
                          for s in SEASONS)

        for total, nm, vals, sd, eff in rows:
            v_str = " ".join(f"{v:>6}" for v in vals)
            marker = " ◄" if total == rows[0][0] else ""
            print(f"  {nm:<33} {v_str} {total:>7} {sd:>5.1f} {eff:>5.1f}%{marker}")

    print()
    print("=" * 120)
    print("BUYBACK IMPACT — Wk1-3, All Entry Counts (5-season totals)")
    print("=" * 120)

    for num_entries in ENTRY_COUNTS:
        print(f"\n--- n={num_entries} ---")
        print(f"{'Strategy':<35} {'No BB':>8} {'BB Wk1-3':>10} {'Δ':>6} {'BB Wk1-4':>10} {'Δ':>6}")
        print("-" * 75)

        rows = []
        for nm in strat_names:
            no_bb = sum(results[nm][num_entries][s]["No Buyback"]['entry_weeks'] for s in SEASONS)
            bb3 = sum(results[nm][num_entries][s]["Buyback Wk1-3"]['entry_weeks'] for s in SEASONS)
            bb4 = sum(results[nm][num_entries][s]["Buyback Wk1-4"]['entry_weeks'] for s in SEASONS)
            rows.append((bb3, nm, no_bb, bb3, bb4))
        rows.sort(reverse=True)

        for _, nm, no_bb, bb3, bb4 in rows:
            d3 = bb3 - no_bb
            d4 = bb4 - no_bb
            print(f"  {nm:<33} {no_bb:>8} {bb3:>10} {d3:>+6} {bb4:>10} {d4:>+6}")

    # ── Winner Summary ─────────────────────────────────────────────────────
    print()
    print("=" * 120)
    print("WINNER SUMMARY")
    print("=" * 120)

    for num_entries in ENTRY_COUNTS:
        print(f"\nn={num_entries}:")
        for bb_label, _ in BUYBACK_CONFIGS:
            best = max(strat_names, key=lambda nm: sum(
                results[nm][num_entries][s][bb_label]['entry_weeks'] for s in SEASONS))
            best_val = sum(results[best][num_entries][s][bb_label]['entry_weeks'] for s in SEASONS)
            print(f"  {bb_label:<18} → {best} ({best_val})")

    # ── Consistency Analysis ───────────────────────────────────────────────
    print()
    print("=" * 120)
    print("CONSISTENCY ANALYSIS — n=10, No Buyback (SD across 5 seasons)")
    print("=" * 120)
    print(f"{'Rank':<5} {'Strategy':<35} {'Total':>7} {'Avg':>6} {'SD':>6} {'CV':>7}")
    print("-" * 65)
    rows = []
    for nm in strat_names:
        vals = [results[nm][10][s]["No Buyback"]['entry_weeks'] for s in SEASONS]
        total = sum(vals)
        avg = total / 5
        sd = std_dev(vals)
        cv = sd / avg if avg > 0 else 0
        rows.append((sd, nm, total, avg, cv))
    rows.sort()
    for rank, (sd, nm, total, avg, cv) in enumerate(rows, 1):
        print(f"  {rank:<4} {nm:<35} {total:>7} {avg:>6.1f} {sd:>6.1f} {cv:>7.3f}")

    # ── Save JSON Results ──────────────────────────────────────────────────
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    serializable = {}
    for nm in strat_names:
        serializable[nm] = {}
        for n in ENTRY_COUNTS:
            serializable[nm][str(n)] = {}
            for season in SEASONS:
                serializable[nm][str(n)][str(season)] = {}
                for bb_label, _ in BUYBACK_CONFIGS:
                    r = results[nm][n][season][bb_label]
                    serializable[nm][str(n)][str(season)][bb_label] = r

    with open(RESULTS_PATH, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    # ── Generate Report ────────────────────────────────────────────────────
    print("Generating research report...")
    report = generate_report(results, strategies)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        f.write(report)
    print(f"Report saved: {REPORT_PATH}")

    print()
    print("=" * 120)
    print("SIMULATION COMPLETE")
    print("=" * 120)


if __name__ == "__main__":
    main()
