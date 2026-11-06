import pandas as pd
import streamlit as st

from modele import BORNES, FEATURES, MODEL_PATH, charger_modele

LIBELLES = {
    "perimeter": ("Périmètre du noyau", 1.0, "%.0f"),
    "area": ("Aire du noyau", 1.0, "%.0f"),
    "smoothness": ("Régularité du contour (smoothness)", 0.001, "%.3f"),
    "compactness": ("Compacité (compactness)", 0.001, "%.3f"),
    "symmetry": ("Symétrie", 0.001, "%.3f"),
    "fractal_dimension": ("Dimension fractale", 0.001, "%.3f"),
}
# Valeurs par défaut : médianes du jeu de données.
DEFAUTS = {"perimeter": 94.0, "area": 644.0, "smoothness": 0.102,
           "compactness": 0.118, "symmetry": 0.190, "fractal_dimension": 0.063}


@st.cache_resource
def modele_en_cache(_version: float):
    """Recharge le modèle quand le fichier change (la version est sa date de modification)."""
    return charger_modele()


def version_modele() -> float:
    return MODEL_PATH.stat().st_mtime if MODEL_PATH.exists() else 0.0


st.title("Faut-il faire une biopsie ?")
st.write("Saisissez les mesures du noyau cellulaire issues de l'analyse d'image du prélèvement. "
         "Le modèle estime la probabilité que la tumeur soit **maligne**.")

modele, metrics = modele_en_cache(version_modele())
if modele is None:
    st.error("Lancez d'abord l'entraînement : `python src/train.py`.", title="Aucun modèle entraîné")
    st.stop()

seuil = metrics["seuil_clinique"]

with st.form("saisie"):
    col1, col2 = st.columns(2)
    valeurs = {}
    for i, f in enumerate(FEATURES):
        label, step, fmt = LIBELLES[f]
        lo, hi = BORNES[f]
        with (col1 if i % 2 == 0 else col2):
            valeurs[f] = st.number_input(label, min_value=lo, max_value=hi, value=DEFAUTS[f],
                                         step=step, format=fmt, key=f"in_{f}")
    envoye = st.form_submit_button("Estimer le risque", type="primary",
                                   icon=":material/analytics:", width="stretch")

if envoye:
    X = pd.DataFrame([valeurs])[FEATURES]
    proba = float(modele.predict_proba(X)[0, 1])
    biopsie = proba >= seuil

    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.metric("Probabilité de malignité", f"{proba:.0%}")
        c2.metric("Seuil de décision", f"{seuil:.0%}",
                  help="Seuil choisi pour détecter au moins 95 % des cancers (validation croisée).")
        st.progress(proba, text=f"Risque estimé : {proba:.0%}")

        if biopsie:
            st.error("La probabilité dépasse le seuil clinique. Une biopsie de confirmation est conseillée.",
                     title="Biopsie recommandée", icon=":material/warning:")
        else:
            st.success("La probabilité est sous le seuil clinique : une surveillance peut être envisagée "
                       "plutôt qu'une biopsie immédiate, après avis médical.",
                       title="Biopsie probablement évitable", icon=":material/check_circle:")

    # Contribution de chaque variable (régression logistique : coefficient × valeur standardisée)
    clf = modele.named_steps["clf"]
    z = modele[:-1].transform(X)[0]
    contrib = pd.DataFrame({"variable": FEATURES, "contribution": clf.coef_[0] * z})
    contrib = contrib[contrib["contribution"] != 0]
    if len(contrib):
        st.subheader("Ce qui influence cette estimation")
        st.caption("Valeur positive = pousse vers « malin » ; négative = pousse vers « bénin ». "
                   "Les variables écartées par le modèle (coefficient nul) ne sont pas affichées.")
        st.bar_chart(contrib, x="variable", y="contribution", horizontal=True,
                     alt="Contribution de chaque variable à la prédiction")

st.caption(f"Modèle entraîné le {metrics['date']} sur {metrics['n_patients']} patients — "
           f"AUC en validation croisée : {metrics['auc_cv']:.2f}.")
