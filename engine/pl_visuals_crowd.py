import plotly.graph_objects as go
import pandas as pd

def create_home_advantage_comparison_chart(comp_stats: dict, theme: str = "light") -> go.Figure:
    """Plots comparative stacked bars showing the collapse in home wins during COVID."""
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
            text="<b>Synthèse Globale : Répartition des issues (Normal vs Huis clos)</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(color=text_color),
        yaxis=dict(title="Proportion des matchs (%)", range=[0, 100], color=text_color),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_color)),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=320,
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

def create_seasons_timeline_chart(seasons_df: pd.DataFrame, theme: str = "light") -> go.Figure:
    """Plots a 5-season chronological timeline highlighting the 2020-21 closed-door drop."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=seasons_df["Saison"],
        y=seasons_df["VictoireDomicilePct"],
        mode='lines+markers',
        name="Victoires Domicile (%)",
        line=dict(color="#2563EB", width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=seasons_df["Saison"],
        y=seasons_df["VictoireExterieurPct"],
        mode='lines+markers',
        name="Victoires Extérieur (%)",
        line=dict(color="#EA580C", width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=seasons_df["Saison"],
        y=seasons_df["NulPct"],
        mode='lines+markers',
        name="Matchs Nuls (%)",
        line=dict(color="#94A3B8", width=2, dash="dot"),
        marker=dict(size=6)
    ))

    # Highlight COVID season 2020-21
    fig.add_vrect(
        x0="2020-21", x1="2020-21",
        fillcolor="rgba(239, 68, 68, 0.12)",
        line=dict(color="#EF4444", width=1.5, dash="dash"),
        annotation_text="<b>Huis Clos COVID (Chute à 37,9 %)</b>",
        annotation_position="top left",
        annotation_font=dict(color="#DC2626", size=11)
    )

    fig.update_layout(
        title=dict(
            text="<b>Évolution Chronologique (2019–2024) : L'inversion historique du Huis Clos</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(title="Saison", color=text_color),
        yaxis=dict(title="Part des issues (%)", range=[15, 55], color=text_color, gridcolor="#334155" if is_dark else "#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_color)),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=340,
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

def create_club_home_impact_dumbbell(sensitivity_df: pd.DataFrame, theme: str = "light") -> go.Figure:
    """Plots a Cleveland dumbbell chart showing the Anfield Effect (home win drop per club)."""
    is_dark = (theme == "dark")
    text_color = "#E2E8F0" if is_dark else "#1E293B"
    bg_color = "rgba(0,0,0,0)"

    top_clubs = sensitivity_df.head(10).iloc[::-1].copy()

    fig = go.Figure()

    # Lines connecting the dots
    for _, row in top_clubs.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["CovidWinPct"], row["NormalWinPct"]],
            y=[row["Team"], row["Team"]],
            mode='lines',
            line=dict(color="#94A3B8", width=2),
            showlegend=False,
            hoverinfo='none'
        ))

    # COVID win dot
    fig.add_trace(go.Scatter(
        x=top_clubs["CovidWinPct"],
        y=top_clubs["Team"],
        mode='markers',
        name="Sans Public (Huis clos)",
        marker=dict(color="#DC2626", size=10),
        hovertemplate="<b>%{y}</b><br>Huis clos : %{x:.1f} %<extra></extra>"
    ))

    # Normal win dot
    fig.add_trace(go.Scatter(
        x=top_clubs["NormalWinPct"],
        y=top_clubs["Team"],
        mode='markers',
        name="Avec Public (Normal)",
        marker=dict(color="#2563EB", size=10),
        hovertemplate="<b>%{y}</b><br>Avec public : %{x:.1f} %<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="<b>L'Effet Anfield & St James' Park : Chute du taux de victoires à domicile sans supporters</b>",
            font=dict(size=14, color=text_color)
        ),
        xaxis=dict(
            title="Taux de victoire à domicile (%)",
            range=[15, 95],
            color=text_color,
            gridcolor="#334155" if is_dark else "#F1F5F9"
        ),
        yaxis=dict(color=text_color),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_color)),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        height=380,
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig
