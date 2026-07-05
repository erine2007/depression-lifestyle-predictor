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
from sklearn.metrics import confusion_matrix, classification_report

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.styles import load_css, page_header, section_header, insight_box
from src.utils import load_data

favicon = Image.open("assets/favicon.png")
st.set_page_config(
    page_title="MindTrack | Résultats ML",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(load_css(), unsafe_allow_html=True)

colors = {
    "Anxiety"   : "#4F7A67",
    "PTSD"      : "#7D9A7B",
    "Depression": "#C97B52",
    "Bipolar"   : "#22372D"
}

page_header(
    icon="fas fa-robot",
    tag="Étape 4",
    title="Résultats du modèle Machine Learning",
    subtitle="Comparaison des modèles, performances et réponse à la problématique"
)

results = {
    "Logistic Regression" : {"accuracy": 28.3, "f1": 27.2, "cv_mean": 23.6},
    "Decision Tree"       : {"accuracy": 23.1, "f1": 22.9, "cv_mean": 23.9},
    "Random Forest"       : {"accuracy": 24.3, "f1": 24.3, "cv_mean": 23.4},
    "Gradient Boosting"   : {"accuracy": 24.3, "f1": 24.1, "cv_mean": 23.9},
}
best_name = "Decision Tree"

@st.cache_resource
def load_model_artifacts():
    model   = joblib.load(os.path.join("models", "best_model.pkl"))
    mapping = joblib.load(os.path.join("models", "class_mapping.pkl"))
    return model, mapping

@st.cache_data
def get_test_data():
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
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_test_s = scaler.transform(X_test)
    return X_test_s, y_test, X.columns.tolist()

best_model, mapping = load_model_artifacts()
X_test_s, y_test, feature_names = get_test_data()
y_pred_best = best_model.predict(X_test_s)
condition_labels = [mapping[i] for i in sorted(mapping.keys())]
cm = confusion_matrix(y_test, y_pred_best)
report = classification_report(
    y_test, y_pred_best,
    target_names=condition_labels,
    output_dict=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 1 — COMPARAISON DES MODÈLES
# ══════════════════════════════════════════
section_header(
    icon="fas fa-ranking-star",
    title="Comparaison des modèles",
    subtitle="Résultats obtenus lors de l'entraînement "
)

col1, col2, col3, col4 = st.columns(4)
model_configs = [
    ("Logistic Regression", "Log. Regression", "#4F7A67"),
    ("Decision Tree",       "Decision Tree",   "#22372D"),
    ("Random Forest",       "Random Forest",   "#4F7A67"),
    ("Gradient Boosting",   "Grad. Boosting",  "#C97B52"),
]

for col, (name, short, accent) in zip([col1, col2, col3, col4], model_configs):
    is_best    = name == best_name
    border_top = "#22372D" if is_best else accent
    badge = (' <span style="background:#22372D;color:#FFFFFF;font-size:0.62rem;'
             'padding:0.1rem 0.4rem;border-radius:4px;margin-left:0.3rem;">BEST</span>'
             if is_best else "")
    with col:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
            f'border-top:4px solid {border_top};border-radius:14px;'
            f'padding:1.3rem 1rem;text-align:center;'
            f'box-shadow:0 4px 16px rgba(34,55,45,0.1);">'
            f'<div style="color:#66736A;font-size:0.72rem;font-weight:600;'
            f'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.5rem;">'
            f'{short}{badge}</div>'
            f'<div style="font-size:1.7rem;font-weight:800;color:#22372D;">'
            f'{results[name]["accuracy"]}%</div>'
            f'<div style="font-size:0.72rem;color:#8C948E;margin-bottom:0.5rem;">Accuracy</div>'
            f'<div style="font-size:1rem;font-weight:600;color:{accent};">'
            f'{results[name]["f1"]}%</div>'
            f'<div style="font-size:0.72rem;color:#8C948E;margin-bottom:0.5rem;">F1-Score</div>'
            f'<div style="font-size:1rem;font-weight:600;color:#22372D;">'
            f'{results[name]["cv_mean"]}%</div>'
            f'<div style="font-size:0.72rem;color:#8C948E;">CV Accuracy</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

fig_comp = go.Figure()
model_names = list(results.keys())
fig_comp.add_trace(go.Bar(
    name="Accuracy (%)", x=model_names,
    y=[results[n]["accuracy"] for n in model_names],
    marker_color="#4F7A67",
    text=[f'{results[n]["accuracy"]}%' for n in model_names],
    textposition="outside", textfont=dict(color="#66736A", size=11)
))
fig_comp.add_trace(go.Bar(
    name="F1-Score (%)", x=model_names,
    y=[results[n]["f1"] for n in model_names],
    marker_color="#C97B52",
    text=[f'{results[n]["f1"]}%' for n in model_names],
    textposition="outside", textfont=dict(color="#66736A", size=11)
))
fig_comp.add_trace(go.Bar(
    name="CV Accuracy (%)", x=model_names,
    y=[results[n]["cv_mean"] for n in model_names],
    marker_color="#7D9A7B",
    text=[f'{results[n]["cv_mean"]}%' for n in model_names],
    textposition="outside", textfont=dict(color="#66736A", size=11)
))
fig_comp.add_hline(
    y=25, line_dash="dash", line_color="#22372D", line_width=1.5,
    annotation_text="Baseline aléatoire (25%)",
    annotation_font=dict(color="#22372D", size=11)
)
fig_comp.update_layout(
    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
    font=dict(color="#66736A", family="Inter"),
    barmode="group",
    xaxis=dict(showgrid=False, color="#66736A"),
    yaxis=dict(showgrid=True, gridcolor="#EEF2EC",
               color="#66736A", ticksuffix="%", range=[0, 45]),
    legend=dict(bgcolor="#F9F7F3", bordercolor="#D6DDD7",
                borderwidth=1, font=dict(color="#66736A")),
    margin=dict(t=30, b=20, l=10, r=10), height=380
)
st.plotly_chart(fig_comp, use_container_width=True)

insight_box(
    "Le <strong>Decision Tree</strong> est sélectionné comme meilleur modèle "
    "(CV Accuracy : <strong>23.9%</strong>). La <strong>Logistic Regression</strong> "
    "obtient la meilleure accuracy brute (28.3%) mais souffre d'overfitting. "
    "Tous les modèles restent proches de la baseline aléatoire de 25%, "
    "cohérent avec l'absence de signal discriminant fort dans les données."
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 2 — MATRICE DE CONFUSION
# ══════════════════════════════════════════
section_header(
    icon="fas fa-grid-4",
    title="Matrice de confusion",
    subtitle=f"Détail des prédictions du modèle sauvegardé : {best_name}"
)

col_cm, col_cm_info = st.columns([2, 1])

with col_cm:
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm, x=condition_labels, y=condition_labels,
        colorscale=[[0.0, "#F6F5F1"], [0.5, "#7D9A7B"], [1.0, "#22372D"]],
        text=cm, texttemplate="<b>%{text}</b>",
        textfont=dict(size=14), showscale=True,
        colorbar=dict(thickness=12,
                      tickfont=dict(color="#66736A", size=10),
                      outlinewidth=0),
        hoverongaps=False
    ))
    fig_cm.update_layout(
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        xaxis=dict(title="Prédiction", color="#66736A",
                   tickfont=dict(size=11), side="bottom"),
        yaxis=dict(title="Réalité", color="#66736A",
                   tickfont=dict(size=11), autorange="reversed"),
        margin=dict(t=20, b=40, l=60, r=10), height=400
    )
    st.plotly_chart(fig_cm, use_container_width=True)

with col_cm_info:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#22372D;font-size:0.82rem;font-weight:600;margin-bottom:0.8rem;">'
        '<i class="fas fa-percent" style="color:#4F7A67;margin-right:0.4rem;"></i>'
        'Taux de bonne classification</div>',
        unsafe_allow_html=True
    )
    for i, label in enumerate(condition_labels):
        total_real = cm[i].sum()
        correct    = cm[i][i]
        taux       = round(correct / total_real * 100, 1) if total_real > 0 else 0
        color_bar  = colors.get(label, "#4F7A67")
        is_dep     = label == "Depression"
        st.markdown(
            f'<div style="margin-bottom:0.8rem;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">'
            f'<span style="color:{"#C97B52" if is_dep else "#66736A"};'
            f'font-size:0.8rem;{"font-weight:700;" if is_dep else ""}">'
            f'{label}{"  ← Focus" if is_dep else ""}</span>'
            f'<span style="color:{"#C97B52" if is_dep else "#22372D"};'
            f'font-size:0.8rem;font-weight:600;">'
            f'{correct}/{total_real} ({taux}%)</span></div>'
            f'<div style="background:#EEF2EC;border-radius:4px;height:6px;">'
            f'<div style="background:{color_bar};width:{taux}%;height:6px;'
            f'border-radius:4px;"></div></div></div>',
            unsafe_allow_html=True
        )
    st.markdown(
        '<div style="background:#F9F7F3;border:1.5px solid #D6DDD7;'
        'border-radius:10px;padding:1rem;margin-top:0.5rem;">'
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.5rem;">'
        'Lecture</div>'
        '<div style="color:#66736A;font-size:0.78rem;line-height:1.6;">'
        'La <strong style="color:#22372D;">diagonale</strong> = bonnes prédictions.<br>'
        'Hors diagonale = erreurs de classification.</div>'
        '</div>',
        unsafe_allow_html=True
    )

