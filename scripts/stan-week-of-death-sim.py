#!/usr/bin/env python3
"""
Stan the Scout: Week-of-Death Distribution Analysis
Gap 1 closure for ROI analysis — tracks WHEN each entry dies, not just how many survived.

Focus strategies:
  - Adaptive Blend 90/10→50/50 (top performer at n=10)
  - SP Balanced 55/25/20
  - SP Conservative 65/25/10
  - Mixed Portfolio
  - Pure Win Probability (naive baseline)
  - 70/30 Blend

Configurations: n=5, 10, 20, 50 × 5 seasons (2021-2025) × no buyback + buyback Wk1-3
"""

import json
import math
import os
import sys
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")
ALT_DATA_DIR = os.path.expanduser("~/Projects/CMEA-Prototype/data")
TOTAL_WEEKS = 18
SEASONS = [2021, 2022, 2023, 2024, 2025]
ENTRY_COUNTS = [5, 10, 20, 50]

OUTPUT_PATH = os.path.expanduser("~/.openclaw/workspace/scripts/stan-wod-results.json")

TARGET_STRATEGIES = [
    "Adaptive Blend 90/10→50/50",
    "SP Balanced 55/25/20",
    "SP Conservative 65/25/10",
    "Mixed Portfolio",
    "Pure Win Probability",
    "70/30 Blend",
]

# ── Data Loading (same as stan-5season-sim.py) ────────────────────────────────

def _resolve_data_dir():
    if os.path.exists(DATA_DIR):
        return DATA_DIR
    if os.path.exists(ALT_DATA_DIR):
        return ALT_DATA_DIR
    raise FileNotFoundError(f"Data dir not found")

def _normalize_game(g):
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

def load_local_season(season, data_dir):
    with open(os.path.join(data_dir, f"nfl_games_{season}.json")) as f:
        raw_games = json.load(f)
    with open(os.path.join(data_dir, f"survivorgrid_picks_{season}.json")) as f:
        picks_data = json.load(f)

    all_week_data = {}
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

def load_2025(data_dir):
    cache_path = os.path.join(data_dir, "nfl_games_2025_cache.json")
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}
    # Try alt path
    alt_cache = os.path.join(ALT_DATA_DIR, "nfl_games_2025_cache.json")
    if os.path.exists(alt_cache):
        with open(alt_cache) as f:
            cached = json.load(f)
        return {int(k): v for k, v in cached.items()}
    raise FileNotFoundError("2025 cache not found")

def load_all_seasons():
    data_dir = _resolve_data_dir()
    season_data = {}
    for season in SEASONS:
        print(f"  Loading {season}...")
        if season == 2025:
            season_data[season] = load_2025(data_dir)
        else:
            season_data[season] = load_local_season(season, data_dir)
        print(f"  {season}: {len(season_data[season])} weeks")
    return season_data

# ── Scoring Functions ──────────────────────────────────────────────────────────

def blend_score(team, wp_w, ps_w):
    return (wp_w / 100) * team['winProbability'] + (ps_w / 100) * (1 - team['pickShare'] / 100)

def compute_expendability(team_id, current_week, all_week_data, lookahead=5):
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

def make_pure_wp_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return team['winProbability']
    return scorer

def make_blend_scorer(wp_w=70, ps_w=30):
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        return blend_score(team, wp_w, ps_w)
    return scorer

def make_sp_conservative_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 65, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.10 * fv
    return scorer

def make_sp_balanced_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        base = blend_score(team, 55, 25)
        exp = compute_expendability(team['teamId'], week, all_week_data, 5)
        fv = 1.0 - exp
        return base + 0.20 * fv
    return scorer

def make_adaptive_scorer():
    def scorer(team, all_teams, all_week_data, available, week, entry_idx=0, all_used=None):
        progress = (week - 1) / max(1, TOTAL_WEEKS - 1)
        eff_wp = 90 - 40 * progress
        eff_ps = 10 + 40 * progress
        return blend_score(team, eff_wp, eff_ps)
    return scorer

_FIVE_BASE_SCORERS = [
    make_blend_scorer(70, 30),
    make_sp_balanced_scorer(),
    make_sp_conservative_scorer(),
    make_blend_scorer(80, 20),
    make_pure_wp_scorer(),
]

def make_mixed_portfolio_scorers(num_entries):
    return [_FIVE_BASE_SCORERS[i % 5] for i in range(num_entries)]

# ── Week-of-Death Simulation ───────────────────────────────────────────────────

