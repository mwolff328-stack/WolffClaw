#!/usr/bin/env python3
"""
Stan the Scout: Game Context Filters Simulation — Round 9

Research questions:
  Do post-scoring game context filters (avoid divisional / prefer home) improve survival?
  4 base strategies × 7 filter modes × 4 entry counts × 3 seasons = 336 runs

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
"""

import json
import os
import sys
import urllib.request

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
GAMES_2025_CACHE = os.path.join(DATA_DIR, "nfl_games_2025_games_cache.json")  # raw games with home/away
PICKS_2025_CACHE = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")        # existing picks/wp cache
BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]
SEASONS = [2023, 2024, 2025]

# ── NFL Division Lookup (exact team IDs from data files) ──────────────────────

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

# Build reverse lookup: teamId -> division name
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

def load_local_season(season: int) -> dict:
    """Load 2023/2024 local JSON files and enrich with game context."""
    with open(os.path.join(DATA_DIR, f"nfl_games_{season}.json")) as f:
        games = json.load(f)
    with open(os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data: dict = {}
    for week in range(1, TOTAL_WEEKS + 1):
        week_games = [g for g in games if g["week"] == week]
        week_picks = picks_data.get("weeks", {}).get(str(week), {}).get("teams", [])
        pick_shares = {p["teamId"]: p.get("average", 0) for p in week_picks}

        teams = []
        for g in week_games:
            home, away = g["homeTeamId"], g["awayTeamId"]
            hwp = float(g["homeWinProbability"])
            awp = float(g["awayWinProbability"])
            completed = g.get("completed", False)
            hs, as_ = g.get("homeScore"), g.get("awayScore")
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

        # Fetch raw games to get home/away
        games = fetch_json(
            f"{BASE_URL}/api/games?season=2025&scheduleType=regular&week={week}"
        )
        if not games:
            # No home/away data available — mark as unknown
            for t in cached_teams:
                t["is_home"] = None
                t["opponent_id"] = None
                t["is_divisional"] = None
            all_week_data[week] = cached_teams
            continue

        # Build game context lookup: teamId -> {is_home, opponent_id, is_divisional}
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


BASE_STRATEGIES = [
    ("70/30 Blend",       score_blend_7030),
    ("SP Production",     score_sp_production),
    ("SP Conservative",   score_sp_conservative),
    # Core/Satellite handled separately in simulation (mixed scorers)
]

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
    """
    scored_teams: list of (base_score, team_dict) sorted desc by base_score.
    Returns reordered/rescored list based on filter mode.
    """
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
            return scored_teams  # Top pick is non-divisional, no swap needed
        # Find best non-divisional alternative within 15% of top score
        threshold = top_score * 0.85
        for score, t in scored_teams[1:]:
            if not t.get("is_divisional") and score >= threshold:
                # Swap: put this non-div team first, keep rest in order
                rest = [(s, tm) for s, tm in scored_teams if tm["teamId"] != t["teamId"]]
                return [(score, t)] + rest
        return scored_teams  # No good alternative, keep original

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
            return scored_teams  # Already home team, no swap
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
        # Tier priority: non-div home > non-div road > div home > div road
        # Within tier, rank by base score. Only drop tier if no alt within 20% of top.
        if not scored_teams:
            return scored_teams

        def tier(t):
            is_div = bool(t.get("is_divisional"))
            is_home = bool(t.get("is_home"))
            if not is_div and is_home:
                return 0  # best
            if not is_div and not is_home:
                return 1
            if is_div and is_home:
                return 2
            return 3  # div + road = worst

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
    """
    Greedy survivor simulation with optional game context filters.

    Returns:
      entry_weeks: total accumulated entry-weeks survived
      final_elim: week last entry died
      picks_log: list of {week, entry, teamId, score, outcome, is_home, is_divisional}
    """
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

            # Score with base strategy
            base_scored = [(scorer(t, week_data, week), t) for t in available]
            base_scored.sort(key=lambda x: x[0], reverse=True)

            # Apply game context filter
            filtered = apply_filter(base_scored, filter_mode)

            best_score, best = filtered[0]

            assigned.add(best["teamId"])
            used_teams[i].add(best["teamId"])

            picks_log.append({
                "week": week,
                "entry": i,
                "teamId": best["teamId"],
                "base_score": base_scored[0][0],  # original top score (before filter)
                "filtered_score": best_score,
                "outcome": best.get("outcome"),
                "is_home": best.get("is_home"),
                "is_divisional": best.get("is_divisional"),
                "filter_swapped": base_scored[0][1]["teamId"] != best["teamId"],
            })

        # Resolve outcomes
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
    """Compute per-category win rates and filter swap stats."""
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
                swap_beneficial += 1  # swapped away from a loss (beneficial — avoided the bad pick)
            else:
                swap_costly += 1  # swapped away from original but new pick also lost

    def wr(w, l):
        total = w + l
        return w / total if total > 0 else None

    return {
        "div_win_rate": wr(divisional_wins, divisional_losses),
        "non_div_win_rate": wr(non_div_wins, non_div_losses),
        "home_win_rate": wr(home_wins, home_losses),
        "road_win_rate": wr(road_wins, road_losses),
        "swap_count": swap_beneficial + swap_costly,
        "swap_beneficial": swap_beneficial,
        "swap_costly": swap_costly,
        "swap_beneficial_pct": wr(swap_beneficial, swap_costly),
    }


def std_dev(vals: list) -> float:
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# ── Results Storage ───────────────────────────────────────────────────────────

class ResultStore:
    def __init__(self):
        self.rows = []  # list of result dicts
        # Aggregated stats per (strategy, filter, n) across seasons
        self.agg = {}
        # Hypothesis validation stats per (strategy, filter, n) per season
        self.hyp = {}
        # Filter swap opportunity cost
        self.swap_stats = {}

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
            **{k: v for k, v in stats.items() if k != "swap_count"},
        }
        self.rows.append(row)

        key = (strategy, filter_mode, n)
        if key not in self.agg:
            self.agg[key] = []
        self.agg[key].append(ew)

        hyp_key = (strategy, filter_mode, n, season)
        self.hyp[hyp_key] = stats

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
    print("STAN: GAME CONTEXT FILTERS SIMULATION — Round 9")
    print("4 base strategies × 7 filter modes × 4 entry counts × 3 seasons = 336 runs")
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

    # Build strategy list including Core/Satellite
    strategies_to_run = [
        ("70/30 Blend",     score_blend_7030,    False),
        ("SP Production",   score_sp_production, False),
        ("Core/Satellite",  None,                True),   # handled via is_core_satellite flag
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
                season_results = []
                for season in SEASONS:
                    result = simulate(
                        scorer,
                        season_data[season],
                        n,
                        filter_mode,
                        is_core_satellite=is_cs,
                    )
                    store.add(strat_name, filter_mode, n, season, result)
                    season_results.append(result["entry_weeks"])
                    run_count += 1

                if run_count % 28 == 0:
                    pct = run_count / total_runs * 100
                    sys.stdout.write(f"\r  Progress: {run_count}/{total_runs} ({pct:.0f}%)...")
                    sys.stdout.flush()

    print(f"\r  Complete: {run_count}/{total_runs} runs finished.          ")
    print()

    # ── Report ────────────────────────────────────────────────────────────────

    # Section 1: Main results table — entry-weeks by strategy, filter, entry count
    print("=" * 120)
    print("SECTION 1: ENTRY-WEEKS RESULTS — Avg across 3 seasons (2023-2025)")
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

    # Section 2: Filter delta vs control (No Filter baseline)
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

    # Section 3: Best filter per strategy per entry count (ranked)
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

    # Section 4: Per-season breakdown (filter impact by season)
    print("=" * 120)
    print("SECTION 4: FILTER IMPACT BY SEASON (70/30 Blend, n=10)")
    print("=" * 120)
    print()

    strat = "70/30 Blend"
    n = 10
    print(f"  {'Filter Mode':<28}  {'2023':>8}  {'2024':>8}  {'2025':>8}")
    print(f"  {'-'*28}  {'-'*8}  {'-'*8}  {'-'*8}")
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

    # Section 5: Hypothesis validation — divisional upset rate and home win rate
    print("=" * 120)
    print("SECTION 5: HYPOTHESIS VALIDATION")
    print("=" * 120)
    print()

    # Aggregate hypothesis stats from No Filter control runs across all configs
    div_wins = div_losses = non_div_wins = non_div_losses = 0
    home_wins = home_losses = road_wins = road_losses = 0

    for row in store.rows:
        if row["filter"] != "No Filter":
            continue
        dwr = row.get("div_win_rate")
        ndwr = row.get("non_div_win_rate")
        hwr = row.get("home_win_rate")
        rwr = row.get("road_win_rate")

    # Better: run a dedicated aggregation pass over No Filter rows
    div_wr_vals = [r["div_win_rate"] for r in store.rows
                   if r["filter"] == "No Filter" and r["div_win_rate"] is not None]
    non_div_wr_vals = [r["non_div_win_rate"] for r in store.rows
                       if r["filter"] == "No Filter" and r["non_div_win_rate"] is not None]
    home_wr_vals = [r["home_win_rate"] for r in store.rows
                    if r["filter"] == "No Filter" and r["home_win_rate"] is not None]
    road_wr_vals = [r["road_win_rate"] for r in store.rows
                    if r["filter"] == "No Filter" and r["road_win_rate"] is not None]

    avg_div_wr = sum(div_wr_vals) / len(div_wr_vals) if div_wr_vals else 0
    avg_non_div_wr = sum(non_div_wr_vals) / len(non_div_wr_vals) if non_div_wr_vals else 0
    avg_home_wr = sum(home_wr_vals) / len(home_wr_vals) if home_wr_vals else 0
    avg_road_wr = sum(road_wr_vals) / len(road_wr_vals) if road_wr_vals else 0

    print(f"  H1: Divisional games are more volatile (lower win rates)")
    print(f"    Divisional picks win rate:     {avg_div_wr*100:.1f}%")
    print(f"    Non-divisional picks win rate: {avg_non_div_wr*100:.1f}%")
    div_gap = (avg_non_div_wr - avg_div_wr) * 100
    sign = "+" if div_gap >= 0 else ""
    print(f"    Gap (non-div minus div):       {sign}{div_gap:.1f}pp")
    print(f"    Hypothesis {'SUPPORTED' if avg_div_wr < avg_non_div_wr else 'NOT SUPPORTED'}")
    print()
    print(f"  H2: Home teams win more often")
    print(f"    Home picks win rate:  {avg_home_wr*100:.1f}%")
    print(f"    Road picks win rate:  {avg_road_wr*100:.1f}%")
    home_gap = (avg_home_wr - avg_road_wr) * 100
    sign = "+" if home_gap >= 0 else ""
    print(f"    Gap (home minus road): {sign}{home_gap:.1f}pp")
    print(f"    Hypothesis {'SUPPORTED' if avg_home_wr > avg_road_wr else 'NOT SUPPORTED'}")
    print()

    # Section 6: Per-season hypothesis validation
    print("=" * 120)
    print("SECTION 6: HYPOTHESIS VALIDATION BY SEASON")
    print("=" * 120)
    print()
    print(f"  {'Season':<8}  {'Div WR':>8}  {'Non-Div WR':>10}  {'Gap':>6}  {'Home WR':>8}  {'Road WR':>8}  {'Gap':>6}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*10}  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*6}")
    for season in SEASONS:
        season_rows = [r for r in store.rows if r["season"] == season and r["filter"] == "No Filter"]
        dw = [r["div_win_rate"] for r in season_rows if r["div_win_rate"] is not None]
        ndw = [r["non_div_win_rate"] for r in season_rows if r["non_div_win_rate"] is not None]
        hw = [r["home_win_rate"] for r in season_rows if r["home_win_rate"] is not None]
        rw = [r["road_win_rate"] for r in season_rows if r["road_win_rate"] is not None]
        div_wr = sum(dw)/len(dw) if dw else 0
        ndiv_wr = sum(ndw)/len(ndw) if ndw else 0
        hm_wr = sum(hw)/len(hw) if hw else 0
        rd_wr = sum(rw)/len(rw) if rw else 0
        dgap = ndiv_wr - div_wr
        hgap = hm_wr - rd_wr
        print(f"  {season:<8}  {div_wr*100:>7.1f}%  {ndiv_wr*100:>9.1f}%  {dgap*100:>+5.1f}pp  {hm_wr*100:>7.1f}%  {rd_wr*100:>7.1f}%  {hgap*100:>+5.1f}pp")
    print()

    # Section 7: Filter swap opportunity cost
    print("=" * 120)
    print("SECTION 7: FILTER SWAP OPPORTUNITY COST")
    print("  (When a filter swaps the top pick, how often did it help vs hurt?)")
    print("=" * 120)
    print()
    print(f"  {'Strategy':<20}  {'Filter':<28}  {'Swaps':>6}  {'Beneficial':>10}  {'Costly':>6}  {'% Beneficial':>12}")
    print(f"  {'-'*20}  {'-'*28}  {'-'*6}  {'-'*10}  {'-'*6}  {'-'*12}")

    for strat_name, _, _ in strategies_to_run:
        for filter_mode in FILTER_MODES:
            if filter_mode == "No Filter":
                continue
            relevant = [r for r in store.rows
                        if r["strategy"] == strat_name and r["filter"] == filter_mode]
            total_swaps = sum(r.get("swap_count", r.get("swap_beneficial", 0) + r.get("swap_costly", 0)) for r in relevant)
            beneficial = sum(r.get("swap_beneficial", 0) for r in relevant)
            costly = sum(r.get("swap_costly", 0) for r in relevant)
            total_tracked = beneficial + costly
            pct = beneficial / total_tracked * 100 if total_tracked > 0 else 0
            # A swap is "beneficial" when it avoided a loss — i.e., original pick would have lost
            # but we swapped. But we're tracking the outcome of the NEW pick:
            # beneficial = swapped AND new pick won (avoided bad pick)
            # But we don't actually track original pick outcome here.
            # swap_beneficial = swapped and WON (new pick won)
            # swap_costly = swapped and LOST (new pick also lost)
            # True benefit = swap_beneficial where original would have lost (we can't fully track)
            # Reported pct = % of swaps where the new pick won
            print(f"  {strat_name:<20}  {filter_mode:<28}  {total_tracked:>6}  {beneficial:>10}  {costly:>6}  {pct:>11.1f}%")
    print()
    print("  Note: 'Beneficial' = swap occurred AND new pick won. 'Costly' = swap occurred AND new pick lost.")
    print("  A high beneficial% means filters tend to redirect to winners, not just away from non-divisional/home teams.")
    print()

    # Section 8: Filter interaction with entry count
    print("=" * 120)
    print("SECTION 8: FILTER INTERACTION WITH ENTRY COUNT")
    print("  (Does filter impact grow or shrink at higher N?)")
    print("=" * 120)
    print()
    print(f"  {'Strategy':<20}  {'Filter':<28}  {'n=5':>6}  {'n=10':>6}  {'n=20':>6}  {'n=50':>6}")
    print(f"  {'-'*20}  {'-'*28}  {'-'*6}  {'-'*6}  {'-'*6}  {'-'*6}")

    for strat_name, _, _ in strategies_to_run:
        baselines = {n: store.season_avg(strat_name, "No Filter", n)[0] for n in ENTRY_COUNTS}
        for filter_mode in FILTER_MODES:
            if filter_mode == "No Filter":
                continue
            print(f"  {strat_name:<20}  {filter_mode:<28}", end="")
            for n in ENTRY_COUNTS:
                avg, _ = store.season_avg(strat_name, filter_mode, n)
                delta = avg - baselines[n]
                sign = "+" if delta >= 0 else ""
                print(f"  {sign}{delta:>4.1f}", end="")
            print()
    print()

    # Section 9: Overall champion per entry count
    print("=" * 120)
    print("SECTION 9: OVERALL CHAMPION — Best Strategy+Filter combo per entry count")
    print("=" * 120)
    print()

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
        print(f"  n={n}: {best_combo[0]} + {best_combo[1]} → {best_avg:.1f} entry-weeks "
              f"(vs No Filter: {sign}{lift:.1f})")
    print()

    print("=" * 120)
    print("COMPLETE")
    print("=" * 120)

    return store


if __name__ == "__main__":
    main()
