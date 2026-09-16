import streamlit as st
import pandas as pd
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

for mod in ["engine.pl_data_loader", "engine.pl_metrics", "engine.pl_visuals", "engine.pl_visuals_crowd", "engine.pl_styles"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from engine.pl_data_loader import (
    load_pl_data,
    get_available_seasons,
    get_available_teams,
    filter_matches,
    compute_team_aggregates
)
from engine.pl_metrics import compute_quadrant_profiles
from engine.pl_visuals import (
    get_custom_css,
    create_quadrant_chart,
    create_club_radar_chart
)

st.set_page_config(
    page_title="Efficacité Offensive · Premier League",
    page_icon="🎯",
    layout="wide"
)

# Appliquer le thème actif
theme = "dark" if st.session_state.get('dark_mode', False) else "light"
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

df_raw = load_pl_data()

# Sidebar filtres
with st.sidebar:
    st.markdown("### 🎯 Filtres d'Efficacité")
    seasons = st.multiselect("Saisons :", options=get_available_seasons(df_raw), default=get_available_seasons(df_raw))
    teams = st.multiselect("Filtrer des équipes spécifiques :", options=get_available_teams(df_raw), default=[])
    venue = st.radio("Lieu :", ["Tous", "Domicile", "Extérieur"], horizontal=True)

df_filtered = filter_matches(df_raw, seasons=seasons, teams=teams, venue=venue)

if df_filtered.empty:
    st.warning("⚠️ Aucun match pour cette sélection.")
    st.stop()

team_stats = compute_team_aggregates(df_filtered, target_teams=teams, venue=venue)
quadrant_df = compute_quadrant_profiles(team_stats)

# Titre portant le message tactique
st.title("Efficacité offensive : cadrer et convertir plutôt que tirer à l'aveugle")
st.caption("Évaluation de la qualité des tirs et du sang-froid devant le gardien adverse.")

st.info("💡 **Repère pour le coach :** Accumuler les frappes lointaines sans cadrer pénalise l'équipe et offre des relances faciles à l'adversaire. La différence entre les équipes du haut de tableau et les relégables se fait d'abord sur la sélection du tir et le calme devant le but.")

# Graphique Quadrant
fig_quad = create_quadrant_chart(quadrant_df, theme=theme)
st.plotly_chart(fig_quad, use_container_width=True)

# Décomposition des profils
st.subheader("Lecture tactique des 4 profils d'équipes")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 🏆 Haute efficacité (Cadrent et marquent)")
    st.write("Précision supérieure à 34 % et finition supérieure à 31 %. Ces équipes créent des situations de tir nettes et trompent le gardien une fois sur trois.")
    elite_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Haute efficacité")]["Team"].tolist()
    st.info(f"Équipes dans cette zone : **{', '.join(elite_teams) if elite_teams else 'Aucune'}**")

    st.markdown("### ⚡ Opportunistes en contre (Peu de frappes, grande finition)")
    st.write("Équipes souvent regroupées en bloc bas : elles tirent peu car elles subissent la possession, mais chaque frappe cadrée est une balle de but exploitée à haute intensité.")
    realist_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Opportunistes")]["Team"].tolist()
    st.warning(f"Équipes dans cette zone : **{', '.join(realist_teams) if realist_teams else 'Aucune'}**")

with c2:
    st.markdown("### ⚠️ Manque de tranchant (Cadrent sans marquer)")
    st.write("Beaucoup de tirs cadrés mais peu de buts. Frappes trop écrasées, prévisibles ou gardiens adverses en réussite : l'énergie dépensée ne se traduit pas au tableau d'affichage.")
    vol_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Manque de tranchant")]["Team"].tolist()
    st.info(f"Équipes dans cette zone : **{', '.join(vol_teams) if vol_teams else 'Aucune'}**")

    st.markdown("### 🚨 Attaque en panne (Ni précision, ni finition)")
    st.write("Déficit cumulé au cadrage et à la finition. Le danger pour la défense adverse est quasi nul tant que les lignes restent en place.")
    releg_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Attaque en panne")]["Team"].tolist()
    st.error(f"Équipes dans cette zone : **{', '.join(releg_teams) if releg_teams else 'Aucune'}**")

st.divider()

# Profilage Radar 360°
st.subheader("Radar comparatif : profil d'attaque d'un club face à la ligue")
st.caption("Comparez les caractéristiques offensives des clubs sélectionnés aux repères moyens de Premier League.")

target_radar = teams if len(teams) > 0 else team_stats.head(2)["Team"].tolist()
fig_radar = create_club_radar_chart(team_stats, selected_teams=target_radar, theme=theme)
st.plotly_chart(fig_radar, use_container_width=True)

st.divider()
st.caption("Premier League Dashboard · Bachelor Data et IA · Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL")
