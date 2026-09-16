import streamlit as st
import pandas as pd
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
from engine.pl_metrics import compute_executive_kpis
from engine.pl_visuals import (
    get_custom_css,
    create_efficiency_ranking_chart,
    create_shot_funnel_chart
)

# 1. Configuration de la page
st.set_page_config(
    page_title="Premier League Analytics · Décision & Performance",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Ingestion des données avec cache
df_raw = load_pl_data()

# 3. Barre latérale & Thème
with st.sidebar:
    st.markdown("### ⚽ Premier League Analytics")
    st.caption("Aide à la décision pour Direction Sportive & Recrutement")
    st.markdown("<span style='font-size:0.75rem; color:#64748B;'>Équipe : AZACRI · EL HAJJI · HAKIK · DEKHAIL</span>", unsafe_allow_html=True)

    dark_mode = st.toggle("🌙 Mode Sombre", value=st.session_state.get('dark_mode', False))
    st.session_state['dark_mode'] = dark_mode
    theme = "dark" if dark_mode else "light"
    st.markdown(get_custom_css(theme), unsafe_allow_html=True)
    st.divider()

    st.markdown("**🔍 Filtres analytiques**")
    all_seasons = get_available_seasons(df_raw)
    selected_seasons = st.multiselect("Saisons :", options=all_seasons, default=all_seasons)

    all_teams = get_available_teams(df_raw)
    selected_teams = st.multiselect("Clubs cibles :", options=all_teams, default=[], placeholder="Tous les clubs (ligue entière)")

    venue_option = st.radio("Lieu des rencontres :", ["Tous", "Domicile", "Extérieur"], horizontal=True)

    if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
        st.rerun()

    st.divider()
    st.info("💡 **Navigation multi-pages** : Utilisez le menu de gauche pour accéder aux analyses détaillées (*Efficacité Offensive*, *Le 12e Homme*, *Simulateur Tactique*).")

# 4. Filtrage dynamique
df_filtered = filter_matches(
    df_raw,
    seasons=selected_seasons,
    teams=selected_teams,
    venue=venue_option
)

if df_filtered.empty:
    st.warning("⚠️ Aucun match ne correspond aux filtres sélectionnés.")
    st.stop()

# 5. Hero Banner Exécutif
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Étude Stratégique · N=1 900 matchs (2019-2024)</div>
    <h1 class="hero-title">L'efficacité de tir surpasse le volume : l'élite de Premier League se décide au cadrage et à la conversion</h1>
    <p class="hero-subtitle">Plateforme décisionnelle conçue pour la direction technique et la cellule de recrutement des clubs professionnels.</p>
    <div class="hero-credits">
        <strong>Équipe :</strong> Ayoub AZACRI · Youssef EL HAJJI · Omar HAKIK · Youssef DEKHAIL · HETIC MD4
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Zone KPIs Exécutifs (2 à 3 indicateurs maximum, contextualisés)
kpi_data = compute_executive_kpis(df_filtered, venue=venue_option, teams=selected_teams)

c1, c2, c3 = st.columns(3)
c1.metric(
    "Taux de cadrage net",
    f"{kpi_data['shot_accuracy']:.1f} %",
    f"{kpi_data['accuracy_diff']:+.1f} pts vs moyenne ligue (34,0 %)",
    delta_color="normal" if kpi_data['accuracy_diff'] >= 0 else "inverse"
)
c2.metric(
    "Taux de conversion clinique",
    f"{kpi_data['conversion_rate']:.1f} %",
    f"{kpi_data['conversion_diff']:+.1f} pts vs moyenne ligue (31,0 %)",
    delta_color="normal" if kpi_data['conversion_diff'] >= 0 else "inverse"
)
c3.metric(
    f"Buts / match ({venue_option})",
    f"{kpi_data['goals_per_match']:.2f}",
    f"{kpi_data['matches']} matchs analysés"
)

# 7. Synthèse Minto & Entonnoir d'Efficacité
col_minto, col_funnel = st.columns([1.2, 0.8])

with col_minto:
    st.markdown("""
    <div class="minto-card">
        <strong>Synthèse de cadrage (Minto) :</strong> Accumuler des frappes non cadrées réduit la rentabilité globale d'une équipe. Les prétendants au titre se distinguent par une précision de cadrage supérieure à 36 % et un taux de conversion supérieur à 33 %, convertissant chaque tir cadré en 0,31 but contre 0,08 pour les équipes reléguées.
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 **Observation clé :** Près de deux tiers des frappes (65 %) sont gaspillées hors cadre. La priorité d'entraînement doit porter sur la sélection des tirs plutôt que sur le volume brut.")

with col_funnel:
    if venue_option == "Domicile":
        sub_f = df_filtered[df_filtered["HomeTeam"].isin(selected_teams)] if (selected_teams and len(selected_teams) > 0) else df_filtered
        tot_shots = sub_f["HS"].sum()
        tot_sot = sub_f["HST"].sum()
        tot_goals = sub_f["FTHG"].sum()
    elif venue_option == "Extérieur":
        sub_f = df_filtered[df_filtered["AwayTeam"].isin(selected_teams)] if (selected_teams and len(selected_teams) > 0) else df_filtered
        tot_shots = sub_f["AS"].sum()
        tot_sot = sub_f["AST"].sum()
        tot_goals = sub_f["FTAG"].sum()
    else:
        tot_shots = df_filtered["TotalShots"].sum()
        tot_sot = df_filtered["TotalShotsTarget"].sum()
        tot_goals = df_filtered["TotalGoals"].sum()

    funnel_label = (selected_teams[0] if len(selected_teams) == 1 else "Échantillon") + (f" - {venue_option}" if venue_option != "Tous" else "")
    fig_funnel = create_shot_funnel_chart(tot_shots, tot_sot, tot_goals, team_name=funnel_label, theme=theme)
    st.plotly_chart(fig_funnel, use_container_width=True)

# 8. Zone Détail : Classement et Benchmark des clubs
team_stats = compute_team_aggregates(df_filtered, target_teams=selected_teams, venue=venue_option)

st.subheader("Classement comparatif de l'efficacité offensive")
st.caption("Mesure de la capacité des clubs à convertir leurs situations chaudes en buts réels.")

metric_labels = {
    "Points / Tir Cadré": ("PointsParTirCadre", "Points / Tir Cadré"),
    "Conversion Buts (%)": ("ConversionButsPct", "Taux de Conversion (%)"),
    "Précision Cadrage (%)": ("PrecisionCadrePct", "Précision de Cadrage (%)"),
    "Buts / Match": ("ButsParMatch", "Buts / Match")
}

selected_metric_name = st.radio(
    "Métrique d'étalonnage :",
    options=list(metric_labels.keys()),
    horizontal=True
)
metric_col, metric_display = metric_labels[selected_metric_name]

# Sort by chosen metric for display
team_stats_sorted = team_stats.sort_values(by=metric_col, ascending=False).reset_index(drop=True)

col_chart, col_table = st.columns([1.2, 0.8])

with col_chart:
    fig_rank = create_efficiency_ranking_chart(
        team_stats_sorted,
        metric=metric_col,
        metric_label=metric_display,
        theme=theme
    )
    st.plotly_chart(fig_rank, use_container_width=True)

with col_table:
    st.markdown("**Top clubs de l'échantillon sélectionné**")
    display_cols = ["Rang", "Team", "Points", "PrecisionCadrePct", "ConversionButsPct", "PointsParTirCadre"]
    st.dataframe(
        team_stats_sorted[display_cols].rename(columns={
            "Team": "Club",
            "PrecisionCadrePct": "Précision (%)",
            "ConversionButsPct": "Conversion (%)",
            "PointsParTirCadre": "Pts / Tir cadré"
        }),
        use_container_width=True,
        height=400,
        hide_index=True
    )

st.divider()
st.caption("Projet Premier League Dashboard · Bachelor Data et IA · Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL")
