import os
import pandas as pd
import streamlit as st

DATA_FILENAME = "premier_league_5seasons.csv"

def get_data_path() -> str:
    """Returns the absolute path to the Premier League dataset."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    primary_path = os.path.join(base_dir, "data", DATA_FILENAME)
    if os.path.exists(primary_path):
        return primary_path
    # Fallback to AED folder if not copied
    fallback_path = "/home/ayoubazacri/Desktop/HETIC/MD4/ANDRE-AED/premier_league_analysis/data/processed/all_seasons_processed.csv"
    if os.path.exists(fallback_path):
        return fallback_path
    raise FileNotFoundError("Premier League dataset not found.")

@st.cache_data
def load_pl_data() -> pd.DataFrame:
    """Loads and preprocesses the Premier League 5-season dataset with caching."""
    path = get_data_path()
    df = pd.read_csv(path)
    
    # Filter to relevant performance columns (dropping unused betting odds columns)
    core_cols = [
        "Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
        "HTHG", "HTAG", "HTR", "Referee", "HS", "AS", "HST", "AST",
        "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR", "Saison"
    ]
    present_cols = [c for c in core_cols if c in df.columns]
    clean_df = df[present_cols].copy()

    # Feature engineering for match-level KPIs
    clean_df["TotalGoals"] = clean_df["FTHG"] + clean_df["FTAG"]
    clean_df["TotalShots"] = clean_df["HS"] + clean_df["AS"]
    clean_df["TotalShotsTarget"] = clean_df["HST"] + clean_df["AST"]
    clean_df["HomeAccuracy"] = (clean_df["HST"] / clean_df["HS"].replace(0, pd.NA) * 100).fillna(0)
    clean_df["AwayAccuracy"] = (clean_df["AST"] / clean_df["AS"].replace(0, pd.NA) * 100).fillna(0)
    clean_df["HomeConversion"] = (clean_df["FTHG"] / clean_df["HST"].replace(0, pd.NA) * 100).fillna(0)
    clean_df["AwayConversion"] = (clean_df["FTAG"] / clean_df["AST"].replace(0, pd.NA) * 100).fillna(0)

    if "is_closed_door" in df.columns:
        clean_df["is_closed_door"] = df["is_closed_door"].astype(bool)
    else:
        clean_df["is_closed_door"] = (clean_df["Saison"] == "2020-21")

    return clean_df

def get_available_seasons(df: pd.DataFrame) -> list:
    """Returns sorted list of available seasons."""
    return sorted(df["Saison"].dropna().unique().tolist())

def get_available_teams(df: pd.DataFrame) -> list:
    """Returns sorted list of unique team names across home and away matches."""
    home_teams = set(df["HomeTeam"].dropna().unique())
    away_teams = set(df["AwayTeam"].dropna().unique())
    return sorted(list(home_teams.union(away_teams)))

def filter_matches(
    df: pd.DataFrame,
    seasons: list = None,
    teams: list = None,
    venue: str = "Tous"
) -> pd.DataFrame:
    """Filters matches according to selected seasons, teams, and venue."""
    filtered = df.copy()

    if seasons:
        filtered = filtered[filtered["Saison"].isin(seasons)]

    if teams and len(teams) > 0:
        if venue == "Domicile":
            filtered = filtered[filtered["HomeTeam"].isin(teams)]
        elif venue == "Extérieur":
            filtered = filtered[filtered["AwayTeam"].isin(teams)]
        else:
            filtered = filtered[(filtered["HomeTeam"].isin(teams)) | (filtered["AwayTeam"].isin(teams))]

    return filtered

def compute_team_aggregates(df: pd.DataFrame, target_teams: list = None) -> pd.DataFrame:
    """Aggregates match performance into team-level season stats."""
    records = []
    teams = target_teams if (target_teams and len(target_teams) > 0) else get_available_teams(df)

    for team in teams:
        home_m = df[df["HomeTeam"] == team]
        away_m = df[df["AwayTeam"] == team]

        played = len(home_m) + len(away_m)
        if played == 0:
            continue

        # Wins, Draws, Losses
        wins = int((home_m["FTR"] == "H").sum() + (away_m["FTR"] == "A").sum())
        draws = int((home_m["FTR"] == "D").sum() + (away_m["FTR"] == "D").sum())
        losses = int((home_m["FTR"] == "A").sum() + (away_m["FTR"] == "H").sum())
        points = wins * 3 + draws

        # Goals
        goals_for = int(home_m["FTHG"].sum() + away_m["FTAG"].sum())
        goals_against = int(home_m["FTAG"].sum() + away_m["FTHG"].sum())
        diff = goals_for - goals_against

        # Shots
        shots_for = float(home_m["HS"].sum() + away_m["AS"].sum())
        shots_target_for = float(home_m["HST"].sum() + away_m["AST"].sum())
        shots_against = float(home_m["AS"].sum() + away_m["HS"].sum())
        shots_target_against = float(home_m["AST"].sum() + away_m["HST"].sum())

        # Ratios
        accuracy_pct = (shots_target_for / shots_for * 100) if shots_for > 0 else 0.0
        conversion_pct = (goals_for / shots_target_for * 100) if shots_target_for > 0 else 0.0
        points_per_sot = (points / shots_target_for) if shots_target_for > 0 else 0.0

        records.append({
            "Team": team,
            "Matchs": played,
            "Victoires": wins,
            "Nuls": draws,
            "Defaites": losses,
            "Points": points,
            "ButsMarques": goals_for,
            "ButsConcedes": goals_against,
            "DiffButs": diff,
            "TirsTotaux": shots_for,
            "TirsCadres": shots_target_for,
            "PrecisionCadrePct": round(accuracy_pct, 1),
            "ConversionButsPct": round(conversion_pct, 1),
            "PointsParTirCadre": round(points_per_sot, 2),
            "TirsParMatch": round(shots_for / played, 1),
            "TirsCadresParMatch": round(shots_target_for / played, 1),
            "ButsParMatch": round(goals_for / played, 2)
        })

    out = pd.DataFrame(records)
    if not out.empty:
        out = out.sort_values(by=["Points", "DiffButs", "ButsMarques"], ascending=False).reset_index(drop=True)
        out["Rang"] = out.index + 1
    return out
