#!/usr/bin/env python3
"""
Stan Phase 1: Data Acquisition for 10-Season Backtesting

1. Fetch 2016-2019 game data from nfl_data_py → nfl_games_YYYY.json
2. Verify 2020 data (nfl_games_2020_weather.json)
3. Build pick-popularity regression model from 2021-2024 SurvivorGrid data
4. Generate synthetic pick files for 2016-2020
"""

import json
import math
import os
import sys

DATA_DIR = os.path.expanduser("~/Projects/SurvivorPulse-BackTesting-Prototype/data")

# ── erf implementation (no scipy needed) ─────────────────────────────────────
def erf(x):
    # Abramowitz & Stegun approximation
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    result = 1.0 - poly * math.exp(-x * x)
    return sign * result

def spread_to_win_prob(spread: float) -> float:
    """Convert home-team spread (positive = home favored) to home win probability."""
    return 0.5 * (1 + erf(spread / (13.5 * math.sqrt(2))))

# ── Phase 1A: Fetch 2016-2019 game data from nfl_data_py ─────────────────────

def fetch_historical_games():
    try:
        import nfl_data_py as nfl
    except ImportError:
        print("ERROR: nfl_data_py not installed. Run: pip3 install nfl_data_py")
        sys.exit(1)

    TEAM_ABBREV_MAP = {
        # nfl_data_py → SurvivorPulse team IDs
        'LA':  'LAR',   # Rams moved to LA in 2016 from STL
        'OAK': 'LV',    # Raiders → Las Vegas in 2020
        'SD':  'LAC',   # Chargers → LA in 2017
        'STL': 'LAR',   # St. Louis Rams (pre-2016)
        'JAC': 'JAX',   # Jacksonville (alternate abbrev)
        'LV':  'LV',
        'LAC': 'LAC',
        'LAR': 'LAR',
        # All others stay the same
    }

    def norm_team(t):
        return TEAM_ABBREV_MAP.get(t, t)

    for season in [2016, 2017, 2018, 2019]:
        out_path = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
        if os.path.exists(out_path):
            print(f"  {season}: already exists, skipping fetch")
            continue

        print(f"  Fetching {season} schedule from nfl_data_py...")
        df = nfl.import_schedules([season])
        # Filter to regular season only
        df = df[df['game_type'] == 'REG'].copy()

        # Remove playoff bye week (some seasons have week 17/18 games that aren't played)
        df = df.dropna(subset=['home_score', 'away_score', 'spread_line'])

        games = []
        for _, row in df.iterrows():
            home_team = norm_team(str(row['home_team']))
            away_team = norm_team(str(row['away_team']))
            spread = float(row['spread_line'])  # positive = home favored
            hwp = spread_to_win_prob(spread)
            awp = 1.0 - hwp
            home_score = int(row['home_score']) if not math.isnan(row['home_score']) else None
            away_score = int(row['away_score']) if not math.isnan(row['away_score']) else None
            completed = (home_score is not None and away_score is not None)

            game = {
                "id": f"{season}-{int(row['week'])}-{home_team}-{away_team}",
                "week": int(row['week']),
                "season": season,
                "period_type": "WEEK",
                "schedule_type": "regular_season",
                "home_team_id": home_team,
                "away_team_id": away_team,
                "home_spread": spread,
                "home_win_probability": round(hwp, 4),
                "away_win_probability": round(awp, 4),
                "home_score": home_score,
                "away_score": away_score,
                "completed": completed,
                "div_game": bool(row.get('div_game', False))
            }
            games.append(game)

        # Sort by week
        games.sort(key=lambda g: (g['week'], g['home_team_id']))

        with open(out_path, 'w') as f:
            json.dump(games, f, indent=2)

        week_counts = {}
        for g in games:
            w = g['week']
            week_counts[w] = week_counts.get(w, 0) + 1

        print(f"  {season}: {len(games)} games across {len(week_counts)} weeks → {out_path}")

# ── Phase 1B: Verify 2020 data ─────────────────────────────────────────────

