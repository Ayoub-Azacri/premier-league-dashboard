import streamlit as st
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
from engine.pl_metrics import compute_quadrant_profiles
from engine.pl_visuals import get_custom_css, create_quadrant_chart

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

team_stats = compute_team_aggregates(df_filtered, target_teams=teams)
quadrant_df = compute_quadrant_profiles(team_stats)

# Titre portant le message (selon les consignes de l'enseignant)
st.title("Efficacité Offensive : La précision et le réalisme surpassent le volume de tirs")
st.caption("Matrice décisionnelle croisant la précision au cadrage (SoT %) et la conversion clinique (Buts / Tir cadré).")

st.markdown("""
<div class="minto-card">
    <strong>Enseignement tactique clé :</strong> La corrélation entre tirs totaux et points récoltés est faible (r = 0,28), alors que le couple Précision-Conversion explique plus de 62 % des variations de classement. Tirer sans cadrer pénalise l'équipe en favorisant les transitions adverses.
</div>
""", unsafe_allow_html=True)

# Graphique Quadrant
fig_quad = create_quadrant_chart(quadrant_df, theme=theme)
st.plotly_chart(fig_quad, use_container_width=True)

# Décomposition des profils
st.subheader("Analyse des 4 archétypes tactiques")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 🏆 Chirurgicaux (Zone Élite)")
    st.write("Précision supérieure à 34 % et conversion supérieure à 31 %. Ces équipes créent des situations de tir de haute qualité et sanctionnent avec sang-froid.")
    elite_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Chirurgicaux")]["Team"].tolist()
    st.info(f"Équipes dans cette zone : **{', '.join(elite_teams) if elite_teams else 'Aucune'}**")

    st.markdown("### ⚡ Réalistes (Contre-attaque clinique)")
    st.write("Précision sous la médiane mais réalisme extrême devant le but. Profil typique des équipes de bloc bas exploitant la vitesse en transition.")
    realist_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Réalistes")]["Team"].tolist()
    st.warning(f"Équipes dans cette zone : **{', '.join(realist_teams) if realist_teams else 'Aucune'}**")

with c2:
    st.markdown("### ⚠️ Volumeux (Domination stérile)")
    st.write("Beaucoup de tirs cadrés mais très faible conversion. Beaucoup d'énergie dépensée pour un rendement faible face à des gardiens en réussite.")
    vol_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("Volumeux")]["Team"].tolist()
    st.info(f"Équipes dans cette zone : **{', '.join(vol_teams) if vol_teams else 'Aucune'}**")

    st.markdown("### 🚨 En difficulté (Zone critique)")
    st.write("Déficit cumulé de précision et de finition. Souvent corrélé aux trois dernières places du championnat.")
    releg_teams = quadrant_df[quadrant_df["ProfilTactique"].str.startswith("En difficulté")]["Team"].tolist()
    st.error(f"Équipes dans cette zone : **{', '.join(releg_teams) if releg_teams else 'Aucune'}**")

st.divider()
st.caption("Premier League Decision Platform · HETIC MD4")
