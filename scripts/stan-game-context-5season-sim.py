#!/usr/bin/env python3
"""
Stan the Scout: Game Context Filters Simulation — 5-Season Expansion

Research questions:
  Do post-scoring game context filters (avoid divisional / prefer home) improve survival?
  4 base strategies × 7 filter modes × 4 entry counts × 5 seasons = 560 runs

Filter modes:
  0. No filter (control)
  1. Avoid divisional (soft: 10% penalty)
  2. Avoid divisional (hard: swap if alt within 15%)
  3. Prefer home (soft: 10% bonus)
  4. Prefer home (hard: swap if alt within 15%)
  5. Both filters combined (soft)
  6. Both filters combined (hard: tiered priority)

Base strategies (Round champions):
  A. 70/30 Blend         — champion at n=5
  B. SP Production       — champion at n=10 (Round 6)
  C. Core/Satellite      — champion at n=10 (Round 7)
  D. SP Conservative     — champion in buyback pools

Seasons: 2021, 2022, 2023, 2024, 2025
"""

import json
import os
import sys
import urllib.request

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
GAMES_2025_CACHE = os.path.join(DATA_DIR, "nfl_games_2025_games_cache.json")
PICKS_2025_CACHE = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]
SEASONS = [2021, 2022, 2023, 2024, 2025]

RESULTS_PATH = os.path.expanduser("~/.openclaw/workspace/scripts/stan-game-context-5season-results.json")

# ── NFL Division Lookup ───────────────────────────────────────────────────────

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


def is_divisional_game(team_id: str, opponent_id: str) -> bool:
    div1 = TEAM_DIVISION.get(team_id)
    div2 = TEAM_DIVISION.get(opponent_id)
    return div1 is not None and div1 == div2


# ── HTTP Helper ───────────────────────────────────────────────────────────────

