# 🧠 MindTrack : Mental Health Analytics Platform

> **Peut-on détecter une dépression grâce aux habitudes de vie ?**

Application de data storytelling explorant les liens entre habitudes de vie quotidiennes et santé mentale, combinant analyse de données, visualisation interactive et machine learning.

---

## Contexte

Projet fil rouge : Bachelor 3 Data & IA  
YNOV Campus Lyon - Promotion 2025/2026  
**Étudiante :** Erine MASSO

---

## Aperçu de l'application

L'application suit une narration en 5 étapes :

| Étape | Page | Description |
|-------|------|-------------|
| 1 | Problème mondial | Répartition des troubles mentaux par pays, genre et âge |
| 2 | Facteurs de risque | Impact du sommeil, stress, exercice et temps d'écran |
| 3 | EDA Interactive | Exploration filtrée des données avec heatmap et scatter plots |
| 4 | Résultats ML | Comparaison de 4 modèles et focus sur la détection de la dépression |
| 5 | Simulateur | Estimation personnalisée du risque de dépression |

---

## Stack technique

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## Structure du projet

```
depression-lifestyle-predictor/
│
├── Accueil.py                        ← Point d'entrée Streamlit
├── requirements.txt                  ← Dépendances Python
├── render.yaml                       ← Configuration déploiement Render
│
├── pages/                            ← Pages de l'application
│   ├── 01_Problème_mondial.py
│   ├── 02_Facteurs_de_risque.py
│   ├── 03_EDA_Interactive.py
│   ├── 04_Résultats_ML.py
│   └── 05_Simulateur.py
│
├── src/                              ← Modules Python
│   ├── utils.py                      ← Chargement des données
│   └── styles.py                     ← CSS et composants UI
│
├── data/
│   ├── raw/                          ← Données brutes (Kaggle)
│   └── processed/                    ← Données nettoyées
│
├── models/                           ← Modèles ML sauvegardés
│   ├── best_model.pkl                ← Decision Tree Classifier
│   ├── scaler.pkl                    ← StandardScaler
│   └── class_mapping.pkl             ← Mapping des classes
│
├── notebooks/                        ← Jupyter Notebooks
│   ├── 01_data_acquisition.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_ml_model.ipynb
│
├── assets/                           ← Images et favicon
└── .streamlit/
    └── config.toml                   ← Configuration du thème
```

---

## Installation locale

### Prérequis

- Python 3.10+
- Git

### Étapes

**1. Cloner le repository**
```bash
git clone https://github.com/erine2007/depression-lifestyle-predictor.git
cd depression-lifestyle-predictor
```

**2. Créer un environnement virtuel**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Lancer l'application**
```bash
streamlit run Accueil.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

---

## Dataset

**Source :** [Kaggle - Mental Health and Lifestyle Habits 2019-2024](https://www.kaggle.com/datasets/atharvasoundankar/mental-health-andlifestyle-habits-2019-2024/data)

| Caractéristique | Détail |
|----------------|--------|
| Lignes | 3 000 (2 405 après nettoyage) |
| Colonnes | 12 |
| Variable cible | Mental Health Condition (4 classes) |
| Type | Dataset synthétique |

**Variables principales :**
- `Sleep Hours` : Heures de sommeil par nuit
- `Stress Level` : Niveau de stress (Low / Moderate / High)
- `Exercise Level` : Niveau d'activité physique
- `Screen Time per Day (Hours)` : Temps d'écran quotidien
- `Social Interaction Score` : Score d'interaction sociale (1-10)
- `Happiness Score` : Score de bien-être (1-10)
- `Mental Health Condition` : Condition mentale (Anxiety / Depression / PTSD / Bipolar)

---

## Pipeline de données

```
Données brutes (Kaggle)
        ↓
01_data_acquisition.ipynb    → Chargement et exploration initiale
        ↓
02_data_cleaning.ipynb       → Nettoyage (NaN, doublons, outliers IQR)
        ↓
03_eda.ipynb                 → Analyse exploratoire et visualisations
        ↓
04_ml_model.ipynb            → Entraînement et évaluation des modèles
        ↓
models/best_model.pkl        → Modèle sauvegardé (Decision Tree)
        ↓
Application Streamlit        → Visualisation et simulateur interactif
```

---

## Résultats ML

### Classification multi-classes (4 conditions)

| Modèle | Accuracy | F1-Score | CV Accuracy |
|--------|----------|----------|-------------|
| Logistic Regression | 28.3% | 27.2% | 23.6% |
| **Decision Tree** ✓ | 23.1% | 22.9% | **23.9%** |
| Random Forest | 24.3% | 24.3% | 23.4% |
| Gradient Boosting | 24.3% | 24.1% | 23.9% |

> Baseline aléatoire : 25% (4 classes équilibrées)

### Focus dépression : Classification binaire

| Modèle | Accuracy | F1-Score Dépression |
|--------|----------|---------------------|
| Logistic Regression | 75.9% | 0.0% |
| **Decision Tree** | 62.2% | **24.8%** |
| Random Forest | 75.5% | 0.0% |
| Gradient Boosting | 74.2% | 1.6% |

### Réponse à la problématique

Les modèles ne parviennent pas à détecter fiablement la dépression à partir des habitudes de vie sur ce dataset synthétique. Les performances restent proches du hasard, ce qui s'explique par l'absence de corrélations réelles entre variables. La démarche reste valide, les signaux identifiés (sédentarité, stress élevé) sont cohérents avec la littérature clinique.

---

## Déploiement

L'application est déployée sur Render :  
🔗 **[mindtrack.onrender.com](https://depression-lifestyle-predictor.onrender.com)**

> Le plan gratuit Render met l'app en veille après 15 min d'inactivité. Ouvrir le lien quelques minutes avant la démonstration.

---

## Disclaimer

Ce projet est réalisé dans un cadre pédagogique. Le dataset utilisé est synthétique, les résultats sont illustratifs et ne constituent pas des conclusions cliniques. Cette application ne remplace en aucun cas un avis médical professionnel.
