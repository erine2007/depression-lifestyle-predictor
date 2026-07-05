import streamlit as st
import sys
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
from PIL import Image
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.styles import load_css, page_header, section_header, insight_box
from src.utils import load_data

favicon = Image.open("assets/favicon.png")
st.set_page_config(
    page_title="MindTrack | Simulateur",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)

@st.cache_resource
def load_model_artifacts():
    model   = joblib.load(os.path.join("models", "best_model.pkl"))
    mapping = joblib.load(os.path.join("models", "class_mapping.pkl"))
    return model, mapping

@st.cache_resource
def load_scaler():
    df    = load_data()
    df_ml = df.copy()
    categorical_cols = ["Country", "Gender", "Exercise Level", "Diet Type", "Stress Level"]
    le = LabelEncoder()
    for col in categorical_cols:
        df_ml[col] = le.fit_transform(df_ml[col])
    le_target = LabelEncoder()
    df_ml["Mental Health Condition"] = le_target.fit_transform(df_ml["Mental Health Condition"])
    X = df_ml.drop(columns=["Mental Health Condition"])
    y = df_ml["Mental Health Condition"]
    X_train, _, _, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler

@st.cache_resource
def load_encoders():
    df = load_data()
    encoders = {}
    categorical_cols = ["Country", "Gender", "Exercise Level", "Diet Type", "Stress Level"]
    for col in categorical_cols:
        le = LabelEncoder()
        le.fit(df[col])
        encoders[col] = le
    return encoders

best_model, mapping = load_model_artifacts()
scaler              = load_scaler()
encoders            = load_encoders()

# Trouver l'index de Depression dans le mapping
depression_idx = None
for idx, label in mapping.items():
    if label == "Depression":
        depression_idx = idx
        break

colors_condition = {
    "Anxiety"   : "#4F7A67",
    "PTSD"      : "#7D9A7B",
    "Depression": "#C97B52",
    "Bipolar"   : "#22372D"
}

page_header(
    icon="fas fa-crosshairs",
    tag="Étape 5",
    title="Simulateur : Détection du risque de dépression",
    subtitle="Renseignez vos habitudes de vie pour estimer votre profil de santé mentale"
)

# Bandeau problématique
st.markdown(
    '<div style="background:#FDF8F4;border:1.5px solid #E8D5C4;'
    'border-left:6px solid #C97B52;border-radius:12px;'
    'padding:1rem 1.5rem;margin-bottom:1.5rem;">'
    '<div style="display:flex;align-items:center;gap:1rem;">'
    '<i class="fas fa-brain" style="color:#C97B52;font-size:1.3rem;flex-shrink:0;"></i>'
    '<div>'
    '<div style="color:#22372D;font-size:0.88rem;font-weight:700;margin-bottom:0.2rem;">'
    'Problématique : Peut-on détecter une dépression grâce aux habitudes de vie ?</div>'
    '<div style="color:#7A5C35;font-size:0.82rem;">'
    'Ce simulateur applique notre modèle Decision Tree sur vos données personnelles. '
    'Le résultat met en avant votre <strong>risque estimé de dépression</strong> '
    'et les facteurs qui y contribuent.</div>'
    '</div></div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FORMULAIRE
# ══════════════════════════════════════════
section_header(
    icon="fas fa-sliders",
    title="Vos habitudes de vie",
    subtitle="Renseignez vos habitudes quotidiennes"
)

col_form1, col_form2 = st.columns(2)

with col_form1:
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;border-top:3px solid #4F7A67;'
        'border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:0.5rem;'
        'box-shadow:0 3px 10px rgba(34,55,45,0.07);">'
        '<div style="color:#22372D;font-size:0.85rem;font-weight:600;margin-bottom:0.8rem;">'
        '<i class="fas fa-user" style="color:#4F7A67;margin-right:0.5rem;"></i>'
        'Profil personnel</div></div>',
        unsafe_allow_html=True
    )
    age      = st.slider("Âge", min_value=18, max_value=64, value=30)
    gender   = st.selectbox("Genre", options=list(encoders["Gender"].classes_))
    country  = st.selectbox("Pays", options=list(encoders["Country"].classes_))
    diet_type = st.selectbox("Alimentation", options=list(encoders["Diet Type"].classes_))

