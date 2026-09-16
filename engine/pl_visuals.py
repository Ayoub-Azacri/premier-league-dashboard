import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from engine.pl_styles import get_custom_css

def create_shot_funnel_chart(
    total_shots: float,
    shots_target: float,
    goals: int,
    team_name: str = "Premier League",
    theme: str = "light"
) -> go.Figure:
    """Plots a 3-stage shooting conversion funnel highlighting wasted shots."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    stages = ["Tirs Totaux", "Tirs Cadrés", "Buts Marqués"]
    val_shots = int(total_shots)
    val_sot = int(shots_target)
    val_goals = int(goals)

    pct_sot_init = (val_sot / val_shots * 100) if val_shots > 0 else 0
    pct_goals_sot = (val_goals / val_sot * 100) if val_sot > 0 else 0
    pct_goals_total = (val_goals / val_shots * 100) if val_shots > 0 else 0

    custom_texts = [
        f"{val_shots:,}".replace(",", " ") + " tirs tentés (100 %)",
        f"{val_sot:,}".replace(",", " ") + f" tirs cadrés ({pct_sot_init:.1f} % des tirs)",
        f"{val_goals:,}".replace(",", " ") + f" buts inscrits ({pct_goals_sot:.1f} % convertis · {pct_goals_total:.1f} % de tous les tirs)"
    ]

    values = [val_shots, val_sot, val_goals]

    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        text=custom_texts,
        textinfo="text",
        textposition="inside",
        textfont=dict(size=13, color="#FFFFFF", family="Arial"),
        marker=dict(
            color=["#2563EB", "#0D9488", "#16A34A"],
            line=dict(color="#0F172A", width=1)
        ),
        connector=dict(line=dict(color="#94A3B8", width=1, dash="dot")),
        hovertemplate="<b>%{y}</b><br>Volume : %{x:,}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Parcours d'une frappe ({team_name}) : de la tentative au but</b>",
            font=dict(size=14, color=text_color)
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=280,
        margin=dict(l=30, r=30, t=40, b=15)
    )
    return fig

def create_efficiency_ranking_chart(
    team_df: pd.DataFrame,
    metric: str = "PointsParTirCadre",
    metric_label: str = "Points / Tir Cadré",
    avg_val: float = None,
    theme: str = "light"
) -> go.Figure:
    """Plots a horizontal bar chart ranking clubs by an actionable KPI with league average benchmark."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    top_teams = team_df.head(20).iloc[::-1].copy()
    if avg_val is None and not team_df.empty and metric in team_df.columns:
        avg_val = team_df[metric].mean()

    # Pre-attentive color coding: Highlight teams performing above the league average
    bar_colors = []
    for val in top_teams[metric]:
        if avg_val is not None and val >= avg_val:
            bar_colors.append("#2563EB")
        else:
            bar_colors.append("#94A3B8" if not is_dark else "#475569")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_teams[metric],
        y=top_teams["Team"],
        orientation='h',
        marker=dict(color=bar_colors, line=dict(color='#1E3A8A', width=0.8)),
        text=[f"{val:.2f}" if "Points" in metric else f"{val:.1f} %" for val in top_teams[metric]],
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>" + metric_label + " : %{x:.2f}<br>Rang : %{customdata[0]}<extra></extra>",
        customdata=top_teams[["Rang"]].values
    ))

    if avg_val is not None:
        fig.add_vline(
            x=avg_val,
            line_dash="dash",
            line_color="#EF4444",
            line_width=1.5,
            annotation_text=f"Moyenne : {avg_val:.2f}" if "Points" in metric else f"Moyenne : {avg_val:.1f} %",
            annotation_position="top right",
            annotation_font=dict(color="#EF4444", size=10)
        )

    max_x = top_teams[metric].max() if not top_teams.empty else 10
    fig.update_layout(
        title=dict(
            text=f"<b>Classement comparatif : {metric_label}</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(
            title=metric_label,
            range=[0, max_x * 1.18 if max_x > 0 else 10],
            color=text_color,
            gridcolor="#334155" if is_dark else "#F1F5F9"
        ),
        yaxis=dict(color=text_color),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=10, r=30, t=40, b=30),
        height=max(220, min(560, len(top_teams) * 26 + 70))
    )
    return fig

