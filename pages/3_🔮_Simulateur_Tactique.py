import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

for mod in ["engine.pl_data_loader", "engine.pl_metrics", "engine.pl_visuals", "engine.pl_visuals_crowd", "engine.pl_styles"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from engine.pl_data_loader import (
    load_pl_data,
    get_available_teams,
    compute_team_aggregates
)
from engine.pl_metrics import (
    simulate_match_outcome,
    compute_poisson_score_distribution
)
from engine.pl_visuals import (
    get_custom_css,
    create_xg_comparison_bar
)

st.set_page_config(
    page_title="Simulateur Tactique · Premier League",
    page_icon="🔮",
    layout="wide"
)

theme = "dark" if st.session_state.get('dark_mode', False) else "light"
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

df_raw = load_pl_data()
team_stats = compute_team_aggregates(df_raw)
teams_list = get_available_teams(df_raw)

st.title("Simulateur Tactique Prédictif : Confrontation & Espérance de Buts")
st.caption("Modélisation prédictive d'aide à la décision basée sur les métriques d'efficacité historique des clubs.")

st.markdown("""
<div class="minto-card">
    <strong>Usage pour le staff technique :</strong> Cet outil combine la puissance offensive relative, la résistance défensive et la prime de terrain pour simuler la probabilité de chaque issue de match avant la préparation tactique.
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    col1, col2, col3 = st.columns([1.2, 1.2, 1])

    with col1:
        default_home = "Arsenal" if "Arsenal" in teams_list else teams_list[0]
        home_team = st.selectbox("Équipe recevante (Domicile) :", options=teams_list, index=teams_list.index(default_home))

    with col2:
        away_options = [t for t in teams_list if t != home_team]
        default_away = "Man City" if "Man City" in away_options else away_options[0]
        away_team = st.selectbox("Équipe visiteuse (Extérieur) :", options=away_options, index=away_options.index(default_away))

    with col3:
        crowd_status = st.toggle("🏟️ Présence du public", value=True, help="Désactiver pour simuler un match à huis clos")

is_closed = not crowd_status
sim = simulate_match_outcome(home_team, away_team, team_stats, is_closed_doors=is_closed)

# Affichage des résultats
st.subheader(f"Pronostic statistique : {home_team} vs {away_team}")

r1, r2, r3 = st.columns(3)
r1.metric(f"Victoire {home_team}", f"{sim['home_prob']:.1f} %", f"{sim['exp_home_goals']:.2f} buts espérés")
r2.metric("Match Nul", f"{sim['draw_prob']:.1f} %", "Score serré")
r3.metric(f"Victoire {away_team}", f"{sim['away_prob']:.1f} %", f"{sim['exp_away_goals']:.2f} buts espérés")

# Barre de distribution de probabilité
fig_prob = go.Figure()
fig_prob.add_trace(go.Bar(
    x=[sim['home_prob']], y=["Issue"], orientation='h', name=f"Victoire {home_team}",
    marker_color="#2563EB", text=[f"{sim['home_prob']:.1f} %"], textposition="inside"
))
fig_prob.add_trace(go.Bar(
    x=[sim['draw_prob']], y=["Issue"], orientation='h', name="Nul",
    marker_color="#94A3B8", text=[f"{sim['draw_prob']:.1f} %"], textposition="inside"
))
fig_prob.add_trace(go.Bar(
    x=[sim['away_prob']], y=["Issue"], orientation='h', name=f"Victoire {away_team}",
    marker_color="#EA580C", text=[f"{sim['away_prob']:.1f} %"], textposition="inside"
))

fig_prob.update_layout(
    barmode='stack',
    xaxis=dict(range=[0, 100], showticklabels=False),
    yaxis=dict(showticklabels=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    height=140,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=30, b=10)
)
st.plotly_chart(fig_prob, use_container_width=True)

# Modélisation xG et Scores exacts Poisson
col_xg, col_scores = st.columns([1.1, 0.9])

with col_xg:
    fig_xg = create_xg_comparison_bar(home_team, away_team, sim['exp_home_goals'], sim['exp_away_goals'], theme=theme)
    st.plotly_chart(fig_xg, use_container_width=True)

with col_scores:
    st.markdown("**Scores exacts les plus probables (Modèle Poisson) :**")
    top_scores = compute_poisson_score_distribution(sim['exp_home_goals'], sim['exp_away_goals'], top_n=3)
    sc1, sc2, sc3 = st.columns(3)
    for col_s, s_info in zip([sc1, sc2, sc3], top_scores):
        col_s.metric(f"Score {s_info['score']}", f"{s_info['prob']:.1f} %")

# Verdict et Clés tactiques
c_v1, c_v2 = st.columns([1.2, 0.8])
with c_v1:
    st.info(f"📋 **Verdict tactique :** {sim['verdict']}")
    st.markdown("**Points d'appui statistiques clés :**")
    for key in sim['keys']:
        st.markdown(f"- {key}")

with c_v2:
    h_row = team_stats[team_stats["Team"] == home_team].iloc[0]
    a_row = team_stats[team_stats["Team"] == away_team].iloc[0]
    st.markdown("**Face-à-face d'efficacité :**")
    st.write(f"- Précision de cadrage : **{h_row['PrecisionCadrePct']}%** vs **{a_row['PrecisionCadrePct']}%**")
    st.write(f"- Taux de conversion : **{h_row['ConversionButsPct']}%** vs **{a_row['ConversionButsPct']}%**")
    st.write(f"- Buts marqués / match : **{h_row['ButsParMatch']}** vs **{a_row['ButsParMatch']}**")

st.divider()
st.caption("Premier League Decision Platform · HETIC MD4")