with col_form2:
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #E8D5C4;border-top:3px solid #C97B52;'
        'border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:0.5rem;'
        'box-shadow:0 3px 10px rgba(201,123,82,0.08);">'
        '<div style="color:#22372D;font-size:0.85rem;font-weight:600;margin-bottom:0.8rem;">'
        '<i class="fas fa-heart-pulse" style="color:#C97B52;margin-right:0.5rem;"></i>'
        'Habitudes — Facteurs liés à la dépression</div></div>',
        unsafe_allow_html=True
    )
    sleep_hours    = st.slider("Heures de sommeil / nuit", 2.5, 10.5, 7.0, 0.5)
    stress_level   = st.selectbox("Niveau de stress", ["Low", "Moderate", "High"], index=1)
    exercise_level = st.selectbox("Activité physique", ["Low", "Moderate", "High"], index=1)
    work_hours     = st.slider("Heures de travail / semaine", 20, 59, 40)
    screen_time    = st.slider("Temps d'écran / jour (h)", 2.0, 8.0, 5.0, 0.5)
    social_score   = st.slider("Score interaction sociale (1-10)", 1.0, 10.0, 5.0, 0.5)
    happiness_score = st.slider("Score bien-être ressenti (1-10)", 1.0, 10.0, 5.0, 0.5)

st.markdown("<br>", unsafe_allow_html=True)

