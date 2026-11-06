"""Script d'entraînement / de réentraînement automatique du modèle.

Étapes :
1. charge les données initiales + les nouveaux cas confirmés (data/nouveaux_patients.csv) ;
2. choisit les hyperparamètres par validation croisée (GridSearchCV) ;
3. estime les performances par validation croisée répétée ;
4. calcule le seuil clinique garantissant une sensibilité >= 95 % ;
5. contrôle qualité : le nouveau modèle n'est déployé que s'il passe les seuils minimaux
   et ne régresse pas nettement par rapport au modèle en production ;
6. sauvegarde le modèle, ses métriques et une ligne d'historique.

Utilisation :
    python src/train.py            # réentraîne, déploie si le contrôle qualité passe
    python src/train.py --force    # déploie même si le contrôle qualité échoue
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import (GridSearchCV, RepeatedStratifiedKFold, StratifiedKFold,
                                     cross_val_predict, cross_validate)

from modele import (FEATURES, HISTORY_PATH, METRICS_PATH, MODEL_PATH, MODELS_DIR,
                    SENSIBILITE_CIBLE, TARGET, charger_donnees, charger_modele,
                    construire_pipeline)

# Contrôle qualité
AUC_MIN = 0.80              # performance minimale acceptable
REGRESSION_MAX = 0.03       # baisse d'AUC tolérée par rapport au modèle en production
SEED = 42

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("train")


def choisir_seuil(y: np.ndarray, proba: np.ndarray, cible: float) -> float:
    """Seuil le plus élevé qui garantit une sensibilité >= cible."""
    for s in np.round(np.arange(0.99, 0.0, -0.01), 2):
        pred = proba >= s
        if pred[y == 1].mean() >= cible:
            return float(s)
    return 0.01


def bilan_seuil(y: np.ndarray, proba: np.ndarray, seuil: float) -> dict:
    tn, fp, fn, tp = confusion_matrix(y, (proba >= seuil).astype(int), labels=[0, 1]).ravel()
    return {"sensibilite": tp / (tp + fn), "specificite": tn / (tn + fp),
            "vrais_positifs": int(tp), "faux_negatifs": int(fn),
            "vrais_negatifs": int(tn), "faux_positifs": int(fp)}


def entrainer() -> tuple:
    df = charger_donnees()
    X, y = df[FEATURES], (df[TARGET] == "M").astype(int).to_numpy()
    log.info("Données : %d patients (%d malins, %d bénins)", len(df), y.sum(), (1 - y).sum())

    # 1. Hyperparamètres
    grid = GridSearchCV(
        construire_pipeline(),
        {"clf__C": [0.01, 0.03, 0.1, 0.3, 1, 3, 10], "clf__l1_ratio": [0.0, 1.0]},
        cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED),
        scoring="roc_auc",
    ).fit(X, y)
    C, l1_ratio = grid.best_params_["clf__C"], grid.best_params_["clf__l1_ratio"]
    log.info("Meilleurs hyperparamètres : C=%s, pénalité=%s", C, "L1 (Lasso)" if l1_ratio == 1 else "L2 (Ridge)")

    # 2. Performances (validation croisée répétée, indépendante de la recherche ci-dessus)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=SEED + 1)
    r = cross_validate(construire_pipeline(C, l1_ratio), X, y, cv=cv,
                       scoring={"auc": "roc_auc", "accuracy": "accuracy", "sensibilite": "recall"})

    # 3. Seuil clinique sur prédictions hors-pli
    proba_oof = cross_val_predict(construire_pipeline(C, l1_ratio), X, y, method="predict_proba",
                                  cv=StratifiedKFold(5, shuffle=True, random_state=SEED))[:, 1]
    seuil = choisir_seuil(y, proba_oof, SENSIBILITE_CIBLE)

    # 4. Modèle final entraîné sur toutes les données
    modele = construire_pipeline(C, l1_ratio).fit(X, y)
    coefs = dict(zip(FEATURES, modele.named_steps["clf"].coef_[0].round(4).tolist()))

    metrics = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "n_patients": int(len(df)), "n_malins": int(y.sum()), "n_benins": int((1 - y).sum()),
        "hyperparametres": {"C": C, "penalite": "L1" if l1_ratio == 1 else "L2"},
        "auc_cv": float(r["test_auc"].mean()), "auc_cv_std": float(r["test_auc"].std()),
        "accuracy_cv": float(r["test_accuracy"].mean()),
        "sensibilite_cv_seuil_05": float(r["test_sensibilite"].mean()),
        "seuil_clinique": seuil,
        "seuil_clinique_bilan": bilan_seuil(y, proba_oof, seuil),
        "coefficients": coefs,
        "variables": FEATURES,
    }
    return modele, metrics


def controle_qualite(metrics: dict) -> tuple[bool, str]:
    if metrics["auc_cv"] < AUC_MIN:
        return False, f"AUC {metrics['auc_cv']:.3f} < minimum {AUC_MIN}"
    _, actuel = charger_modele()
    if actuel and "auc_cv" in actuel:
        baisse = actuel["auc_cv"] - metrics["auc_cv"]
        if baisse > REGRESSION_MAX:
            return False, (f"régression d'AUC de {baisse:.3f} "
                           f"({actuel['auc_cv']:.3f} -> {metrics['auc_cv']:.3f})")
    return True, "contrôle qualité réussi"


def sauvegarder(modele, metrics: dict, deploye: bool, raison: str) -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    if deploye:
        joblib.dump(modele, MODEL_PATH)
        METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    ligne = pd.DataFrame([{
        "date": metrics["date"], "n_patients": metrics["n_patients"],
        "auc_cv": round(metrics["auc_cv"], 4), "accuracy_cv": round(metrics["accuracy_cv"], 4),
        "seuil_clinique": metrics["seuil_clinique"],
        "sensibilite_seuil": round(metrics["seuil_clinique_bilan"]["sensibilite"], 4),
        "specificite_seuil": round(metrics["seuil_clinique_bilan"]["specificite"], 4),
        "deploye": deploye, "raison": raison,
    }])
    ligne.to_csv(HISTORY_PATH, mode="a", header=not HISTORY_PATH.exists(), index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="déployer même si le contrôle qualité échoue")
    args = parser.parse_args()

    modele, metrics = entrainer()
    log.info("AUC CV = %.3f ± %.3f | seuil clinique = %.2f | sensibilité = %.1f %% | spécificité = %.1f %%",
             metrics["auc_cv"], metrics["auc_cv_std"], metrics["seuil_clinique"],
             100 * metrics["seuil_clinique_bilan"]["sensibilite"],
             100 * metrics["seuil_clinique_bilan"]["specificite"])

    ok, raison = controle_qualite(metrics)
    deploye = ok or args.force
    if not ok and args.force:
        raison += " (déploiement forcé)"
    sauvegarder(modele, metrics, deploye, raison)

    if deploye:
        log.info("Nouveau modèle déployé dans %s — %s", MODEL_PATH, raison)
        return 0
    log.warning("Modèle NON déployé — %s. Le modèle en production est conservé.", raison)
    return 1


if __name__ == "__main__":
    sys.exit(main())
