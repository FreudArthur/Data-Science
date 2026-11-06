"""Éléments partagés entre le script d'entraînement et l'application.

Centralise les chemins, les variables utilisées et la construction du pipeline,
pour que l'entraînement et l'application utilisent exactement les mêmes règles.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

# --- Chemins 
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_INITIALES = DATA_DIR / "Prostate_Cancer.csv"
DATA_NOUVELLES = DATA_DIR / "nouveaux_patients.csv"   # cas confirmés ajoutés via l'app
MODELS_DIR = ROOT / "models"
MODEL_PATH = MODELS_DIR / "model.joblib"
METRICS_PATH = MODELS_DIR / "metrics.json"
HISTORY_PATH = MODELS_DIR / "historique.csv"

# --- Variables ---------------------------------------------------------------
# radius et texture sont exclues : incohérentes avec perimeter/area (voir EDA).
FEATURES = ["perimeter", "area", "smoothness", "compactness", "symmetry", "fractal_dimension"]
TARGET = "diagnosis_result"
COLONNES = ["id", TARGET, "radius", "texture", *FEATURES]

# Bornes de validation des saisies (plages observées dans les données, élargies).
BORNES = {
    "perimeter": (30.0, 250.0),
    "area": (100.0, 3000.0),
    "smoothness": (0.04, 0.20),
    "compactness": (0.01, 0.50),
    "symmetry": (0.08, 0.40),
    "fractal_dimension": (0.04, 0.12),
}

SENSIBILITE_CIBLE = 0.95


def construire_pipeline(C: float = 0.3, l1_ratio: float = 1.0) -> Pipeline:
    """log -> standardisation -> régression logistique.

    l1_ratio = 1 : pénalité L1 (Lasso, sélection de variables) ; 0 : pénalité L2 (Ridge).
    """
    return Pipeline([
        ("log", FunctionTransformer(np.log)),
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=C, l1_ratio=l1_ratio, solver="liblinear", max_iter=1000)),
    ])


def charger_donnees() -> pd.DataFrame:
    """Données initiales + cas confirmés ajoutés depuis l'application."""
    df = pd.read_csv(DATA_INITIALES)
    if DATA_NOUVELLES.exists():
        nouv = pd.read_csv(DATA_NOUVELLES)
        if len(nouv):
            df = pd.concat([df, nouv[df.columns.intersection(nouv.columns)]], ignore_index=True)
    df = df.dropna(subset=FEATURES + [TARGET])
    df = df[df[TARGET].isin(["B", "M"])]
    df = df[(df[FEATURES] > 0).all(axis=1)]          # le log exige des valeurs > 0
    return df.reset_index(drop=True)


def charger_modele():
    """Retourne (pipeline, métriques) ou (None, None) si aucun modèle n'est entraîné."""
    if not MODEL_PATH.exists():
        return None, None
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8")) if METRICS_PATH.exists() else {}
    return joblib.load(MODEL_PATH), metrics
