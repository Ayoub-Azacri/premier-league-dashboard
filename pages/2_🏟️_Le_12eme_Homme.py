import streamlit as st
import pandas as pd
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

for mod in ["engine.pl_data_loader", "engine.pl_metrics", "engine.pl_visuals", "engine.pl_visuals_crowd", "engine.pl_styles"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from engine.pl_data_loader import load_pl_data
from engine.pl_metrics import (
    compute_home_advantage_comparison,
    compute_season_outcomes,
    compute_club_crowd_sensitivity
)
from engine.pl_visuals import (
    get_custom_css,
    create_home_advantage_comparison_chart,
    create_seasons_timeline_chart,
    create_club_home_impact_dumbbell
)

st.set_page_config(
    page_title="L'Effet Domicile · Premier League",
    page_icon="🏟️",
    layout="wide"
)

theme = "dark" if st.session_state.get('dark_mode', False) else "light"
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

df_raw = load_pl_data()
comp_stats = compute_home_advantage_comparison(df_raw)

st.title("L'effet domicile : le public fait-il vraiment gagner les matchs ?")
st.caption("Analyse tactique sur 1 900 matchs de Premier League : comment l'absence de supporters en 2020-21 a transformé le comportement des équipes.")

st.info("💡 **Ce que les chiffres révèlent au staff :** Recevoir à domicile offre d'ordinaire un avantage décisif (près d'une victoire sur deux). Privées de leurs supporters en 2020-21, les équipes locales ont vu leur taux de succès s'effondrer : les visiteurs ont remporté plus de matchs (40,3 %) que les clubs receveurs (37,9 %).")

# 3 KPIs d'impact
k1, k2, k3 = st.columns(3)
k1.metric(
    "Victoires à domicile avec public",
    f"{comp_stats['normal']['home_win']:.1f} %",
    "Standard habituel en Premier League"
)
k2.metric(
    "Victoires à domicile à huis clos",
    f"{comp_stats['covid']['home_win']:.1f} %",
    f"-{comp_stats['home_drop_pts']:.1f} pts sans supporters",
    delta_color="inverse"
)
k3.metric(
    "Victoires des visiteurs à huis clos",
    f"{comp_stats['covid']['away_win']:.1f} %",
    f"+{comp_stats['away_boost_pts']:.1f} pts pour les visiteurs",
    delta_color="normal"
)

# 1. Évolution temporelle sur 5 saisons
st.subheader("1. Évolution des victoires sur 5 saisons : la bascule historique")
st.caption("Observez le croisement lors de la saison à huis clos : la courbe des victoires à l'extérieur passe pour la première fois au-dessus de celle du domicile.")
seasons_df = compute_season_outcomes(df_raw)
fig_timeline = create_seasons_timeline_chart(seasons_df, theme=theme)
st.plotly_chart(fig_timeline, use_container_width=True)

# 2. Zone d'impact par club et synthèse
st.subheader("2. Quels clubs dépendent le plus de la ferveur de leur stade ?")
st.caption("Chute du pourcentage de victoires à domicile sans public. Les stades à forte ambiance comme Anfield (Liverpool), St James' Park (Newcastle) ou l'Emirates (Arsenal) accusent les plus fortes baisses.")
col_db, col_stack = st.columns([1.25, 0.75])

with col_db:
    sens_df = compute_club_crowd_sensitivity(df_raw)
    fig_db = create_club_home_impact_dumbbell(sens_df, theme=theme)
    st.plotly_chart(fig_db, use_container_width=True)

with col_stack:
    fig_home = create_home_advantage_comparison_chart(comp_stats, theme=theme)
    st.plotly_chart(fig_home, use_container_width=True)

st.subheader("Leçons tactiques pour le staff technique")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 📋 Préparation des matchs à l'extérieur")
    st.write("Sans la pression acoustique du public adverse, les joueurs visiteurs osent presser plus haut, tentent plus de passes vers l'avant et commettent moins de fautes sous panique. Pour un entraîneur en déplacement, la donnée confirme qu'il ne faut pas se replier en bloc bas mais imposer son jeu.")

with c2:
    st.markdown("### ⚖️ Pression arbitrale et gestion des temps faibles")
    st.write("La présence des supporters pèse directement sur les décisions arbitrales lors des moments chauds. Avec du public, les receveurs obtiennent un écart de +0,44 but par match en moyenne. À huis clos, cet avantage tombe à seulement +0,07 but, prouvant que le stade protège l'équipe qui reçoit.")

st.divider()
st.caption("Premier League Dashboard · Bachelor Data et IA · Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL")
