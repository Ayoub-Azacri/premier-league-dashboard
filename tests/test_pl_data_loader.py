import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.pl_data_loader import (
    load_pl_data,
    get_available_seasons,
    get_available_teams,
    filter_matches,
    compute_team_aggregates
)

def test_load_pl_data():
    df = load_pl_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1900
    assert "TotalGoals" in df.columns
    assert "HomeAccuracy" in df.columns
    assert "AwayConversion" in df.columns
    assert "is_closed_door" in df.columns

def test_get_available_seasons_and_teams():
    df = load_pl_data()
    seasons = get_available_seasons(df)
    teams = get_available_teams(df)
    
    assert len(seasons) == 5
    assert "2019-20" in seasons
    assert "2023-24" in seasons
    assert len(teams) >= 20
    assert "Arsenal" in teams
    assert "Liverpool" in teams

def test_filter_matches():
    df = load_pl_data()
    
    # 1. Filter single season
    f1 = filter_matches(df, seasons=["2020-21"])
    assert len(f1) == 380
    assert (f1["Saison"] == "2020-21").all()

    # 2. Filter team
    f2 = filter_matches(df, teams=["Arsenal"], venue="Tous")
    assert len(f2) == 190  # 38 * 5 seasons
    assert ((f2["HomeTeam"] == "Arsenal") | (f2["AwayTeam"] == "Arsenal")).all()

    # 3. Filter team home venue
    f3 = filter_matches(df, teams=["Arsenal"], venue="Domicile")
    assert len(f3) == 95
    assert (f3["HomeTeam"] == "Arsenal").all()

def test_compute_team_aggregates():
    df = load_pl_data()
    team_stats = compute_team_aggregates(df)
    
    assert isinstance(team_stats, pd.DataFrame)
    assert not team_stats.empty
    assert "Team" in team_stats.columns
    assert "PrecisionCadrePct" in team_stats.columns
    assert "ConversionButsPct" in team_stats.columns
    assert "PointsParTirCadre" in team_stats.columns
    assert team_stats["PrecisionCadrePct"].between(15, 60).all()
    assert team_stats["ConversionButsPct"].between(15, 60).all()
