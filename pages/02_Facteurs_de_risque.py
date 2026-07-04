import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.styles import load_css, page_header, section_header, insight_box
from src.utils import load_data

# ── Config & CSS
st.set_page_config(
    page_title="MindTrack | Facteurs de risque",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)

# ── Chargement des données
df = load_data()

# Palette couleurs conditions
colors = {
    "Anxiety"   : "#2DD4BF",
    "PTSD"      : "#0EA5E9",
    "Depression": "#8B5CF6",
    "Bipolar"   : "#F59E0B"
}

# ── Header
page_header(
    icon="fas fa-magnifying-glass-chart",
    tag="Étape 2",
    title="Les facteurs de risque",
    subtitle="Explorer l'impact des habitudes de vie sur la santé mentale"
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 1 : Sommeil
section_header(
    icon="fas fa-moon",
    title="Sommeil",
    subtitle="Impact des heures de sommeil sur la condition mentale"
)

col_left, col_right = st.columns([3, 2])

with col_left:
    fig_sleep = go.Figure()
    for condition, color in colors.items():
        data = df[df["Mental Health Condition"] == condition]["Sleep Hours"]
        fig_sleep.add_trace(go.Box(
            y=data,
            name=condition,
            marker_color=color,
            boxmean=True,
            line_width=1.5
        ))

    fig_sleep.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B"),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Heures de sommeil"
        ),
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

with col_right:
    sleep_means = df.groupby(
        "Mental Health Condition"
    )["Sleep Hours"].mean().sort_values()

    fig_sleep_bar = go.Figure(go.Bar(
        x=sleep_means.values.round(2),
        y=sleep_means.index,
        orientation="h",
        marker_color=[colors[c] for c in sleep_means.index],
        text=[f"{v:.2f}h" for v in sleep_means.values],
        textposition="outside",
        textfont=dict(color="#94A3B8")
    ))

    fig_sleep_bar.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Moyenne heures de sommeil",
            range=[0, 10]
        ),
        yaxis=dict(showgrid=False, color="#64748B"),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_sleep_bar, use_container_width=True)

insight_box("""
    Les moyennes de sommeil sont très proches entre conditions
    (entre <strong>6.45h et 6.48h</strong>). Les boxplots montrent des
    dispersions similaires pour toutes les conditions — le sommeil seul
    ne permet pas de discriminer les groupes. Cependant, les individus
    dormant <strong>moins de 5h ou plus de 9h</strong> présentent une
    distribution plus marquée vers Depression et PTSD, suggérant que
    ce sont les <strong>extrêmes de sommeil</strong> qui constituent
    un signal, plus que la moyenne.
""")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 2 : Stress
section_header(
    icon="fas fa-brain",
    title="Niveau de stress",
    subtitle="Répartition du stress selon la condition mentale"
)

stress_cross = pd.crosstab(
    df["Mental Health Condition"],
    df["Stress Level"],
    normalize="index"
) * 100

stress_order  = ["Low", "Moderate", "High"]
stress_cross  = stress_cross[
    [c for c in stress_order if c in stress_cross.columns]
]
stress_colors = {
    "Low"     : "#2DD4BF",
    "Moderate": "#F59E0B",
    "High"    : "#EF4444"
}

col_stress_left, col_stress_right = st.columns([3, 2])

with col_stress_left:
    fig_stress = go.Figure()
    for level in stress_order:
        if level in stress_cross.columns:
            fig_stress.add_trace(go.Bar(
                name=level,
                x=stress_cross.index,
                y=stress_cross[level].round(1),
                marker_color=stress_colors[level],
                text=[f"{v:.1f}%" for v in stress_cross[level].values],
                textposition="inside",
                textfont=dict(color="white", size=10)
            ))

    fig_stress.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        barmode="stack",
        xaxis=dict(showgrid=False, color="#64748B"),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Pourcentage (%)",
            ticksuffix="%"
        ),
        legend=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            borderwidth=1,
            font=dict(color="#94A3B8"),
            title=dict(text="Niveau de stress", font=dict(color="#64748B"))
        ),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_stress, use_container_width=True)

with col_stress_right:
    fig_heatmap = px.imshow(
        stress_cross.round(1),
        color_continuous_scale="Teal",
        text_auto=True,
        labels=dict(x="Niveau de stress", y="Condition", color="%")
    )

    fig_heatmap.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

insight_box("""
    La <strong>Depression</strong> présente la plus forte proportion de stress
    élevé (~35%) et la plus faible proportion de stress modéré (~30%) parmi
    les 4 conditions. À l'inverse, <strong>Bipolar</strong> montre la répartition
    la plus équilibrée entre les trois niveaux. Ces écarts, bien que modestes,
    indiquent que le niveau de stress est <strong>légèrement plus discriminant
    pour la dépression</strong> que pour les autres conditions — ce qui en fait
    une variable à inclure dans le modèle prédictif.
""")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 3 : Activité physique
section_header(
    icon="fas fa-person-running",
    title="Activité physique",
    subtitle="Lien entre niveau d'exercice et condition mentale"
)

exercise_cross = pd.crosstab(
    df["Mental Health Condition"],
    df["Exercise Level"],
    normalize="index"
) * 100

exercise_order  = ["Low", "Moderate", "High"]
exercise_cross  = exercise_cross[
    [c for c in exercise_order if c in exercise_cross.columns]
]
exercise_colors = {
    "Low"     : "#EF4444",
    "Moderate": "#F59E0B",
    "High"    : "#2DD4BF"
}

col_ex_left, col_ex_right = st.columns([3, 2])