def fetch_json(url: str, timeout: int = 20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


# ── Data Loading ──────────────────────────────────────────────────────────────

def _normalize_game_record(g: dict) -> dict:
    """Normalize snake_case (2021/2022) or camelCase (2023/2024) game records."""
    return {
        'homeTeamId':        g.get('homeTeamId') or g.get('home_team_id'),
        'awayTeamId':        g.get('awayTeamId') or g.get('away_team_id'),
        'homeWinProbability': float(g.get('homeWinProbability') or g.get('home_win_probability') or 0),
        'awayWinProbability': float(g.get('awayWinProbability') or g.get('away_win_probability') or 0),
        'homeScore':         g.get('homeScore') if g.get('homeScore') is not None else g.get('home_score'),
        'awayScore':         g.get('awayScore') if g.get('awayScore') is not None else g.get('away_score'),
        'completed':         bool(g.get('completed', False)),
        'week':              g.get('week'),
    }


def load_local_season(season: int) -> dict:
    """Load local JSON files (2021-2024) and enrich with game context."""
    with open(os.path.join(DATA_DIR, f"nfl_games_{season}.json")) as f:
        raw_games = json.load(f)
    with open(os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data: dict = {}
    for week in range(1, TOTAL_WEEKS + 1):
        week_games = [_normalize_game_record(g) for g in raw_games if g.get("week") == week]
        week_picks = picks_data.get("weeks", {}).get(str(week), {}).get("teams", [])
        pick_shares = {p["teamId"]: p.get("average", 0) for p in week_picks}

        teams = []
        for g in week_games:
            home = g['homeTeamId']
            away = g['awayTeamId']
            hwp = g['homeWinProbability']
            awp = g['awayWinProbability']
            completed = g['completed']
            hs, as_ = g['homeScore'], g['awayScore']
            ho = ("Win" if hs > as_ else "Loss") if (completed and hs is not None and as_ is not None) else None
            ao = ("Win" if as_ > hs else "Loss") if (completed and hs is not None and as_ is not None) else None

            divisional = is_divisional_game(home, away)

            teams.append({
                "teamId": home,
                "winProbability": hwp,
                "pickShare": pick_shares.get(home, 0),
                "outcome": ho,
                "is_home": True,
                "opponent_id": away,
                "is_divisional": divisional,
            })
            teams.append({
                "teamId": away,
                "winProbability": awp,
                "pickShare": pick_shares.get(away, 0),
                "outcome": ao,
                "is_home": False,
                "opponent_id": home,
                "is_divisional": divisional,
            })
        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025() -> dict:
    """Load 2025 data, fetching raw games if needed to get home/away context."""
    # Check if we already have rich game context cache
    if os.path.exists(GAMES_2025_CACHE):
        print("  2025: Loading from game context cache...")
        with open(GAMES_2025_CACHE) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}

    # Load existing picks/WP cache
    if not os.path.exists(PICKS_2025_CACHE):
        print("  2025: No picks cache found — fetching all data from API...")
        return fetch_2025_full()

    print("  2025: Loading picks cache and fetching game context from API...")
    with open(PICKS_2025_CACHE) as f:
        picks_cache = json.load(f)

    all_week_data: dict = {}
    for week in range(1, TOTAL_WEEKS + 1):
        sys.stdout.write(f"\r  2025: Enriching week {week}/{TOTAL_WEEKS}...")
        sys.stdout.flush()

        cached_teams = picks_cache.get(str(week), [])
        if not cached_teams:
            continue

        games = fetch_json(
            f"{BASE_URL}/api/games?season=2025&scheduleType=regular&week={week}"
        )
        if not games:
            for t in cached_teams:
                t["is_home"] = None
                t["opponent_id"] = None
                t["is_divisional"] = None
            all_week_data[week] = cached_teams
            continue

        ctx = {}
        for g in games:
            home, away = g["homeTeamId"], g["awayTeamId"]
            div = is_divisional_game(home, away)
            ctx[home] = {"is_home": True, "opponent_id": away, "is_divisional": div}
            ctx[away] = {"is_home": False, "opponent_id": home, "is_divisional": div}

        enriched = []
        for t in cached_teams:
            gc = ctx.get(t["teamId"], {})
            enriched.append({
                **t,
                "is_home": gc.get("is_home"),
                "opponent_id": gc.get("opponent_id"),
                "is_divisional": gc.get("is_divisional"),
            })
        all_week_data[week] = enriched

    print(f"\r  2025: Enriched {len(all_week_data)} weeks.          ")
    with open(GAMES_2025_CACHE, "w") as f:
        json.dump(all_week_data, f)
    print(f"  2025: Cached to {GAMES_2025_CACHE}")
    return all_week_data


def fetch_2025_full() -> dict:
    """Fetch 2025 data completely fresh from API."""
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
        if not games:
            continue

        pick_shares = {}
        if dynamics:
            pick_shares = {
                t["teamId"]: t.get("pickShare", 0)
                for t in dynamics.get("teamDynamics", [])
            }

        teams = []
        for g in games:
            hwp = float(g["homeWinProbability"]) if g.get("homeWinProbability") else 0
            awp = float(g["awayWinProbability"]) if g.get("awayWinProbability") else 0
            completed = g.get("completed", False)
            hs, as_ = g.get("homeScore"), g.get("awayScore")
            ho = ("Win" if hs > as_ else "Loss") if (completed and hs is not None and as_ is not None) else None
            ao = ("Win" if as_ > hs else "Loss") if (completed and hs is not None and as_ is not None) else None
            home, away = g["homeTeamId"], g["awayTeamId"]
            div = is_divisional_game(home, away)
            teams.append({
                "teamId": home, "winProbability": hwp,
                "pickShare": pick_shares.get(home, 0), "outcome": ho,
                "is_home": True, "opponent_id": away, "is_divisional": div,
            })
            teams.append({
                "teamId": away, "winProbability": awp,
                "pickShare": pick_shares.get(away, 0), "outcome": ao,
                "is_home": False, "opponent_id": home, "is_divisional": div,
            })
        if teams:
            all_week_data[week] = teams

    print(f"\r  2025: Loaded {len(all_week_data)} weeks.          ")
    with open(GAMES_2025_CACHE, "w") as f:
        json.dump(all_week_data, f)
    print(f"  2025: Cached to {GAMES_2025_CACHE}")
    return all_week_data


# ── Scoring Primitives ────────────────────────────────────────────────────────

def compute_expendability(team_id: str, current_week: int, all_week_data: dict, lookahead: int = 5) -> float:
    max_future_score = 0.0
    for offset in range(1, lookahead + 1):
        fw = current_week + offset
        if fw > TOTAL_WEEKS:
            break
        ft = next((t for t in all_week_data.get(fw, []) if t["teamId"] == team_id), None)
        if not ft:
            continue
        fs = 0.7 * ft["winProbability"] + 0.3 * (1 - ft["pickShare"] / 100)
        decay = 0.5 ** (offset - 1)
        max_future_score = max(max_future_score, fs * decay)
    return max(0.0, min(1.0, 1.0 - max_future_score))


def blend_score(team: dict, wp_w: float = 70, ps_w: float = 30) -> float:
    return (wp_w / 100) * team["winProbability"] + (ps_w / 100) * (1 - team["pickShare"] / 100)


def sp_production_score(team: dict, all_week_data: dict, week: int) -> float:
    ev = team["winProbability"] - (team["pickShare"] / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team["teamId"], week, all_week_data, 5)
    fv = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * fv


def sp_conservative_score(team: dict, all_week_data: dict, week: int) -> float:
    base = blend_score(team, 65, 25)
    exp = compute_expendability(team["teamId"], week, all_week_data, 5)
    fv = 1.0 - exp
    return base + 0.10 * fv


# ── Base Strategy Scorers ─────────────────────────────────────────────────────

def score_blend_7030(team, all_week_data, week):
    return blend_score(team, 70, 30)


def score_sp_production(team, all_week_data, week):
    return sp_production_score(team, all_week_data, week)


def score_sp_conservative(team, all_week_data, week):
    return sp_conservative_score(team, all_week_data, week)


FILTER_MODES = [
    "No Filter",
    "Avoid Div (Soft)",
    "Avoid Div (Hard)",
    "Prefer Home (Soft)",
    "Prefer Home (Hard)",
    "Both (Soft)",
    "Both (Hard)",
]


# ── Filter Application ────────────────────────────────────────────────────────

def apply_filter(scored_teams: list, filter_mode: str) -> list:
    if filter_mode == "No Filter":
        return scored_teams

    if filter_mode == "Avoid Div (Soft)":
        adjusted = []
        for score, t in scored_teams:
            mult = 0.90 if t.get("is_divisional") else 1.0
            adjusted.append((score * mult, t))
        return sorted(adjusted, key=lambda x: x[0], reverse=True)

    if filter_mode == "Avoid Div (Hard)":
        if not scored_teams:
            return scored_teams
        top_score, top_team = scored_teams[0]
        if not top_team.get("is_divisional"):
            return scored_teams
        threshold = top_score * 0.85
        for score, t in scored_teams[1:]:
            if not t.get("is_divisional") and score >= threshold:
                rest = [(s, tm) for s, tm in scored_teams if tm["teamId"] != t["teamId"]]
                return [(score, t)] + rest
        return scored_teams

    if filter_mode == "Prefer Home (Soft)":
        adjusted = []
        for score, t in scored_teams:
            mult = 1.10 if t.get("is_home") else 1.0
            adjusted.append((score * mult, t))
        return sorted(adjusted, key=lambda x: x[0], reverse=True)

    if filter_mode == "Prefer Home (Hard)":
        if not scored_teams:
            return scored_teams
        top_score, top_team = scored_teams[0]
        if top_team.get("is_home"):
            return scored_teams
        threshold = top_score * 0.85
        for score, t in scored_teams[1:]:
            if t.get("is_home") and score >= threshold:
                rest = [(s, tm) for s, tm in scored_teams if tm["teamId"] != t["teamId"]]
                return [(score, t)] + rest
        return scored_teams

    if filter_mode == "Both (Soft)":
        adjusted = []
        for score, t in scored_teams:
            div_mult = 0.90 if t.get("is_divisional") else 1.0
            home_mult = 1.10 if t.get("is_home") else 1.0
            adjusted.append((score * div_mult * home_mult, t))
        return sorted(adjusted, key=lambda x: x[0], reverse=True)

    if filter_mode == "Both (Hard)":
        if not scored_teams:
            return scored_teams

        def tier(t):
            is_div = bool(t.get("is_divisional"))
            is_home = bool(t.get("is_home"))
            if not is_div and is_home:
                return 0
            if not is_div and not is_home:
                return 1
            if is_div and is_home:
                return 2
            return 3

        top_score = scored_teams[0][0]
        threshold = top_score * 0.80
        eligible = [(s, t) for s, t in scored_teams if s >= threshold]
        if not eligible:
            return scored_teams

        eligible_sorted = sorted(eligible, key=lambda x: (tier(x[1]), -x[0]))
        best = eligible_sorted[0]
        rest = [(s, t) for s, t in scored_teams if t["teamId"] != best[1]["teamId"]]
        return [best] + rest

    return scored_teams


# ── Core Simulation Engine ────────────────────────────────────────────────────

def simulate(
    base_scorer_or_list,
    week_data: dict,
    num_entries: int,
    filter_mode: str,
    is_core_satellite: bool = False,
) -> dict:
    if is_core_satellite:
        n_core = round(num_entries * 0.6)
        n_sat = num_entries - n_core
        scorers = ([score_blend_7030] * n_core) + ([score_sp_production] * n_sat)
    elif callable(base_scorer_or_list):
        scorers = [base_scorer_or_list] * num_entries
    else:
        scorers = list(base_scorer_or_list)

    while len(scorers) < num_entries:
        scorers.append(scorers[len(scorers) % len(scorers)])

    alive = set(range(num_entries))
    used_teams = [set() for _ in range(num_entries)]
    entry_weeks = 0
    final_elim_week = None
    picks_log = []

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned: set = set()

        for i in sorted(alive):
            scorer = scorers[i]
            available = [t for t in teams
                         if t["teamId"] not in assigned and t["teamId"] not in used_teams[i]]
            if not available:
                available = [t for t in teams if t["teamId"] not in used_teams[i]]
            if not available:
                continue

            base_scored = [(scorer(t, week_data, week), t) for t in available]
            base_scored.sort(key=lambda x: x[0], reverse=True)

            filtered = apply_filter(base_scored, filter_mode)
            best_score, best = filtered[0]

            assigned.add(best["teamId"])
            used_teams[i].add(best["teamId"])

            picks_log.append({
                "week": week,
                "entry": i,
                "teamId": best["teamId"],
                "base_score": base_scored[0][0],
                "filtered_score": best_score,
                "outcome": best.get("outcome"),
                "is_home": best.get("is_home"),
                "is_divisional": best.get("is_divisional"),
                "filter_swapped": base_scored[0][1]["teamId"] != best["teamId"],
            })

        newly_eliminated = set()
        week_picks = {p["entry"]: p for p in picks_log if p["week"] == week}
        for i in sorted(alive):
            p = week_picks.get(i)
            if p and p["outcome"] == "Loss":
                newly_eliminated.add(i)
            elif p and p["outcome"] == "Win":
                entry_weeks += 1

        for i in newly_eliminated:
            alive.discard(i)

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {
        "entry_weeks": entry_weeks,
        "final_elim": final_elim_week,
        "picks_log": picks_log,
    }


# ── Analysis Helpers ──────────────────────────────────────────────────────────

def analyze_picks_log(picks_log: list) -> dict:
    divisional_wins = divisional_losses = 0
    non_div_wins = non_div_losses = 0
    home_wins = home_losses = 0
    road_wins = road_losses = 0
    swap_beneficial = swap_costly = 0

    for p in picks_log:
        outcome = p.get("outcome")
        if outcome is None:
            continue
        won = outcome == "Win"

        if p.get("is_divisional") is True:
            if won:
                divisional_wins += 1
            else:
                divisional_losses += 1
        elif p.get("is_divisional") is False:
            if won:
                non_div_wins += 1
            else:
                non_div_losses += 1

        if p.get("is_home") is True:
            if won:
                home_wins += 1
            else:
                home_losses += 1
        elif p.get("is_home") is False:
            if won:
                road_wins += 1
            else:
                road_losses += 1

        if p.get("filter_swapped"):
            if won:
                swap_beneficial += 1
            else:
                swap_costly += 1

    def wr(w, l):
        total = w + l
        return w / total if total > 0 else None

    return {
        "div_wins": divisional_wins,
        "div_losses": divisional_losses,
        "non_div_wins": non_div_wins,
        "non_div_losses": non_div_losses,
        "home_wins": home_wins,
        "home_losses": home_losses,
        "road_wins": road_wins,
        "road_losses": road_losses,
        "div_win_rate": wr(divisional_wins, divisional_losses),
        "non_div_win_rate": wr(non_div_wins, non_div_losses),
        "home_win_rate": wr(home_wins, home_losses),
        "road_win_rate": wr(road_wins, road_losses),
        "swap_beneficial": swap_beneficial,
        "swap_costly": swap_costly,
    }


def std_dev(vals: list) -> float:
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# ── Results Storage ───────────────────────────────────────────────────────────

class ResultStore:
    def __init__(self):
        self.rows = []
        self.agg = {}

    def add(self, strategy, filter_mode, n, season, result):
        ew = result["entry_weeks"]
        log = result["picks_log"]
        stats = analyze_picks_log(log)

        row = {
            "strategy": strategy,
            "filter": filter_mode,
            "n": n,
            "season": season,
            "entry_weeks": ew,
            "final_elim": result["final_elim"],
            **stats,
        }
        self.rows.append(row)

        key = (strategy, filter_mode, n)
        if key not in self.agg:
            self.agg[key] = []
        self.agg[key].append(ew)

    def season_avg(self, strategy, filter_mode, n):
        key = (strategy, filter_mode, n)
        vals = self.agg.get(key, [])
        if not vals:
            return 0, 0
        avg = sum(vals) / len(vals)
        sd = std_dev(vals)
        return avg, sd


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 120)
    print("STAN: GAME CONTEXT FILTERS SIMULATION — 5-SEASON EXPANSION")
    print("4 base strategies × 7 filter modes × 4 entry counts × 5 seasons = 560 runs")
    print("=" * 120)
    print()

    # Load all season data
    print("Loading season data...")
    season_data = {}
    for season in SEASONS:
        print(f"  Loading {season}...")
        if season == 2025:
            season_data[season] = load_2025()
        else:
            season_data[season] = load_local_season(season)
        total_games = sum(len(v) // 2 for v in season_data[season].values())
        print(f"  {season}: {len(season_data[season])} weeks, {total_games} games loaded.")
    print()

    # Verify division lookups
    unknown_teams = set()
    for season, wd in season_data.items():
        for week, teams in wd.items():
            for t in teams:
                if t["teamId"] not in TEAM_DIVISION:
                    unknown_teams.add(t["teamId"])
    if unknown_teams:
        print(f"WARNING: Teams not in division lookup: {sorted(unknown_teams)}")
    else:
        print("Division lookup: all teams resolved correctly.")
    print()

    strategies_to_run = [
        ("70/30 Blend",     score_blend_7030,      False),
        ("SP Production",   score_sp_production,   False),
        ("Core/Satellite",  None,                  True),
        ("SP Conservative", score_sp_conservative, False),
    ]

    store = ResultStore()
    total_runs = len(strategies_to_run) * len(FILTER_MODES) * len(ENTRY_COUNTS) * len(SEASONS)
    run_count = 0

    print(f"Running {total_runs} simulations...")
    print()

    for strat_name, scorer, is_cs in strategies_to_run:
        for filter_mode in FILTER_MODES:
            for n in ENTRY_COUNTS:
                for season in SEASONS:
                    result = simulate(
                        scorer,
                        season_data[season],
                        n,
                        filter_mode,
                        is_core_satellite=is_cs,
                    )
                    store.add(strat_name, filter_mode, n, season, result)
                    run_count += 1

                if run_count % 20 == 0:
                    pct = run_count / total_runs * 100
                    sys.stdout.write(f"\r  Progress: {run_count}/{total_runs} ({pct:.0f}%)...")
                    sys.stdout.flush()

    print(f"\r  Complete: {run_count}/{total_runs} runs finished.          ")
    print()

    # ── Report ────────────────────────────────────────────────────────────────

    print("=" * 120)
    print("SECTION 1: ENTRY-WEEKS RESULTS — Avg across 5 seasons (2021-2025)")
    print("=" * 120)
    print()

    for strat_name, _, _ in strategies_to_run:
        print(f"  Strategy: {strat_name}")
        print(f"  {'Filter Mode':<28}", end="")
        for n in ENTRY_COUNTS:
            print(f"  n={n:<5}", end="")
        print()
        print(f"  {'-'*28}", end="")
        for _ in ENTRY_COUNTS:
            print(f"  {'-'*7}", end="")
        print()

        for filter_mode in FILTER_MODES:
            print(f"  {filter_mode:<28}", end="")
            for n in ENTRY_COUNTS:
                avg, sd = store.season_avg(strat_name, filter_mode, n)
                print(f"  {avg:>5.1f} ", end="")
            print()
        print()

    print("=" * 120)
    print("SECTION 2: FILTER DELTA vs 'No Filter' BASELINE (+ = improvement)")
    print("=" * 120)
    print()

    for strat_name, _, _ in strategies_to_run:
        print(f"  Strategy: {strat_name}")
        print(f"  {'Filter Mode':<28}", end="")
        for n in ENTRY_COUNTS:
            print(f"  n={n:<5}", end="")
        print()
        print(f"  {'-'*28}", end="")
        for _ in ENTRY_COUNTS:
            print(f"  {'-'*7}", end="")
        print()

        baselines = {n: store.season_avg(strat_name, "No Filter", n)[0] for n in ENTRY_COUNTS}

        for filter_mode in FILTER_MODES:
            if filter_mode == "No Filter":
                continue
            print(f"  {filter_mode:<28}", end="")
            for n in ENTRY_COUNTS:
                avg, _ = store.season_avg(strat_name, filter_mode, n)
                delta = avg - baselines[n]
                sign = "+" if delta >= 0 else ""
                print(f"  {sign}{delta:>4.1f}  ", end="")
            print()
        print()

    print("=" * 120)
    print("SECTION 3: BEST FILTER PER STRATEGY × ENTRY COUNT (top 3)")
    print("=" * 120)
    print()

    for strat_name, _, _ in strategies_to_run:
        print(f"  Strategy: {strat_name}")
        for n in ENTRY_COUNTS:
            ranked = []
            for filter_mode in FILTER_MODES:
                avg, sd = store.season_avg(strat_name, filter_mode, n)
                ranked.append((avg, filter_mode))
            ranked.sort(reverse=True)
            tops = ranked[:3]
            print(f"    n={n}: ", end="")
            for avg, fm in tops:
                marker = " *" if fm == "No Filter" else ""
                print(f"  {fm}{marker} ({avg:.1f})", end=" |")
            print()
        print()

    print("=" * 120)
    print("SECTION 4: PER-SEASON BREAKDOWN (70/30 Blend, n=10)")
    print("=" * 120)
    print()

    strat = "70/30 Blend"
    n = 10
    print(f"  {'Filter Mode':<28}  {'2021':>8}  {'2022':>8}  {'2023':>8}  {'2024':>8}  {'2025':>8}")
    print(f"  {'-'*28}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}")
    for filter_mode in FILTER_MODES:
        print(f"  {filter_mode:<28}", end="")
        for season in SEASONS:
            matching = [r for r in store.rows
                        if r["strategy"] == strat and r["filter"] == filter_mode
                        and r["n"] == n and r["season"] == season]
            ew = matching[0]["entry_weeks"] if matching else 0
            print(f"  {ew:>8.1f}", end="")
        print()
    print()

    print("=" * 120)
    print("SECTION 5: HYPOTHESIS VALIDATION — Win rates across all seasons")
    print("=" * 120)
    print()

    # Aggregate divisional/home win rates from No Filter control runs
    div_wr_vals = [r["div_win_rate"] for r in store.rows
                   if r["filter"] == "No Filter" and r.get("div_win_rate") is not None]
    non_div_wr_vals = [r["non_div_win_rate"] for r in store.rows
                       if r["filter"] == "No Filter" and r.get("non_div_win_rate") is not None]
    home_wr_vals = [r["home_win_rate"] for r in store.rows
                    if r["filter"] == "No Filter" and r.get("home_win_rate") is not None]
    road_wr_vals = [r["road_win_rate"] for r in store.rows
                    if r["filter"] == "No Filter" and r.get("road_win_rate") is not None]

    # Also aggregate raw counts for accurate overall rates
    total_div_wins = sum(r.get("div_wins", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_div_losses = sum(r.get("div_losses", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_non_div_wins = sum(r.get("non_div_wins", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_non_div_losses = sum(r.get("non_div_losses", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_home_wins = sum(r.get("home_wins", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_home_losses = sum(r.get("home_losses", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_road_wins = sum(r.get("road_wins", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)
    total_road_losses = sum(r.get("road_losses", 0) for r in store.rows if r["filter"] == "No Filter" and r["n"] == 10)

    div_wr_raw = total_div_wins / (total_div_wins + total_div_losses) if (total_div_wins + total_div_losses) > 0 else 0
    non_div_wr_raw = total_non_div_wins / (total_non_div_wins + total_non_div_losses) if (total_non_div_wins + total_non_div_losses) > 0 else 0
    home_wr_raw = total_home_wins / (total_home_wins + total_home_losses) if (total_home_wins + total_home_losses) > 0 else 0
    road_wr_raw = total_road_wins / (total_road_wins + total_road_losses) if (total_road_wins + total_road_losses) > 0 else 0

    avg_div_wr = sum(div_wr_vals) / len(div_wr_vals) if div_wr_vals else 0
    avg_non_div_wr = sum(non_div_wr_vals) / len(non_div_wr_vals) if non_div_wr_vals else 0
    avg_home_wr = sum(home_wr_vals) / len(home_wr_vals) if home_wr_vals else 0
    avg_road_wr = sum(road_wr_vals) / len(road_wr_vals) if road_wr_vals else 0

    print(f"  H1: Divisional games are more volatile (lower win rates)")
    print(f"    Divisional picks win rate (raw aggregate, n=10):     {div_wr_raw*100:.1f}%  ({total_div_wins}W / {total_div_losses}L)")
    print(f"    Non-divisional picks win rate (raw aggregate, n=10): {non_div_wr_raw*100:.1f}%  ({total_non_div_wins}W / {total_non_div_losses}L)")
    div_gap = (non_div_wr_raw - div_wr_raw) * 100
    sign = "+" if div_gap >= 0 else ""
    print(f"    Gap (non-div minus div): {sign}{div_gap:.1f}pp")
    print(f"    Hypothesis {'SUPPORTED' if div_wr_raw < non_div_wr_raw else 'NOT SUPPORTED'}")
    print()
    print(f"  H2: Home teams win more often")
    print(f"    Home picks win rate (raw aggregate, n=10):  {home_wr_raw*100:.1f}%  ({total_home_wins}W / {total_home_losses}L)")
    print(f"    Road picks win rate (raw aggregate, n=10):  {road_wr_raw*100:.1f}%  ({total_road_wins}W / {total_road_losses}L)")
    home_gap = (home_wr_raw - road_wr_raw) * 100
    sign = "+" if home_gap >= 0 else ""
    print(f"    Gap (home minus road): {sign}{home_gap:.1f}pp")
    print(f"    Hypothesis {'SUPPORTED' if home_wr_raw > road_wr_raw else 'NOT SUPPORTED'}")
    print()

    print("=" * 120)
    print("SECTION 6: HYPOTHESIS VALIDATION BY SEASON")
    print("=" * 120)
    print()
    print(f"  {'Season':<8}  {'Div WR':>8}  {'Non-Div WR':>10}  {'Gap':>6}  {'Home WR':>8}  {'Road WR':>8}  {'Gap':>6}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*10}  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*6}")
    for season in SEASONS:
        # Use raw aggregated counts for accuracy
        dw = sum(r.get("div_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        dl = sum(r.get("div_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        ndw = sum(r.get("non_div_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        ndl = sum(r.get("non_div_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        hw = sum(r.get("home_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        hl = sum(r.get("home_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        rw = sum(r.get("road_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        rl = sum(r.get("road_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)

        div_wr = dw / (dw + dl) if (dw + dl) > 0 else 0
        ndiv_wr = ndw / (ndw + ndl) if (ndw + ndl) > 0 else 0
        hm_wr = hw / (hw + hl) if (hw + hl) > 0 else 0
        rd_wr = rw / (rw + rl) if (rw + rl) > 0 else 0
        dgap = ndiv_wr - div_wr
        hgap = hm_wr - rd_wr
        print(f"  {season:<8}  {div_wr*100:>7.1f}%  {ndiv_wr*100:>9.1f}%  {dgap*100:>+5.1f}pp  {hm_wr*100:>7.1f}%  {rd_wr*100:>7.1f}%  {hgap*100:>+5.1f}pp")
    print()

    print("=" * 120)
    print("SECTION 7: FILTER SWAP OPPORTUNITY COST")
    print("=" * 120)
    print()
    print(f"  {'Strategy':<20}  {'Filter':<28}  {'Beneficial':>10}  {'Costly':>6}  {'% Beneficial':>12}")
    print(f"  {'-'*20}  {'-'*28}  {'-'*10}  {'-'*6}  {'-'*12}")

    for strat_name, _, _ in strategies_to_run:
        for filter_mode in FILTER_MODES:
            if filter_mode == "No Filter":
                continue
            relevant = [r for r in store.rows
                        if r["strategy"] == strat_name and r["filter"] == filter_mode]
            beneficial = sum(r.get("swap_beneficial", 0) for r in relevant)
            costly = sum(r.get("swap_costly", 0) for r in relevant)
            total_tracked = beneficial + costly
            pct = beneficial / total_tracked * 100 if total_tracked > 0 else 0
            print(f"  {strat_name:<20}  {filter_mode:<28}  {beneficial:>10}  {costly:>6}  {pct:>11.1f}%")
    print()

    print("=" * 120)
    print("SECTION 8: OVERALL CHAMPION — Best Strategy+Filter combo per entry count")
    print("=" * 120)
    print()

    champion_table = {}
    for n in ENTRY_COUNTS:
        best_avg = 0
        best_combo = None
        for strat_name, _, _ in strategies_to_run:
            for filter_mode in FILTER_MODES:
                avg, _ = store.season_avg(strat_name, filter_mode, n)
                if avg > best_avg:
                    best_avg = avg
                    best_combo = (strat_name, filter_mode)

        baseline_avg, _ = store.season_avg(best_combo[0], "No Filter", n) if best_combo else (0, 0)
        lift = best_avg - baseline_avg
        sign = "+" if lift >= 0 else ""
        champion_table[n] = {"strategy": best_combo[0], "filter": best_combo[1],
                              "avg_ew": best_avg, "lift_vs_no_filter": lift}
        print(f"  n={n}: {best_combo[0]} + {best_combo[1]} → {best_avg:.1f} entry-weeks avg "
              f"(vs No Filter: {sign}{lift:.1f})")
    print()

    print("=" * 120)
    print("COMPLETE")
    print("=" * 120)

    # ── Save JSON Results ──────────────────────────────────────────────────────
    serializable_rows = []
    for row in store.rows:
        r = {k: v for k, v in row.items() if k != "picks_log"}
        serializable_rows.append(r)

    output = {
        "meta": {
            "description": "Game context filter simulation — 5 seasons (2021-2025)",
            "runs": total_runs,
            "seasons": SEASONS,
            "entry_counts": ENTRY_COUNTS,
            "filter_modes": FILTER_MODES,
        },
        "rows": serializable_rows,
        "champion_table": {str(k): v for k, v in champion_table.items()},
        "hypothesis": {
            "div_win_rate_raw": round(div_wr_raw, 4),
            "non_div_win_rate_raw": round(non_div_wr_raw, 4),
            "div_gap_pp": round((non_div_wr_raw - div_wr_raw) * 100, 2),
            "home_win_rate_raw": round(home_wr_raw, 4),
            "road_win_rate_raw": round(road_wr_raw, 4),
            "home_gap_pp": round((home_wr_raw - road_wr_raw) * 100, 2),
        },
        "season_hypothesis": {},
    }

    for season in SEASONS:
        dw = sum(r.get("div_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        dl = sum(r.get("div_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        ndw = sum(r.get("non_div_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        ndl = sum(r.get("non_div_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        hw = sum(r.get("home_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        hl = sum(r.get("home_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        rw = sum(r.get("road_wins", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        rl = sum(r.get("road_losses", 0) for r in store.rows if r["season"] == season and r["filter"] == "No Filter" and r["n"] == 10)
        output["season_hypothesis"][str(season)] = {
            "div_wr": round(dw / (dw + dl), 4) if (dw + dl) > 0 else None,
            "non_div_wr": round(ndw / (ndw + ndl), 4) if (ndw + ndl) > 0 else None,
            "home_wr": round(hw / (hw + hl), 4) if (hw + hl) > 0 else None,
            "road_wr": round(rw / (rw + rl), 4) if (rw + rl) > 0 else None,
        }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    return store, output


if __name__ == "__main__":
    main()
