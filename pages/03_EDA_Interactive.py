import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.styles import load_css, page_header, section_header, insight_box
from src.utils import load_data

favicon = Image.open("assets/favicon.png")
st.set_page_config(
    page_title="MindTrack | EDA Interactive",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)

df = load_data()

colors = {
    "Anxiety"   : "#4F7A67",
    "PTSD"      : "#7D9A7B",
    "Depression": "#C97B52",
    "Bipolar"   : "#22372D"
}

# Header
page_header(
    icon="fas fa-chart-bar",
    tag="Étape 3",
    title="Exploration interactive des données",
    subtitle="Analysez et filtrez les données pour découvrir des patterns"
)

# ══════════════════════════════════════════
# FILTRES GLOBAUX
# ══════════════════════════════════════════
st.markdown(
    '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;border-radius:12px;'
    'padding:1.2rem 1.5rem;margin-bottom:1.5rem;'
    'box-shadow:0 3px 10px rgba(34,55,45,0.08);">'
    '<div style="color:#22372D;font-size:0.85rem;font-weight:600;margin-bottom:0.8rem;">'
    '<i class="fas fa-sliders" style="color:#4F7A67;margin-right:0.5rem;"></i>'
    'Filtres globaux : appliqués à toutes les visualisations</div>'
    '</div>',
    unsafe_allow_html=True
)

col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    conditions = ["Toutes"] + sorted(df["Mental Health Condition"].unique().tolist())
    selected_condition = st.selectbox("Condition", conditions)

with col_f2:
    pays = ["Tous"] + sorted(df["Country"].unique().tolist())
    selected_pays = st.selectbox("Pays", pays)

with col_f3:
    genres = ["Tous"] + sorted(df["Gender"].unique().tolist())
    selected_genre = st.selectbox("Genre", genres)

with col_f4:
    age_range = st.slider(
        "Tranche d'âge",
        min_value=int(df["Age"].min()),
        max_value=int(df["Age"].max()),
        value=(int(df["Age"].min()), int(df["Age"].max()))
    )

# Application des filtres
df_f = df.copy()
if selected_condition != "Toutes":
    df_f = df_f[df_f["Mental Health Condition"] == selected_condition]
if selected_pays != "Tous":
    df_f = df_f[df_f["Country"] == selected_pays]
if selected_genre != "Tous":
    df_f = df_f[df_f["Gender"] == selected_genre]
df_f = df_f[(df_f["Age"] >= age_range[0]) & (df_f["Age"] <= age_range[1])]

# Résumé filtres
total_f = len(df_f)
pct = round(total_f / len(df) * 100, 1)
st.markdown(
    f'<div style="color:#66736A;font-size:0.8rem;margin-bottom:1.5rem;">'
    f'<i class="fas fa-filter" style="color:#4F7A67;margin-right:0.4rem;"></i>'
    f'<strong style="color:#22372D;">{total_f}</strong> individus sélectionnés '
    f'({pct}% du dataset total)</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 1 — HEATMAP CORRÉLATIONS
# ══════════════════════════════════════════
section_header(
    icon="fas fa-table-cells",
    title="Heatmap des corrélations",
    subtitle="Relations entre variables numériques sur la sélection filtrée"
)

numerical_cols = [
    "Age", "Sleep Hours", "Work Hours per Week",
    "Screen Time per Day (Hours)", "Social Interaction Score", "Happiness Score"
]

col_heat, col_heat_info = st.columns([3, 1])

with col_heat:
    corr = df_f[numerical_cols].corr()

    fig_heat = go.Figure(data=go.Heatmap(
        z=corr.values.round(2),
        x=[c.replace(" per Day (Hours)", "").replace(" per Week", "")
           .replace(" Hours", " Hrs") for c in numerical_cols],
        y=[c.replace(" per Day (Hours)", "").replace(" per Week", "")
           .replace(" Hours", " Hrs") for c in numerical_cols],
        colorscale=[
            [0.0, "#C97B52"],
            [0.5, "#F6F5F1"],
            [1.0, "#22372D"]
        ],
        zmid=0,
        text=corr.values.round(2),
        texttemplate="%{text}",
        textfont=dict(size=11, color="#22372D"),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(
            thickness=12,
            tickcolor="#66736A",
            tickfont=dict(color="#66736A", size=10),
            outlinewidth=0
        )
    ))

    fig_heat.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=380,
        xaxis=dict(tickfont=dict(size=10, color="#66736A"), side="bottom"),
        yaxis=dict(tickfont=dict(size=10, color="#66736A"), autorange="reversed")
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col_heat_info:
    st.markdown("<br>", unsafe_allow_html=True)

    # Top corrélations positives et négatives
    corr_pairs = []
    for i in range(len(numerical_cols)):
        for j in range(i+1, len(numerical_cols)):
            corr_pairs.append({
                "var1": numerical_cols[i],
                "var2": numerical_cols[j],
                "corr": corr.iloc[i, j]
            })
    corr_df = pd.DataFrame(corr_pairs).sort_values("corr", ascending=False)

    top_pos = corr_df.head(3)
    top_neg = corr_df.tail(3)

    st.markdown(
        '<div style="background:#F9F7F3;border:1.5px solid #D6DDD7;'
        'border-radius:10px;padding:1rem;">'
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.7rem;">'
        '<i class="fas fa-arrow-trend-up" style="color:#4F7A67;margin-right:0.4rem;"></i>'
        'Corrélations positives</div>',
        unsafe_allow_html=True
    )
    for _, row in top_pos.iterrows():
        v1 = row["var1"].split(" ")[0]
        v2 = row["var2"].split(" ")[0]
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;'
            f'padding:0.3rem 0;border-bottom:1px solid #EEF2EC;font-size:0.78rem;">'
            f'<span style="color:#66736A;">{v1} × {v2}</span>'
            f'<span style="color:#4F7A67;font-weight:600;">{row["corr"]:.3f}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div style="background:#F9F7F3;border:1.5px solid #D6DDD7;'
        'border-radius:10px;padding:1rem;">'
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.7rem;">'
        '<i class="fas fa-arrow-trend-down" style="color:#C97B52;margin-right:0.4rem;"></i>'
        'Corrélations négatives</div>',
        unsafe_allow_html=True
    )
    for _, row in top_neg.iterrows():
        v1 = row["var1"].split(" ")[0]
        v2 = row["var2"].split(" ")[0]
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;'
            f'padding:0.3rem 0;border-bottom:1px solid #EEF2EC;font-size:0.78rem;">'
            f'<span style="color:#66736A;">{v1} × {v2}</span>'
            f'<span style="color:#C97B52;font-weight:600;">{row["corr"]:.3f}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