with col_ex_left:
    fig_exercise = go.Figure()
    for level in exercise_order:
        if level in exercise_cross.columns:
            fig_exercise.add_trace(go.Bar(
                name=level,
                x=exercise_cross.index,
                y=exercise_cross[level].round(1),
                marker_color=exercise_colors[level],
                text=[f"{v:.1f}%" for v in exercise_cross[level].values],
                textposition="inside",
                textfont=dict(color="white", size=10)
            ))

    fig_exercise.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        barmode="stack",
        xaxis=dict(showgrid=False, color="#64748B"),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Pourcentage (%)",
            ticksuffix="%"
        ),
        legend=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            borderwidth=1,
            font=dict(color="#94A3B8"),
            title=dict(text="Niveau d'exercice", font=dict(color="#64748B"))
        ),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_exercise, use_container_width=True)

with col_ex_right:
    high_exercise = exercise_cross["High"].sort_values()

    fig_high = go.Figure(go.Bar(
        x=high_exercise.values.round(1),
        y=high_exercise.index,
        orientation="h",
        marker_color=[colors[c] for c in high_exercise.index],
        text=[f"{v:.1f}%" for v in high_exercise.values],
        textposition="outside",
        textfont=dict(color="#94A3B8")
    ))

    fig_high.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        title=dict(
            text="% d'exercice élevé par condition",
            font=dict(color="#64748B", size=12)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            ticksuffix="%"
        ),
        yaxis=dict(showgrid=False, color="#64748B"),
        margin=dict(t=40, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_high, use_container_width=True)

insight_box("""
    La <strong>Depression</strong> présente le taux d'exercice élevé le plus bas
    (~30.5%) et le taux d'exercice faible le plus élevé (~35%) parmi les 4 conditions.
    C'est le signal le plus marqué observé dans toute cette analyse des facteurs —
    une tendance cohérente avec la littérature clinique qui établit un lien direct
    entre <strong>sédentarité et risque dépressif</strong>. L'activité physique
    est donc la variable catégorielle la plus prometteuse pour notre modèle prédictif.
""")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 4 : Temps d'écran
section_header(
    icon="fas fa-display",
    title="Temps d'écran",
    subtitle="Impact du temps passé sur les écrans sur la santé mentale"
)

col_screen_left, col_screen_right = st.columns(2)

with col_screen_left:
    fig_screen = px.violin(
        df,
        x="Mental Health Condition",
        y="Screen Time per Day (Hours)",
        color="Mental Health Condition",
        color_discrete_map=colors,
        box=True,
        points=False,
        labels={
            "Screen Time per Day (Hours)": "Heures d'écran par jour",
            "Mental Health Condition"    : "Condition"
        }
    )

    fig_screen.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B", title=""),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_screen, use_container_width=True)

with col_screen_right:
    screen_means = df.groupby(
        "Mental Health Condition"
    )["Screen Time per Day (Hours)"].mean().sort_values()

    fig_screen_bar = go.Figure(go.Bar(
        x=screen_means.values.round(2),
        y=screen_means.index,
        orientation="h",
        marker_color=[colors[c] for c in screen_means.index],
        text=[f"{v:.2f}h" for v in screen_means.values],
        textposition="outside",
        textfont=dict(color="#94A3B8")
    ))

    fig_screen_bar.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        title=dict(
            text="Moyenne heures d'écran par condition",
            font=dict(color="#64748B", size=12)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Heures/jour"
        ),
        yaxis=dict(showgrid=False, color="#64748B"),
        margin=dict(t=40, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_screen_bar, use_container_width=True)

insight_box("""
    Les distributions de temps d'écran sont quasi-identiques entre les 4 conditions
    (médiane autour de <strong>5h/jour</strong>). Les moyennes par condition
    confirment l'absence de signal discriminant — les écarts sont inférieurs
    à 10 minutes entre groupes. Contrairement aux idées reçues,
    <strong>le temps d'écran seul n'est pas un prédicteur fiable</strong>
    de la condition mentale dans cet échantillon, ce qui suggère que c'est
    davantage le <strong>type d'usage des écrans</strong>
    (réseaux sociaux vs lecture vs travail) qui importe, plutôt que la durée brute.
""")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 5 : Score social & bonheur
section_header(
    icon="fas fa-heart",
    title="Interaction sociale & bonheur",
    subtitle="Impact des scores sociaux sur la condition mentale"
)

col_soc_left, col_soc_right = st.columns(2)

with col_soc_left:
    fig_social = px.violin(
        df,
        x="Mental Health Condition",
        y="Social Interaction Score",
        color="Mental Health Condition",
        color_discrete_map=colors,
        box=True,
        points=False,
        labels={
            "Social Interaction Score": "Score d'interaction sociale",
            "Mental Health Condition" : "Condition"
        }
    )

    fig_social.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B", title=""),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_social, use_container_width=True)

with col_soc_right:
    fig_happy = px.violin(
        df,
        x="Mental Health Condition",
        y="Happiness Score",
        color="Mental Health Condition",
        color_discrete_map=colors,
        box=True,
        points=False,
        labels={
            "Happiness Score"        : "Score de bonheur",
            "Mental Health Condition": "Condition"
        }
    )

    fig_happy.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B", title=""),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_happy, use_container_width=True)

insight_box("""
    Les scores d'interaction sociale et de bonheur présentent des distributions
    similaires entre conditions, avec des médianes proches de <strong>5.5/10</strong>
    pour les deux métriques. Toutefois, la <strong>Depression</strong> montre
    une légère concentration vers les scores de bonheur bas (1-3) plus marquée
    que les autres conditions — un signal faible mais cohérent avec l'intuition
    clinique. Ces deux variables seront incluses dans le modèle comme
    <strong>features secondaires</strong>, en complément des variables
    comportementales plus discriminantes.
""")