insight_box(
    "La matrice révèle un résultat clé : le modèle ne prédit "
    "<strong style='color:#C97B52;'>jamais Depression (0/116)</strong> , "
    "tous les cas réels de dépression sont confondus avec Anxiety (20 cas) "
    "et Bipolar (96 cas). "
    "Ce comportement illustre parfaitement la difficulté de détecter la dépression "
    "à partir d'habitudes de vie seules : sans signal discriminant fort, "
    "le modèle ne parvient pas à isoler cette condition des autres."
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 3 — FEATURE IMPORTANCE
# ══════════════════════════════════════════
section_header(
    icon="fas fa-ranking-star",
    title="Importance des variables",
    subtitle=f"Contribution de chaque variable : {best_name}"
)

model_class = type(best_model).__name__
tree_based  = ["RandomForestClassifier", "GradientBoostingClassifier", "DecisionTreeClassifier"]
importances = best_model.feature_importances_ if model_class in tree_based \
              else np.abs(best_model.coef_).mean(axis=0)

feat_df = pd.DataFrame({
    "Feature"   : feature_names,
    "Importance": importances
}).sort_values("Importance", ascending=True)

feat_df["Couleur"] = feat_df["Importance"].apply(
    lambda x: "#22372D" if x >= feat_df["Importance"].quantile(0.75)
    else "#4F7A67" if x >= feat_df["Importance"].quantile(0.5)
    else "#7D9A7B"
)

col_fi, col_fi_info = st.columns([3, 1])

with col_fi:
    fig_fi = go.Figure(go.Bar(
        x=feat_df["Importance"], y=feat_df["Feature"],
        orientation="h",
        marker_color=feat_df["Couleur"].tolist(),
        text=[f"{v:.4f}" for v in feat_df["Importance"]],
        textposition="outside",
        textfont=dict(color="#66736A", size=10)
    ))
    fig_fi.update_layout(
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="#EEF2EC",
                   color="#66736A", title="Importance"),
        yaxis=dict(showgrid=False, color="#66736A"),
        margin=dict(t=20, b=20, l=10, r=60), height=380
    )
    st.plotly_chart(fig_fi, use_container_width=True)

