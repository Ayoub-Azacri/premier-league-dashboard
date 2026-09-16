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
    st.caption("Tableau de bord tactique pour entraîneurs, analystes et passionnés")
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

# 5. Hero Banner Tactique (Public & Entraîneurs)
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Analyse Tactique · 1 900 matchs de Premier League (2019-2024)</div>
    <h1 class="hero-title">Cadrer et marquer : pourquoi la précision bat le volume brut en Premier League</h1>
    <p class="hero-subtitle">Tableau de bord tactique pour entraîneurs, analystes et passionnés de football : comprendre comment les meilleures équipes transforment leurs occasions en victoires.</p>
    <div class="hero-credits">
        <strong>Équipe :</strong> Ayoub AZACRI · Youssef EL HAJJI · Omar HAKIK · Youssef DEKHAIL
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Zone KPIs : Indicateurs clés contextualisés
kpi_data = compute_executive_kpis(df_filtered, venue=venue_option, teams=selected_teams)

# Repère historique 5 saisons pour les buts par match
BASELINE_GOALS_PER_MATCH = 2.82
goals_diff = round(kpi_data['goals_per_match'] - BASELINE_GOALS_PER_MATCH, 2)

c1, c2, c3 = st.columns(3)
c1.metric(
    "Précision des tirs (Cadrage)",
    f"{kpi_data['shot_accuracy']:.1f} %",
    f"{kpi_data['accuracy_diff']:+.1f} pts vs moyenne ligue (34,0 %)",
    delta_color="normal" if kpi_data['accuracy_diff'] >= 0 else "inverse"
)
c2.metric(
    "Efficacité devant le but (Finition)",
    f"{kpi_data['conversion_rate']:.1f} %",
    f"{kpi_data['conversion_diff']:+.1f} pts vs moyenne ligue (31,0 %)",
    delta_color="normal" if kpi_data['conversion_diff'] >= 0 else "inverse"
)
c3.metric(
    f"Moyenne de buts ({venue_option})",
    f"{kpi_data['goals_per_match']:.2f} / match",
    f"{goals_diff:+.2f} vs moyenne globale saison ({BASELINE_GOALS_PER_MATCH:.2f})",
    delta_color="normal" if goals_diff >= 0 else "inverse"
)

st.caption(
    f"📊 Volume analysé : {kpi_data['matches']:,} matchs · "
    f"{kpi_data['shots_per_match']:.1f} tirs tentés par match dont {kpi_data['sot_per_match']:.1f} cadrés · "
    f"{kpi_data['goals_per_sot']:.2f} but par frappe cadrée (1 tir cadré sur 3 converti)."
)

# 7. Parcours d'une frappe : du tir tenté au but marqué (Niveau visuel dédié)
st.markdown("---")
st.subheader("Parcours d'une frappe : du tir tenté au but marqué")
st.caption("Visualisation de la déperdition des frappes : 65 % des tirs ne sont pas cadrés. Prioriser la qualité du tir plutôt que l'accumulation de frappes lointaines.")

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

funnel_label = (selected_teams[0] if len(selected_teams) == 1 else "Ensemble des clubs") + (f" - {venue_option}" if venue_option != "Tous" else "")
fig_funnel = create_shot_funnel_chart(tot_shots, tot_sot, tot_goals, team_name=funnel_label, theme=theme)
st.plotly_chart(fig_funnel, use_container_width=True)

# 8. Classement tactique et efficacité des clubs (Niveau visuel dédié)
st.markdown("---")
st.subheader("Classement tactique et efficacité des clubs")
st.caption("Comparaison de la capacité des clubs à convertir leurs situations chaudes en buts réels.")

team_stats = compute_team_aggregates(df_filtered, target_teams=selected_teams, venue=venue_option)

metric_labels = {
    "Points / Tir Cadré": ("PointsParTirCadre", "Points récoltés par tir cadré"),
    "Conversion Buts (%)": ("ConversionButsPct", "Taux de conversion des tirs cadrés (%)"),
    "Précision Cadrage (%)": ("PrecisionCadrePct", "Précision de cadrage (%)"),
    "Buts / Match": ("ButsParMatch", "Moyenne de buts par match")
}

selected_metric_name = st.radio(
    "Métrique d'évaluation :",
    options=list(metric_labels.keys()),
    horizontal=True
)
metric_col, metric_display = metric_labels[selected_metric_name]

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
    st.markdown("**Tableau comparatif des clubs**")
    display_cols = ["Rang", "Team", "Points", "PrecisionCadrePct", "ConversionButsPct", "PointsParTirCadre"]
    st.dataframe(
        team_stats_sorted[display_cols].rename(columns={
            "Team": "Club",
            "PrecisionCadrePct": "Précision (%)",
            "ConversionButsPct": "Conversion (%)",
            "PointsParTirCadre": "Pts / Tir cadré"
        }),
        use_container_width=True,
        height=420,
        hide_index=True
    )

st.divider()
st.caption("Premier League Dashboard · Bachelor Data et IA · Ayoub AZACRI, Youssef EL HAJJI, Omar HAKIK, Youssef DEKHAIL")