col_btn, _, _ = st.columns([1, 2, 1])
with col_btn:
    predict_btn = st.button("Lancer l'analyse", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# RÉSULTATS
# ══════════════════════════════════════════
if predict_btn:
    input_data = {
        "Country"                    : encoders["Country"].transform([country])[0],
        "Age"                        : age,
        "Gender"                     : encoders["Gender"].transform([gender])[0],
        "Exercise Level"             : encoders["Exercise Level"].transform([exercise_level])[0],
        "Diet Type"                  : encoders["Diet Type"].transform([diet_type])[0],
        "Sleep Hours"                : sleep_hours,
        "Stress Level"               : encoders["Stress Level"].transform([stress_level])[0],
        "Work Hours per Week"        : work_hours,
        "Screen Time per Day (Hours)": screen_time,
        "Social Interaction Score"   : social_score,
        "Happiness Score"            : happiness_score,
    }

    input_df    = pd.DataFrame([input_data])
    input_s     = scaler.transform(input_df)
    prediction  = best_model.predict(input_s)[0]
    predicted_label = mapping[prediction]

    has_proba = hasattr(best_model, "predict_proba")
    if has_proba:
        probas     = best_model.predict_proba(input_s)[0]
        proba_dict = {mapping[i]: round(p * 100, 1) for i, p in enumerate(probas)}
        dep_proba  = proba_dict.get("Depression", 25.0)
    else:
        proba_dict = {mapping[i]: 25.0 for i in mapping}
        dep_proba  = 25.0

    section_header(
        icon="fas fa-chart-pie",
        title="Résultats de l'analyse",
        subtitle="Focus sur le risque de dépression et profil général"
    )

    # FOCUS DÉPRESSION EN PREMIER
    dep_color = "#C97B52"
    risk_level = "Élevé" if dep_proba >= 35 else "Modéré" if dep_proba >= 20 else "Faible"
    risk_bg    = "#FDF8F4" if dep_proba >= 20 else "#EEF2EC"
    risk_border = "#C97B52" if dep_proba >= 20 else "#4F7A67"
    risk_icon  = "fas fa-triangle-exclamation" if dep_proba >= 35 \
                 else "fas fa-circle-exclamation" if dep_proba >= 20 \
                 else "fas fa-circle-check"
    risk_text_color = "#C97B52" if dep_proba >= 20 else "#4F7A67"

    st.markdown(
        f'<div style="background:{risk_bg};border:2px solid {risk_border};'
        f'border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;'
        f'box-shadow:0 6px 24px rgba(201,123,82,0.12);">'
        f'<div style="color:{dep_color};font-size:0.75rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">'
        f'<i class="fas fa-crosshairs" style="margin-right:0.5rem;"></i>'
        f'Réponse à la problématique : Risque de dépression estimé</div>'
        f'<div style="display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">'
        f'<div style="text-align:center;">'
        f'<div style="font-size:3.5rem;font-weight:900;color:{dep_color};line-height:1;">'
        f'{dep_proba}%</div>'
        f'<div style="color:#66736A;font-size:0.8rem;margin-top:0.3rem;">Probabilité estimée</div>'
        f'</div>'
        f'<div style="flex:1;min-width:200px;">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">'
        f'<i class="{risk_icon}" style="color:{risk_text_color};font-size:1.2rem;"></i>'
        f'<span style="color:#22372D;font-size:1.1rem;font-weight:700;">'
        f'Niveau de risque : {risk_level}</span></div>'
        f'<div style="background:#FFFFFF;border-radius:8px;height:12px;margin-bottom:0.8rem;">'
        f'<div style="background:{dep_color};width:{min(dep_proba, 100)}%;height:12px;'
        f'border-radius:8px;transition:width 0.5s;"></div></div>'
        f'<div style="color:#66736A;font-size:0.84rem;line-height:1.5;">'
        f'Ce score représente la probabilité que votre profil d\'habitudes '
        f'soit associé à une condition dépressive selon notre modèle.</div>'
        f'</div></div></div>',
        unsafe_allow_html=True
    )

    col_result, col_probas = st.columns([1, 2])

    with col_result:
        # Condition prédite générale
        accent = colors_condition.get(predicted_label, "#4F7A67")
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
            f'border-top:4px solid {accent};border-radius:14px;'
            f'padding:1.5rem;text-align:center;margin-bottom:1rem;'
            f'box-shadow:0 4px 16px rgba(34,55,45,0.08);">'
            f'<div style="color:#8C948E;font-size:0.72rem;text-transform:uppercase;'
            f'letter-spacing:0.08em;margin-bottom:0.4rem;">Condition prédite</div>'
            f'<div style="font-size:1.6rem;font-weight:800;color:{accent};">'
            f'{predicted_label}</div>'
            f'<div style="color:#66736A;font-size:0.78rem;margin-top:0.4rem;">'
            f'Profil le plus proche selon<br>vos habitudes de vie</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Facteurs de risque liés à la dépression
        risk_factors = []
        if sleep_hours < 6:
            risk_factors.append(("fas fa-moon", "Manque de sommeil", f"{sleep_hours}h/nuit", "#C97B52"))
        if stress_level == "High":
            risk_factors.append(("fas fa-brain", "Stress élevé", "Niveau High", "#C97B52"))
        if exercise_level == "Low":
            risk_factors.append(("fas fa-person-running", "Sédentarité", "Exercice faible", "#C97B52"))
        if happiness_score < 4:
            risk_factors.append(("fas fa-face-sad-tear", "Bien-être bas", f"{happiness_score}/10", "#C97B52"))
        if social_score < 4:
            risk_factors.append(("fas fa-users-slash", "Isolement social", f"{social_score}/10", "#C97B52"))

        # Facteurs protecteurs
        protect_factors = []
        if sleep_hours >= 7:
            protect_factors.append(("fas fa-moon", "Sommeil suffisant", f"{sleep_hours}h/nuit"))
        if exercise_level == "High":
            protect_factors.append(("fas fa-person-running", "Activité physique élevée", "High"))
        if happiness_score >= 7:
            protect_factors.append(("fas fa-face-smile", "Bien-être élevé", f"{happiness_score}/10"))
        if social_score >= 7:
            protect_factors.append(("fas fa-users", "Bonne vie sociale", f"{social_score}/10"))

        if risk_factors:
            st.markdown(
                '<div style="background:#FFFFFF;border:1.5px solid #E8D5C4;'
                'border-left:4px solid #C97B52;border-radius:12px;'
                'padding:1rem;margin-bottom:0.8rem;">'
                '<div style="color:#22372D;font-size:0.82rem;font-weight:600;margin-bottom:0.6rem;">'
                '<i class="fas fa-triangle-exclamation" style="color:#C97B52;margin-right:0.5rem;"></i>'
                'Facteurs de risque identifiés</div>',
                unsafe_allow_html=True
            )
            for icon, label, value, color in risk_factors:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.7rem;'
                    f'padding:0.4rem 0;border-bottom:1px solid #EEF2EC;">'
                    f'<i class="{icon}" style="color:{color};width:14px;"></i>'
                    f'<span style="color:#66736A;font-size:0.8rem;flex:1;">{label}</span>'
                    f'<span style="color:#22372D;font-size:0.8rem;font-weight:500;">{value}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

        if protect_factors:
            st.markdown(
                '<div style="background:#EEF2EC;border:1.5px solid #D6DDD7;'
                'border-left:4px solid #4F7A67;border-radius:12px;padding:1rem;">'
                '<div style="color:#22372D;font-size:0.82rem;font-weight:600;margin-bottom:0.6rem;">'
                '<i class="fas fa-shield-heart" style="color:#4F7A67;margin-right:0.5rem;"></i>'
                'Facteurs protecteurs</div>',
                unsafe_allow_html=True
            )
            for icon, label, value in protect_factors:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.7rem;'
                    f'padding:0.4rem 0;border-bottom:1px solid #D6DDD7;">'
                    f'<i class="{icon}" style="color:#4F7A67;width:14px;"></i>'
                    f'<span style="color:#66736A;font-size:0.8rem;flex:1;">{label}</span>'
                    f'<span style="color:#22372D;font-size:0.8rem;font-weight:500;">{value}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

    with col_probas:
        if has_proba:
            proba_sorted = dict(sorted(proba_dict.items(), key=lambda x: x[1], reverse=True))
            fig_proba = go.Figure()
            for condition, proba in proba_sorted.items():
                is_dep  = condition == "Depression"
                is_pred = condition == predicted_label
                fig_proba.add_trace(go.Bar(
                    x=[proba], y=[condition], orientation="h",
                    marker_color=colors_condition.get(condition, "#4F7A67"),
                    marker_opacity=1.0 if (is_dep or is_pred) else 0.4,
                    text=[f"{proba}%"],
                    textposition="outside",
                    textfont=dict(
                        color="#22372D" if (is_dep or is_pred) else "#8C948E",
                        size=13 if (is_dep or is_pred) else 11
                    ),
                    showlegend=False
                ))
            fig_proba.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                font=dict(color="#66736A", family="Inter"),
                xaxis=dict(showgrid=True, gridcolor="#EEF2EC",
                           color="#66736A", ticksuffix="%",
                           range=[0, max(proba_dict.values()) * 1.3]),
                yaxis=dict(showgrid=False, color="#22372D",
                           tickfont=dict(size=13, color="#22372D")),
                margin=dict(t=10, b=10, l=10, r=60), height=260
            )
            st.plotly_chart(fig_proba, use_container_width=True)

        # Radar chart
        categories = ["Sommeil", "Anti-stress", "Exercice",
                      "Social", "Bien-être", "Équilibre écran"]
        radar_values = [
            min(sleep_hours / 8 * 10, 10),
            {"Low": 9, "Moderate": 5, "High": 2}[stress_level],
            {"Low": 2, "Moderate": 6, "High": 10}[exercise_level],
            social_score, happiness_score,
            max(0, 10 - (screen_time - 2) / 6 * 10)
        ]
        ideal = [8, 8, 8, 8, 8, 8]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values + [radar_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(201, 123, 82, 0.15)",
            line=dict(color="#C97B52", width=2),
            name="Votre profil"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=ideal + [ideal[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(79, 122, 103, 0.07)",
            line=dict(color="#4F7A67", width=1.5, dash="dot"),
            name="Profil équilibré"
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#FFFFFF",
                radialaxis=dict(visible=True, range=[0, 10],
                                tickfont=dict(color="#8C948E", size=9),
                                gridcolor="#EEF2EC", linecolor="#EEF2EC"),
                angularaxis=dict(tickfont=dict(color="#22372D", size=11),
                                 linecolor="#EEF2EC", gridcolor="#EEF2EC")
            ),
            paper_bgcolor="#FFFFFF",
            font=dict(color="#66736A", family="Inter"),
            showlegend=True,
            legend=dict(bgcolor="#F9F7F3", bordercolor="#D6DDD7",
                        borderwidth=1, font=dict(color="#66736A", size=11)),
            margin=dict(t=30, b=30, l=30, r=30), height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # RECOMMANDATIONS
    st.markdown("<br>", unsafe_allow_html=True)
    section_header(
        icon="fas fa-lightbulb",
        title="Pistes d'amélioration",
        subtitle="Suggestions basées sur votre profil, facteurs protecteurs contre la dépression"
    )

    recommendations = []
    if sleep_hours < 7:
        recommendations.append((
            "fas fa-moon", "#4F7A67", "Améliorer le sommeil",
            f"Vous dormez {sleep_hours}h/nuit. Viser 7-9h est associé "
            "à une réduction significative du risque dépressif."
        ))
    if stress_level == "High":
        recommendations.append((
            "fas fa-spa", "#7D9A7B", "Réduire le stress",
            "Le stress élevé est le facteur le plus corrélé à la dépression. "
            "Méditation, exercice ou thérapie cognitivo-comportementale peuvent aider."
        ))
    if exercise_level == "Low":
        recommendations.append((
            "fas fa-person-running", "#C97B52", "Augmenter l'activité physique",
            "30 min d'exercice/jour est l'un des facteurs protecteurs les mieux "
            "documentés contre la dépression, efficacité comparable à certains antidépresseurs."
        ))
    if social_score < 5:
        recommendations.append((
            "fas fa-users", "#4F7A67", "Renforcer les liens sociaux",
            f"Score : {social_score}/10. L'isolement social multiplie par 2-3 "
            "le risque de développer un épisode dépressif."
        ))
    if happiness_score < 5:
        recommendations.append((
            "fas fa-heart", "#C97B52", "Travailler le bien-être",
            f"Score : {happiness_score}/10. Des activités à valeur personnelle "
            "(hobbies, bénévolat, création) peuvent progressivement améliorer ce score."
        ))
    if not recommendations:
        recommendations.append((
            "fas fa-circle-check", "#4F7A67", "Profil équilibré",
            "Vos habitudes de vie semblent globalement protectrices. "
            "Maintenir cet équilibre est la meilleure prévention contre la dépression."
        ))

    cols_reco = st.columns(min(len(recommendations), 3))
    for i, (icon, color, title, desc) in enumerate(recommendations):
        with cols_reco[i % len(cols_reco)]:
            st.markdown(
                f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
                f'border-top:4px solid {color};border-radius:12px;'
                f'padding:1.2rem;box-shadow:0 3px 10px rgba(34,55,45,0.07);">'
                f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.7rem;">'
                f'<div style="width:32px;height:32px;border-radius:8px;'
                f'background:{color}22;color:{color};display:flex;align-items:center;'
                f'justify-content:center;font-size:0.9rem;">'
                f'<i class="{icon}"></i></div>'
                f'<div style="color:#22372D;font-size:0.88rem;font-weight:600;">{title}</div>'
                f'</div>'
                f'<div style="color:#66736A;font-size:0.82rem;line-height:1.5;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Note finale
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#8C948E;font-size:0.78rem;text-align:center;line-height:1.5;">'
        '<i class="fas fa-circle-info" style="color:#C97B52;margin-right:0.4rem;"></i>'
        'Ces estimations sont basées sur un modèle entraîné sur un dataset synthétique. '
        'Elles ne constituent pas un diagnostic médical. '
        'En cas de détresse, consultez un professionnel de santé mentale.'
        '</div>',
        unsafe_allow_html=True
    )

else:
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;border-radius:16px;'
        'padding:3rem;text-align:center;box-shadow:0 4px 16px rgba(34,55,45,0.08);">'
        '<div style="width:64px;height:64px;border-radius:16px;background:#FDF8F4;'
        'display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;'
        'border:1.5px solid #E8D5C4;">'
        '<i class="fas fa-crosshairs" style="color:#C97B52;font-size:1.5rem;"></i></div>'
        '<div style="color:#22372D;font-size:1.1rem;font-weight:600;margin-bottom:0.5rem;">'
        'Estimez votre risque de dépression</div>'
        '<div style="color:#8C948E;font-size:0.88rem;line-height:1.6;">'
        'Ajustez les paramètres ci-dessus selon vos habitudes réelles,<br>'
        'puis cliquez sur <strong style="color:#22372D;">Lancer l\'analyse</strong> '
        'pour obtenir votre estimation personnalisée.</div>'
        '</div>',
        unsafe_allow_html=True
    )
