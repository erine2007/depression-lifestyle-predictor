# Documentation Technique : MindTrack

## Table des matières

1. [Présentation du projet](#1-présentation-du-projet)
2. [Architecture de l'application](#2-architecture-de-lapplication)
3. [Dataset et pipeline de données](#3-dataset-et-pipeline-de-données)
4. [Choix techniques justifiés](#4-choix-techniques-justifiés)
5. [Modélisation Machine Learning](#5-modélisation-machine-learning)
6. [Application Streamlit](#6-application-streamlit)
7. [Manuel d'installation](#7-manuel-dinstallation)
8. [Déploiement](#8-déploiement)
9. [Limites et perspectives](#9-limites-et-perspectives)

---

## 1. Présentation du projet

### Problématique

> **Peut-on détecter une dépression grâce aux habitudes de vie ?**

Les habitudes quotidiennes : sommeil, activité physique, stress, temps d'écran, peuvent-elles constituer des signaux prédictifs d'un risque de dépression ? Ce projet explore cette question à travers une démarche data science complète, de l'acquisition des données jusqu'au déploiement d'une application interactive.

### Objectifs

- Acquérir et préparer un dataset sur la santé mentale et les habitudes de vie
- Réaliser une analyse exploratoire pour identifier les facteurs discriminants
- Entraîner et comparer plusieurs modèles de classification
- Déployer une application de data storytelling interactive
- Répondre honnêtement à la problématique avec les résultats obtenus

---

## 2. Architecture de l'application

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│                    Utilisateur                          │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────────────────┐
│              Application Streamlit                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Accueil  │  │  Pages   │  │   src/   │             │
│  │   .py    │  │  (1-5)   │  │  utils   │             │
│  └──────────┘  └──────────┘  │  styles  │             │
│                               └──────────┘             │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
┌───────▼────────┐          ┌────────▼───────┐
│  data/         │          │  models/       │
│  processed/    │          │  best_model.pkl│
│  *.csv         │          │  scaler.pkl    │
└────────────────┘          └────────────────┘
```

### Flux de données

```
data/raw/                    Notebooks/              data/processed/
Mental_Health_              01_acquisition    →      mental_health_
Lifestyle_Dataset.csv   →   02_cleaning       →      cleaned.csv
                            03_eda
                            04_ml_model       →      models/*.pkl
```

---

## 3. Dataset et pipeline de données

### Source des données

**Dataset :** Mental Health and Lifestyle Habits 2019-2024  
**Plateforme :** Kaggle  
**URL :** https://www.kaggle.com/datasets/atharvasoundankar/mental-health-andlifestyle-habits-2019-2024

### Description des variables

| Variable | Type | Description | Valeurs |
|----------|------|-------------|---------|
| Country | Catégorielle | Pays de résidence | 7 pays |
| Age | Numérique | Âge en années | 18 - 64 |
| Gender | Catégorielle | Genre | Male / Female / Other |
| Exercise Level | Catégorielle | Niveau d'activité physique | Low / Moderate / High |
| Diet Type | Catégorielle | Type d'alimentation | Vegetarian / Vegan / Balanced / Junk Food / Keto |
| Sleep Hours | Numérique | Heures de sommeil / nuit | 1.4 - 11.3 |
| Stress Level | Catégorielle | Niveau de stress | Low / Moderate / High |
| Work Hours per Week | Numérique | Heures de travail / semaine | 20 - 59 |
| Screen Time per Day (Hours) | Numérique | Temps d'écran / jour | 2 - 8 |
| Social Interaction Score | Numérique | Score interaction sociale | 1 - 10 |
| Happiness Score | Numérique | Score de bien-être | 1 - 10 |
| Mental Health Condition | Catégorielle | **Variable cible** | Anxiety / Depression / PTSD / Bipolar |

### Étape 1 : Acquisition (01_data_acquisition.ipynb)

- Chargement du CSV via `pandas.read_csv()`
- Vérification des dimensions : 3 000 lignes × 12 colonnes
- Identification des valeurs manquantes : 595 NaN dans `Mental Health Condition` (19.83%)
- Analyse des types de données et valeurs uniques par colonne catégorielle

### Étape 2 : Nettoyage (02_data_cleaning.ipynb)

**Traitement des doublons :**
- Détection : `df.duplicated().sum()`
- Aucun doublon détecté

**Traitement des valeurs manquantes :**
- Suppression des 595 lignes où `Mental Health Condition` est manquant
- Justification : la variable cible ne peut pas être imputée sans introduire un biais
- Dataset résultant : 2 405 lignes

**Détection et traitement des outliers (méthode IQR) :**
- Formule : bornes = [Q1 − 1.5×IQR, Q3 + 1.5×IQR]
- 12 outliers détectés sur `Sleep Hours` uniquement
- Traitement par écrêtage (clipping) plutôt que suppression pour préserver le volume de données
- Toutes les autres colonnes numériques : 0 outlier

**Sauvegarde :**
- Fichier nettoyé : `data/processed/mental_health_cleaned.csv`

### Étape 3 - EDA (03_eda.ipynb)

Analyses réalisées :
- Distribution de la variable cible → 4 classes équilibrées (~25% chacune)
- Histogrammes de toutes les variables numériques → distributions uniformes (caractéristique d'un dataset synthétique)
- Heatmap des corrélations → corrélations proches de 0 entre toutes les variables numériques
- Boxplots par condition → distributions quasi-identiques entre classes
- Tableaux croisés pour les variables catégorielles → `Exercise Level` est la variable la plus discriminante pour la dépression

**Conclusion EDA :** Le dataset est synthétique. Les variables numériques ne montrent aucune corrélation avec la variable cible. Les variables catégorielles présentent des signaux faibles mais cohérents avec la littérature clinique.

---

## 4. Choix techniques justifiés

### Langage : Python

Python est le standard de l'industrie pour la data science. Son écosystème (pandas, scikit-learn, plotly) couvre toutes les étapes du projet de façon cohérente.

### Analyse de données : Pandas + NumPy

- **Pandas** : manipulation des DataFrames, nettoyage, agrégations
- **NumPy** : opérations mathématiques, calcul des bornes IQR
- Alternative écartée : R - moins adapté pour l'intégration avec une application web

### Visualisation : Plotly + Seaborn + Matplotlib

- **Plotly** : graphiques interactifs (hover, filtres) pour l'application Streamlit
- **Seaborn + Matplotlib** : graphiques statiques dans les notebooks Jupyter
- Justification : Plotly est natif dans Streamlit et offre une meilleure UX pour l'utilisateur final

### Machine Learning : Scikit-learn

- Bibliothèque de référence pour le ML classique en Python
- Couvre tous nos besoins : preprocessing, modèles, métriques, validation croisée
- Alternative écartée : TensorFlow/PyTorch : sur-dimensionné pour une classification sur données tabulaires

### Application : Streamlit

- Framework Python-first, pas de JavaScript requis
- Déploiement simple (un fichier Python = une application)
- Support natif de Plotly et des widgets interactifs
- Alternative considérée : Dash (Plotly) : plus flexible mais plus complexe à maintenir

### Versionning : Git + GitHub

- Branches par feature (`feature/data-acquisition`, `feature/streamlit-app`...)
- Pull Requests pour merger dans `dev` puis `main`
- Simulation d'un travail en binôme via deux identités Git

---

## 5. Modélisation Machine Learning

### Préparation des features

**Encodage des variables catégorielles :**
```python
LabelEncoder()  # pour chaque variable catégorielle
```
Justification : toutes les variables catégorielles ont un nombre limité de modalités, LabelEncoder est suffisant.

**Normalisation :**
```python
StandardScaler()  # fit sur train uniquement
```
Justification : évite le data leakage (le scaler ne voit pas les données de test).

**Split train/test :**
```python
train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```
- 80% entraînement / 20% test
- `stratify=y` : proportions des classes identiques dans les deux ensembles
- `random_state=42` : reproductibilité

### Modèles comparés

| Modèle | Justification |
|--------|---------------|
| Logistic Regression | Baseline linéaire, interprétable |
| Decision Tree | Non-linéaire, interprétable via feature importance |
| Random Forest | Ensemble de Decision Trees, robuste au surapprentissage |
| Gradient Boosting | Ensemble boosting, souvent performant sur données tabulaires |

### Métriques d'évaluation

- **Accuracy** : pourcentage global de bonnes prédictions
- **F1-Score pondéré** : moyenne harmonique precision/recall, adaptée aux classes équilibrées
- **CV Accuracy (5-fold)** : métrique la plus fiable, évalue la capacité de généralisation

### Sélection du meilleur modèle

Critère : **CV Accuracy** (plus robuste que l'accuracy brute car calculée sur 5 découpages).

**Decision Tree** sélectionné avec CV Accuracy = 23.9%.

### Sauvegarde

```python
joblib.dump(best_model, "models/best_model.pkl")
joblib.dump(scaler,     "models/scaler.pkl")
joblib.dump(mapping,    "models/class_mapping.pkl")
```

Les fichiers `.pkl` sont chargés directement dans l'application Streamlit: pas de ré-entraînement à chaque lancement.

---

## 6. Application Streamlit

### Architecture multi-pages

Streamlit détecte automatiquement les fichiers dans `pages/` et les ajoute à la navigation.

```
Accueil.py          ← Page principale (set_page_config ici)
pages/
├── 01_Problème_mondial.py
├── 02_Facteurs_de_risque.py
├── 03_EDA_Interactive.py
├── 04_Résultats_ML.py
└── 05_Simulateur.py
```

### Module src/

**`utils.py`** : centralise le chargement des données avec cache :
```python
@st.cache_data      # cache les DataFrames
@st.cache_resource  # cache les modèles ML (objets lourds)
```

**`styles.py`** : centralise le CSS et les composants réutilisables :
- `load_css()` : injection du CSS global + Font Awesome
- `page_header()` : header standardisé pour chaque page
- `section_header()` : titre de section standardisé
- `insight_box()` : boîte d'observation/interprétation

### Thème

Défini dans `.streamlit/config.toml` :
```toml
primaryColor = "#4F7A67"      # Vert sauge
backgroundColor = "#F6F5F1"   # Beige crème
secondaryBackgroundColor = "#EEF2EC"
textColor = "#22372D"         # Vert forêt
```

### Choix de design

- **Pas d'emojis** → icônes Font Awesome (cohérence professionnelle)
- **Styles inline HTML** → contournement des limitations CSS de Streamlit
- **Charte nature/bien-être** → cohérente avec le sujet santé mentale

---

## 7. Manuel d'installation

### Prérequis système

- Python 3.10 ou supérieur
- Git
- 500 Mo d'espace disque

### Installation pas à pas

**Étape 1 — Cloner le repository**
```bash
git clone https://github.com/erine2007/depression-lifestyle-predictor.git
cd depression-lifestyle-predictor
```

**Étape 2 : Créer l'environnement virtuel**
```bash
# Création
python -m venv .venv

# Activation Windows
.venv\Scripts\activate

# Activation Mac / Linux
source .venv/bin/activate
```

**Étape 3 : Installer les dépendances**
```bash
pip install -r requirements.txt
```

**Étape 4 : Vérifier la structure des fichiers**

S'assurer que les fichiers suivants sont présents :
```
data/processed/mental_health_cleaned.csv
models/best_model.pkl
models/scaler.pkl
models/class_mapping.pkl
assets/favicon.png
assets/hero_illustration.webp
```

**Étape 5 — Lancer l'application**
```bash
streamlit run Accueil.py
```

L'application s'ouvre sur : `http://localhost:8501`

### Résolution des problèmes courants

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Vérifier que le venv est activé et les dépendances installées |
| `FileNotFoundError` sur les CSV | Vérifier que `data/processed/` contient le fichier nettoyé |
| `FileNotFoundError` sur les .pkl | Re-exécuter `04_ml_model.ipynb` pour régénérer les modèles |
| Page blanche Streamlit | Vider le cache : `streamlit cache clear` |

---

## 8. Déploiement

### Plateforme : Render

**Justification du choix :**
- Gratuit pour les projets personnels
- Déploiement depuis GitHub en quelques clics
- Support Python natif, pas de configuration Docker nécessaire

**Configuration (`render.yaml`) :**
```yaml
services:
  - type: web
    name: mindtrack
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run Accueil.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**URL de production :** https://depression-lifestyle-predictor.onrender.com

**Limitations du plan gratuit :**
- Mise en veille après 15 minutes d'inactivité
- Redémarrage de ~30 secondes à la première visite
- Recommandation : ouvrir l'URL 5 minutes avant toute démonstration

---

## 9. Limites et perspectives

### Limites identifiées

**Dataset synthétique :**
Le dataset Kaggle utilisé est généré algorithmiquement. Les variables numériques ne montrent aucune corrélation réelle (heatmap proche de 0), ce qui limite considérablement le pouvoir prédictif des modèles. Les distributions uniformes et l'absence de signal discriminant sont caractéristiques de données synthétiques.

**Performances des modèles :**
Tous les modèles performent autour de la baseline aléatoire (25% pour 4 classes équilibrées). Le Decision Tree ne détecte aucun cas de dépression en classification multi-classes (0/116 vrais positifs).

**Périmètre géographique limité :**
Le dataset couvre seulement 7 pays avec des distributions homogènes, pas représentatif de la diversité mondiale.

### Perspectives d'amélioration

**Données :**
- Utiliser un dataset clinique réel (ex. données IHME, PHQ-9 réels)
- Enrichir avec des données longitudinales (évolution dans le temps)
- Intégrer des données biologiques (cortisol, mélatonine...)

**Modélisation :**
- Appliquer SMOTE pour rééquilibrer les classes en binaire
- Tester XGBoost et LightGBM
- Implémenter SHAP pour une meilleure interprétabilité

**Application :**
- Ajouter une authentification utilisateur
- Permettre à l'utilisateur de sauvegarder son historique
- Intégrer des recommandations basées sur des guidelines cliniques réelles

---

*Documentation rédigée dans le cadre du projet fil rouge Bachelor 3 Data & IA | YNOV Campus Lyon 2025/2026*
