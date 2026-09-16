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
    simulate_match_outcome
)

def test_compute_executive_kpis():
    df = load_pl_data()
    kpis = compute_executive_kpis(df)
    
    assert kpis["matches"] == 1900
    assert kpis["total_goals"] > 4000
    assert 2.4 <= kpis["goals_per_match"] <= 3.6
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
