import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.pl_data_loader import load_pl_data, compute_team_aggregates
from engine.pl_metrics import (
    compute_executive_kpis,
    compute_quadrant_profiles,
    compute_home_advantage_comparison,
    simulate_match_outcome,
    compute_season_outcomes,
    compute_club_crowd_sensitivity,
    compute_poisson_score_distribution
)

def test_compute_executive_kpis():
    df = load_pl_data()
    kpis = compute_executive_kpis(df)
    
    assert kpis["matches"] == 1900
    assert kpis["total_goals"] > 4000
    assert 2.4 <= kpis["goals_per_match"] <= 3.6
    assert 20.0 <= kpis["shots_per_match"] <= 30.0
    assert 7.0 <= kpis["sot_per_match"] <= 12.0
    assert 0.20 <= kpis["goals_per_sot"] <= 0.40
    assert 30.0 <= kpis["shot_accuracy"] <= 40.0
    assert 25.0 <= kpis["conversion_rate"] <= 38.0
    assert kpis["points_per_sot"] > 0

def test_compute_quadrant_profiles():
    df = load_pl_data()
    team_stats = compute_team_aggregates(df)
    quad_df = compute_quadrant_profiles(team_stats)
    
    assert "ProfilTactique" in quad_df.columns
    profiles = quad_df["ProfilTactique"].unique().tolist()
    assert len(profiles) >= 3

def test_compute_home_advantage_comparison():
    df = load_pl_data()
    comp = compute_home_advantage_comparison(df)
    
    assert comp["normal"]["home_win"] > comp["covid"]["home_win"]
    assert comp["home_drop_pts"] > 5.0  # Confirmed drop of ~8 points
    assert comp["covid"]["away_win"] > comp["normal"]["away_win"]

def test_simulate_match_outcome():
    df = load_pl_data()
    team_stats = compute_team_aggregates(df)
    
    sim = simulate_match_outcome("Arsenal", "Burnley", team_stats, is_closed_doors=False)
    assert sim["home_prob"] > sim["away_prob"]
    assert sim["exp_home_goals"] > sim["exp_away_goals"]
    assert len(sim["keys"]) == 3
    assert "verdict" in sim

def test_compute_season_outcomes():
    df = load_pl_data()
    seasons_df = compute_season_outcomes(df)
    assert len(seasons_df) == 5
    assert "VictoireDomicilePct" in seasons_df.columns
    # Verify 2020-21 COVID season has the lowest home win percentage
    covid_row = seasons_df[seasons_df["Saison"] == "2020-21"].iloc[0]
    assert covid_row["VictoireDomicilePct"] < 40.0

def test_compute_club_crowd_sensitivity():
    df = load_pl_data()
    sens_df = compute_club_crowd_sensitivity(df, min_matches=10)
    assert not sens_df.empty
    assert "Liverpool" in sens_df["Team"].values
    liv = sens_df[sens_df["Team"] == "Liverpool"].iloc[0]
    # Liverpool suffered a substantial drop (> 15 pts) without crowd at Anfield
    assert liv["DiffPct"] < -15.0

def test_compute_poisson_score_distribution():
    scores = compute_poisson_score_distribution(1.8, 1.1, top_n=3)
    assert len(scores) == 3
    assert all("score" in s and "prob" in s for s in scores)
    assert scores[0]["prob"] >= scores[1]["prob"] >= scores[2]["prob"]