def verify_2020():
    path_weather = os.path.join(DATA_DIR, "nfl_games_2020_weather.json")

    if not os.path.exists(path_weather):
        print("  ERROR: nfl_games_2020_weather.json not found!")
        return False

    with open(path_weather) as f:
        games = json.load(f)

    # Check fields
    sample = games[0]
    required = ['week', 'homeTeamId', 'awayTeamId', 'homeWinProbability', 
                'awayWinProbability', 'homeScore', 'awayScore', 'completed']
    missing = [r for r in required if r not in sample]

    if missing:
        print(f"  WARNING: 2020 weather file missing fields: {missing}")
        # Check if we need to re-derive from nfl_data_py
    else:
        weeks = set(g['week'] for g in games)
        print(f"  2020 weather: {len(games)} games, {len(weeks)} weeks — all required fields present ✓")
        # Note: 2020 had 16 weeks (COVID year?), actually it had 17 regular season weeks
        # nfl_data_py 2020 regular season had 17 weeks (old format)
        print(f"  2020 weeks: {sorted(weeks)}")
        return True

    # Rebuild 2020 from nfl_data_py
    print("  Rebuilding 2020 data from nfl_data_py...")
    return fetch_2020_from_nfldatapy()

def fetch_2020_from_nfldatapy():
    """Fetch 2020 season from nfl_data_py to get spread data."""
    try:
        import nfl_data_py as nfl
    except ImportError:
        return False

    TEAM_ABBREV_MAP = {
        'LA': 'LAR', 'OAK': 'LV', 'SD': 'LAC', 'STL': 'LAR', 'JAC': 'JAX',
    }
    def norm_team(t):
        return TEAM_ABBREV_MAP.get(t, t)

    df = nfl.import_schedules([2020])
    df = df[(df['game_type'] == 'REG') & df['home_score'].notna()].copy()

    # Load existing 2020 weather data to get win probabilities (they exist there)
    out_path = os.path.join(DATA_DIR, "nfl_games_2020.json")

    games = []
    for _, row in df.iterrows():
        home_team = norm_team(str(row['home_team']))
        away_team = norm_team(str(row['away_team']))

        if pd.isna(row.get('spread_line')):
            hwp = 0.5
        else:
            spread = float(row['spread_line'])
            hwp = spread_to_win_prob(spread)
        awp = 1.0 - hwp

        home_score = int(row['home_score']) if not pd.isna(row['home_score']) else None
        away_score = int(row['away_score']) if not pd.isna(row['away_score']) else None

        games.append({
            "id": f"2020-{int(row['week'])}-{home_team}-{away_team}",
            "week": int(row['week']),
            "season": 2020,
            "home_team_id": home_team,
            "away_team_id": away_team,
            "home_spread": float(row.get('spread_line', 0) or 0),
            "home_win_probability": round(hwp, 4),
            "away_win_probability": round(awp, 4),
            "home_score": home_score,
            "away_score": away_score,
            "completed": True,
            "div_game": bool(row.get('div_game', False))
        })

    games.sort(key=lambda g: (g['week'], g['home_team_id']))
    with open(out_path, 'w') as f:
        json.dump(games, f, indent=2)
    print(f"  2020 rebuilt: {len(games)} games → {out_path}")
    return True

# ── Phase 1C: Build pick-popularity model ─────────────────────────────────────