with col_fi_info:
    st.markdown("<br>", unsafe_allow_html=True)
    top3   = feat_df.sort_values("Importance", ascending=False).head(3)
    medals = ["#C97B52", "#7D9A7B", "#4F7A67"]

    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
        'border-top:4px solid #22372D;border-radius:10px;padding:1rem;margin-bottom:0.8rem;">'
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.6rem;">'
        '<i class="fas fa-trophy" style="color:#C97B52;margin-right:0.4rem;"></i>'
        'Top 3 variables</div>',
        unsafe_allow_html=True
    )
    for rank, (_, row) in enumerate(top3.iterrows(), 1):
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.6rem;'
            f'padding:0.4rem 0;border-bottom:1px solid #EEF2EC;">'
            f'<div style="width:20px;height:20px;border-radius:50%;'
            f'background:{medals[rank-1]};color:#FFFFFF;font-size:0.65rem;font-weight:700;'
            f'display:flex;align-items:center;justify-content:center;">{rank}</div>'
            f'<div>'
            f'<div style="color:#22372D;font-size:0.78rem;font-weight:500;">'
            f'{row["Feature"].split("(")[0].strip()}</div>'
            f'<div style="color:#8C948E;font-size:0.7rem;">{row["Importance"]:.4f}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    bot3 = feat_df.sort_values("Importance", ascending=True).head(3)
    st.markdown(
        '<div style="background:#F9F7F3;border:1.5px solid #D6DDD7;'
        'border-radius:10px;padding:1rem;">'
        '<div style="color:#22372D;font-size:0.8rem;font-weight:600;margin-bottom:0.6rem;">'
        '<i class="fas fa-arrow-down" style="color:#66736A;margin-right:0.4rem;"></i>'
        'Moins importantes</div>',
        unsafe_allow_html=True
    )
    for _, row in bot3.iterrows():
        st.markdown(
            f'<div style="color:#8C948E;font-size:0.78rem;padding:0.3rem 0;'
            f'border-bottom:1px solid #EEF2EC;">'
            f'{row["Feature"].split("(")[0].strip()} '
            f'<span style="color:#D6DDD7;">({row["Importance"]:.4f})</span></div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

insight_box(
    "<strong>Age (0.1531)</strong>, <strong>Happiness Score (0.1378)</strong> et "
    "<strong>Sleep Hours (0.1361)</strong> sont les variables les plus utilisées. "
    "Paradoxalement, <strong>Stress Level</strong> et <strong>Exercise Level</strong> "
    "arrivent en dernière position malgré leur pertinence clinique. "
    "L'homogénéité des importances confirme l'absence de variable véritablement discriminante."
)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 4 — RAPPORT DE CLASSIFICATION
# ══════════════════════════════════════════
section_header(
    icon="fas fa-file-lines",
    title="Rapport de classification détaillé",
    subtitle="Precision, Recall et F1-Score par condition mentale"
)

col_r1, col_r2, col_r3, col_r4 = st.columns(4)
for col, label in zip([col_r1, col_r2, col_r3, col_r4], condition_labels):
    r      = report[label]
    accent = colors.get(label, "#4F7A67")
    is_dep = label == "Depression"
    with col:
        st.markdown(
            f'<div style="background:#FFFFFF;'
            f'border:{"2px" if is_dep else "1.5px"} solid '
            f'{"#E8D5C4" if is_dep else "#D6DDD7"};'
            f'border-top:{"6px" if is_dep else "4px"} solid {accent};'
            f'border-radius:14px;padding:1.2rem 1rem;'
            f'box-shadow:0 {"8px 28px rgba(201,123,82,0.15)" if is_dep else "4px 16px rgba(34,55,45,0.08)"};">'
            f'<div style="color:#22372D;font-size:0.88rem;font-weight:700;'
            f'margin-bottom:{"0.3rem" if is_dep else "1rem"};text-align:center;">{label}</div>'
            + (f'<div style="color:#C97B52;font-size:0.68rem;text-align:center;'
               f'margin-bottom:0.8rem;">← Condition cible</div>' if is_dep else '')
            + f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">'
            f'<div style="text-align:center;">'
            f'<div style="font-size:1.3rem;font-weight:800;color:#22372D;">'
            f'{r["precision"]:.2f}</div>'
            f'<div style="font-size:0.68rem;color:#8C948E;text-transform:uppercase;'
            f'letter-spacing:0.06em;">Precision</div></div>'
            f'<div style="text-align:center;">'
            f'<div style="font-size:1.3rem;font-weight:800;color:#22372D;">'
            f'{r["recall"]:.2f}</div>'
            f'<div style="font-size:0.68rem;color:#8C948E;text-transform:uppercase;'
            f'letter-spacing:0.06em;">Recall</div></div>'
            f'<div style="text-align:center;grid-column:1/-1;margin-top:0.3rem;'
            f'padding-top:0.5rem;border-top:1px solid #EEF2EC;">'
            f'<div style="font-size:1.5rem;font-weight:800;color:{accent};">'
            f'{r["f1-score"]:.2f}</div>'
            f'<div style="font-size:0.68rem;color:#8C948E;text-transform:uppercase;'
            f'letter-spacing:0.06em;">F1-Score</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SECTION 5 — FOCUS DÉPRESSION
# ══════════════════════════════════════════
st.markdown(
    '<div style="background:#FDF8F4;border:2px solid #E8D5C4;'
    'border-left:6px solid #C97B52;border-radius:14px;'
    'padding:1.5rem 2rem;margin-bottom:1.5rem;">'
    '<div style="color:#C97B52;font-size:0.75rem;font-weight:700;'
    'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">'
    '<i class="fas fa-crosshairs" style="margin-right:0.5rem;"></i>'
    'Réponse à la problématique</div>'
    '<div style="color:#22372D;font-size:1.3rem;font-weight:800;margin-bottom:0.5rem;">'
    'Peut-on détecter une dépression grâce aux habitudes de vie ?</div>'
    '<div style="color:#66736A;font-size:0.9rem;line-height:1.6;">'
    'Cette section synthétise ce que nos modèles nous apprennent spécifiquement '
    'sur la détection de la dépression.</div>'
    '</div>',
    unsafe_allow_html=True
)

# Métriques réelles depuis le rapport
dep_metrics   = report.get("Depression", {})
dep_precision = dep_metrics.get("precision", 0.0)
dep_recall    = dep_metrics.get("recall", 0.0)
dep_f1        = dep_metrics.get("f1-score", 0.0)

col_dep1, col_dep2, col_dep3 = st.columns(3)
dep_cards = [
    (dep_precision, "Precision",
     "Parmi les cas prédits dépression,<br>combien l'étaient vraiment"),
    (dep_recall,    "Recall",
     "Parmi les vrais cas de dépression,<br>combien ont été détectés"),
    (dep_f1,        "F1-Score",
     "Score global de détection<br>de la dépression"),
]
for col, (val, label, desc) in zip([col_dep1, col_dep2, col_dep3], dep_cards):
    with col:
        st.markdown(
            f'<div style="background:#FFFFFF;border:1.5px solid #E8D5C4;'
            f'border-top:4px solid #C97B52;border-radius:14px;'
            f'padding:1.4rem;text-align:center;'
            f'box-shadow:0 4px 16px rgba(201,123,82,0.1);">'
            f'<div style="font-size:2.2rem;font-weight:800;color:#C97B52;">'
            f'{val:.0%}</div>'
            f'<div style="font-size:0.72rem;color:#8C948E;text-transform:uppercase;'
            f'letter-spacing:0.08em;margin-top:0.3rem;">{label}</div>'
            f'<div style="color:#66736A;font-size:0.78rem;margin-top:0.5rem;line-height:1.4;">'
            f'{desc}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# Résumé matrice pour la dépression
dep_idx    = condition_labels.index("Depression")
dep_row    = cm[dep_idx]
dep_total  = dep_row.sum()
dep_correct = dep_row[dep_idx]

st.markdown(
    f'<div style="background:#FFFFFF;border:1.5px solid #E8D5C4;'
    f'border-left:4px solid #C97B52;border-radius:12px;'
    f'padding:1.2rem 1.5rem;margin-bottom:1.5rem;">'
    f'<div style="color:#22372D;font-size:0.88rem;font-weight:700;margin-bottom:0.8rem;">'
    f'<i class="fas fa-magnifying-glass" style="color:#C97B52;margin-right:0.5rem;"></i>'
    f'Zoom sur la dépression dans la matrice de confusion</div>'
    f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">'
    f'<div style="text-align:center;background:#FDF8F4;border-radius:10px;padding:1rem;">'
    f'<div style="font-size:1.8rem;font-weight:800;color:#C97B52;">{dep_total}</div>'
    f'<div style="color:#66736A;font-size:0.78rem;">Vrais cas de dépression</div></div>'
    f'<div style="text-align:center;background:#FDF8F4;border-radius:10px;padding:1rem;">'
    f'<div style="font-size:1.8rem;font-weight:800;color:#C97B52;">{dep_correct}</div>'
    f'<div style="color:#66736A;font-size:0.78rem;">Correctement détectés</div></div>'
    f'<div style="text-align:center;background:#EEF2EC;border-radius:10px;padding:1rem;">'
    f'<div style="font-size:1.8rem;font-weight:800;color:#4F7A67;">{dep_total - dep_correct}</div>'
    f'<div style="color:#66736A;font-size:0.78rem;">Mal classifiés</div></div>'
    f'</div>'
    f'<div style="color:#66736A;font-size:0.82rem;margin-top:1rem;line-height:1.6;">'
    f'Sur <strong style="color:#22372D;">{dep_total} vrais cas de dépression</strong>, '
    f'le modèle en détecte <strong style="color:#C97B52;">{dep_correct} correctement '
    f'({round(dep_correct/dep_total*100, 1) if dep_total > 0 else 0}%)</strong>. '
    f'Les {dep_total - dep_correct} cas restants sont confondus avec les autres conditions, '
    f'illustration directe de la limite du modèle face à notre problématique.</div>'
    f'</div>',
    unsafe_allow_html=True
)

# Classification binaire
st.markdown(
    '<div style="color:#22372D;font-size:0.95rem;font-weight:700;margin-bottom:1rem;">'
    '<i class="fas fa-code-branch" style="color:#C97B52;margin-right:0.5rem;"></i>'
    'Classification binaire : Dépression vs Reste</div>',
    unsafe_allow_html=True
)

col_bin1, col_bin2 = st.columns([2, 1])

with col_bin1:
    binary_results = {
        "Logistic Regression": {"accuracy": 75.9, "f1": 0.0,  "cv": 75.9},
        "Decision Tree"      : {"accuracy": 62.2, "f1": 24.8, "cv": 63.5},
        "Random Forest"      : {"accuracy": 75.5, "f1": 0.0,  "cv": 75.5},
        "Gradient Boosting"  : {"accuracy": 74.2, "f1": 1.6,  "cv": 74.8},
    }
    bin_names = list(binary_results.keys())
    fig_bin = go.Figure()
    fig_bin.add_trace(go.Bar(
        name="Accuracy (%)", x=bin_names,
        y=[binary_results[n]["accuracy"] for n in bin_names],
        marker_color="#7D9A7B",
        text=[f'{binary_results[n]["accuracy"]}%' for n in bin_names],
        textposition="outside", textfont=dict(color="#66736A", size=10)
    ))
    fig_bin.add_trace(go.Bar(
        name="F1-Score Dépression (%)", x=bin_names,
        y=[binary_results[n]["f1"] for n in bin_names],
        marker_color="#C97B52",
        text=[f'{binary_results[n]["f1"]}%' for n in bin_names],
        textposition="outside", textfont=dict(color="#66736A", size=10)
    ))
    fig_bin.add_hline(
        y=24.1, line_dash="dash", line_color="#C97B52", line_width=1.5,
        annotation_text="Taux réel de dépression (24.1%)",
        annotation_font=dict(color="#C97B52", size=10)
    )
    fig_bin.update_layout(
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(color="#66736A", family="Inter"),
        barmode="group",
        xaxis=dict(showgrid=False, color="#66736A"),
        yaxis=dict(showgrid=True, gridcolor="#EEF2EC",
                   color="#66736A", ticksuffix="%", range=[0, 100]),
        legend=dict(bgcolor="#F9F7F3", bordercolor="#D6DDD7",
                    borderwidth=1, font=dict(color="#66736A")),
        margin=dict(t=20, b=20, l=10, r=10), height=320
    )
    st.plotly_chart(fig_bin, use_container_width=True)

with col_bin2:
    st.markdown(
        '<div style="background:#FFFFFF;border:1.5px solid #D6DDD7;'
        'border-radius:12px;padding:1.2rem;">'
        '<div style="color:#22372D;font-size:0.85rem;font-weight:600;margin-bottom:1rem;">'
        '<i class="fas fa-triangle-exclamation" style="color:#C97B52;margin-right:0.5rem;"></i>'
        'Le paradoxe du F1=0</div>'
        '<div style="color:#66736A;font-size:0.82rem;line-height:1.6;margin-bottom:1rem;">'
        '<strong style="color:#22372D;">Logistic Regression</strong> et '
        '<strong style="color:#22372D;">Random Forest</strong> obtiennent ~75% d\'accuracy '
        'mais un F1-Score de <strong style="color:#C97B52;">0%</strong> pour la dépression.</div>'
        '<div style="background:#FDF8F4;border-radius:8px;padding:0.8rem;margin-bottom:0.8rem;">'
        '<div style="color:#7A5C35;font-size:0.8rem;line-height:1.5;">'
        'Ces modèles ont appris à <strong>toujours prédire "non-dépressif"</strong> '
        'car 76% des cas ne sont pas dépressifs.</div></div>'
        '<div style="background:#EEF2EC;border-radius:8px;padding:0.8rem;">'
        '<div style="color:#22372D;font-size:0.8rem;line-height:1.5;">'
        'Seul le <strong>Decision Tree</strong> (F1=24.8%) détecte réellement '
        'des cas de dépression.</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

# Conclusion finale
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div style="background:#FFFFFF;border:2px solid #D6DDD7;'
    'border-radius:14px;padding:1.8rem 2rem;'
    'box-shadow:0 4px 20px rgba(34,55,45,0.08);">'
    '<div style="color:#22372D;font-size:1rem;font-weight:700;margin-bottom:1rem;">'
    '<i class="fas fa-flag-checkered" style="color:#4F7A67;margin-right:0.5rem;"></i>'
    'Réponse à la problématique</div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">'
    '<div style="background:#FDF8F4;border:1px solid #E8D5C4;border-radius:10px;padding:1rem;">'
    '<div style="color:#C97B52;font-size:0.78rem;font-weight:700;text-transform:uppercase;'
    'letter-spacing:0.06em;margin-bottom:0.5rem;">'
    '<i class="fas fa-times-circle" style="margin-right:0.4rem;"></i>Avec ce dataset</div>'
    '<div style="color:#66736A;font-size:0.84rem;line-height:1.6;">'
    'Non, le modèle ne parvient pas à détecter la dépression de façon fiable. '
    'Il prédit 0 cas sur 116 en classification multi-classes, '
    'et 24.8% de F1 seulement en binaire.</div></div>'
    '<div style="background:#EEF2EC;border:1px solid #D6DDD7;border-radius:10px;padding:1rem;">'
    '<div style="color:#4F7A67;font-size:0.78rem;font-weight:700;text-transform:uppercase;'
    'letter-spacing:0.06em;margin-bottom:0.5rem;">'
    '<i class="fas fa-check-circle" style="margin-right:0.4rem;"></i>Perspective</div>'
    '<div style="color:#66736A;font-size:0.84rem;line-height:1.6;">'
    'La démarche reste valide, les signaux identifiés (sédentarité, stress) '
    'sont cohérents avec la littérature clinique. '
    'Sur un dataset réel, de meilleures performances seraient attendues.</div></div>'
    '</div></div>',
    unsafe_allow_html=True
)
