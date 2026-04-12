#!/usr/bin/env python3
"""
Stan the Scout: Buyback Mechanics Simulation (Round 8)

Research questions:
  Part 1: How does each strategy perform with vs without buybacks?
           12 strategies × 4 entry counts × 3 seasons × 3 buyback configs = 432 runs
  Part 2: Do split (buyback-aware) strategies outperform the best non-split with buybacks?
           5 split configs × 4 entry counts × 3 seasons = 60 runs
  Part 3: Buyback ROI — what is the expected return on the buyback investment?
"""

import json
import os
import sys
import urllib.request

DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
CACHE_FILE = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
BASE_URL = "https://survivorpulse.com"
POOL_ID_2025 = "04e2471b-6498-4a59-8a95-c0dc50221457"
TOTAL_WEEKS = 18
ENTRY_COUNTS = [5, 10, 20, 50]
SEASONS = [2023, 2024, 2025]


# ── Data Loading ──────────────────────────────────────────────────────────────

def fetch_json(url, timeout=20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def load_local_season(season: int) -> dict:
    with open(os.path.join(DATA_DIR, f"nfl_games_{season}.json")) as f:
        games = json.load(f)
    with open(os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data: dict = {}
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
            hs, as_ = g.get('homeScore'), g.get('awayScore')
            ho = ('Win' if hs > as_ else 'Loss') if (completed and hs is not None and as_ is not None) else None
            ao = ('Win' if as_ > hs else 'Loss') if (completed and hs is not None and as_ is not None) else None
            teams.append({'teamId': home, 'winProbability': hwp,
                          'pickShare': pick_shares.get(home, 0), 'outcome': ho})
            teams.append({'teamId': away, 'winProbability': awp,
                          'pickShare': pick_shares.get(away, 0), 'outcome': ao})
        if teams:
            all_week_data[week] = teams
    return all_week_data


def load_2025() -> dict:
    if os.path.exists(CACHE_FILE):
        print("  2025: Loading from cache...")
        with open(CACHE_FILE) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}

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
    with open(CACHE_FILE, 'w') as f:
        json.dump(all_week_data, f)
    print(f"  2025: Cached to {CACHE_FILE}")
    return all_week_data


# ── Scoring Primitives ────────────────────────────────────────────────────────

def blend_score(team: dict, wp_w: float, ps_w: float) -> float:
    return (wp_w / 100) * team['winProbability'] + (ps_w / 100) * (1 - team['pickShare'] / 100)


def compute_expendability(team_id: str, current_week: int, all_week_data: dict, lookahead: int = 5) -> float:
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


def sp_production_score(team: dict, all_week_data: dict, week: int, lookahead: int = 5) -> float:
    ev = team['winProbability'] - (team['pickShare'] / 100)
    ev_norm = max(0.0, min(1.0, (ev + 0.5) / 1.5))
    exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
    fv = 1.0 - exp
    return 0.70 * ev_norm + 0.30 * fv


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
    """65/25/10 WP/anti-chalk/FV — conservative SP variant."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 65, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.10 * fv
    return scorer


def make_expendable_first_scorer(lookahead: int = 3):
    """65/25/10 WP/anti-chalk/expendability — burn low-FV teams first."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 65, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, lookahead)
        return base + 0.10 * exp
    return scorer


def make_adaptive_scorer():
    """Adaptive blend: 90/10 week 1 → 50/50 week 18."""
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        progress = (week - 1) / max(1, TOTAL_WEEKS - 1)
        eff_wp = 90 - 40 * progress
        eff_ps = 10 + 40 * progress
        return blend_score(team, eff_wp, eff_ps)
    return scorer


# ── Portfolio Builders ────────────────────────────────────────────────────────

_FIVE_BASE_SCORERS = [
    make_blend_scorer(70, 30),
    make_sp_production_scorer(),
    make_expendable_first_scorer(3),
    make_blend_scorer(80, 20),
    make_pure_wp_scorer(),
]


def make_mixed_portfolio_scorers(num_entries: int) -> list:
    return [_FIVE_BASE_SCORERS[i % 5] for i in range(num_entries)]


def make_core_satellite_scorers(num_entries: int) -> list:
    n_core = round(num_entries * 0.6)
    n_sat = num_entries - n_core
    return [make_blend_scorer(70, 30)] * n_core + [make_sp_production_scorer()] * n_sat


def make_ev_gradient_scorers(num_entries: int) -> list:
    gradient = [(95, 5), (85, 15), (75, 25), (65, 35), (55, 45)]
    per_level = max(1, num_entries // 5)
    scorers = []
    for wp_w, ps_w in gradient:
        scorers.extend([make_blend_scorer(wp_w, ps_w)] * per_level)
    while len(scorers) < num_entries:
        scorers.append(make_blend_scorer(75, 25))
    return scorers[:num_entries]


def make_safety_contrarian_scorers(num_entries: int) -> list:
    n_safe = num_entries // 2
    n_cont = num_entries - n_safe
    return [make_blend_scorer(85, 15)] * n_safe + [make_blend_scorer(55, 45)] * n_cont


# ── Core Simulation Engine WITH Buyback Support ───────────────────────────────

def simulate_with_buyback(
    scorer_or_list,
    week_data: dict,
    num_entries: int,
    buyback_window_end: int = 0,          # 0 = no buybacks
    split_scorer_after=None,  # dict {entry_idx: scorer} to use post-window, or None
) -> dict:
    """
    Sequential greedy survivor simulation with optional buyback mechanics.

    buyback_window_end: last week in which an eliminated entry can buy back.
                        0 = disabled.
    split_scorer_after: optional dict mapping entry_idx -> scorer used from
                        week (buyback_window_end + 1) onward (Part 2 splits).

    Returns:
      entry_weeks: total accumulated entry-weeks survived
      final_elim:  week when last entry died (or "18+")
      buyback_count: number of buyback events used
      buyback_events: list of {entry, week} dicts
      post_buyback_survival: {entry: weeks_survived_after_buyback}
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

    # ROI tracking
    buyback_events = []                        # {entry, week_eliminated, week_returned}
    post_buyback_weeks = {}                    # entry -> weeks survived after buyback week

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            continue

        assigned: set = set()
        picks: dict = {}

        for i in sorted(alive):
            # Select scorer — if post-window split, switch to new scorer
            if split_scorer_after and week > buyback_window_end and i in split_scorer_after:
                scorer = split_scorer_after[i]
            else:
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

        # Resolve outcomes
        newly_eliminated = set()
        for i in sorted(alive):
            p = picks.get(i)
            if p:
                if p['outcome'] == 'Loss':
                    newly_eliminated.add(i)
                else:
                    entry_weeks += 1
                    # Track post-buyback survival
                    if i in post_buyback_weeks:
                        post_buyback_weeks[i] = post_buyback_weeks.get(i, 0) + 1

        for i in newly_eliminated:
            alive.discard(i)

            # Buyback check
            if buyback_window_end > 0 and week <= buyback_window_end and not buyback_used[i]:
                buyback_used[i] = True
                alive.add(i)  # Resurrect — comes back alive next week (no pick this week)
                buyback_events.append({'entry': i, 'week_eliminated': week, 'week_returned': week + 1})
                post_buyback_weeks[i] = 0  # Start counting post-buyback survival

        if not alive and final_elim_week is None:
            final_elim_week = week

    if final_elim_week is None:
        final_elim_week = "18+" if alive else 18

    return {
        'entry_weeks': entry_weeks,
        'final_elim': final_elim_week,
        'buyback_count': sum(buyback_used),
        'buyback_events': buyback_events,
        'post_buyback_weeks': post_buyback_weeks,
    }


# ── Strategy Definitions (Part 1) ────────────────────────────────────────────

PART1_STRATEGIES = [
    ("Pure Win Probability",
     lambda wd, n, bb: simulate_with_buyback(make_pure_wp_scorer(), wd, n, bb)),

    ("70/30 Blend",
     lambda wd, n, bb: simulate_with_buyback(make_blend_scorer(70, 30), wd, n, bb)),

    ("80/20 Blend",
     lambda wd, n, bb: simulate_with_buyback(make_blend_scorer(80, 20), wd, n, bb)),

    ("60/40 Blend",
     lambda wd, n, bb: simulate_with_buyback(make_blend_scorer(60, 40), wd, n, bb)),

    ("SP Production 70EV+30FV",
     lambda wd, n, bb: simulate_with_buyback(make_sp_production_scorer(), wd, n, bb)),

    ("SP Conservative 65/25/10",
     lambda wd, n, bb: simulate_with_buyback(make_sp_conservative_scorer(), wd, n, bb)),

    ("Expendable-First 65/25/10 3wk",
     lambda wd, n, bb: simulate_with_buyback(make_expendable_first_scorer(3), wd, n, bb)),

    ("Adaptive Blend 90/10→50/50",
     lambda wd, n, bb: simulate_with_buyback(make_adaptive_scorer(), wd, n, bb)),

    ("Mixed Portfolio",
     lambda wd, n, bb: simulate_with_buyback(make_mixed_portfolio_scorers(n), wd, n, bb)),

    ("Core/Satellite 60blend+40EV",
     lambda wd, n, bb: simulate_with_buyback(make_core_satellite_scorers(n), wd, n, bb)),

    ("EV Gradient 95/5→55/45",
     lambda wd, n, bb: simulate_with_buyback(make_ev_gradient_scorers(n), wd, n, bb)),

    ("Safety/Contrarian Split",
     lambda wd, n, bb: simulate_with_buyback(make_safety_contrarian_scorers(n), wd, n, bb)),
]

BUYBACK_CONFIGS = [
    ("No Buyback", 0),
    ("Buyback Wk1-3", 3),
    ("Buyback Wk1-4", 4),
]


# ── Split Strategy Definitions (Part 2) ──────────────────────────────────────

def build_split_scorers(num_entries: int, pre_scorer, post_scorer, buyback_window_end: int):
    """
    All entries use pre_scorer during buyback window, post_scorer after.
    Returns (scorers_list, split_scorer_after_dict).
    """
    scorers = [pre_scorer] * num_entries
    split_after = {i: post_scorer for i in range(num_entries)}
    return scorers, split_after


def run_split_strategy(pre_scorer, post_scorer, week_data: dict, num_entries: int, buyback_window_end: int = 3) -> dict:
    scorers, split_after = build_split_scorers(num_entries, pre_scorer, post_scorer, buyback_window_end)
    return simulate_with_buyback(scorers, week_data, num_entries, buyback_window_end, split_after)


PART2_SPLITS = [
    ("A. Aggressive/Safe Split",
     "60/40 during window → 80/20 after",
     lambda wd, n: run_split_strategy(
         make_blend_scorer(60, 40), make_blend_scorer(80, 20), wd, n, 3)),

    ("B. EV/Blend Split",
     "SP Production during window → 70/30 after",
     lambda wd, n: run_split_strategy(
         make_sp_production_scorer(), make_blend_scorer(70, 30), wd, n, 3)),

    ("C. Contrarian/Conservative Split",
     "30/70 WP/anti-chalk during window → SP Conservative after",
     lambda wd, n: run_split_strategy(
         make_blend_scorer(30, 70), make_sp_conservative_scorer(), wd, n, 3)),

    ("D. Expendable/Safe Split",
     "Expendable-First during window → 70/30 after",
     lambda wd, n: run_split_strategy(
         make_expendable_first_scorer(3), make_blend_scorer(70, 30), wd, n, 3)),

    ("E. Max Aggression/Max Safety",
     "20/80 during window → Pure WP after",
     lambda wd, n: run_split_strategy(
         make_blend_scorer(20, 80), make_pure_wp_scorer(), wd, n, 3)),
]


# ── Output Helpers ────────────────────────────────────────────────────────────

def std_dev(vals: list) -> float:
    if len(vals) < 2:
        return 0.0
    avg = sum(vals) / len(vals)
    return (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 130)
    print("STAN: BUYBACK MECHANICS SIMULATION — Round 8")
    print("Part 1: 12 strategies × 4 entry counts × 3 seasons × 3 buyback configs = 432 runs")
    print("Part 2: 5 split configs × 4 entry counts × 3 seasons = 60 runs")
    print("Part 3: Buyback ROI analysis")
    print("=" * 130)
    print()

    # ── Load Data ─────────────────────────────────────────────────────────────
    print("Loading season data...")
    season_data: dict = {}
    for season in [2023, 2024]:
        print(f"  Loading {season}...")
        season_data[season] = load_local_season(season)
        print(f"  {season}: {len(season_data[season])} weeks loaded")
    print("  Loading 2025...")
    season_data[2025] = load_2025()
    print()

    # ── PART 1 ────────────────────────────────────────────────────────────────
    print("=" * 130)
    print("PART 1: BUYBACK BASELINE — All strategies vs all buyback configs")
    print("=" * 130)
    print()

    # Collect all Part 1 results
    # results[strat_name][num_entries][season][bb_label] = sim_result
    p1_results: dict = {}
    total_p1 = len(PART1_STRATEGIES) * len(ENTRY_COUNTS) * len(SEASONS) * len(BUYBACK_CONFIGS)
    run_num = 0

    for strat_name, run_fn in PART1_STRATEGIES:
        p1_results[strat_name] = {}
        for num_entries in ENTRY_COUNTS:
            p1_results[strat_name][num_entries] = {}
            for season in SEASONS:
                p1_results[strat_name][num_entries][season] = {}
                for bb_label, bb_end in BUYBACK_CONFIGS:
                    run_num += 1
                    sys.stdout.write(
                        f"\r  P1 [{run_num:3d}/{total_p1}] {strat_name[:35]:<35} "
                        f"n={num_entries:2d} {season} {bb_label}"
                    )
                    sys.stdout.flush()
                    r = run_fn(season_data[season], num_entries, bb_end)
                    p1_results[strat_name][num_entries][season][bb_label] = r

    print(f"\r  All {total_p1} Part 1 runs complete.{'':60}")
    print()

    # Print Part 1 tables — one table per entry count
    strat_names_p1 = [n for n, _ in PART1_STRATEGIES]

    for num_entries in ENTRY_COUNTS:
        max_possible = num_entries * TOTAL_WEEKS
        print("=" * 130)
        print(f"PART 1 — n={num_entries}  (max possible per season: {max_possible}, per 3 seasons: {max_possible * 3})")
        print("=" * 130)
        hdr = (f"{'Strategy':<35} {'No Buyback':>11} {'BB Wk1-3':>10} {'BB Wk1-4':>10} "
               f"{'Δ(Wk1-3)':>10} {'Δ(Wk1-4)':>10} {'BB%':>6}")
        print(hdr)
        print("-" * 130)

        rows = []
        for name in strat_names_p1:
            no_bb_total = sum(
                p1_results[name][num_entries][s]["No Buyback"]['entry_weeks']
                for s in SEASONS
            )
            bb3_total = sum(
                p1_results[name][num_entries][s]["Buyback Wk1-3"]['entry_weeks']
                for s in SEASONS
            )
            bb4_total = sum(
                p1_results[name][num_entries][s]["Buyback Wk1-4"]['entry_weeks']
                for s in SEASONS
            )
            delta3 = bb3_total - no_bb_total
            delta4 = bb4_total - no_bb_total
            # BB% = how much does buyback improve performance (relative)
            bb_pct = (delta3 / no_bb_total * 100) if no_bb_total > 0 else 0.0
            rows.append((bb3_total, name, no_bb_total, bb3_total, bb4_total, delta3, delta4, bb_pct))

        rows.sort(key=lambda x: x[0], reverse=True)
        for _, name, no_bb, bb3, bb4, d3, d4, bb_pct in rows:
            d3_str = f"+{d3}" if d3 >= 0 else str(d3)
            d4_str = f"+{d4}" if d4 >= 0 else str(d4)
            print(f"  {name:<33} {no_bb:>11} {bb3:>10} {bb4:>10} "
                  f"{d3_str:>10} {d4_str:>10} {bb_pct:>5.1f}%")
        print()

    # Per-season breakdown for top strategies
    print("=" * 130)
    print("PART 1 — Per-Season Detail: 70/30 Blend and Core/Satellite (Best n=5 and n=10 from Round 7)")
    print("=" * 130)
    for highlight in ["70/30 Blend", "Core/Satellite 60blend+40EV"]:
        print(f"\n  Strategy: {highlight}")
        print(f"  {'':8} {'No Buyback':>11} {'BB Wk1-3':>10} {'BB Wk1-4':>10} {'Δ(Wk1-3)':>10}")
        for num_entries in ENTRY_COUNTS:
            for season in SEASONS:
                no_bb = p1_results[highlight][num_entries][season]["No Buyback"]['entry_weeks']
                bb3 = p1_results[highlight][num_entries][season]["Buyback Wk1-3"]['entry_weeks']
                bb4 = p1_results[highlight][num_entries][season]["Buyback Wk1-4"]['entry_weeks']
                d3 = bb3 - no_bb
                d3_str = f"+{d3}" if d3 >= 0 else str(d3)
                print(f"  n={num_entries:2d} {season}  {no_bb:>11} {bb3:>10} {bb4:>10} {d3_str:>10}")
    print()

    # ── PART 2 ────────────────────────────────────────────────────────────────
    print("=" * 130)
    print("PART 2: SPLIT STRATEGIES (Buyback-Aware) — Aggressive early, safe late")
    print("All split strategies use Buyback Wk1-3 window")
    print("=" * 130)
    print()

    # Find the best non-split strategy with Buyback Wk1-3 for comparison
    best_baseline_by_n: dict = {}
    for num_entries in ENTRY_COUNTS:
        best_name = max(
            strat_names_p1,
            key=lambda n: sum(
                p1_results[n][num_entries][s]["Buyback Wk1-3"]['entry_weeks']
                for s in SEASONS
            )
        )
        best_val = sum(
            p1_results[best_name][num_entries][s]["Buyback Wk1-3"]['entry_weeks']
            for s in SEASONS
        )
        best_baseline_by_n[num_entries] = (best_name, best_val)

    # Run Part 2
    p2_results: dict = {}
    total_p2 = len(PART2_SPLITS) * len(ENTRY_COUNTS) * len(SEASONS)
    run_num = 0

    for split_name, split_desc, run_fn in PART2_SPLITS:
        p2_results[split_name] = {}
        for num_entries in ENTRY_COUNTS:
            p2_results[split_name][num_entries] = {}
            for season in SEASONS:
                run_num += 1
                sys.stdout.write(
                    f"\r  P2 [{run_num:3d}/{total_p2}] {split_name[:35]:<35} "
                    f"n={num_entries:2d} {season}"
                )
                sys.stdout.flush()
                r = run_fn(season_data[season], num_entries)
                p2_results[split_name][num_entries][season] = r

    print(f"\r  All {total_p2} Part 2 runs complete.{'':60}")
    print()

    # Print Part 2 tables — one table per entry count
    for num_entries in ENTRY_COUNTS:
        best_baseline_name, best_baseline_val = best_baseline_by_n[num_entries]
        print(f"PART 2 — n={num_entries}  |  Best baseline w/BB: {best_baseline_name} ({best_baseline_val} entry-weeks)")
        print(f"  {'Strategy':<35} {'Description':<38} {'TOTAL':>7} {'vs Baseline':>12}")
        print("  " + "-" * 95)

        split_rows = []
        for split_name, split_desc, _ in PART2_SPLITS:
            total = sum(p2_results[split_name][num_entries][s]['entry_weeks'] for s in SEASONS)
            delta = total - best_baseline_val
            d_str = f"+{delta}" if delta >= 0 else str(delta)
            split_rows.append((total, split_name, split_desc, total, d_str))

        split_rows.sort(key=lambda x: x[0], reverse=True)
        for _, name, desc, total, d_str in split_rows:
            marker = " ◄ WINNER" if total > best_baseline_val else ""
            print(f"  {name:<35} {desc:<38} {total:>7} {d_str:>12}{marker}")
        print()

    # ── PART 3 ────────────────────────────────────────────────────────────────
    print("=" * 130)
    print("PART 3: BUYBACK ROI ANALYSIS")
    print("Metrics: buybacks used | % survived 3+ more weeks | % survived to wk10+ | net entry-weeks gained")
    print("=" * 130)
    print()

    # For ROI, focus on Buyback Wk1-3 (standard pool config)
    for num_entries in ENTRY_COUNTS:
        print(f"ROI Analysis — n={num_entries}")
        print(f"  {'Strategy':<35} {'BB Used':>8} {'BB/entry':>9} {'Surv3+%':>9} {'Surv10+%':>9} {'Net EW':>8} {'EW/BB':>7}")
        print("  " + "-" * 90)

        roi_rows = []
        for name in strat_names_p1:
            total_bb_used = 0
            total_bb_events = 0
            survived_3plus = 0
            survived_10plus = 0
            net_ew = 0

            for season in SEASONS:
                r_bb = p1_results[name][num_entries][season]["Buyback Wk1-3"]
                r_no = p1_results[name][num_entries][season]["No Buyback"]

                bb_events = r_bb['buyback_events']
                total_bb_events += len(bb_events)
                total_bb_used += r_bb['buyback_count']
                net_ew += r_bb['entry_weeks'] - r_no['entry_weeks']

                pb_weeks = r_bb['post_buyback_weeks']
                for weeks_survived in pb_weeks.values():
                    if weeks_survived >= 3:
                        survived_3plus += 1
                    if weeks_survived >= 7:  # returned at week 4 at latest, week 10+ = 6+ more
                        survived_10plus += 1

            total_runs = len(SEASONS)
            # Average buybacks per season per run
            bb_per_entry = total_bb_used / (total_runs * num_entries) if total_bb_used > 0 else 0
            surv3_pct = (survived_3plus / total_bb_events * 100) if total_bb_events > 0 else 0.0
            surv10_pct = (survived_10plus / total_bb_events * 100) if total_bb_events > 0 else 0.0
            ew_per_bb = (net_ew / total_bb_events) if total_bb_events > 0 else 0.0

            roi_rows.append((net_ew, name, total_bb_used, bb_per_entry, surv3_pct, surv10_pct, net_ew, ew_per_bb))

        roi_rows.sort(key=lambda x: x[0], reverse=True)
        for _, name, bb_used, bb_per_e, s3, s10, net_ew, ew_per_bb in roi_rows:
            print(f"  {name:<35} {bb_used:>8} {bb_per_e:>9.3f} {s3:>8.1f}% {s10:>8.1f}% "
                  f"{net_ew:>+8} {ew_per_bb:>7.2f}")
        print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 130)
    print("ROUND 8 SUMMARY")
    print("=" * 130)
    print()

    # Best strategy per entry count across all buyback configs
    for num_entries in ENTRY_COUNTS:
        print(f"n={num_entries} WINNERS:")
        for bb_label, bb_end in BUYBACK_CONFIGS:
            best = max(
                strat_names_p1,
                key=lambda n: sum(
                    p1_results[n][num_entries][s][bb_label]['entry_weeks']
                    for s in SEASONS
                )
            )
            best_val = sum(
                p1_results[best][num_entries][s][bb_label]['entry_weeks']
                for s in SEASONS
            )
            print(f"  {bb_label:<16} → {best} ({best_val} entry-weeks)")
        print()

    # Global buyback uplift summary
    print("BUYBACK UPLIFT ACROSS ALL STRATEGIES AND ENTRY COUNTS:")
    print(f"  {'n':>3}  {'Avg uplift Wk1-3':>18}  {'Avg uplift Wk1-4':>18}  {'Best strategy w/ BB':>35}")
    for num_entries in ENTRY_COUNTS:
        uplifts_3 = []
        uplifts_4 = []
        for name in strat_names_p1:
            no_bb = sum(p1_results[name][num_entries][s]["No Buyback"]['entry_weeks'] for s in SEASONS)
            bb3 = sum(p1_results[name][num_entries][s]["Buyback Wk1-3"]['entry_weeks'] for s in SEASONS)
            bb4 = sum(p1_results[name][num_entries][s]["Buyback Wk1-4"]['entry_weeks'] for s in SEASONS)
            uplifts_3.append(bb3 - no_bb)
            uplifts_4.append(bb4 - no_bb)

        avg3 = sum(uplifts_3) / len(uplifts_3)
        avg4 = sum(uplifts_4) / len(uplifts_4)
        best_name, best_val = best_baseline_by_n[num_entries]
        print(f"  n={num_entries:2d}  {avg3:>+17.1f}  {avg4:>+17.1f}  {best_name:<35} ({best_val})")

    print()
    print("DONE.")


if __name__ == "__main__":
    main()