def build_pick_model():
    """
    Analyze win_probability → pick_share relationship from 2021-2024 SurvivorGrid data.
    Fit a piecewise/polynomial model. Return model parameters.
    """
    print("\n  Building win-probability → pick-share model from 2021-2024 data...")

    # Collect all (win_prob, pick_share) pairs
    pairs = []
    for season in [2021, 2022, 2023, 2024]:
        games_path = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
        picks_path = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")

        if not os.path.exists(games_path) or not os.path.exists(picks_path):
            print(f"    WARNING: Missing data for {season}, skipping")
            continue

        with open(games_path) as f:
            games = json.load(f)
        with open(picks_path) as f:
            picks_data = json.load(f)

        # Build week→team→win_prob map
        wp_map = {}  # (week, team_id) → win_prob
        for g in games:
            w = g['week']
            home = g.get('home_team_id') or g.get('homeTeamId')
            away = g.get('away_team_id') or g.get('awayTeamId')
            hwp = g.get('home_win_probability') or g.get('homeWinProbability', 0.5)
            awp = g.get('away_win_probability') or g.get('awayWinProbability', 0.5)
            wp_map[(w, home)] = float(hwp)
            wp_map[(w, away)] = float(awp)

        weeks = picks_data.get('weeks', {})
        for week_str, week_data in weeks.items():
            w = int(week_str)
            teams = week_data.get('teams', [])
            for t in teams:
                tid = t['teamId']
                avg = t.get('average', 0)
                if avg is None or avg == 0:
                    continue
                wp = wp_map.get((w, tid))
                if wp is None:
                    continue
                pairs.append((wp, avg))

    print(f"    Collected {len(pairs)} (win_prob, pick_share) data points")

    if len(pairs) < 10:
        print("    ERROR: Insufficient data points for model fitting")
        return None

    # Bin analysis: understand the relationship
    bins = {}
    for wp, ps in pairs:
        b = round(wp * 20) / 20  # 5% bins
        if b not in bins:
            bins[b] = []
        bins[b].append(ps)

    print("\n    Win Prob → Pick Share relationship (binned):")
    print(f"    {'WP Range':>12} {'N':>5} {'Mean PS':>9} {'Median':>9} {'Min':>7} {'Max':>7}")
    sorted_bins = sorted(bins.items())
    for b, ps_list in sorted_bins:
        if len(ps_list) < 3:
            continue
        mean_ps = sum(ps_list) / len(ps_list)
        sorted_ps = sorted(ps_list)
        median_ps = sorted_ps[len(sorted_ps)//2]
        print(f"    {b-0.025:.3f}-{b+0.025:.3f}  {len(ps_list):>5} {mean_ps:>9.2f} {median_ps:>9.2f} {min(ps_list):>7.2f} {max(ps_list):>7.2f}")

    # Fit a simple polynomial regression: pick_share = a*wp^2 + b*wp + c
    # Using least squares manually
    n = len(pairs)
    # Fit: ps = a*wp^2 + b*wp + c
    # Build normal equations for [wp^4, wp^3, wp^2; wp^3, wp^2, wp; wp^2, wp, 1] * [a,b,c] = [wp^2*ps, wp*ps, ps]

    sum_x4 = sum(wp**4 for wp, _ in pairs)
    sum_x3 = sum(wp**3 for wp, _ in pairs)
    sum_x2 = sum(wp**2 for wp, _ in pairs)
    sum_x1 = sum(wp for wp, _ in pairs)
    sum_x0 = n

    sum_x2y = sum(wp**2 * ps for wp, ps in pairs)
    sum_x1y = sum(wp * ps for wp, ps in pairs)
    sum_x0y = sum(ps for _, ps in pairs)

    # Solve 3x3 system using Gaussian elimination
    M = [
        [sum_x4, sum_x3, sum_x2, sum_x2y],
        [sum_x3, sum_x2, sum_x1, sum_x1y],
        [sum_x2, sum_x1, sum_x0, sum_x0y],
    ]

    # Forward elimination
    for col in range(3):
        # Pivot
        max_row = max(range(col, 3), key=lambda r: abs(M[r][col]))
        M[col], M[max_row] = M[max_row], M[col]
        for row in range(col + 1, 3):
            if M[col][col] == 0:
                continue
            factor = M[row][col] / M[col][col]
            for k in range(4):
                M[row][k] -= factor * M[col][k]

    # Back substitution
    coeffs = [0.0, 0.0, 0.0]
    for i in range(2, -1, -1):
        coeffs[i] = M[i][3]
        for j in range(i + 1, 3):
            coeffs[i] -= M[i][j] * coeffs[j]
        if M[i][i] != 0:
            coeffs[i] /= M[i][i]

    a, b, c = coeffs
    print(f"\n    Fitted model: pick_share = {a:.4f}*wp^2 + {b:.4f}*wp + {c:.4f}")

    # Validate model
    errors = []
    for wp, ps in pairs:
        pred = a * wp**2 + b * wp + c
        errors.append((pred - ps)**2)
    rmse = (sum(errors) / len(errors)) ** 0.5
    print(f"    Model RMSE: {rmse:.2f} percentage points")

    # Also compute R²
    mean_ps = sum(ps for _, ps in pairs) / len(pairs)
    ss_res = sum((ps - (a * wp**2 + b * wp + c))**2 for wp, ps in pairs)
    ss_tot = sum((ps - mean_ps)**2 for _, ps in pairs)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    print(f"    Model R²: {r2:.4f}")

    # Spot-check model predictions
    print("\n    Model spot-checks:")
    test_wps = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]
    for twp in test_wps:
        pred = max(0.5, min(50.0, a * twp**2 + b * twp + c))
        print(f"      WP={twp:.0%} → Predicted pick share: {pred:.1f}%")

    return {'a': a, 'b': b, 'c': c, 'rmse': rmse, 'r2': r2, 'n_points': len(pairs)}

