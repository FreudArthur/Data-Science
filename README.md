# Prédiction de la malignité d'une tumeur de la prostate

**Projet intégrateur — Science des Données (IFRI)** · Enseignant : Msc. Osias Noël TOSSOU
Groupe 5 : BOKOSSA Freud Arthur, FAKEYE Grace, AHOUANDJINOU Jean Marie, OKPEICHA Jaurès

> **Problématique :** peut-on prédire si une tumeur de la prostate est bénigne ou maligne à partir de mesures
> cellulaires, afin d'**éviter des biopsies inutiles** sans rater de cancer ?

Le projet couvre tout le cycle : analyse exploratoire → modélisation → application web Streamlit →
réentraînement automatique planifié.

## Résultats en bref

| | Valeur |
|---|---|
| Modèle | Régression logistique pénalisée L1 (Lasso), variables passées au log et standardisées |
| Variables réellement utilisées | `area` (taille du noyau) et `compactness` (irrégularité de la forme) |
| AUC (validation croisée) | ≈ 0,91 |
| Seuil clinique | choisi pour détecter **≥ 95 % des cancers** |
| Biopsies inutiles évitées | environ **2 sur 3** chez les patients bénins |

⚠️ Outil pédagogique d'aide à la décision : il ne remplace pas l'avis d'un médecin.

## Structure du dépôt

```
.
├── app/                         Application Streamlit
│   ├── streamlit_app.py         Point d'entrée (navigation)
│   └── app_pages/
│       ├── prediction.py        Saisie des mesures → probabilité + recommandation
│       ├── performances.py      Métriques du modèle + historique des réentraînements
│       └── ajouter_cas.py       Enregistrement de cas confirmés pour le réentraînement
├── src/
│   ├── modele.py                Chemins, variables, pipeline (partagés app / entraînement)
│   └── train.py                 Script d'entraînement / réentraînement avec contrôle qualité
├── data/
│   ├── Prostate_Cancer.csv      Dataset principal (Kaggle, 100 patients)
│   ├── prostate.csv             Dataset Stamey (1989), étudié puis écarté (voir EDA)
│   └── nouveaux_patients.csv    Créé par l'application : cas confirmés en attente
├── models/
│   ├── model.joblib             Modèle en production
│   ├── metrics.json             Ses performances et son seuil clinique
│   └── historique.csv           Historique de tous les réentraînements
├── Jean-Marie/
│   └── Revue_litterature_cancer_de_la_prostate.pdf   Revue de littérature (contexte clinique, épidémiologie, état de l'art)
├── notebook/
│   ├── notebook.ipynb           EDA du dataset Stamey (et raison de son abandon)
│   ├── eda_prostate_cancer.ipynb   EDA du dataset retenu
│   └── modelisation.ipynb       Comparaison des modèles, réglage, seuil clinique, interprétation
├── tests/test_app.py            Tests de l'application (sans navigateur)
├── .github/workflows/retrain.yml   Réentraînement automatique planifié (GitHub Actions)
└── requirements.txt
```

## Installation

Prérequis : Python 3.12.

```bash
git clone https://github.com/FreudArthur/Data-Science.git
cd Data-Science

python -m venv .venv
# Windows :
.venv\Scripts\activate
# Linux / macOS :
source .venv/bin/activate

pip install -r requirements.txt
```

## Utilisation

Toutes les commandes se lancent **depuis la racine du projet**.

### 1. Entraîner le modèle

```bash
python src/train.py
```

Un modèle déjà entraîné est fourni dans `models/`, cette étape est donc facultative au premier lancement.

### 2. Lancer l'application

```bash
streamlit run app/streamlit_app.py
```

Puis ouvrir http://localhost:8501. L'application contient trois pages :

- **Prédiction** : saisir les 6 mesures du noyau cellulaire. L'application affiche la probabilité de
  malignité, la recommandation (« biopsie recommandée » ou « biopsie probablement évitable ») et les
  variables qui ont le plus pesé.
- **Performances du modèle** : AUC, seuil clinique, sensibilité / spécificité, matrice de confusion,
  coefficients et historique des réentraînements.
- **Ajouter un cas confirmé** : après une biopsie, enregistrer les mesures et le diagnostic réel.
  Ces cas sont intégrés au prochain réentraînement.

### 3. Explorer les analyses

```bash
jupyter notebook notebook/
```

Ordre de lecture conseillé : `notebook.ipynb` → `eda_prostate_cancer.ipynb` → `modelisation.ipynb`.

## Réentraînement automatique

### Ce que fait `src/train.py`

1. Charge `data/Prostate_Cancer.csv` **et** les cas confirmés de `data/nouveaux_patients.csv`.
2. Choisit les hyperparamètres (force `C` et type de pénalité L1/L2) par validation croisée.
3. Estime les performances par validation croisée stratifiée répétée (5 plis × 10).
4. Calcule le **seuil clinique** : le seuil le plus élevé qui garantit une sensibilité ≥ 95 %.
5. **Contrôle qualité** : le nouveau modèle n'est mis en production que si
   - son AUC est ≥ 0,80, et
   - elle ne baisse pas de plus de 0,03 par rapport au modèle actuel.

   Sinon, le modèle actuel est conservé (`python src/train.py --force` pour passer outre).
6. Sauvegarde le modèle, ses métriques et ajoute une ligne à `models/historique.csv`.

L'application recharge automatiquement le nouveau modèle, sans redémarrage.

### Planification

**GitHub Actions** ([.github/workflows/retrain.yml](.github/workflows/retrain.yml)) : chaque **lundi à 03:00 UTC**,
le workflow réentraîne le modèle, vérifie que l'application démarre, puis enregistre le modèle et
l'historique dans le dépôt. On peut aussi le lancer à la main : onglet *Actions* → *Réentraînement du
modèle* → *Run workflow*.

Pour un serveur local, il y a deux équivalents :

- **Linux (cron)** : `crontab -e` puis ajouter
  ```
  0 3 * * 1 cd /chemin/vers/Data-Science && .venv/bin/python src/train.py >> models/train.log 2>&1
  ```
- **Windows (Planificateur de tâches)** :
  ```
  schtasks /create /tn "Reentrainement prostate" /sc weekly /d MON /st 03:00 /tr "cmd /c cd /d C:\chemin\vers\Data-Science && .venv\Scripts\python.exe src\train.py"
  ```

## Tests

```bash
pip install pytest
python -m pytest tests
```

Les tests vérifient que les trois pages se chargent, qu'un cas bénin et un cas malin typiques donnent
la bonne recommandation, et que le formulaire refuse une saisie incomplète.

## Données et limites

- Le dataset `Prostate_Cancer.csv` (Kaggle) contient 100 patients. Ses variables sont celles du dataset
  *Breast Cancer Wisconsin* (UCI) : il en est très probablement une version dérivée.
- `radius` et `texture` sont **exclues**. Elles sont incohérentes avec `perimeter` et `area`
  (corrélation de −0,24 au lieu de ≈ +1) et semblent aléatoires (voir l'EDA).
- Avec 100 patients, les métriques ont une incertitude de plusieurs points. Il faudrait une validation
  externe sur une cohorte plus grande, idéalement hospitalière et africaine.
