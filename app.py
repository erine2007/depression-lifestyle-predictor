import streamlit as st

#  Configuration générale
st.set_page_config(
    page_title="MindTrack",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  CSS custom global
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid #2DD4BF22;
    }

    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] span {
        color: #F1F5F9 !important;
    }

    .sidebar-title {
        color: #2DD4BF;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 1px solid #2DD4BF44;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 8px;
        padding: 0.6rem 1rem !important;
        margin-bottom: 0.3rem;
        border: 1px solid transparent;
        transition: all 0.2s;
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: #2DD4BF11 !important;
        border-color: #2DD4BF44 !important;
        color: #2DD4BF !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #2DD4BF22 !important;
        border-color: #2DD4BF !important;
        color: #2DD4BF !important;
        font-weight: 600 !important;
    }

    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 50%, #0F2D40 100%);
        border: 1px solid #2DD4BF33;
        border-radius: 16px;
        padding: 3rem 3.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.7s ease both;
    }

    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, #2DD4BF11 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #2DD4BF22;
        color: #2DD4BF;
        border: 1px solid #2DD4BF44;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #F1F5F9;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    .hero-title span {
        background: linear-gradient(90deg, #2DD4BF, #0EA5E9, #2DD4BF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        line-height: 1.7;
        max-width: 600px;
    }

    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #2DD4BF;
        border-radius: 12px;
        padding: 1.4rem 1.5rem;
        text-align: center;
        animation: fadeInUp 0.5s ease both;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px #2DD4BF22;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #2DD4BF;
        margin-bottom: 0.2rem;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 500;
    }

    .step-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        animation: fadeInUp 0.5s ease both;
        transition: all 0.25s ease;
    }

    .step-card:hover {
        transform: translateX(6px);
        border-color: #2DD4BF66;
        box-shadow: -3px 0 0 0 #2DD4BF, 0 4px 20px #2DD4BF11;
    }

    .step-card:nth-child(1) { animation-delay: 0.1s; }
    .step-card:nth-child(2) { animation-delay: 0.2s; }
    .step-card:nth-child(3) { animation-delay: 0.3s; }
    .step-card:nth-child(4) { animation-delay: 0.4s; }
    .step-card:nth-child(5) { animation-delay: 0.5s; }

    .step-icon-box {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: #2DD4BF15;
        border: 1px solid #2DD4BF33;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: #2DD4BF;
        font-size: 1rem;
    }

    .step-content h4 {
        color: #F1F5F9;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 0.2rem 0;
    }

    .step-content p {
        color: #64748B;
        font-size: 0.85rem;
        margin: 0;
    }

    .disclaimer {
        background: #1E293B;
        border: 1px solid #F59E0B44;
        border-left: 4px solid #F59E0B;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: #94A3B8;
        font-size: 0.9rem;
        animation: fadeIn 1s ease 0.8s both;
    }

    .about-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .about-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.9rem 1rem;
        background: #0F172A;
        border-radius: 10px;
        margin-bottom: 0.7rem;
        border: 1px solid #1E293B;
        transition: border-color 0.2s;
    }

    .about-item:hover {
        border-color: #2DD4BF33;
    }

    .about-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
    }

    .about-label {
        color: #64748B;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .about-value {
        color: #F1F5F9;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .about-sub {
        color: #2DD4BF;
        font-size: 0.8rem;
    }

    .about-status {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.7rem 1rem;
        background: #2DD4BF11;
        border: 1px solid #2DD4BF33;
        border-radius: 10px;
    }

    .about-dot {
        width: 8px;
        height: 8px;
        background: #2DD4BF;
        border-radius: 50%;
        flex-shrink: 0;
        animation: pulse 2s infinite;
    }

    .about-status-text {
        color: #2DD4BF;
        font-size: 0.8rem;
        font-weight: 500;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 #2DD4BF22; }
        50%       { box-shadow: 0 0 0 8px #2DD4BF00; }
    }

    #MainMenu {visibility: hidden;}
    footer    {visibility: hidden;}
    header [data-testid="stToolbar"]    {visibility: hidden;}
    header [data-testid="stDecoration"] {visibility: hidden;}

    [data-testid="collapsedControl"] {
        visibility: visible !important;
        background: #2DD4BF !important;
        border-radius: 0 8px 8px 0 !important;
    }

    ::-webkit-scrollbar       { width: 6px; }
    ::-webkit-scrollbar-track { background: #0F172A; }
    ::-webkit-scrollbar-thumb { background: #2DD4BF44; border-radius: 3px; }

    @media (max-width: 1024px) {
        .hero-title     { font-size: 2rem; }
        .hero-container { padding: 2rem; }
        .metric-value   { font-size: 1.5rem; }
    }

    @media (max-width: 768px) {
        .hero-title      { font-size: 1.5rem; }
        .hero-subtitle   { font-size: 0.95rem; }
        .hero-container  { padding: 1.5rem; }
        .metric-card     { padding: 1rem; }
        .metric-value    { font-size: 1.3rem; }
        .metric-label    { font-size: 0.7rem; }
        .step-card       { padding: 1rem; }
        .step-content h4 { font-size: 0.85rem; }
        .step-content p  { font-size: 0.78rem; }
    }

    @media (max-width: 480px) {
        .hero-title   { font-size: 1.2rem; }
        .metric-value { font-size: 1.1rem; }
    }
</style>
""", unsafe_allow_html=True)

#  Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <i class="fas fa-brain"></i> MindTrack
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color: #64748B; font-size: 0.8rem; margin-bottom: 1.5rem;">
        Mental Health Analytics Platform
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    st.markdown("""
    <div style="color: #64748B; font-size: 0.8rem; margin-top: 0.5rem;">
        Sélectionnez une étape<br>dans le menu ci-dessus
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**Projet**")
    st.markdown("""
    <div style="color: #64748B; font-size: 0.8rem; line-height: 2;">
        <i class="fas fa-bullseye" style="color:#2DD4BF; width:16px;"></i>
        &nbsp;Health Data Analytics<br>
        <i class="fas fa-database" style="color:#2DD4BF; width:16px;"></i>
        &nbsp;2 400+ observations<br>
        <i class="fas fa-robot" style="color:#2DD4BF; width:16px;"></i>
        &nbsp;Decision Tree Classifier<br>
        <i class="fab fa-python" style="color:#2DD4BF; width:16px;"></i>
        &nbsp;Python · Streamlit · Plotly
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="color: #64748B; font-size: 0.75rem; text-align: center; margin-top: 1rem;">
        <i class="fas fa-code" style="color:#334155;"></i> Développé par<br>
        <span style="color: #2DD4BF; font-weight: 600;">Erine MASSO</span><br>
        <span style="color: #334155;">Data & AI Engineer</span>
    </div>
    """, unsafe_allow_html=True)

#  Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">
        <i class="fas fa-brain"></i>
        Mental Health Analytics Platform
    </div>
    <div class="hero-title">
        Peut-on détecter une <span>dépression</span><br>
        grâce aux habitudes de vie ?
    </div>
    <div class="hero-subtitle">
        Une plateforme d'analyse et de prédiction explorant les corrélations
        entre habitudes de vie quotidiennes et santé mentale, combinant
        data science et machine learning pour des insights actionnables.
    </div>
</div>
""", unsafe_allow_html=True)

#  Métriques
col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("2 405", "Observations",        "fas fa-users"),
    ("11",    "Variables analysées", "fas fa-layer-group"),
    ("4",     "Modèles comparés",    "fas fa-robot"),
    ("23.9%", "Meilleure CV Accuracy","fas fa-chart-line"),
]

for col, (value, label, icon) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <i class="{icon}" style="color:#2DD4BF44; font-size:1.2rem; margin-bottom:0.5rem;"></i>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#  Démarche + À propos
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### La démarche")

    steps = [
        ("fas fa-globe",        "Étape 1 : Le problème mondial",
         "Visualiser l'ampleur des troubles mentaux par pays et condition"),
        ("fas fa-search",       "Étape 2 : Les facteurs de risque",
         "Explorer l'impact du sommeil, stress, sport et temps d'écran"),
        ("fas fa-chart-bar",    "Étape 3 : Exploration des données",
         "Analyse exploratoire interactive avec filtres dynamiques"),
        ("fas fa-robot",        "Étape 4 : Modèle Machine Learning",
         "Comparaison de 4 modèles de classification et interprétation"),
        ("fas fa-crosshairs",   "Étape 5 : Simulateur de risque",
         "Entrez vos habitudes et obtenez une estimation personnalisée"),
    ]

    for icon, title, desc in steps:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-icon-box">
                <i class="{icon}"></i>
            </div>
            <div class="step-content">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### Stack technique")
    st.markdown("""
    ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
    ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
    ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
    ![Scikit--learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
    ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### À propos du projet")
    st.markdown("""
    <div class="about-container">
        <div class="about-item">
            <div class="about-icon" style="background:#2DD4BF22; color:#2DD4BF;">
                <i class="fas fa-bullseye"></i>
            </div>
            <div>
                <div class="about-label">Objectif</div>
                <div class="about-value">Prédiction du risque de dépression</div>
                <div class="about-sub">Classification multi-classes par ML</div>
            </div>
        </div>
        <div class="about-item">
            <div class="about-icon" style="background:#0EA5E922; color:#0EA5E9;">
                <i class="fas fa-diagram-project"></i>
            </div>
            <div>
                <div class="about-label">Approche</div>
                <div class="about-value">End-to-end Data Science</div>
                <div class="about-sub">EDA · ML · Application interactive</div>
            </div>
        </div>
        <div class="about-item">
            <div class="about-icon" style="background:#8B5CF622; color:#8B5CF6;">
                <i class="fas fa-user-tie"></i>
            </div>
            <div>
                <div class="about-label">Développée par</div>
                <div class="about-value">Erine MASSO</div>
                <div class="about-sub">Data & AI Engineer</div>
            </div>
        </div>
        <div class="about-item">
            <div class="about-icon" style="background:#F59E0B22; color:#F59E0B;">
                <i class="fas fa-heart-pulse"></i>
            </div>
            <div>
                <div class="about-label">Domaine</div>
                <div class="about-value">Health Data Analytics</div>
                <div class="about-sub">Mental Health & Lifestyle</div>
            </div>
        </div>
        <div class="about-status">
            <div class="about-dot"></div>
            <div class="about-status-text">
                <i class="fas fa-code-branch" style="margin-right:0.4rem;"></i>
                Version 1.0 — Juin 2026
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

#  Disclaimer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="disclaimer">
    <i class="fas fa-triangle-exclamation" style="color:#F59E0B; margin-right:0.5rem;"></i>
    <strong>Note</strong> : Les analyses présentées sont basées sur un dataset
    synthétique à des fins de démonstration. Les résultats ne constituent pas
    des conclusions cliniques et ne remplacent pas un avis médical professionnel.
</div>
""", unsafe_allow_html=True)