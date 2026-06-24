import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.styles import load_css, page_header, section_header, insight_box
from src.utils import load_data

# Config & CSS
st.set_page_config(
    page_title="MindTrack | Problème mondial",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)

# Chargement des données
df = load_data()

# Header de page
page_header(
    icon="fas fa-globe",
    tag="Étape 1",
    title="Le problème mondial",
    subtitle="Visualiser la répartition des troubles mentaux dans notre dataset"
)

# Métriques rapides
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

total       = len(df)
nb_pays     = df["Country"].nunique()
nb_depression = len(df[df["Mental Health Condition"] == "Depression"])
pct_depression = round(nb_depression / total * 100, 1)
conditions  = df["Mental Health Condition"].nunique()

metrics = [
    ("fas fa-users",         str(total),           "Individus analysés"),
    ("fas fa-earth-americas",str(nb_pays),          "Pays représentés"),
    ("fas fa-heart-crack",   str(nb_depression),    "Cas de dépression"),
    ("fas fa-percent",       f"{pct_depression}%",  "Taux de dépression"),
]

for col, (icon, value, label) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="content-card" style="text-align:center;">
            <i class="{icon}" style="color:#2DD4BF; font-size:1.3rem; margin-bottom:0.6rem; display:block;"></i>
            <div style="font-size:1.8rem; font-weight:800; color:#2DD4BF;">{value}</div>
            <div style="font-size:0.75rem; color:#64748B; text-transform:uppercase; 
                        letter-spacing:0.08em; margin-top:0.2rem;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 1 : Distribution des conditions
section_header(
    icon="fas fa-chart-pie",
    title="Distribution des conditions de santé mentale",
    subtitle="Répartition des 4 conditions dans le dataset"
)

col_left, col_right = st.columns([3, 2])

with col_left:
    # Comptage des conditions
    condition_counts = df["Mental Health Condition"].value_counts().reset_index()
    condition_counts.columns = ["Condition", "Nombre"]
    condition_counts["Pourcentage"] = (
        condition_counts["Nombre"] / total * 100
    ).round(1)

    # Couleurs par condition
    colors = {
        "Anxiety"   : "#2DD4BF",
        "PTSD"      : "#0EA5E9",
        "Depression": "#8B5CF6",
        "Bipolar"   : "#F59E0B"
    }
    condition_counts["Couleur"] = condition_counts["Condition"].map(colors)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=condition_counts["Condition"],
        y=condition_counts["Nombre"],
        marker_color=condition_counts["Couleur"],
        text=condition_counts["Pourcentage"].apply(lambda x: f"{x}%"),
        textposition="outside",
        textfont=dict(color="#94A3B8", size=12)
    ))

    fig.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(
            showgrid=False,
            color="#64748B",
            title=""
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            color="#64748B",
            title="Nombre d'individus"
        ),
        margin=dict(t=30, b=20, l=10, r=10),
        height=350,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with col_right:
    # Donut chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=condition_counts["Condition"],
        values=condition_counts["Nombre"],
        hole=0.6,
        marker_colors=list(colors.values()),
        textinfo="label+percent",
        textfont=dict(color="#F1F5F9", size=11),
        hovertemplate="<b>%{label}</b><br>%{value} individus<br>%{percent}<extra></extra>"
    )])

    fig_donut.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Inter"),
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
        annotations=[dict(
            text=f"<b>{total}</b><br>individus",
            x=0.5, y=0.5,
            font=dict(size=14, color="#F1F5F9"),
            showarrow=False
        )]
    )

    st.plotly_chart(fig_donut, use_container_width=True)

insight_box("""
    <strong>Anxiety</strong> est la condition la plus représentée avec 26.1% des cas, 
    suivie de près par <strong>PTSD</strong> (25.9%). La <strong>Depression</strong> 
    représente 24.1% de l'échantillon, soit environ 1 individu sur 4. 
    La distribution équilibrée entre conditions favorise une comparaison fiable entre groupes.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Section 2 : Répartition par pays
section_header(
    icon="fas fa-map-location-dot",
    title="Répartition par pays",
    subtitle="Distribution des conditions mentales selon les 7 pays du dataset"
)

# Filtre interactif
conditions_list = ["Toutes"] + sorted(df["Mental Health Condition"].unique().tolist())
selected_condition = st.selectbox(
    "Filtrer par condition",
    conditions_list,
    key="condition_filter"
)

if selected_condition != "Toutes":
    df_filtered = df[df["Mental Health Condition"] == selected_condition]
else:
    df_filtered = df

# Comptage par pays
country_counts = df_filtered.groupby(
    ["Country", "Mental Health Condition"]
).size().reset_index(name="Nombre")

fig_country = px.bar(
    country_counts,
    x="Country",
    y="Nombre",
    color="Mental Health Condition",
    color_discrete_map=colors,
    barmode="group",
    labels={"Country": "Pays", "Nombre": "Nombre d'individus",
            "Mental Health Condition": "Condition"}
)

fig_country.update_layout(
    plot_bgcolor="#1E293B",
    paper_bgcolor="#1E293B",
    font=dict(color="#94A3B8", family="Inter"),
    xaxis=dict(showgrid=False, color="#64748B"),
    yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
    legend=dict(
        bgcolor="#0F172A",
        bordercolor="#334155",
        borderwidth=1,
        font=dict(color="#94A3B8")
    ),
    margin=dict(t=20, b=20, l=10, r=10),
    height=400
)

st.plotly_chart(fig_country, use_container_width=True)

insight_box("""
    La répartition par pays révèle que le <strong>pays d'origine influence peu 
    la condition mentale observée</strong>, les écarts entre nations restent 
    minimes (62 à 105 cas par condition). Cette absence de signal géographique 
    fort soulève une question naturelle : <strong>les caractéristiques 
    démographiques comme le genre et l'âge sont-elles davantage discriminantes ?
    </strong> C'est ce que nous allons explorer dans la section suivante.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Section 3 : Répartition par genre et âge
section_header(
    icon="fas fa-users",
    title="Profil démographique",
    subtitle="Analyse des conditions mentales selon le genre et l'âge"
)

col_genre, col_age = st.columns(2)

with col_genre:
    st.markdown("""
    <div class="content-card-title">
        <i class="fas fa-venus-mars"></i> Par genre
    </div>
    """, unsafe_allow_html=True)

    gender_counts = df.groupby(
        ["Gender", "Mental Health Condition"]
    ).size().reset_index(name="Nombre")

    fig_gender = px.bar(
        gender_counts,
        x="Gender",
        y="Nombre",
        color="Mental Health Condition",
        color_discrete_map=colors,
        barmode="group",
        labels={"Gender": "Genre", "Nombre": "Nombre d'individus",
                "Mental Health Condition": "Condition"}
    )

    fig_gender.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B"),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
        legend=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            font=dict(color="#94A3B8")
        ),
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col_age:
    st.markdown("""
    <div class="content-card-title">
        <i class="fas fa-chart-area"></i> Distribution par âge
    </div>
    """, unsafe_allow_html=True)

    fig_age = px.violin(
        df,
        x="Mental Health Condition",
        y="Age",
        color="Mental Health Condition",
        color_discrete_map=colors,
        box=True,          # Affiche le boxplot à l'intérieur
        points=False,      # Pas de points individuels pour rester lisible
        labels={
            "Age": "Âge",
            "Mental Health Condition": "Condition"
        }
    )

    fig_age.update_layout(
        plot_bgcolor="#1E293B",
        paper_bgcolor="#1E293B",
        font=dict(color="#94A3B8", family="Inter"),
        xaxis=dict(showgrid=False, color="#64748B", title=""),
        yaxis=dict(showgrid=True, gridcolor="#334155", color="#64748B"),
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=350
    )
    st.plotly_chart(fig_age, use_container_width=True)

insight_box("""
    Ni le genre ni l'âge ne permettent de distinguer les conditions mentales, 
    les distributions sont quasi-identiques entre groupes, avec des médianes 
    d'âge toutes centrées autour de <strong>40 ans</strong> et des effectifs 
    par genre très proches. Ce double résultat est décisif pour notre 
    problématique : <strong>les variables démographiques classiques ne sont pas 
    des prédicteurs suffisants</strong> de la condition mentale. Cela justifie 
    l'exploration des <strong>habitudes de vie</strong> comme source principale 
    de signal prédictif ce que nous analysons dans l'étape suivante.
""")