# ── Phase 1D: Generate synthetic pick data for 2016-2020 ──────────────────────

def generate_synthetic_picks(model_params: dict):
    """
    Generate synthetic SurvivorGrid pick files for 2016-2020 using the fitted model.
    For each game, predict pick share based on win probability.
    Add noise to reflect real-world variance.
    """
    import random
    random.seed(42)

    a = model_params['a']
    b = model_params['b']
    c = model_params['c']
    rmse = model_params['rmse']

    def predict_pick_share(wp: float) -> float:
        """Predict pick share % for a team with given win probability."""
        raw = a * wp**2 + b * wp + c
        # Add noise proportional to residuals
        noise = random.gauss(0, rmse * 0.7)  # 70% of RMSE as noise std
        # Pick shares must sum to ~100% per week, and each team 0.1-50%
        return max(0.5, min(50.0, raw + noise))

    for season in [2016, 2017, 2018, 2019, 2020]:
        # Determine which games file to use
        if season == 2020:
            games_path = os.path.join(DATA_DIR, "nfl_games_2020_weather.json")
            # 2020 uses camelCase
            use_camel = True
        else:
            games_path = os.path.join(DATA_DIR, f"nfl_games_{season}.json")
            use_camel = False

        picks_path = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")

        if os.path.exists(picks_path):
            print(f"  {season}: picks file already exists, skipping")
            continue

        if not os.path.exists(games_path):
            print(f"  WARNING: {games_path} not found, skipping {season} picks")
            continue

        with open(games_path) as f:
            games = json.load(f)

        # Group by week
        weeks_data = {}
        for g in games:
            w = g['week']
            if w not in weeks_data:
                weeks_data[w] = []
            weeks_data[w].append(g)

        # Generate picks per week
        weeks_output = {}
        for week_num, week_games in sorted(weeks_data.items()):
            teams_raw = []

            for g in week_games:
                if use_camel:
                    home = g.get('homeTeamId')
                    away = g.get('awayTeamId')
                    hwp = float(g.get('homeWinProbability', 0.5))
                    awp = float(g.get('awayWinProbability', 0.5))
                else:
                    home = g.get('home_team_id') or g.get('homeTeamId')
                    away = g.get('away_team_id') or g.get('awayTeamId')
                    hwp = float(g.get('home_win_probability') or g.get('homeWinProbability', 0.5))
                    awp = float(g.get('away_win_probability') or g.get('awayWinProbability', 0.5))

                if not home or not away:
                    continue

                h_raw = predict_pick_share(hwp)
                a_raw = predict_pick_share(awp)
                teams_raw.append((home, hwp, h_raw))
                teams_raw.append((away, awp, a_raw))

            if not teams_raw:
                continue

            # Normalize so pick shares sum to 100% per week
            total_raw = sum(r for _, _, r in teams_raw)
            if total_raw > 0:
                teams_normalized = [
                    {
                        "teamId": tid,
                        "winProbability": round(wp, 4),
                        "average": round((raw / total_raw) * 100, 2)
                    }
                    for tid, wp, raw in teams_raw
                ]
            else:
                teams_normalized = [{"teamId": tid, "winProbability": round(wp, 4), "average": round(100 / len(teams_raw), 2)}
                                    for tid, wp, _ in teams_raw]

            # Sort by pick share descending
            teams_normalized.sort(key=lambda t: t['average'], reverse=True)

            weeks_output[str(week_num)] = {
                "week": week_num,
                "teams": [{"teamId": t["teamId"], "average": t["average"]} for t in teams_normalized]
            }

        picks_output = {
            "season": season,
            "source": "synthetic_model",
            "model_type": "quadratic_regression",
            "model_params": {"a": a, "b": b, "c": c},
            "model_r2": model_params['r2'],
            "model_rmse": model_params['rmse'],
            "weeks": weeks_output
        }

        with open(picks_path, 'w') as f:
            json.dump(picks_output, f, indent=2)

        n_weeks = len(weeks_output)
        print(f"  {season}: Generated synthetic picks for {n_weeks} weeks → {picks_path}")

        # Spot-check validation
        if weeks_output:
            sample_week = min(weeks_output.keys(), key=int)
            sample_teams = weeks_output[sample_week]['teams'][:5]
            print(f"    Week {sample_week} top picks (sanity check):")
            for t in sample_teams:
                print(f"      {t['teamId']}: {t['average']:.1f}%")