def simulate_with_death_tracking(scorer_or_list, week_data, num_entries, buyback_window_end=0):
    """
    Same simulation as stan-5season-sim.py but tracks week-of-death for each entry.
    
    Returns:
      death_weeks: list of (week_died, bought_back) for each entry. None = survived to end.
      entry_weeks: total entry-weeks (compatibility)
      survival_by_week: dict {week: num_entries_still_alive_after_week}
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
    
    # Track death events per entry (week of final death)
    death_week = [None] * num_entries  # None = alive at end
    
    entry_weeks = 0
    survival_by_week = {}

    for week in range(1, TOTAL_WEEKS + 1):
        teams = week_data.get(week, [])
        if not teams or not alive:
            survival_by_week[week] = 0
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
                alive.add(i)  # Resurrect — not actually dead yet
            else:
                death_week[i] = week  # Final death recorded

        survival_by_week[week] = len(alive)

    # Any entry still alive at end: death_week stays None (survived)
    
    return {
        'death_weeks': death_week,  # list[int | None], length = num_entries
        'entry_weeks': entry_weeks,
        'survival_by_week': survival_by_week,
    }


# ── Analysis Functions ────────────────────────────────────────────────────────

def compute_survival_stats(all_death_weeks):
    """
    Given a flat list of death_week values (from multiple seasons),
    compute survival curve and key milestone percentages.
    None = survived full season.
    """
    total = len(all_death_weeks)
    if total == 0:
        return {}
    
    # Count how many died each week
    deaths_by_week = defaultdict(int)
    survivors = 0
    for dw in all_death_weeks:
        if dw is None:
            survivors += 1
        else:
            deaths_by_week[dw] += 1
    
    # Survival curve: % still alive after each week
    cum_alive = total
    survival_curve = {}
    for week in range(1, TOTAL_WEEKS + 1):
        cum_alive -= deaths_by_week.get(week, 0)
        survival_curve[week] = round(cum_alive / total * 100, 1)
    
    # Key milestones
    pct_past_10 = survival_curve.get(10, 0)
    pct_past_14 = survival_curve.get(14, 0)
    pct_past_16 = survival_curve.get(16, 0)
    pct_survived_all = round(survivors / total * 100, 1)
    
    # Median death week
    sorted_deaths = sorted(dw for dw in all_death_weeks if dw is not None)
    median_dw = sorted_deaths[len(sorted_deaths)//2] if sorted_deaths else None
    
    # Death distribution
    death_dist = {}
    for w in range(1, TOTAL_WEEKS + 1):
        cnt = deaths_by_week.get(w, 0)
        death_dist[f"wk{w}"] = round(cnt / total * 100, 1)
    
    return {
        'total_entries': total,
        'pct_past_wk10': pct_past_10,
        'pct_past_wk14': pct_past_14,
        'pct_past_wk16': pct_past_16,
        'pct_survived_all': pct_survived_all,
        'median_death_week': median_dw,
        'survival_curve': survival_curve,
        'death_distribution_pct': death_dist,
    }


def compute_tiered_payout_ev(all_death_weeks, pool_config):
    """
    Given death week distribution and tiered payout config, compute expected value.
    
    pool_config: dict with:
      - 'name': str
      - 'total_entries': int (total field)
      - 'total_prize': int
      - 'structure': 'wta' | 'circa_progressive' | 'dk_tiered'
    """
    total = len(all_death_weeks)
    if total == 0:
        return 0
    
    ptype = pool_config.get('structure', 'wta')
    total_field = pool_config.get('total_entries', 100)
    total_prize = pool_config.get('total_prize', 10000)
    
    if ptype == 'wta':
        # Winner-take-all: prize proportional to survival advantage
        # EV = prize * (SP entry-weeks / naive entry-weeks) / total_field
        # Use survival curve to estimate late-season survivors
        survivors_at_end = sum(1 for dw in all_death_weeks if dw is None)
        # Simplified: entries that survive longest have proportional share
        ev = total_prize / total_field  # base EV per entry
        return round(ev, 2)
    
    elif ptype == 'circa_progressive':
        # Circa: WTA but surviving longer = bigger share of final prize
        # Approximate: entries surviving to week 15+ get disproportionate share
        # Based on Circa 2024: ~14,266 entries, $14.3M prize
        # Entries surviving to week 15-18 get ~95%+ of prize
        # Approximate by weighting survival weeks exponentially
        
        total_weighted = 0
        for dw in all_death_weeks:
            if dw is None:
                week_val = TOTAL_WEEKS  # survived all
            else:
                week_val = dw - 1  # weeks survived before dying
            # Exponential weight: surviving to week W = 1.15^W relative value
            total_weighted += 1.15 ** week_val
        
        avg_weighted = total_weighted / total
        # Base EV assumes uniform weight = 1.15^9 (avg death wk ~9)
        base_weighted = 1.15 ** 9
        
        # Scale EV by weight ratio
        base_ev = total_prize / total_field
        return round(base_ev * (avg_weighted / base_weighted), 2)
    
    elif ptype == 'dk_tiered':
        # DK: top 5, 10, 20 finishers each get prize tiers
        # Simplified model: % of entries making it to final weeks
        # Using known DK 2024 structure from research:
        # Last survivor: 30% of prize; next 4: 15%; next 5-10: 25%; next 10-20: 15%; rest: 15%
        # (approximate based on known DK payout tiers)
        
        deaths = sorted([(dw if dw is not None else 19, i) for i, dw in enumerate(all_death_weeks)],
                        key=lambda x: -x[0])  # sort by death week desc (survived longest first)
        
        final_place = defaultdict(int)
        # Assign prize share based on survival rank
        for rank, (dw, idx) in enumerate(deaths):
            if rank == 0:
                share = 0.30  # Winner
            elif rank <= 4:
                share = 0.15 / 4  # 2nd-5th
            elif rank <= 9:
                share = 0.25 / 5  # 6th-10th
            elif rank <= 19:
                share = 0.15 / 10  # 11th-20th
            else:
                share = 0.15 / max(1, total - 20)  # rest share equally
            final_place[idx] = share * total_prize
        
        avg_prize = sum(final_place.values()) / total
        return round(avg_prize, 2)
    
    return 0.0


# ── Strategy Registry ─────────────────────────────────────────────────────────

def get_strategy_runner(strat_name, num_entries):
    """Return a function that runs the simulation for a given week_data."""
    if strat_name == "Pure Win Probability":
        scorer = make_pure_wp_scorer()
        return lambda wd, n, bb: simulate_with_death_tracking(scorer, wd, n, bb)
    elif strat_name == "70/30 Blend":
        scorer = make_blend_scorer(70, 30)
        return lambda wd, n, bb: simulate_with_death_tracking(scorer, wd, n, bb)
    elif strat_name == "SP Conservative 65/25/10":
        scorer = make_sp_conservative_scorer()
        return lambda wd, n, bb: simulate_with_death_tracking(scorer, wd, n, bb)
    elif strat_name == "SP Balanced 55/25/20":
        scorer = make_sp_balanced_scorer()
        return lambda wd, n, bb: simulate_with_death_tracking(scorer, wd, n, bb)
    elif strat_name == "Adaptive Blend 90/10→50/50":
        scorer = make_adaptive_scorer()
        return lambda wd, n, bb: simulate_with_death_tracking(scorer, wd, n, bb)
    elif strat_name == "Mixed Portfolio":
        scorers = make_mixed_portfolio_scorers(num_entries)
        return lambda wd, n, bb: simulate_with_death_tracking(scorers, wd, n, bb)
    else:
        raise ValueError(f"Unknown strategy: {strat_name}")


# ── Tiered Payout Models ──────────────────────────────────────────────────────

POOL_CONFIGS = {
    "circa_10entry": {
        "name": "Circa Survivor (10-entry max)",
        "total_entries": 14266,  # 2024 field
        "total_prize": 14266000,  # $14.3M
        "structure": "circa_progressive",
        "entry_fee": 1000,
    },
    "dk_main_100": {
        "name": "DraftKings Main Event ($100)",
        "total_entries": 18515,  # 2024 field
        "total_prize": 1500000,  # $1.5M guaranteed
        "structure": "dk_tiered",
        "entry_fee": 100,
        "rake_pct": 0.188,  # (18515*100 - 1500000) / (18515*100)
    },
    "private_100_wta": {
        "name": "Private Pool ($100 WTA, 100 players)",
        "total_entries": 100,
        "total_prize": 10000,
        "structure": "wta",
        "entry_fee": 100,
    },
}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("STAN: WEEK-OF-DEATH DISTRIBUTION ANALYSIS")
    print(f"{len(TARGET_STRATEGIES)} strategies × {len(ENTRY_COUNTS)} n × 5 seasons × 2 buyback configs")
    print("=" * 80)
    
    print("\nLoading season data...")
    season_data = load_all_seasons()
    print()

    # results[strat][n][bb_label] = {death_weeks: [...], stats: {...}}
    results = {}
    
    buyback_configs = [("No Buyback", 0), ("Buyback Wk1-3", 3)]
    total_runs = len(TARGET_STRATEGIES) * len(ENTRY_COUNTS) * len(SEASONS) * len(buyback_configs)
    run_num = 0

    for strat_name in TARGET_STRATEGIES:
        results[strat_name] = {}
        for n in ENTRY_COUNTS:
            results[strat_name][n] = {}
            runner = get_strategy_runner(strat_name, n)
            
            for bb_label, bb_end in buyback_configs:
                # Collect death_weeks across all 5 seasons
                all_death_weeks = []
                per_season = {}
                
                for season in SEASONS:
                    run_num += 1
                    sys.stdout.write(
                        f"\r  [{run_num:3d}/{total_runs}] {strat_name[:32]:<32} "
                        f"n={n:2d} {season} {bb_label}"
                    )
                    sys.stdout.flush()
                    
                    r = runner(season_data[season], n, bb_end)
                    all_death_weeks.extend(r['death_weeks'])
                    per_season[season] = {
                        'death_weeks': r['death_weeks'],
                        'entry_weeks': r['entry_weeks'],
                    }
                
                stats = compute_survival_stats(all_death_weeks)
                
                results[strat_name][n][bb_label] = {
                    'stats': stats,
                    'per_season': per_season,
                    'all_death_weeks': all_death_weeks,
                }
    
    print(f"\r  All {total_runs} runs complete.{'':60}")
    print()

    # ── Summary Output ────────────────────────────────────────────────────
    print("=" * 80)
    print("KEY SURVIVAL MILESTONES (5-season aggregate, No Buyback)")
    print("Strategies × Entry Counts: % alive after Week 10 / 14 / 16")
    print("=" * 80)
    
    for n in ENTRY_COUNTS:
        print(f"\n--- n={n} entries ---")
        print(f"{'Strategy':<38} {'Wk10+':>7} {'Wk14+':>7} {'Wk16+':>7} {'Survived':>9} {'Median★':>8}")
        print("-" * 75)
        for strat_name in TARGET_STRATEGIES:
            s = results[strat_name][n]["No Buyback"]['stats']
            print(f"  {strat_name:<36} {s['pct_past_wk10']:>7.1f}% {s['pct_past_wk14']:>7.1f}% "
                  f"{s['pct_past_wk16']:>7.1f}% {s['pct_survived_all']:>8.1f}% "
                  f"{str(s['median_death_week']):>8}")
    
    print()
    print("=" * 80)
    print("BUYBACK IMPACT ON LATE-SEASON SURVIVAL (n=10)")
    print("=" * 80)
    print(f"{'Strategy':<38} {'No BB Wk14+':>12} {'BB Wk1-3 Wk14+':>15} {'Δ':>6}")
    print("-" * 75)
    for strat_name in TARGET_STRATEGIES:
        no_bb = results[strat_name][10]["No Buyback"]['stats']['pct_past_wk14']
        bb3 = results[strat_name][10]["Buyback Wk1-3"]['stats']['pct_past_wk14']
        delta = bb3 - no_bb
        print(f"  {strat_name:<36} {no_bb:>11.1f}% {bb3:>14.1f}% {delta:>+6.1f}%")
    
    # ── Save JSON ─────────────────────────────────────────────────────────
    # Save without raw death_weeks list for cleaner output (keep stats)
    save_results = {}
    for strat_name in TARGET_STRATEGIES:
        save_results[strat_name] = {}
        for n in ENTRY_COUNTS:
            save_results[strat_name][str(n)] = {}
            for bb_label, _ in buyback_configs:
                r = results[strat_name][n][bb_label]
                # Save stats + per-season entry_weeks but not raw death_weeks (too large)
                per_season_compact = {}
                for season in SEASONS:
                    ps = r['per_season'][season]
                    # Compute per-season stats
                    ps_stats = compute_survival_stats(ps['death_weeks'])
                    per_season_compact[str(season)] = {
                        'entry_weeks': ps['entry_weeks'],
                        'pct_past_wk10': ps_stats.get('pct_past_wk10', 0),
                        'pct_past_wk14': ps_stats.get('pct_past_wk14', 0),
                        'pct_past_wk16': ps_stats.get('pct_past_wk16', 0),
                        'median_death_week': ps_stats.get('median_death_week'),
                        'death_distribution_pct': ps_stats.get('death_distribution_pct', {}),
                    }
                save_results[strat_name][str(n)][bb_label] = {
                    'aggregate_stats': r['stats'],
                    'per_season': per_season_compact,
                }
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(save_results, f, indent=2)
    print(f"\nResults saved: {OUTPUT_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
