"""Point d'entrée de l'application Streamlit.

Lancement (depuis la racine du projet) :
    streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Rendre le module partagé src/modele.py importable depuis les pages.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

st.set_page_config(page_title="Aide à la décision — biopsie prostate",
                   page_icon=":material/health_and_safety:", layout="centered")

page = st.navigation([
    st.Page("app_pages/prediction.py", title="Prédiction", icon=":material/stethoscope:", default=True),
    st.Page("app_pages/performances.py", title="Performances du modèle", icon=":material/monitoring:"),
    st.Page("app_pages/ajouter_cas.py", title="Ajouter un cas confirmé", icon=":material/add_circle:"),
])

with st.sidebar:
    st.caption("Projet Data Science — IFRI.  ")

page.run()
