"""Tests de l'application (sans navigateur) — lancer avec : python -m pytest tests"""

import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
PAGES = ROOT / "app" / "app_pages"


def _run(page: str) -> AppTest:
    at = AppTest.from_file(str(PAGES / page), default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def test_prediction_benin():
    at = _run("prediction.py")
    for f, v in {"in_perimeter": 60, "in_area": 280, "in_compactness": 0.05}.items():
        at.number_input(key=f).set_value(v)
    at.button[0].click().run()
    assert not at.exception
    assert any("évitable" in s.title for s in at.success)


def test_prediction_malin():
    at = _run("prediction.py")
    for f, v in {"in_perimeter": 140, "in_area": 1300, "in_compactness": 0.25}.items():
        at.number_input(key=f).set_value(v)
    at.button[0].click().run()
    assert not at.exception
    assert any("recommandée" in e.title for e in at.error)


def test_performances():
    at = _run("performances.py")
    assert len(at.metric) == 4


def test_ajouter_cas_incomplet():
    at = _run("ajouter_cas.py")
    at.button[0].click().run()
    assert not at.exception
    assert len(at.warning) == 1
