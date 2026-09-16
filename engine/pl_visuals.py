import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def get_custom_css(theme: str = "light") -> str:
    """Returns custom CSS for an executive sports analytics dashboard."""
    is_dark = (theme == "dark")
    bg_card = "#1E293B" if is_dark else "#FFFFFF"
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#64748B"
    border_color = "#334155" if is_dark else "#E2E8F0"
    minto_bg = "#172554" if is_dark else "#EFF6FF"
    minto_border = "#1E3A8A" if is_dark else "#BFDBFE"
    minto_text = "#93C5FD" if is_dark else "#1E3A8A"

    return f"""
    <style>
    .hero-banner {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .hero-badge {{
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #2563EB;
        background: {minto_bg};
        border: 1px solid {minto_border};
        border-radius: 9999px;
        padding: 4px 12px;
        margin-bottom: 8px;
    }}
    .hero-title {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {text_color};
        margin: 6px 0 8px 0;
        line-height: 1.25;
    }}
    .hero-subtitle {{
        font-size: 0.95rem;
        color: {sub_color};
        margin-bottom: 12px;
        line-height: 1.5;
    }}
    .minto-card {{
        background: {minto_bg};
        border-left: 4px solid #2563EB;
        border-top: 1px solid {minto_border};
        border-right: 1px solid {minto_border};
        border-bottom: 1px solid {minto_border};
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.92rem;
        color: {text_color};
        line-height: 1.45;
    }}
    .minto-highlight {{
        font-weight: 700;
        color: {minto_text};
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }}
    div[data-testid="stMetricDelta"] {{
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}
    </style>
    """

def create_efficiency_ranking_chart(team_df: pd.DataFrame, theme: str = "light") -> go.Figure:
    """Plots a clean horizontal bar chart ranking teams by conversion and accuracy."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    top_teams = team_df.head(15).iloc[::-1]  # Reverse for bottom-to-top order in horizontal bar

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_teams["ConversionButsPct"],
        y=top_teams["Team"],
        orientation='h',
        marker=dict(
            color=top_teams["ConversionButsPct"],
            colorscale='Blues',
            line=dict(color='#1E3A8A', width=1)
        ),
        text=[f"{val:.1f} %" for val in top_teams["ConversionButsPct"]],
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Conversion : %{x:.1f} %<br>Précision cadrée : %{customdata[0]:.1f} %<extra></extra>",
        customdata=top_teams[["PrecisionCadrePct"]].values
    ))

    fig.update_layout(
        title=dict(
            text="<b>Classement d'efficacité clinique : Taux de conversion (Buts / Tir cadré)</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(
            title="Taux de conversion (%)",
            range=[0, max(top_teams["ConversionButsPct"].max() + 8, 45)],
            color=text_color,
            gridcolor="#334155" if is_dark else "#F1F5F9"
        ),
        yaxis=dict(color=text_color),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=10, r=20, t=40, b=30),
        height=450
    )
    return fig

def create_quadrant_chart(team_df: pd.DataFrame, theme: str = "light") -> go.Figure:
    """Plots the 4-quadrant strategic map: Accuracy (Precision) vs Conversion."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    med_x = team_df["PrecisionCadrePct"].median()
    med_y = team_df["ConversionButsPct"].median()

    color_palette = {
        "Chirurgicaux (Haute précision & conversion)": "#16A34A",
        "Volumeux (Domination stérile devant le but)": "#2563EB",
        "Réalistes (Opportunisme clinique en contre)": "#D97706",
        "En difficulté (Manque de précision et de réalisme)": "#DC2626"
    }

    fig = go.Figure()

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
                size=grp["PointsParTirCadre"] * 28 + 8,
                color=color_palette.get(prof, "#64748B"),
                line=dict(color="#0F172A", width=1),
                opacity=0.85
            ),
            hovertemplate="<b>%{text}</b><br>Précision : %{x:.1f} %<br>Conversion : %{y:.1f} %<br>Points/Tir cadré : %{customdata:.2f}<extra></extra>",
            customdata=grp["PointsParTirCadre"]
        ))

    # Median threshold lines
    fig.add_vline(x=med_x, line_dash="dash", line_color="#94A3B8", line_width=1.5)
    fig.add_hline(y=med_y, line_dash="dash", line_color="#94A3B8", line_width=1.5)

    # Quadrant annotations
    x_min, x_max = team_df["PrecisionCadrePct"].min() - 2, team_df["PrecisionCadrePct"].max() + 3
    y_min, y_max = team_df["ConversionButsPct"].min() - 3, team_df["ConversionButsPct"].max() + 4

    fig.add_annotation(x=x_max - 1, y=y_max - 1, text="<b>ZONE ÉLITE : Chirurgicaux</b>", showarrow=False, font=dict(color="#16A34A", size=11))
    fig.add_annotation(x=x_min + 1, y=y_max - 1, text="<b>Contre-attaque réaliste</b>", showarrow=False, font=dict(color="#D97706", size=11))
    fig.add_annotation(x=x_max - 1, y=y_min + 1, text="<b>Volume stérile</b>", showarrow=False, font=dict(color="#2563EB", size=11))
    fig.add_annotation(x=x_min + 1, y=y_min + 1, text="<b>Zone de relégation</b>", showarrow=False, font=dict(color="#DC2626", size=11))

    fig.update_layout(
        title=dict(
            text="<b>Matrice Tactique : Précision au tir vs Conversion clinique</b>",
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

def create_home_advantage_comparison_chart(comp_stats: dict, theme: str = "light") -> go.Figure:
    """Plots comparative stacked or grouped bars showing the drop in home wins during COVID."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    categories = ["Saisons avec public (Normales)", "Saison 2020-21 (Huis clos COVID)"]
    home_wins = [comp_stats["normal"]["home_win"], comp_stats["covid"]["home_win"]]
    draws = [comp_stats["normal"]["draw"], comp_stats["covid"]["draw"]]
    away_wins = [comp_stats["normal"]["away_win"], comp_stats["covid"]["away_win"]]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Victoires Domicile",
        x=categories,
        y=home_wins,
        marker_color="#2563EB",
        text=[f"{v:.1f} %" for v in home_wins],
        textposition="inside"
    ))
    fig.add_trace(go.Bar(
        name="Matchs Nuls",
        x=categories,
        y=draws,
        marker_color="#94A3B8",
        text=[f"{v:.1f} %" for v in draws],
        textposition="inside"
    ))
    fig.add_trace(go.Bar(
        name="Victoires Extérieur",
        x=categories,
        y=away_wins,
        marker_color="#EA580C",
        text=[f"{v:.1f} %" for v in away_wins],
        textposition="inside"
    ))

    fig.update_layout(
        barmode='stack',
        title=dict(
            text="<b>Répartition des issues de match : Effondrement du 12e Homme pendant le huis clos</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(color=text_color),
        yaxis=dict(title="Proportion des matchs (%)", range=[0, 100], color=text_color),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_color)),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=380,
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig
