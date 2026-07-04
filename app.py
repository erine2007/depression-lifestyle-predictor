from PIL import Image
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.styles import load_css

favicon = Image.open("assets/favicon.png")
st.set_page_config(
    page_title="MindTrack",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(load_css(), unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:0.6rem;color:#22372D;'
        'font-size:1.1rem;font-weight:700;padding:0.8rem 0 0.3rem 0;'
        'border-bottom:2px solid #4F7A67;margin-bottom:0.4rem;">'
        '<i class="fas fa-brain" style="color:#4F7A67;"></i> MindTrack</div>'
        '<div style="color:#66736A;font-size:0.76rem;margin-bottom:1.2rem;">'
        'Mental Health Analytics Platform</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="color:#66736A;font-size:0.76rem;margin-bottom:0.8rem;">'
        'Sélectionnez une étape ci-dessus</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.6rem;">Projet</div>'
        '<div style="color:#66736A;font-size:0.76rem;line-height:2;">'
        '<i class="fas fa-bullseye" style="color:#4F7A67;width:14px;"></i>&nbsp;Health Data Analytics<br>'
        '<i class="fas fa-database" style="color:#4F7A67;width:14px;"></i>&nbsp;2 400+ observations<br>'
        '<i class="fas fa-robot" style="color:#4F7A67;width:14px;"></i>&nbsp;Decision Tree Classifier<br>'
        '<i class="fab fa-python" style="color:#4F7A67;width:14px;"></i>&nbsp;Python · Streamlit · Plotly'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;font-size:0.74rem;color:#66736A;">'
        '<i class="fas fa-code" style="color:#4F7A67;"></i> Développé par<br>'
        '<span style="color:#22372D;font-weight:600;">Erine MASSO</span><br>'
        '<span style="color:#8C948E;">Data & AI Engineer</span></div>',
        unsafe_allow_html=True
    )

# HERO
col_hero, col_img = st.columns([3, 2])

with col_hero:
    st.markdown(
        '<div style="padding:2rem 1.5rem 2rem 0;">'
        '<div style="display:inline-flex;align-items:center;gap:0.5rem;'
        'background:#EEF2EC;color:#4F7A67;border:1.5px solid #7D9A7B;'
        'border-radius:20px;padding:0.3rem 1rem;font-size:0.76rem;'
        'font-weight:600;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:1.2rem;">'
        '<i class="fas fa-brain"></i> Mental Health Analytics Platform</div>'
        '<div style="font-size:2.3rem;font-weight:800;color:#22372D;line-height:1.25;margin-bottom:1rem;">'
        'Peut-on détecter une <span style="color:#C97B52;">dépression</span><br>'
        'grâce aux habitudes de vie ?</div>'
        '<div style="font-size:0.98rem;color:#66736A;line-height:1.7;max-width:480px;">'
        "Une plateforme d'analyse et de prédiction explorant les corrélations "
        "entre habitudes de vie quotidiennes et santé mentale, combinant "
        "data science et machine learning pour des insights actionnables."
        '</div></div>',
        unsafe_allow_html=True
    )

with col_img:
    st.image("assets/hero_illustration.webp", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# MÉTRIQUES
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("fas fa-users",       "2 405",  "Observations",        "#4F7A67"),
    ("fas fa-layer-group", "11",     "Variables analysées",  "#C97B52"),
    ("fas fa-robot",       "4",      "Modèles comparés",     "#4F7A67"),
    ("fas fa-chart-line",  "23.9%",  "Meilleure CV Accuracy","#C97B52"),
]
for col, (icon, value, label, accent) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
            f'border-top:4px solid {accent};border-radius:14px;'
            f'padding:1.6rem 1.2rem;text-align:center;'
            f'box-shadow:0 4px 16px rgba(34,55,45,0.1),0 1px 4px rgba(34,55,45,0.06);">'
            f'<div style="color:{accent};font-size:1.4rem;margin-bottom:0.7rem;"><i class="{icon}"></i></div>'
            f'<div style="font-size:2rem;font-weight:800;color:#22372D;margin-bottom:0.3rem;">{value}</div>'
            f'<div style="font-size:0.72rem;color:#8C948E;text-transform:uppercase;'
            f'letter-spacing:0.08em;font-weight:600;">{label}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# DÉMARCHE + À PROPOS
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown(
        '<h3 style="color:#22372D;font-size:1.2rem;font-weight:700;margin-bottom:1rem;">La démarche</h3>',
        unsafe_allow_html=True
    )
    steps = [
        ("fas fa-globe",      "Étape 1 — Le problème mondial",
         "Visualiser l'ampleur des troubles mentaux par pays et condition", "#4F7A67"),
        ("fas fa-search",     "Étape 2 — Les facteurs de risque",
         "Explorer l'impact du sommeil, stress, sport et temps d'écran", "#C97B52"),
        ("fas fa-chart-bar",  "Étape 3 — Exploration des données",
         "Analyse exploratoire interactive avec filtres dynamiques", "#4F7A67"),
        ("fas fa-robot",      "Étape 4 — Modèle Machine Learning",
         "Comparaison de 4 modèles de classification et interprétation", "#C97B52"),
        ("fas fa-crosshairs", "Étape 5 — Simulateur de risque",
         "Entrez vos habitudes et obtenez une estimation personnalisée", "#4F7A67"),
    ]
    for icon, title, desc, accent in steps:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
            f'border-left:4px solid {accent};border-radius:12px;'
            f'padding:1rem 1.3rem;margin-bottom:0.7rem;display:flex;align-items:flex-start;'
            f'gap:1rem;box-shadow:0 3px 10px rgba(34,55,45,0.08);">'
            f'<div style="width:40px;height:40px;border-radius:10px;background:#EEF2EC;'
            f'border:1.5px solid #D6DDD7;display:flex;align-items:center;justify-content:center;'
            f'flex-shrink:0;color:{accent};font-size:1rem;"><i class="{icon}"></i></div>'
            f'<div>'
            f'<div style="color:#22372D;font-size:0.92rem;font-weight:600;margin-bottom:0.2rem;">{title}</div>'
            f'<div style="color:#8C948E;font-size:0.82rem;">{desc}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

with col_right:
    st.markdown(
        '<h3 style="color:#22372D;font-size:1.2rem;font-weight:700;margin-bottom:1rem;">Stack technique</h3>',
        unsafe_allow_html=True
    )
    st.markdown(
        "![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) "
        "![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) "
        "![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) "
        "![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) "
        "![Scikit--learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) "
        "![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)"
    )
    st.markdown(
        '<h3 style="color:#22372D;font-size:1.2rem;font-weight:700;margin:1.5rem 0 1rem 0;">À propos du projet</h3>',
        unsafe_allow_html=True
    )

    about_items = [
        ("#EEF2EC", "#4F7A67", "fas fa-bullseye",
         "Objectif", "Prédiction du risque de dépression", "Classification multi-classes par ML"),
        ("#FDF5EF", "#C97B52", "fas fa-diagram-project",
         "Approche", "End-to-end Data Science", "EDA · ML · Application interactive"),
        ("#EEF2EC", "#4F7A67", "fas fa-user-tie",
         "Développée par", "Erine MASSO", "Data & AI Engineer"),
        ("#FDF5EF", "#C97B52", "fas fa-heart-pulse",
         "Domaine", "Health Data Analytics", "Mental Health & Lifestyle"),
    ]

    html = (
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;border-radius:16px;'
        'padding:1.3rem;box-shadow:0 4px 16px rgba(34,55,45,0.09);">'
    )
    for bg, color, icon, label, value, sub in about_items:
        html += (
            f'<div style="display:flex;align-items:center;gap:0.9rem;padding:0.85rem 1rem;'
            f'background:{bg};border-radius:10px;margin-bottom:0.6rem;'
            f'border:1.5px solid #D6DDD7;">'
            f'<div style="width:36px;height:36px;border-radius:9px;background:#FFFFFF;'
            f'color:{color};border:1.5px solid #D6DDD7;'
            f'display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0;">'
            f'<i class="{icon}"></i></div>'
            f'<div>'
            f'<div style="color:#8C948E;font-size:0.67rem;text-transform:uppercase;'
            f'letter-spacing:0.08em;font-weight:700;margin-bottom:0.15rem;">{label}</div>'
            f'<div style="color:#22372D;font-size:0.88rem;font-weight:600;">{value}</div>'
            f'<div style="color:{color};font-size:0.77rem;">{sub}</div>'
            f'</div></div>'
        )
    html += (
        '<div style="display:flex;align-items:center;gap:0.6rem;padding:0.65rem 1rem;'
        'background:#EEF2EC;border:1.5px solid #D6DDD7;border-radius:10px;">'
        '<div style="width:8px;height:8px;background:#4F7A67;border-radius:50%;flex-shrink:0;"></div>'
        '<div style="color:#4F7A67;font-size:0.78rem;font-weight:500;">'
        '<i class="fas fa-code-branch" style="margin-right:0.4rem;"></i>Version 1.0 — Juillet 2026</div>'
        '</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)

# NOTE
st.markdown("<br>", unsafe_allow_html=True)
col_note, _, _ = st.columns([2, 1, 1])
with col_note:
    st.markdown(
        '<div style="display:flex;align-items:flex-start;gap:0.8rem;'
        'color:#8C948E;font-size:0.82rem;line-height:1.6;'
        'border-top:1px solid #D6DDD7;padding-top:1rem;">'
        '<i class="fas fa-circle-info" style="color:#C97B52;margin-top:0.15rem;flex-shrink:0;"></i>'
        '<span>Les analyses présentées sont basées sur un dataset synthétique à des fins de démonstration. '
        'Les résultats ne constituent pas des conclusions cliniques et ne remplacent pas un avis médical professionnel.</span>'
        '</div>',
        unsafe_allow_html=True
    )
