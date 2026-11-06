import pandas as pd
import streamlit as st

from modele import HISTORY_PATH, charger_modele

st.title("Performances du modèle")

modele, m = charger_modele()
if modele is None:
    st.error("Lancez d'abord `python src/train.py`.", title="Aucun modèle entraîné")
    st.stop()

b = m["seuil_clinique_bilan"]
st.write(f"Régression logistique (pénalité {m['hyperparametres']['penalite']}, "
         f"C = {m['hyperparametres']['C']}) entraînée le **{m['date']}** sur "
         f"**{m['n_patients']} patients** ({m['n_malins']} malins, {m['n_benins']} bénins).")

with st.container(horizontal=True):
    st.metric("AUC (validation croisée)", f"{m['auc_cv']:.3f}", border=True,
              help=f"Écart-type entre plis : {m['auc_cv_std']:.3f}")
    st.metric("Seuil clinique", f"{m['seuil_clinique']:.2f}", border=True)
    st.metric("Sensibilité au seuil", f"{b['sensibilite']:.0%}", border=True,
              help="Part des cancers détectés.")
    st.metric("Spécificité au seuil", f"{b['specificite']:.0%}", border=True,
              help="Part des biopsies inutiles évitées chez les patients bénins.")

st.subheader("Au seuil clinique (prédictions hors-pli)")
st.table(pd.DataFrame(
    {"Prédit bénin (pas de biopsie)": [b["vrais_negatifs"], b["faux_negatifs"]],
     "Prédit malin (biopsie)": [b["faux_positifs"], b["vrais_positifs"]]},
    index=["Réellement bénin", "Réellement malin"]))
st.caption(f"{b['vrais_negatifs']} biopsies inutiles évitées sur {b['vrais_negatifs'] + b['faux_positifs']} "
           f"patients bénins ; {b['faux_negatifs']} cancer(s) non détecté(s) sur "
           f"{b['vrais_positifs'] + b['faux_negatifs']}.")

st.subheader("Variables utilisées par le modèle")
coefs = pd.DataFrame({"variable": list(m["coefficients"]), "coefficient": list(m["coefficients"].values())})
st.bar_chart(coefs, x="variable", y="coefficient", horizontal=True,
             alt="Coefficients de la régression logistique")
st.caption("Un coefficient nul signifie que la pénalité Lasso a écarté la variable (redondante).")

st.subheader("Historique des réentraînements")
if HISTORY_PATH.exists():
    hist = pd.read_csv(HISTORY_PATH)
    st.dataframe(hist.iloc[::-1], hide_index=True, alt="Historique des réentraînements",
                 column_config={
                     "deploye": st.column_config.CheckboxColumn("Déployé"),
                     "auc_cv": st.column_config.NumberColumn("AUC CV", format="%.3f"),
                     "sensibilite_seuil": st.column_config.NumberColumn("Sensibilité", format="percent"),
                     "specificite_seuil": st.column_config.NumberColumn("Spécificité", format="percent"),
                 })
    if len(hist) > 1:
        st.line_chart(hist, x="date", y="auc_cv", alt="Évolution de l'AUC au fil des réentraînements")
else:
    st.info("Aucun historique pour l'instant.")
