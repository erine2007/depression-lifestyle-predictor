def load_css():
    return """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid #2DD4BF22;
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

    /* Titres de section */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1E293B;
    }

    .section-header-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #2DD4BF15;
        border: 1px solid #2DD4BF33;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2DD4BF;
        font-size: 1rem;
        flex-shrink: 0;
    }

    .section-header-text h2 {
        color: #F1F5F9;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }

    .section-header-text p {
        color: #64748B;
        font-size: 0.85rem;
        margin: 0;
    }

    /* Cartes de contenu */
    .content-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }

    .content-card:hover {
        border-color: #2DD4BF33;
    }

    .content-card-title {
        color: #94A3B8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .content-card-title i {
        color: #2DD4BF;
    }

    /* Insight boxes */
    .insight-box {
        background: #0F172A;
        border: 1px solid #2DD4BF22;
        border-left: 3px solid #2DD4BF;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        color: #94A3B8;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    .insight-box strong {
        color: #2DD4BF;
    }

    /* Metric cards inline */
    .mini-metric {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }

    .mini-metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2DD4BF;
    }

    .mini-metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* Page header */
    .page-hero {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        animation: fadeInUp 0.6s ease both;
    }

    .page-hero-icon {
        width: 56px;
        height: 56px;
        border-radius: 14px;
        background: #2DD4BF15;
        border: 1px solid #2DD4BF33;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #2DD4BF;
        font-size: 1.4rem;
        flex-shrink: 0;
    }

    .page-hero-content h1 {
        color: #F1F5F9;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
    }

    .page-hero-content p {
        color: #64748B;
        font-size: 0.9rem;
        margin: 0;
    }

    .page-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #2DD4BF11;
        color: #2DD4BF;
        border: 1px solid #2DD4BF33;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
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

    /* Plotly charts dark theme fix */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }

    /* Streamlit elements overrides */
    .stSelectbox label, .stSlider label, .stMultiSelect label {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
    }

    div[data-baseweb="select"] {
        background: #0F172A !important;
        border-color: #334155 !important;
    }

    .stSlider .stSlider-thumb {
        background: #2DD4BF !important;
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

    @media (max-width: 768px) {
        .page-hero         { padding: 1.2rem; flex-direction: column; }
        .page-hero-icon    { width: 44px; height: 44px; font-size: 1.1rem; }
        .page-hero-content h1 { font-size: 1.2rem; }
        .content-card      { padding: 1rem; }
    }
</style>
"""


def page_header(icon, tag, title, subtitle):
    """
    Génère un header de page standardisé.
    
    Args:
        icon    : classe Font Awesome (ex: "fas fa-globe")
        tag     : label du badge (ex: "Étape 1")
        title   : titre principal
        subtitle: sous-titre descriptif
    """
    import streamlit as st
    st.markdown(f"""
    <div class="page-hero">
        <div class="page-hero-icon">
            <i class="{icon}"></i>
        </div>
        <div class="page-hero-content">
            <div class="page-tag">
                <i class="fas fa-circle-dot"></i> {tag}
            </div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon, title, subtitle=""):
    """
    Génère un titre de section standardisé.
    
    Args:
        icon    : classe Font Awesome
        title   : titre de la section
        subtitle: description optionnelle
    """
    import streamlit as st
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-icon">
            <i class="{icon}"></i>
        </div>
        <div class="section-header-text">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def insight_box(text):
    """
    Génère une boîte d'insight/observation.
    
    Args:
        text: contenu HTML de l'insight
    """
    import streamlit as st
    st.markdown(f"""
    <div class="insight-box">
        <i class="fas fa-lightbulb" style="color:#2DD4BF; margin-right:0.5rem;"></i>
        {text}
    </div>
    """, unsafe_allow_html=True)