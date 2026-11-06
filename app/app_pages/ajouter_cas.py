"""Enregistre des cas dont le diagnostic a été confirmé (par biopsie).

Ces cas sont ajoutés à data/nouveaux_patients.csv et seront intégrés
au prochain réentraînement automatique (src/train.py).
"""

import pandas as pd
import streamlit as st

from modele import BORNES, COLONNES, DATA_INITIALES, DATA_NOUVELLES, FEATURES

st.title("Ajouter un cas confirmé")
st.write("Après une biopsie, enregistrez ici les mesures et le **diagnostic confirmé**. "
         "Ces nouveaux cas enrichissent les données utilisées au prochain réentraînement automatique.")

with st.form("nouveau_cas", clear_on_submit=True):
    diag = st.segmented_control("Diagnostic confirmé", ["Bénin", "Malin"], key="diag")
    col1, col2 = st.columns(2)
    valeurs = {}
    for i, f in enumerate(FEATURES):
        lo, hi = BORNES[f]
        with (col1 if i % 2 == 0 else col2):
            valeurs[f] = st.number_input(f, min_value=lo, max_value=hi, value=None,
                                         placeholder=f"{lo} – {hi}", key=f"cas_{f}")
    ok = st.form_submit_button("Enregistrer le cas", type="primary", icon=":material/save:")

if ok:
    manquants = [f for f, v in valeurs.items() if v is None]
    if diag is None or manquants:
        st.warning("Renseignez le diagnostic et toutes les mesures.", title="Formulaire incomplet")
    else:
        existant = pd.read_csv(DATA_NOUVELLES) if DATA_NOUVELLES.exists() else pd.DataFrame(columns=COLONNES)
        prochain_id = int(max(pd.read_csv(DATA_INITIALES)["id"].max(),
                              existant["id"].max() if len(existant) else 0)) + 1
        ligne = {"id": prochain_id, "diagnosis_result": "M" if diag == "Malin" else "B",
                 "radius": None, "texture": None, **valeurs}
        pd.DataFrame([ligne], columns=COLONNES).to_csv(
            DATA_NOUVELLES, mode="a", header=not DATA_NOUVELLES.exists(), index=False)
        st.success(f"Cas n°{prochain_id} enregistré. Il sera pris en compte au prochain réentraînement.",
                   title="Cas ajouté")

st.subheader("Cas en attente de réentraînement")
if DATA_NOUVELLES.exists():
    st.dataframe(pd.read_csv(DATA_NOUVELLES)[["id", "diagnosis_result", *FEATURES]],
                 hide_index=True, alt="Nouveaux cas confirmés")
else:
    st.info("Aucun nouveau cas pour l'instant.")
st.caption("Réentraînement : automatique (planifié) ou manuel avec `python src/train.py`.")
