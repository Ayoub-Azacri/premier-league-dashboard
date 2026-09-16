import pandas as pd
import numpy as np
import math

def compute_executive_kpis(
    df: pd.DataFrame,
    venue: str = "Tous",
    teams: list = None
) -> dict:
    """Computes executive-level actionable KPIs contextualized against league baselines."""
    total_matches = len(df)
    if total_matches == 0:
        return {
            "matches": 0, "total_goals": 0, "goals_per_match": 0.0,
            "shot_accuracy": 0.0, "accuracy_diff": 0.0,
            "conversion_rate": 0.0, "conversion_diff": 0.0,
            "points_per_sot": 0.0
        }

    if venue == "Domicile":
        sub = df[df["HomeTeam"].isin(teams)] if (teams and len(teams) > 0) else df
        total_goals = int(sub["FTHG"].sum())
        total_shots = float(sub["HS"].sum())
        total_sot = float(sub["HST"].sum())
        total_matches = len(sub)
    elif venue == "Extérieur":
        sub = df[df["AwayTeam"].isin(teams)] if (teams and len(teams) > 0) else df
        total_goals = int(sub["FTAG"].sum())
        total_shots = float(sub["AS"].sum())
        total_sot = float(sub["AST"].sum())
        total_matches = len(sub)
    else:
        total_goals = int(df["TotalGoals"].sum())
        total_shots = float(df["TotalShots"].sum())
        total_sot = float(df["TotalShotsTarget"].sum())

    goals_per_match = round(total_goals / total_matches, 2) if total_matches > 0 else 0.0

    # Historical 5-season Premier League baselines
    BASELINE_ACCURACY = 34.0  # 34.0% shots on target
    BASELINE_CONVERSION = 31.0  # 31.0% goals per shot on target

    shot_accuracy = round(total_sot / total_shots * 100, 1) if total_shots > 0 else 0.0
    conversion_rate = round(total_goals / total_sot * 100, 1) if total_sot > 0 else 0.0
    points_per_sot = round((total_goals * 1.3) / total_sot, 2) if total_sot > 0 else 0.0

    return {
        "matches": total_matches,
        "total_goals": total_goals,
        "goals_per_match": goals_per_match,
        "shot_accuracy": shot_accuracy,
        "accuracy_diff": round(shot_accuracy - BASELINE_ACCURACY, 1),
        "conversion_rate": conversion_rate,
        "conversion_diff": round(conversion_rate - BASELINE_CONVERSION, 1),
        "points_per_sot": points_per_sot
    }

def compute_quadrant_profiles(team_df: pd.DataFrame) -> pd.DataFrame:
    """Classifies teams into 4 strategic efficiency quadrants based on accuracy and conversion."""
    if team_df.empty:
        return team_df

    df_q = team_df.copy()
    med_acc = df_q["PrecisionCadrePct"].median()
    med_conv = df_q["ConversionButsPct"].median()

    def assign_profile(row):
        acc = row["PrecisionCadrePct"]
        conv = row["ConversionButsPct"]
        if acc >= med_acc and conv >= med_conv:
            return "Chirurgicaux (Haute précision & conversion)"
        elif acc >= med_acc and conv < med_conv:
            return "Volumeux (Domination stérile devant le but)"
        elif acc < med_acc and conv >= med_conv:
            return "Réalistes (Opportunisme clinique en contre)"
        else:
            return "En difficulté (Manque de précision et de réalisme)"

    df_q["ProfilTactique"] = df_q.apply(assign_profile, axis=1)
    df_q["MedianPrecision"] = med_acc
    df_q["MedianConversion"] = med_conv
    return df_q

def compute_home_advantage_comparison(df: pd.DataFrame) -> dict:
    """Calculates home advantage metrics comparing normal crowds vs closed-door COVID season."""
    normal_matches = df[~df["is_closed_door"]]
    covid_matches = df[df["is_closed_door"]]

    def get_split(subset):
        n = len(subset)
        if n == 0:
            return {"n": 0, "home_win": 0.0, "draw": 0.0, "away_win": 0.0, "diff_goals": 0.0}
        h_win = round((subset["FTR"] == "H").sum() / n * 100, 1)
        draw = round((subset["FTR"] == "D").sum() / n * 100, 1)
        a_win = round((subset["FTR"] == "A").sum() / n * 100, 1)
        diff_goals = round((subset["FTHG"].sum() - subset["FTAG"].sum()) / n, 2)
        return {"n": n, "home_win": h_win, "draw": draw, "away_win": a_win, "diff_goals": diff_goals}

    normal_stats = get_split(normal_matches)
    covid_stats = get_split(covid_matches)
    all_stats = get_split(df)

    return {
        "normal": normal_stats,
        "covid": covid_stats,
        "all": all_stats,
        "home_drop_pts": round(normal_stats["home_win"] - covid_stats["home_win"], 1),
        "away_boost_pts": round(covid_stats["away_win"] - normal_stats["away_win"], 1)
    }

