def load_css():
    return """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background-color: #F6F5F1 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #ECEBE5 !important;
        border-right: 1.5px solid #D6DDD7 !important;
    }

    [data-testid="stSidebar"] * {
        color: #22372D !important;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 8px !important;
        padding: 0.55rem 1rem !important;
        margin-bottom: 0.2rem !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
        color: #66736A !important;
        font-size: 0.88rem !important;
        text-decoration: none !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: #E4EAE4 !important;
        border-color: #7D9A7B !important;
        color: #22372D !important;
        transform: translateX(3px) !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #E4EAE4 !important;
        border-color: #4F7A67 !important;
        border-left: 3px solid #4F7A67 !important;
        color: #22372D !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] {
     width: 280px !important;
     min-width: 280px !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] {
     width: 280px !important;
     min-width: 280px !important;
     display: block !important;
    }

    .stSelectbox label,
    .stSlider label,
    .stMultiSelect label,
    .stRadio label {
        color: #66736A !important;
        font-size: 0.85rem !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #D6DDD7 !important;
        color: #22372D !important;
    }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }

    
    header [data-testid="stDecoration"] { visibility: hidden; }


    [data-testid="collapsedControl"] {
     visibility: visible !important;
     display: flex !important;
     background-color: #4F7A67 !important;
     border-radius: 0 8px 8px 0 !important;
     color: white !important;
    }

    button[data-testid="baseButton-header"] {
     visibility: visible !important;
     display: flex !important;
    }
    ::-webkit-scrollbar       { width: 5px; }
    ::-webkit-scrollbar-track { background: #F6F5F1; }
    ::-webkit-scrollbar-thumb { background: #C8D4C8; border-radius: 3px; }

    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-16px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 #4F7A6722; }
        50%       { box-shadow: 0 0 0 6px #4F7A6700; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-4px); }
    }

    .card-float {
        animation: float 4s ease-in-out infinite;
    }

    .card-hover {
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }

    .card-hover:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 32px rgba(34,55,45,0.15) !important;
    }

    .step-hover {
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    }

    .step-hover:hover {
        transform: translateX(6px) !important;
        box-shadow: 0 6px 20px rgba(34,55,45,0.12) !important;
    }

    @media (max-width: 768px) {
        .stColumn { padding: 0.3rem !important; }
    }
</style>
"""


def page_header(icon, tag, title, subtitle):
    import streamlit as st
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
        'border-top:4px solid #4F7A67;border-radius:14px;'
        'padding:1.8rem 2.2rem;margin-bottom:2rem;display:flex;align-items:center;'
        'gap:1.5rem;box-shadow:0 4px 20px rgba(34,55,45,0.1);'
        'animation:fadeInUp 0.5s ease both;">'
        '<div style="width:52px;height:52px;border-radius:14px;background:#EEF2EC;'
        'border:1.5px solid #D6DDD7;display:flex;align-items:center;'
        'justify-content:center;color:#4F7A67;font-size:1.3rem;flex-shrink:0;">'
        f'<i class="{icon}"></i></div>'
        '<div>'
        '<div style="display:inline-flex;align-items:center;gap:0.4rem;'
        'background:#EEF2EC;color:#4F7A67;border:1.5px solid #7D9A7B;'
        'border-radius:20px;padding:0.2rem 0.8rem;font-size:0.72rem;'
        f'font-weight:600;margin-bottom:0.4rem;"><i class="fas fa-circle-dot"></i> {tag}</div>'
        f'<h1 style="color:#22372D;font-size:1.5rem;font-weight:700;margin:0 0 0.3rem 0;">{title}</h1>'
        f'<p style="color:#66736A;font-size:0.88rem;margin:0;">{subtitle}</p>'
        '</div></div>',
        unsafe_allow_html=True
    )


def section_header(icon, title, subtitle=""):
    import streamlit as st
    st.markdown(
        '<div style="display:flex;align-items:center;gap:0.8rem;'
        'margin-bottom:1.5rem;padding-bottom:0.8rem;'
        'border-bottom:2px solid #EEF2EC;animation:slideInLeft 0.4s ease both;">'
        '<div style="width:40px;height:40px;border-radius:10px;background:#EEF2EC;'
        'border:1.5px solid #D6DDD7;display:flex;align-items:center;'
        f'justify-content:center;color:#4F7A67;font-size:1rem;flex-shrink:0;">'
        f'<i class="{icon}"></i></div>'
        '<div>'
        f'<h2 style="color:#22372D;font-size:1.25rem;font-weight:700;margin:0;">{title}</h2>'
        f'<p style="color:#66736A;font-size:0.83rem;margin:0;">{subtitle}</p>'
        '</div></div>',
        unsafe_allow_html=True
    )


def insight_box(text):
    import streamlit as st
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
        'border-left:4px solid #4F7A67;border-radius:10px;'
        'padding:1.1rem 1.3rem;margin-top:1rem;color:#66736A;'
        'font-size:0.88rem;line-height:1.6;'
        'box-shadow:0 3px 12px rgba(34,55,45,0.08);'
        'animation:fadeIn 0.5s ease both;">'
        f'<i class="fas fa-lightbulb" style="color:#C97B52;margin-right:0.5rem;"></i>{text}</div>',
        unsafe_allow_html=True
    )
