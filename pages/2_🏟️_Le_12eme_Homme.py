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
    page_title="Le 12e Homme · Premier League",
    page_icon="🏟️",
    layout="wide"
)

theme = "dark" if st.session_state.get('dark_mode', False) else "light"
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

df_raw = load_pl_data()
comp_stats = compute_home_advantage_comparison(df_raw)

st.title("Le 12e Homme : L'avantage à domicile s'est effondré de 8 points pendant le huis clos COVID")
st.caption("Étude comparative sur 1 900 matchs démontrant l'impact statistique direct de la présence des supporters.")

st.markdown("""
<div class="minto-card">
    <strong>Preuve empirique (Minto) :</strong> En temps normal, jouer à domicile assure 46,2 % de victoires. Durant la saison 2020-21 disputée à huis clos, les victoires à domicile sont tombées à 37,9 % tandis que les victoires à l'extérieur sont devenues majoritaires (40,3 %), une anomalie unique dans l'histoire moderne du football anglais.
</div>
""", unsafe_allow_html=True)

# 3 KPIs d'impact
k1, k2, k3 = st.columns(3)
k1.metric(
    "Victoires domicile (Normales)",
    f"{comp_stats['normal']['home_win']:.1f} %",
    "4 saisons avec public"
)
k2.metric(
    "Victoires domicile (Huis clos COVID)",
    f"{comp_stats['covid']['home_win']:.1f} %",
    f"-{comp_stats['home_drop_pts']:.1f} pts de chute",
    delta_color="inverse"
)
k3.metric(
    "Surcroît victoires extérieur",
    f"{comp_stats['covid']['away_win']:.1f} %",
    f"+{comp_stats['away_boost_pts']:.1f} pts vs normal"
)

# 1. Évolution temporelle sur 5 saisons
seasons_df = compute_season_outcomes(df_raw)
fig_timeline = create_seasons_timeline_chart(seasons_df, theme=theme)
st.plotly_chart(fig_timeline, use_container_width=True)

# 2. Zone d'impact par club et synthèse
col_db, col_stack = st.columns([1.25, 0.75])

with col_db:
    sens_df = compute_club_crowd_sensitivity(df_raw)
    fig_db = create_club_home_impact_dumbbell(sens_df, theme=theme)
    st.plotly_chart(fig_db, use_container_width=True)

with col_stack:
    fig_home = create_home_advantage_comparison_chart(comp_stats, theme=theme)
    st.plotly_chart(fig_home, use_container_width=True)

st.subheader("Ce que révèle l'expérience naturelle du huis clos")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 📣 Pression psychologique et arbitrage")
    st.write("L'analyse des sanctions disciplinaires montre que l'écart de cartons jaunes entre visiteurs et receveurs s'est resserré de 38 % à huis clos. Sans les clameurs du stade, l'arbitrage est plus neutre et le visiteur subit moins d'inhibition.")

with c2:
    st.markdown("### ⚽ Différentiel de buts net")
    st.write(f"En présence du public, l'équipe à domicile bénéficie d'un différentiel moyen de **+{comp_stats['normal']['diff_goals']} but par match**. Durant le huis clos, ce surplus est tombé à **+{comp_stats['covid']['diff_goals']} but**, effaçant presque totalement la forteresse du domicile.")

st.divider()
st.caption("Premier League Decision Platform · HETIC MD4")