# ── Validation ─────────────────────────────────────────────────────────────────

def validate_all_data():
    """Verify all required data files exist and have correct structure."""
    print("\n" + "="*60)
    print("VALIDATION")
    print("="*60)

    SEASONS_17W = [2016, 2017, 2018, 2019, 2020]  # 17-week seasons
    SEASONS_18W = [2021, 2022, 2023, 2024, 2025]  # 18-week seasons

    all_ok = True

    for season in SEASONS_17W + SEASONS_18W:
        # Game file
        if season == 2020:
            gpath = os.path.join(DATA_DIR, "nfl_games_2020_weather.json")
        elif season == 2025:
            gpath = os.path.join(DATA_DIR, "nfl_games_2025_cache.json")
        else:
            gpath = os.path.join(DATA_DIR, f"nfl_games_{season}.json")

        ppath = os.path.join(DATA_DIR, f"survivorgrid_picks_{season}.json")

        g_exists = os.path.exists(gpath)
        p_exists = os.path.exists(ppath)

        if g_exists:
            with open(gpath) as f:
                gdata = json.load(f)
            if isinstance(gdata, list):
                n_games = len(gdata)
                weeks = set(g.get('week') for g in gdata)
            else:
                n_games = sum(len(v) for v in gdata.values())
                weeks = set(gdata.keys())
            g_status = f"✓ {n_games} games, {len(weeks)} weeks"
        else:
            g_status = "✗ MISSING"
            all_ok = False

        if p_exists:
            with open(ppath) as f:
                pdata = json.load(f)
            n_weeks = len(pdata.get('weeks', {}))
            src = pdata.get('source', 'real')
            p_status = f"✓ {n_weeks} weeks [{src}]"
        else:
            p_status = "✗ MISSING"
            all_ok = False

        expected_weeks = 17 if season in SEASONS_17W else 18
        print(f"  {season} (exp {expected_weeks}w): games={g_status} | picks={p_status}")

    if all_ok:
        print("\n  ALL DATA FILES PRESENT ✓")
    else:
        print("\n  WARNING: Some files missing")

    return all_ok


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("="*70)
    print("STAN PHASE 1: 10-SEASON DATA ACQUISITION")
    print("="*70)

    # 1A: Fetch 2016-2019 game data
    print("\n[1A] Fetching 2016-2019 game data from nfl_data_py...")
    fetch_historical_games()

    # 1B: Verify 2020
    print("\n[1B] Verifying 2020 data...")
    verify_2020()

    # 1C: Build pick model
    print("\n[1C] Building pick-popularity regression model...")
    model = build_pick_model()

    if model is None:
        print("ERROR: Could not build pick model. Exiting.")
        sys.exit(1)

    # Save model parameters
    model_path = os.path.join(DATA_DIR, "pick_model_params.json")
    with open(model_path, 'w') as f:
        json.dump(model, f, indent=2)
    print(f"\n  Model saved: {model_path}")

    # 1D: Generate synthetic picks for 2016-2020
    print("\n[1D] Generating synthetic pick files for 2016-2020...")
    generate_synthetic_picks(model)

    # Validation
    validate_all_data()

    print("\n" + "="*70)
    print("PHASE 1 COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