def simulate_match_outcome(
    home_team: str,
    away_team: str,
    team_stats: pd.DataFrame,
    is_closed_doors: bool = False
) -> dict:
    """Simulates match outcome probabilities and expected goals based on historical efficiency ratings."""
    h_row = team_stats[team_stats["Team"] == home_team]
    a_row = team_stats[team_stats["Team"] == away_team]

    if h_row.empty or a_row.empty:
        return {
            "home_prob": 33.3, "draw_prob": 33.4, "away_prob": 33.3,
            "exp_home_goals": 1.2, "exp_away_goals": 1.1,
            "verdict": "Données insuffisantes pour les équipes sélectionnées.",
            "keys": []
        }

    h = h_row.iloc[0]
    a = a_row.iloc[0]

    # Offensive power and defensive resistance
    league_avg_goals = team_stats["ButsParMatch"].mean() if not team_stats.empty else 1.4
    h_attack = h["ButsParMatch"] / league_avg_goals
    a_attack = a["ButsParMatch"] / league_avg_goals

    h_defense = (h["ButsConcedes"] / h["Matchs"]) / league_avg_goals
    a_defense = (a["ButsConcedes"] / a["Matchs"]) / league_avg_goals

    # Home crowd bonus
    home_bonus = 0.05 if is_closed_doors else 0.28

    # Expected goals
    exp_h_goals = max(0.4, round(league_avg_goals * h_attack * a_defense + home_bonus, 2))
    exp_a_goals = max(0.3, round(league_avg_goals * a_attack * h_defense - (home_bonus * 0.4), 2))

    # Calculate probabilities via Poisson-like logistic weighting
    diff = exp_h_goals - exp_a_goals
    p_draw = max(18.0, round(28.0 - abs(diff) * 5.5, 1))
    remaining = 100.0 - p_draw

    p_home = round(1.0 / (1.0 + np.exp(-1.4 * diff)) * remaining, 1)
    p_away = round(remaining - p_home, 1)

    # Key tactical takeaway
    if p_home >= 50:
        verdict = f"Avantage net pour {home_team} : volume de frappes cadrées et ascendant tactique."
    elif p_away >= 45:
        verdict = f"Danger pour {home_team} : {away_team} dispose d'un réalisme supérieur en transition."
    else:
        verdict = "Confrontation indécise : résultat hautement dépendant du premier tir cadré."

    keys = [
        f"Précision au tir : {home_team} ({h['PrecisionCadrePct']} %) vs {away_team} ({a['PrecisionCadrePct']} %)",
        f"Taux de conversion : {home_team} ({h['ConversionButsPct']} %) vs {away_team} ({a['ConversionButsPct']} %)",
        f"Pression du public : {'Absente (huis clos, avantage domicile neutralisé)' if is_closed_doors else 'Active (+0,28 but espéré pour le club recevant)'}"
    ]

    return {
        "home_prob": p_home,
        "draw_prob": p_draw,
        "away_prob": p_away,
        "exp_home_goals": exp_h_goals,
        "exp_away_goals": exp_a_goals,
        "verdict": verdict,
        "keys": keys
    }

def compute_season_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates home win, draw, and away win rates across each season."""
    if df.empty or "Saison" not in df.columns:
        return pd.DataFrame()

    records = []
    for s, g in df.groupby("Saison"):
        n = len(g)
        if n == 0:
            continue
        h_pct = round((g["FTR"] == "H").sum() / n * 100, 1)
        d_pct = round((g["FTR"] == "D").sum() / n * 100, 1)
        a_pct = round((g["FTR"] == "A").sum() / n * 100, 1)
        records.append({
            "Saison": s,
            "Matchs": n,
            "VictoireDomicilePct": h_pct,
            "NulPct": d_pct,
            "VictoireExterieurPct": a_pct,
            "IsCovid": bool((g["is_closed_door"]).mean() > 0.5) if "is_closed_door" in g.columns else False
        })
    out = pd.DataFrame(records).sort_values("Saison").reset_index(drop=True)
    return out

def compute_club_crowd_sensitivity(df: pd.DataFrame, min_matches: int = 10) -> pd.DataFrame:
    """Calculates each club's home win percentage with crowds vs closed doors."""
    if df.empty or "is_closed_door" not in df.columns:
        return pd.DataFrame()

    covid = df[df["is_closed_door"] == 1]
    normal = df[df["is_closed_door"] == 0]

    all_teams = df["HomeTeam"].unique()
    records = []

    for t in all_teams:
        c_m = covid[covid["HomeTeam"] == t]
        n_m = normal[normal["HomeTeam"] == t]
        if len(c_m) >= min_matches and len(n_m) >= min_matches:
            c_win = round((c_m["FTR"] == "H").sum() / len(c_m) * 100, 1)
            n_win = round((n_m["FTR"] == "H").sum() / len(n_m) * 100, 1)
            diff = round(c_win - n_win, 1)
            records.append({
                "Team": t,
                "NormalWinPct": n_win,
                "CovidWinPct": c_win,
                "DiffPct": diff,
                "MatchsNormal": len(n_m),
                "MatchsCovid": len(c_m)
            })

    out = pd.DataFrame(records)
    if not out.empty:
        out = out.sort_values("DiffPct").reset_index(drop=True)
    return out

def compute_poisson_score_distribution(exp_home: float, exp_away: float, top_n: int = 3) -> list:
    """Computes exact scoreline probabilities using the Poisson distribution."""
    scores = []
    for h in range(6):
        p_h = (np.exp(-exp_home) * (exp_home ** h)) / math.factorial(h)
        for a in range(6):
            p_a = (np.exp(-exp_away) * (exp_away ** a)) / math.factorial(a)
            prob_pct = round(p_h * p_a * 100, 1)
            scores.append({
                "score": f"{h} - {a}",
                "prob": prob_pct,
                "home_goals": h,
                "away_goals": a
            })
    scores.sort(key=lambda x: x["prob"], reverse=True)
    return scores[:top_n]