def create_quadrant_chart(team_df: pd.DataFrame, theme: str = "light") -> go.Figure:
    """Plots the 4-quadrant strategic map: Precision vs Conversion with colored zones."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    med_x = team_df["PrecisionCadrePct"].median() if not team_df.empty else 34.0
    med_y = team_df["ConversionButsPct"].median() if not team_df.empty else 31.0

    x_min = max(20.0, team_df["PrecisionCadrePct"].min() - 2) if not team_df.empty else 20.0
    x_max = team_df["PrecisionCadrePct"].max() + 3 if not team_df.empty else 45.0
    y_min = max(15.0, team_df["ConversionButsPct"].min() - 3) if not team_df.empty else 15.0
    y_max = team_df["ConversionButsPct"].max() + 4 if not team_df.empty else 45.0

    fig = go.Figure()

    # Add shaded background zones for each quadrant
    fig.add_shape(type="rect", x0=med_x, y0=med_y, x1=x_max, y1=y_max,
                  fillcolor="rgba(22, 163, 74, 0.08)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=med_x, y0=y_min, x1=x_max, y1=med_y,
                  fillcolor="rgba(37, 99, 235, 0.08)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=x_min, y0=med_y, x1=med_x, y1=y_max,
                  fillcolor="rgba(217, 119, 6, 0.08)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=x_min, y0=y_min, x1=med_x, y1=med_y,
                  fillcolor="rgba(220, 38, 38, 0.08)", line_width=0, layer="below")

    color_palette = {
        "Chirurgicaux (Haute précision & conversion)": "#16A34A",
        "Volumeux (Domination stérile devant le but)": "#2563EB",
        "Réalistes (Opportunisme clinique en contre)": "#D97706",
        "En difficulté (Manque de précision et de réalisme)": "#DC2626"
    }

    for prof, grp in team_df.groupby("ProfilTactique"):
        fig.add_trace(go.Scatter(
            x=grp["PrecisionCadrePct"],
            y=grp["ConversionButsPct"],
            mode='markers+text',
            name=prof.split("(")[0].strip(),
            text=grp["Team"],
            textposition="top center",
            textfont=dict(size=10, color=text_color),
            marker=dict(
                size=np.clip(grp["Points"] / 3.4, 9, 30),
                color=color_palette.get(prof, "#64748B"),
                line=dict(color="#0F172A", width=1.2),
                opacity=0.88
            ),
            hovertemplate="<b>%{text}</b><br>Précision : %{x:.1f} %<br>Conversion : %{y:.1f} %<br>Points totaux : %{customdata[0]}<br>Points/Tir cadré : %{customdata[1]:.2f}<extra></extra>",
            customdata=grp[["Points", "PointsParTirCadre"]].values
        ))

    # Median threshold lines
    fig.add_vline(x=med_x, line_dash="dash", line_color="#94A3B8", line_width=1.5)
    fig.add_hline(y=med_y, line_dash="dash", line_color="#94A3B8", line_width=1.5)

    # Quadrant annotations
    fig.add_annotation(x=x_max - 1, y=y_max - 1, text="<b>ZONE ÉLITE : Chirurgicaux</b>", showarrow=False, font=dict(color="#16A34A", size=11))
    fig.add_annotation(x=x_min + 1, y=y_max - 1, text="<b>Contre-attaque réaliste</b>", showarrow=False, font=dict(color="#D97706", size=11))
    fig.add_annotation(x=x_max - 1, y=y_min + 1, text="<b>Volume stérile</b>", showarrow=False, font=dict(color="#2563EB", size=11))
    fig.add_annotation(x=x_min + 1, y=y_min + 1, text="<b>Zone de relégation</b>", showarrow=False, font=dict(color="#DC2626", size=11))

    fig.update_layout(
        title=dict(
            text="<b>Matrice Tactique : Précision au cadrage vs Conversion clinique (Taille = Points)</b>",
            font=dict(size=15, color=text_color)
        ),
        xaxis=dict(
            title="Précision au cadrage (Tirs cadrés / Tirs totaux en %)",
            range=[x_min, x_max],
            color=text_color,
            gridcolor="#334155" if is_dark else "#F1F5F9"
        ),
        yaxis=dict(
            title="Taux de conversion (Buts / Tirs cadrés en %)",
            range=[y_min, y_max],
            color=text_color,
            gridcolor="#334155" if is_dark else "#F1F5F9"
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_color, size=10)),
        height=540,
        margin=dict(l=20, r=20, t=70, b=40)
    )
    return fig

def create_club_radar_chart(
    team_stats: pd.DataFrame,
    selected_teams: list = None,
    theme: str = "light"
) -> go.Figure:
    """Plots a 360-degree tactical radar profiling selected clubs against the Premier League benchmark."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    categories = [
        "Précision Cadrage (%)",
        "Conversion Buts (%)",
        "Points / Tir Cadré (x100)",
        "Tirs Cadrés / Match (x10)",
        "Points / Match (x25)"
    ]

    # Benchmark league average
    league_acc = team_stats["PrecisionCadrePct"].mean()
    league_conv = team_stats["ConversionButsPct"].mean()
    league_pts_sot = team_stats["PointsParTirCadre"].mean() * 100
    league_sot_match = team_stats["TirsCadresParMatch"].mean() * 10
    league_pts_match = (team_stats["Points"] / team_stats["Matchs"]).mean() * 25

    league_vals = [league_acc, league_conv, league_pts_sot, league_sot_match, league_pts_match]
    league_vals.append(league_vals[0])  # Close the radar loop

    cats_closed = categories + [categories[0]]
    fig = go.Figure()

    # League benchmark
    fig.add_trace(go.Scatterpolar(
        r=league_vals,
        theta=cats_closed,
        name="Moyenne Premier League",
        line=dict(color="#94A3B8", dash="dash", width=1.5),
        fill='none'
    ))

    # Determine teams to plot
    teams_to_plot = selected_teams if (selected_teams and len(selected_teams) > 0) else team_stats.head(2)["Team"].tolist()
    teams_to_plot = teams_to_plot[:2]  # Limit to 2 for visual clarity

    colors = ["#2563EB", "#EA580C"]
    for idx, team in enumerate(teams_to_plot):
        row = team_stats[team_stats["Team"] == team]
        if row.empty:
            continue
        r = row.iloc[0]
        vals = [
            r["PrecisionCadrePct"],
            r["ConversionButsPct"],
            r["PointsParTirCadre"] * 100,
            r["TirsCadresParMatch"] * 10,
            (r["Points"] / r["Matchs"]) * 25
        ]
        vals.append(vals[0])

        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=cats_closed,
            name=team,
            line=dict(color=colors[idx % len(colors)], width=2.5),
            fill='toself',
            opacity=0.35
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 55], color=text_color, gridcolor="#334155" if is_dark else "#E2E8F0"),
            angularaxis=dict(color=text_color, gridcolor="#334155" if is_dark else "#E2E8F0")
        ),
        title=dict(
            text="<b>Profil Tactique 360° : Évaluation Scout & Recrutement vs Moyenne Ligue</b>",
            font=dict(size=14, color=text_color)
        ),
        showlegend=True,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=380,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    return fig

