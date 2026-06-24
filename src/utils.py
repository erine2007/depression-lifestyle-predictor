import pandas as pd
import joblib
import streamlit as st
import os

@st.cache_data
def load_data():
    """
    Charge le dataset nettoyé depuis data/processed/.
    Mis en cache par Streamlit pour éviter les rechargements inutiles.
    """
    path = os.path.join("data", "processed", "mental_health_cleaned.csv")
    return pd.read_csv(path)

@st.cache_resource
def load_model():
    """
    Charge le modèle ML sauvegardé.
    cache_resource : pour les objets lourds non-sérialisables (modèles ML)
    """
    model   = joblib.load(os.path.join("models", "best_model.pkl"))
    scaler  = joblib.load(os.path.join("models", "scaler.pkl"))
    mapping = joblib.load(os.path.join("models", "class_mapping.pkl"))
    return model, scaler, mapping