insight_box(
    "La heatmap révèle des corrélations très faibles entre toutes les variables numériques "
    ",les valeurs restent proches de <strong>0</strong> quelle que soit la sélection. "
    "Cela confirme que les variables numériques sont <strong>indépendantes entre elles</strong>, "
    "et que le pouvoir prédictif du modèle reposera principalement sur les "
    "<strong>variables catégorielles</strong> (stress, exercice, alimentation)."
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 2 — DISTRIBUTIONS
# ══════════════════════════════════════════
section_header(
    icon="fas fa-chart-area",
    title="Distributions des variables",
    subtitle="Sélectionnez une variable pour explorer sa distribution"
)

col_var, col_type = st.columns([2, 1])

with col_var:
    selected_var = st.selectbox(
        "Variable à analyser",
        numerical_cols,
        index=1
    )

with col_type:
    chart_type = st.selectbox(
        "Type de graphique",
        ["Histogramme", "Violin plot", "Box plot"]
    )

col_dist_left, col_dist_right = st.columns([3, 2])

with col_dist_left:
    if chart_type == "Histogramme":
        fig_dist = px.histogram(
            df_f,
            x=selected_var,
            color="Mental Health Condition",
            color_discrete_map=colors,
            nbins=25,
            barmode="overlay",
            opacity=0.7,
            labels={selected_var: selected_var, "count": "Fréquence",
                    "Mental Health Condition": "Condition"}
        )
    elif chart_type == "Violin plot":
        fig_dist = px.violin(
            df_f,
            x="Mental Health Condition",
            y=selected_var,
            color="Mental Health Condition",
            color_discrete_map=colors,
            box=True,
            points=False,
            labels={"Mental Health Condition": "Condition", selected_var: selected_var}
        )
    else:
        fig_dist = px.box(
            df_f,
            x="Mental Health Condition",
            y=selected_var,
            color="Mental Health Condition",
            color_discrete_map=colors,
            labels={"Mental Health Condition": "Condition", selected_var: selected_var}
        )

    fig_dist.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        xaxis=dict(showgrid=False, color="#66736A"),
        yaxis=dict(showgrid=True, gridcolor="#EEF2EC", color="#66736A"),
        legend=dict(
            bgcolor="#F9F7F3",
            bordercolor="#D6DDD7",
            borderwidth=1,
            font=dict(color="#66736A", size=11)
        ),
        margin=dict(t=20, b=20, l=10, r=10),
        height=380
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col_dist_right:
    st.markdown("<br>", unsafe_allow_html=True)

    # Statistiques descriptives par condition
    stats = df_f.groupby("Mental Health Condition")[selected_var].agg(
        ["mean", "median", "std", "min", "max"]
    ).round(2)

    for condition, row in stats.iterrows():
        color_cond = colors.get(condition, "#4F7A67")
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
            f'border-left:4px solid {color_cond};border-radius:10px;'
            f'padding:0.8rem 1rem;margin-bottom:0.6rem;'
            f'box-shadow:0 2px 8px rgba(34,55,45,0.06);">'
            f'<div style="color:#22372D;font-size:0.82rem;font-weight:600;'
            f'margin-bottom:0.4rem;">{condition}</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.2rem;">'
            f'<div style="color:#8C948E;font-size:0.72rem;">Moyenne</div>'
            f'<div style="color:#22372D;font-size:0.72rem;font-weight:500;">{row["mean"]}</div>'
            f'<div style="color:#8C948E;font-size:0.72rem;">Médiane</div>'
            f'<div style="color:#22372D;font-size:0.72rem;font-weight:500;">{row["median"]}</div>'
            f'<div style="color:#8C948E;font-size:0.72rem;">Écart-type</div>'
            f'<div style="color:#22372D;font-size:0.72rem;font-weight:500;">{row["std"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 3 — SCATTER PLOT
# ══════════════════════════════════════════
section_header(
    icon="fas fa-circle-dot",
    title="Analyse bivariée",
    subtitle="Explorez la relation entre deux variables numériques"
)

col_x, col_y, col_size = st.columns(3)

with col_x:
    var_x = st.selectbox("Variable X", numerical_cols, index=1)
with col_y:
    var_y = st.selectbox("Variable Y", numerical_cols, index=5)
with col_size:
    var_size_opt = ["Aucune"] + numerical_cols
    var_size = st.selectbox("Taille des points", var_size_opt, index=0)

fig_scatter = px.scatter(
    df_f,
    x=var_x,
    y=var_y,
    color="Mental Health Condition",
    color_discrete_map=colors,
    size=var_size if var_size != "Aucune" else None,
    opacity=0.55,
    hover_data=["Country", "Gender", "Age"],
    labels={
        var_x: var_x,
        var_y: var_y,
        "Mental Health Condition": "Condition"
    }
)

fig_scatter.update_traces(marker=dict(line=dict(width=0.3, color="#FFFFFF")))
fig_scatter.update_layout(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(color="#66736A", family="Inter"),
    xaxis=dict(showgrid=True, gridcolor="#EEF2EC", color="#66736A", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#EEF2EC", color="#66736A", zeroline=False),
    legend=dict(
        bgcolor="#F9F7F3",
        bordercolor="#D6DDD7",
        borderwidth=1,
        font=dict(color="#66736A", size=11)
    ),
    margin=dict(t=20, b=20, l=10, r=10),
    height=420
)
st.plotly_chart(fig_scatter, use_container_width=True)

insight_box(
    "Le scatter plot confirme l'absence de clusters distincts entre les 4 conditions, "
    "les points de chaque couleur se mélangent uniformément dans tout l'espace de représentation. "
    "Cette absence de séparation linéaire explique pourquoi nos modèles ML "
    "peinent à dépasser <strong>25% de précision</strong> en classification multi-classes : "
    "il n'existe pas de frontière décision claire entre les groupes dans cet espace de features."
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 4 — ANALYSE CATÉGORIELLE
# ══════════════════════════════════════════
section_header(
    icon="fas fa-tags",
    title="Variables catégorielles",
    subtitle="Distribution des variables catégorielles par condition mentale"
)

col_cat1, col_cat2 = st.columns(2)

with col_cat1:
    cat_var = st.selectbox(
        "Variable catégorielle",
        ["Stress Level", "Exercise Level", "Diet Type", "Country", "Gender"],
        index=0
    )

    cat_cross = pd.crosstab(
        df_f["Mental Health Condition"],
        df_f[cat_var],
        normalize="index"
    ) * 100

    cat_melted = cat_cross.reset_index().melt(
        id_vars="Mental Health Condition",
        var_name=cat_var,
        value_name="Pourcentage"
    )

    fig_cat = px.bar(
        cat_melted,
        x="Mental Health Condition",
        y="Pourcentage",
        color=cat_var,
        barmode="group",
        labels={
            "Mental Health Condition": "Condition",
            "Pourcentage": "Pourcentage (%)",
        },
        color_discrete_sequence=["#4F7A67", "#7D9A7B", "#C97B52", "#22372D", "#D6DDD7"]
    )
    fig_cat.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        xaxis=dict(showgrid=False, color="#66736A"),
        yaxis=dict(
            showgrid=True, gridcolor="#EEF2EC",
            color="#66736A", ticksuffix="%"
        ),
        legend=dict(
            bgcolor="#F9F7F3", bordercolor="#D6DDD7",
            borderwidth=1, font=dict(color="#66736A", size=11)
        ),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_cat2:
    # Tableau récapitulatif
    cat_abs = pd.crosstab(
        df_f["Mental Health Condition"],
        df_f[cat_var]
    )
    st.markdown(
        '<div style="color:#22372D;font-size:0.82rem;font-weight:600;margin-bottom:0.8rem;">'
        f'<i class="fas fa-table" style="color:#4F7A67;margin-right:0.4rem;"></i>'
        f'Tableau croisé — {cat_var}</div>',
        unsafe_allow_html=True
    )
    st.dataframe(
        cat_abs.style.background_gradient(
            cmap="Greens", axis=None
        ).format("{:.0f}"),
        use_container_width=True,
        height=300
    )

insight_box(
    f"L'analyse de <strong>{cat_var}</strong> révèle des répartitions proches entre conditions. "
    "Les écarts les plus notables concernent <strong>Exercise Level</strong> où la Depression "
    "présente le taux d'exercice élevé le plus bas (~30.5%) signal le plus discriminant "
    "identifié dans l'ensemble du dataset. Utilisez les filtres en haut de page pour "
    "explorer ces nuances sur des sous-groupes spécifiques."
)