from engine.pl_visuals_crowd import (
    create_home_advantage_comparison_chart,
    create_seasons_timeline_chart,
    create_club_home_impact_dumbbell
)

def create_xg_comparison_bar(
    home_team: str,
    away_team: str,
    exp_home: float,
    exp_away: float,
    theme: str = "light"
) -> go.Figure:
    """Plots a clean comparative bar of expected goals (xG)."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[exp_home],
        y=[f"{home_team} (Dom)"],
        orientation='h',
        marker_color="#2563EB",
        text=[f"{exp_home:.2f} buts"],
        textposition="inside",
        name=home_team
    ))

    fig.add_trace(go.Bar(
        x=[exp_away],
        y=[f"{away_team} (Ext)"],
        orientation='h',
        marker_color="#EA580C",
        text=[f"{exp_away:.2f} buts"],
        textposition="inside",
        name=away_team
    ))

    fig.update_layout(
        title=dict(
            text="<b>Espérance de buts attendus (xG Model)</b>",
            font=dict(size=13, color=text_color)
        ),
        xaxis=dict(title="Buts attendus", range=[0, max(exp_home, exp_away) * 1.3], color=text_color),
        yaxis=dict(color=text_color),
        showlegend=False,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=160,
        margin=dict(l=10, r=10, t=35, b=25)
    )
    return fig

