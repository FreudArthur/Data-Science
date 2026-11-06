# Prompts pour générer les livrables

Deux prompts autonomes, à copier-coller tels quels dans un assistant IA (Claude, ChatGPT…).
Ils contiennent **tous les résultats réels** du projet pour que l'IA n'invente rien.

Avant de les utiliser, remplacer :

- les `[À COMPLÉTER]` restants : URL d'hébergement si l'application est mise en ligne ;

Joindre aussi les captures d'écran de l'application Streamlit (pages Prédiction, Performances, Ajouter un cas).

Joindre aussi le PDF de la revue de littérature de Jean-Marie (`Jean-Marie/Revue_litterature_cancer_de_la_prostate.pdf`) aux deux prompts : l'IA pourra y reprendre les chiffres, les notions et les références.

Conseil : joindre aussi les captures des graphiques des notebooks (`eda_prostate_cancer.ipynb`, `modelisation.ipynb`) pour qu'ils soient insérés dans les documents.

---

## PROMPT 1 — Rapport écrit (PDF)

```
Tu es un data scientist qui rédige le rapport final d'un projet universitaire de Science des Données (Master, IFRI). Rédige un rapport complet, en français, structuré et rigoureux, à exporter en PDF (fournis-le en Markdown structuré ou en document Word prêt à exporter).

RÈGLES IMPORTANTES
- N'invente AUCUN chiffre ni résultat : utilise uniquement les données fournies ci-dessous.
- Pour le contexte clinique et épidémiologique, utilise UNIQUEMENT les chiffres de la revue de littérature ci-dessous, avec leur référence [n]. Si un chiffre manque, écris [À SOURCER : ...] au lieu d'en inventer un.
- Là où un graphique est pertinent, insère un emplacement du type « [Figure X : description — capture du notebook] ».
- Ton professionnel, phrases claires, vocabulaire technique expliqué brièvement.
- Longueur visée : 15 à 25 pages.

INFORMATIONS GÉNÉRALES
- Titre : Prédiction de la malignité d'une tumeur de la prostate pour réduire les biopsies inutiles
- Cours : Travaux Pratiques – Science des Données, projet intégrateur « De la donnée brute au déploiement »
- Enseignant : Msc. Osias Noël TOSSOU
- Groupe  5 :
- Memebrs Groupe :  BOKOSSA Freud Arthur, FAKEYE Grace, AHOUANDJINOU Jean Marie , OKPEICHA Jaurès
- Dépôt GitHub : https://github.com/FreudArthur/Data-Science 

STRUCTURE IMPOSÉE
0. Page de garde, résumé (10 lignes), table des matières
1. Problématique métier et revue de littérature (contexte clinique, épidémiologie mondiale et africaine, état de l'art en science des données)
2. Analyse exploratoire des données (EDA)
3. Modélisation
4. Déploiement et automatisation
5. Résultats et limites
6. Conclusion et perspectives
Annexes : description des variables, structure du dépôt GitHub, glossaire (PSA, Gleason/ISUP, csPCa, PI-RADS…)
Références : liste numérotée reprise de la revue de littérature (seulement celles citées)

=== 1. PROBLÉMATIQUE MÉTIER ===
- Question : peut-on prédire si une tumeur de la prostate est bénigne ou maligne à partir de mesures cliniques, afin d'éviter des biopsies inutiles ?
- Contexte : santé, contexte africain. 2e cancer le plus fréquent chez l'homme dans le monde, derrière le poumon ; en Afrique, 7 % des cas mais 14 % des décès, ratio décès/cas de 54 %, 45 % des diagnostics au stade IV (détails et références dans le bloc REVUE DE LITTÉRATURE). La biopsie est un examen invasif, coûteux, avec des risques (infection, saignement), et l'accès aux anatomopathologistes est limité dans de nombreux pays africains.
- Acteurs : patients, urologues, anatomopathologistes, hôpitaux / centres de santé, ministère de la Santé, assurances.
- Enjeux : ne pas rater de cancer (sensibilité élevée) tout en évitant un maximum de biopsies inutiles chez les patients bénins (spécificité) → réduction des coûts, du risque pour le patient et de la charge des laboratoires.
- Formulation Data Science : classification binaire supervisée (cible : M = malin / B = bénin).
- Métrique métier : sensibilité ≥ 95 % imposée, puis maximisation de la spécificité (= part des biopsies inutiles évitées). Métrique de comparaison : AUC ROC.

=== REVUE DE LITTÉRATURE (rédigée par Jean-Marie — fichier Jean-Marie/Revue_litterature_cancer_de_la_prostate.pdf, joint) ===
Revue narrative (non systématique), 28 références, chiffres GLOBOCAN 2022. Si le PDF est joint, appuie-toi dessus en priorité ; sinon utilise les éléments ci-dessous. Cite les sources par leur numéro [n] tel qu'il figure dans la revue, et reprends la liste des références utilisées en fin de rapport.

Épidémiologie :
- Monde 2022 : 1 467 854 nouveaux cas (2e cancer masculin derrière le poumon — attention, la §1 de la revue dit « le plus fréquent », c'est une erreur : retenir 2e ; 4e tous cancers), 397 430 décès ; taux standardisés : incidence 29,4 / 100 000, mortalité 7,3 / 100 000 [1,2].
- Afrique 2022 : 103 050 cas (7 % des cas mondiaux) mais 55 744 décès (14 % des décès) → ratio décès/cas 54,1 %, contre 24,4 % en Europe et 15,5 % en Amérique du Nord [2].
- Afrique subsaharienne (1 406 patients, 12 registres, 10 pays, 2005-2015) : 45,2 % de diagnostics au stade IV, 31,2 % au stade III, seulement 23,6 % aux stades I-II ; survie relative à 5 ans 60,0 % [19]. États-Unis : 69,5 % diagnostiqués à un stade localisé [26,27].
- À taux constants, le nombre annuel de cas en Afrique doublera en une vingtaine d'années (vieillissement, croissance démographique) [19].
- Message clé : en Afrique, le problème n'est pas l'incidence mais le retard au diagnostic, lié à l'accès au dépistage, à l'imagerie et à la biopsie. Pas de programme de dépistage organisé dans la plupart des pays [19,20]. Les chiffres africains sont probablement sous-estimés (registres partiels).

Notions cliniques utiles :
- Facteurs de risque établis : âge (premier facteur), ascendance africaine (incidence plus élevée, mortalité 2 à 5 fois supérieure selon les sources américaines [21,23]), antécédents familiaux (BRCA2, HOXB13), facteurs métaboliques (association sans causalité démontrée).
- PSA : marqueur d'organe, pas de cancer. Au seuil de 4 ng/mL, il détecte environ 91 % des cancers [12], mais sa spécificité est faible (0,02 à 0,63 selon les études [11]) → beaucoup de biopsies inutiles. D'où l'intérêt des modèles multivariés.
- Parcours diagnostique : suspicion (PSA, toucher rectal) → IRM multiparamétrique (score PI-RADS) → biopsie → anatomopathologie (score de Gleason / groupes ISUP) [14,5].
- Cancer cliniquement significatif (csPCa) : ISUP ≥ 2 (Gleason ≥ 7) et/ou volume > 0,5 cm³ et/ou extension extraprostatique [14].
- Dépistage : ERSPC (182 000 hommes) → mortalité −20 % [9] ; PLCO → pas de bénéfice, mais bras contrôle contaminé [10]. Coût : surdiagnostic (20 à 50 % des cancers dépistés selon les modèles), biopsies inutiles et complications.
- Gleason / ISUP (5 groupes de grade, réforme 2014) [5] ; TNM ; classification de D'Amico (faible / intermédiaire / haut risque) [7] ; nomogramme de Kattan (précision interne 77-81 %, performance variable en validation externe) [15].

Science des données et cancer de la prostate (état de l'art) :
- Trois familles de travaux : modèles tabulaires clinico-biologiques (les plus proches de notre projet), imagerie IRM par apprentissage profond [25], approches multimodales / omiques.
- Les méta-analyses rapportent des AUC souvent > 0,75-0,80, mais avec un risque de biais élevé, une validation externe rare et une faible reproductibilité [24].
- Leçon méthodologique : les modèles les plus utiles ne sont pas les plus complexes ; une régression bien conduite (baseline, validation croisée honnête, discussion des limites) vaut mieux qu'un modèle exotique non validé.

Points de la revue à utiliser pour JUSTIFIER nos choix (fais explicitement le lien dans le rapport) :
- PSA peu spécifique + biopsies inutiles → justifie notre objectif (éviter les biopsies inutiles) et notre métrique (sensibilité ≥ 95 % puis spécificité maximale).
- Contexte africain : IRM et biopsie sont des goulots d'étranglement ; un modèle « frugal » doit utiliser peu de variables peu coûteuses, être interprétable et fonctionner simplement (§12.4) → justifie notre modèle final à 2 variables (régression logistique Lasso) et l'application légère.
- « Les modèles les plus utiles ne sont pas les plus complexes » (§13.3) → cohérent avec notre comparaison de modèles (les modèles complexes n'apportent rien sur 100 patients).
- « Un modèle hérite de la prévalence de sa population d'entraînement et ne se transpose pas sans recalibration » (§5.2) et la validation externe du nomogramme de Kattan (§11.2) → justifient nos limites et la boucle de réentraînement de l'application (recalibrer sur des cas locaux confirmés).
- « Un modèle entraîné sur une cohorte européenne/américaine n'est pas transposable, et l'affirmer sans le vérifier est une faute méthodologique » (§12.3) → à citer dans les limites.

Nuance importante à écrire dans les limites (§15 de la revue) : le problème clinique central est de distinguer cancer indolent et cancer agressif, pas seulement de détecter le cancer. Notre modèle prédit bénin / malin : c'est une première étape de tri, à compléter par une évaluation de l'agressivité (Gleason / ISUP).

=== DÉMARCHE DE CHOIX DES DONNÉES (à raconter dans le rapport, c'est un point fort) ===
- Premier dataset étudié : « Prostate » de Stamey et al. (1989), 97 patients, variables lcavol, lweight, age, lbph, svi, lcp, gleason, pgg45, lpsa (log du PSA), train.
  - EDA réalisée : aucune valeur manquante, lpsa fortement corrélé à lcavol (r = 0,73), puis svi (0,57) et lcp (0,55) ; zéros codés en log(0,25) dans lbph (44 %) et lcp (46 %) ; pgg45 = 0 pour 36 % ; multicolinéarité gleason/pgg45 ; split train/test d'origine représentatif (tests KS p > 0,29).
  - Problème bloquant : les 97 patients ont TOUS un cancer (prostatectomie radicale) → pas de variable bénin/malin, donc inadapté à la problématique. De plus, gleason, svi, lcp sont mesurés sur la pièce opératoire, donc indisponibles avant biopsie.
  - La revue de littérature confirme cette analyse (§14.3) : chronologie inversée (variables mesurées après le PSA), effectif minuscule, cohorte américaine des années 1980, donc pas de prétention clinique possible.
  - Décision : changement de dataset.
- Dataset retenu : « Prostate_Cancer.csv » (Kaggle), qui contient la cible bénin/malin.

=== 2. EDA (dataset retenu) ===
Description :
- Source : Kaggle (Prostate_Cancer.csv). 100 patients, 10 colonnes.
- Variables : id ; diagnosis_result (cible M/B) ; radius, texture, perimeter, area (entiers) ; smoothness, compactness, symmetry, fractal_dimension (continues). Ce sont des mesures de noyaux cellulaires sur image de prélèvement.
- Remarque de provenance : ces variables sont exactement celles du dataset « Breast Cancer Wisconsin » (UCI) ; ce fichier en est très probablement une version dérivée, la provenance « prostate » n'est pas documentée.

Qualité :
- 0 valeur manquante, 0 doublon, id unique de 1 à 100.
- Cible : 62 M (62 %) / 38 B (38 %) → déséquilibre modéré ; un modèle qui prédit toujours M a 62 % d'accuracy.
- ANOMALIE 1 : radius et texture incohérentes. Par géométrie, le rayon devrait être corrélé à ~+1 avec perimeter/2π ; or corr(radius, perimeter/2π) = −0,24 et corr(radius, √(area/π)) = −0,25, alors que corr(perimeter, √area) = +0,98 (cohérent). radius = entiers de 9 à 25 de distribution uniforme (test KS d'uniformité p = 0,47) ; texture = entiers de 11 à 27, quasi uniforme (p = 0,04), corrélée à aucune variable (|r| < 0,25). → Colonnes jugées corrompues/aléatoires, exclues.
- ANOMALIE 2 : fichier trié selon la cible. Proportion de malins par tranche d'id : 1–25 : 76 % ; 26–50 : 84 % ; 51–75 : 40 % ; 76–100 : 48 %. → Mélange + stratification obligatoires, id exclu.
- Valeurs aberrantes (|z| > 3) : 5 patients (ids 4, 26, 72, 79, 83), dont 4 malins → cas réels, conservés.

Statistiques et distributions :
- Asymétrie à droite : area (0,84), compactness (0,98), symmetry (0,98), fractal_dimension (1,15) → transformation log pertinente. Seule smoothness est normale (Shapiro p = 0,17).
- Moyennes : perimeter 96,8 ; area 702,9 ; compactness 0,127 ; smoothness 0,103 ; symmetry 0,193 ; fractal_dimension 0,065.

Bénin vs malin (moyennes, AUC univariée, test de Mann-Whitney) :
- perimeter : B 78,5 vs M 108,0 (+37 %), AUC 0,89, p = 3,9e-11
- area : B 474 vs M 843 (+78 %), AUC 0,88, p = 1,4e-10
- compactness : B 0,087 vs M 0,151 (+74 %), AUC 0,84, p = 1,0e-08
- symmetry : AUC 0,65, p = 0,013 ; smoothness : AUC 0,63, p = 0,03
- texture : AUC 0,54 (non significatif) ; fractal_dimension : AUC 0,50 (p = 0,97)
- radius : AUC 0,40 (incohérent : suggérerait des noyaux malins plus petits, en contradiction avec perimeter/area)

Corrélations :
- perimeter–area r = 0,98 (redondance).
- Bloc « forme » : compactness–symmetry 0,68, compactness–fractal_dimension 0,65, symmetry–fractal_dimension 0,57.
- Taille vs forme moyennement liées (perimeter–compactness 0,53 ; area–symmetry 0,11) → informations en partie complémentaires.
- ACP sur les 6 variables fiables : PC1 ≈ axe global, PC2 oppose taille (perimeter, area) et forme (fractal_dimension, symmetry) ; bonne séparation B/M avec une zone de chevauchement.

Enseignements métier :
- Les tumeurs malignes ont des noyaux plus GRANDS et plus IRRÉGULIERS : la taille et la forme sont les deux signaux clés.

=== 3. MODÉLISATION ===
Prétraitement / feature engineering :
- Variables retenues (6) : perimeter, area, smoothness, compactness, symmetry, fractal_dimension (exclusion de radius, texture, id).
- Transformation log (toutes les variables > 0) + standardisation, dans un Pipeline scikit-learn (pas de fuite de données).
- Split stratifié et mélangé : 75 train (63 % M) / 25 test (60 % M), random_state = 42. Le test n'est utilisé qu'une fois, à la fin.

Comparaison de 8 modèles (validation croisée stratifiée 5 plis × 10 répétitions sur le train, AUC moyenne ± écart-type) :
| Modèle | AUC | Accuracy | Sensibilité | F1 |
| SVM (RBF) | 0,915 (±0,067) | 0,853 | 0,920 | 0,887 |
| Random Forest | 0,896 | 0,809 | 0,865 | 0,851 |
| Régression logistique (log) | 0,893 (±0,100) | 0,827 | 0,912 | 0,868 |
| Régression logistique | 0,886 | 0,835 | 0,900 | 0,872 |
| KNN (k=7) | 0,884 | 0,863 | 0,922 | 0,894 |
| Gradient Boosting | 0,883 | 0,805 | 0,881 | 0,850 |
| Arbre de décision (prof. 3) | 0,814 | 0,789 | 0,833 | 0,829 |
| Référence (classe majoritaire) | 0,500 | 0,627 | 1,000 | 0,770 |
Lecture : écarts entre les meilleurs modèles < écart-type → non significatifs ; l'arbre seul sur-apprend ; les modèles complexes n'apportent rien sur 75 patients.

Vérification de l'exclusion (régression logistique log, AUC CV) :
- 6 variables fiables : 0,893 ; + radius et texture : 0,877 (dégradation) ; sans area : 0,898 ; radius + texture seuls : 0,582.

Optimisation (GridSearchCV, 5 plis × 5 répétitions) :
- Régression logistique : meilleur = pénalité L1 (Lasso), C = 0,3 → AUC CV 0,908.
- SVM : C = 1, gamma = « scale » → AUC CV 0,928.

Sélection du modèle final : régression logistique Lasso, car performance comparable au SVM, meilleure sur le test, interprétable (indispensable en médecine), probabilités exploitables pour fixer un seuil clinique.

=== 5. RÉSULTATS (à placer dans « Résultats et limites ») ===
Jeu de test (25 patients) :
- AUC : régression logistique 0,947 ; SVM 0,867 (ordre inversé par rapport à la CV → modèles en réalité équivalents, test trop petit pour les départager).
- Seuil 0,5 : accuracy 0,88 ; malins : précision 0,875, rappel 0,933 ; bénins : précision 0,889, rappel 0,800. 1 cancer raté sur 15, 2 biopsies inutiles sur 10 bénins.

Seuil clinique (choisi sur prédictions hors-pli du train pour garantir sensibilité ≥ 95 %) : seuil = 0,37
- Test : sensibilité 100 % (0 cancer raté / 15), spécificité 70 % (7 biopsies évitées / 10 bénins, 3 biopsies inutiles).
- Train hors-pli : sensibilité 95,7 % (2 cancers ratés / 47), spécificité 67,9 % (19 biopsies évitées / 28).
- Conclusion métier : environ 2 biopsies inutiles sur 3 évitées en ne ratant que très peu de cancers. Le choix du seuil est une décision clinique.

Interprétation :
- Le Lasso ne garde que 2 variables : area (coefficient 1,03, odds ratio 2,79) et compactness (coefficient 0,85, odds ratio 2,33). Toutes les autres ont un coefficient nul (redondance avec area ou compactness).
- +1 écart-type de log(area) → cote de malignité × 2,8 ; +1 écart-type de log(compactness) → × 2,3.
- Importance par permutation (test) : area −0,26 d'AUC, compactness −0,14 ; autres : 0.
- Modèle final très simple (2 variables) qui confirme l'EDA : taille + forme.

Limites :
1. Très petit échantillon (100 patients, 25 en test) : incertitude de ± 5 à 10 points ; un patient mal classé = 4 points d'accuracy.
2. Provenance douteuse (variables du Breast Cancer Wisconsin) et colonnes corrompues → conclusions non transposables telles quelles à la prostate.
3. Les variables supposent déjà un prélèvement cellulaire (cytoponction), moins invasif qu'une biopsie mais pas nul.
4. Sensibilité 95 % = environ 1 cancer sur 20 raté → outil d'aide à la décision, pas de remplacement du médecin.
5. Absence de validation externe ; pas de données africaines spécifiques (la revue rappelle qu'un modèle ne se transpose pas d'une population à une autre sans recalibration [§5.2, §12.3]).
6. Notre cible est bénin / malin, alors que le problème clinique central est de distinguer cancer indolent et agressif (revue §15) : le modèle est une première étape de tri.

Perspectives : validation croisée imbriquée, intervalles de confiance par bootstrap, courbe de calibration, validation sur une cohorte plus grande (ex. Breast Cancer Wisconsin complet, 569 patients) et sur des données hospitalières africaines, intégration du PSA sanguin.

=== 4. DÉPLOIEMENT ET AUTOMATISATION ===
Rédige cette section avec un schéma d'architecture : données (CSV initial + cas confirmés) → script d'entraînement → contrôle qualité → modèle sauvegardé → application Streamlit → utilisateur (médecin), avec la boucle de réentraînement (cas confirmés saisis dans l'app → réentraînement planifié).
Ne mentionne PAS Docker (choix du groupe : pas de conteneurisation).

Architecture du code (dépôt GitHub) :
- src/modele.py : module partagé (chemins, liste des 6 variables, bornes de saisie, construction du pipeline log → standardisation → régression logistique). Garantit que l'entraînement et l'application appliquent exactement le même prétraitement.
- src/train.py : script d'entraînement / réentraînement.
- app/streamlit_app.py + app/app_pages/ : application web Streamlit (3 pages).
- models/ : model.joblib (modèle en production), metrics.json (performances + seuil), historique.csv (tous les réentraînements).
- .github/workflows/retrain.yml : réentraînement planifié.
- tests/test_app.py : tests automatiques de l'application (sans navigateur, streamlit.testing AppTest).
- Technologies : Python 3.12, scikit-learn 1.9, Streamlit 1.67, pandas, joblib, GitHub Actions.

Application Streamlit (lancement : streamlit run app/streamlit_app.py) :
- Page « Prédiction » : formulaire avec les 6 mesures du noyau (perimeter, area, smoothness, compactness, symmetry, fractal_dimension), valeurs par défaut = médianes, saisies bornées. Sortie : probabilité de malignité, barre de risque, décision au seuil clinique (« Biopsie recommandée » en rouge / « Biopsie probablement évitable » en vert), et graphique des contributions de chaque variable à la prédiction (coefficient × valeur standardisée) pour expliquer la décision.
- Page « Performances du modèle » : AUC CV, seuil clinique, sensibilité, spécificité, matrice de confusion au seuil, coefficients du modèle, historique des réentraînements et courbe d'évolution de l'AUC.
- Page « Ajouter un cas confirmé » : après une biopsie, le médecin saisit les mesures et le diagnostic confirmé ; le cas est ajouté à data/nouveaux_patients.csv et sera intégré au prochain réentraînement (boucle de rétroaction : le modèle apprend des nouveaux cas réels).
- L'application recharge automatiquement le nouveau modèle quand le fichier change (cache invalidé par la date de modification), sans redémarrage.
- Avertissement affiché : outil d'aide à la décision, ne remplace pas l'avis médical.

Script de réentraînement src/train.py (étapes) :
1. Charge les données initiales + les cas confirmés ajoutés via l'app (nettoyage : cible B/M, valeurs > 0).
2. Choix des hyperparamètres par GridSearchCV (C de 0,01 à 10, pénalité L1 ou L2), validation croisée 5 plis × 5.
3. Estimation des performances par validation croisée stratifiée répétée 5 plis × 10.
4. Calcul du seuil clinique sur prédictions hors-pli : seuil le plus élevé garantissant une sensibilité ≥ 95 %.
5. Contrôle qualité avant mise en production : AUC CV ≥ 0,80 ET pas de baisse de plus de 0,03 par rapport au modèle en production ; sinon le modèle actuel est conservé (option --force pour forcer).
6. Sauvegarde du modèle (joblib), des métriques (JSON) et d'une ligne d'historique (CSV), avec journalisation (logging).

Planification :
- GitHub Actions (.github/workflows/retrain.yml) : chaque lundi à 03:00 UTC (cron "0 3 * * 1") + déclenchement manuel. Le workflow installe les dépendances, lance src/train.py, vérifie que les 3 pages de l'application démarrent sans erreur, puis commite le nouveau modèle et l'historique dans le dépôt.
- Alternative locale documentée dans le README : cron (Linux) ou Planificateur de tâches Windows (schtasks).

Modèle en production (réentraîné sur les 100 patients par src/train.py) — à distinguer de l'évaluation du notebook, qui garde 25 patients de test :
- Hyperparamètres retenus : L1 (Lasso), C = 0,3 (identiques au notebook).
- AUC CV = 0,913 (± 0,077) ; accuracy CV = 0,857.
- Seuil clinique = 0,42 → sensibilité 95,2 % (59 cancers détectés / 62, 3 ratés), spécificité 76,3 % (29 biopsies évitées / 38 bénins, 9 biopsies inutiles).
- Coefficients : area 1,28 ; compactness 0,93 ; les 4 autres variables à 0 (même conclusion que le notebook).

Tests et validation du déploiement :
- 4 tests automatiques réussis : chargement des 3 pages, un cas bénin typique → « biopsie évitable », un cas malin typique → « biopsie recommandée », formulaire incomplet refusé.
- Boucle complète testée : ajout d'un cas via l'app → réentraînement (101 patients) → nouveau modèle déployé et visible dans l'historique.

Hébergement : [À COMPLÉTER si mise en ligne — ex. Streamlit Community Cloud, URL : ...] ; sinon exécution locale.
```

---

## PROMPT 2 — Présentation PowerPoint (20 slides max)

```
Tu es un data scientist qui prépare la soutenance d'un projet universitaire de Science des Données (Master, IFRI). Crée une présentation PowerPoint en français de 18 à 20 slides MAXIMUM (fichier .pptx si tu peux le générer ; sinon donne, pour chaque slide : titre, contenu en puces courtes, visuel suggéré et notes de l'orateur).

RÈGLES
- N'invente aucun chiffre : utilise uniquement les résultats fournis.
- Peu de texte par slide (5 puces max, phrases courtes), un message clé par slide.
- Visuels : graphiques, schémas, gros chiffres clés. Indique « [Capture : … du notebook] » quand une figure du projet doit être insérée.
- Style sobre et professionnel, thème santé (bleu / vert / orange pour malin).
- Ajoute des notes de l'orateur (3–5 phrases) pour chaque slide ; durée totale visée : 15 minutes.
- La présentation doit couvrir : contexte, méthodologie, résultats, démonstration de l'application.

INFORMATIONS GÉNÉRALES
- Titre : Prédiction de la malignité d'une tumeur de la prostate pour réduire les biopsies inutiles
- Cours : TP Science des Données — Projet intégrateur — Msc. Osias Noël TOSSOU
- Groupe 5 : BOKOSSA Freud Arthur, FAKEYE Grace, AHOUANDJINOU Jean Marie, OKPEICHA Jaurès
- GitHub : https://github.com/FreudArthur/Data-Science

PLAN SUGGÉRÉ
1. Titre
2. Contexte : 2e cancer masculin dans le monde (1,47 million de cas, 397 430 décès en 2022) ; en Afrique 7 % des cas mais 14 % des décès, ratio décès/cas 54 % (vs 15 % en Amérique du Nord), 45 % de diagnostics au stade IV, survie à 5 ans 60 % [GLOBOCAN 2022 ; Seraphin et al. 2021] — gros chiffre + graphique en barres
3. Problématique, acteurs et enjeux : PSA sensible (≈ 91 %) mais peu spécifique → biopsies inutiles ; IRM et biopsie = goulots d'étranglement en Afrique ; classification binaire bénin/malin, objectif sensibilité ≥ 95 % puis éviter un maximum de biopsies ; acteurs : patients, urologues, pathologistes, hôpitaux, ministère
4. Ce que dit la littérature : modèles ML souvent AUC > 0,75-0,80 mais biais élevé et peu de validation externe ; « les modèles les plus utiles ne sont pas les plus complexes » ; cahier des charges d'un modèle frugal pour l'Afrique (peu de variables, interprétable, validé localement) [revue de littérature, Jean-Marie]
5. Méthodologie globale : schéma du cycle données → EDA → modélisation → déploiement → réentraînement
6. Le choix des données : 1er dataset Stamey (97 patients, tous cancéreux → inadapté) → dataset Kaggle Prostate_Cancer (100 patients, cible M/B)
7. Description du dataset : 100 patients, 8 mesures de noyaux cellulaires, 62 % M / 38 % B, 0 manquant, 0 doublon
8. Anomalies détectées (point fort) : radius incohérent avec perimeter (r = −0,24 au lieu de ~+1), radius/texture quasi aléatoires → exclues ; fichier trié (80 % de M dans les 50 premiers id vs 44 % ensuite) → mélange + stratification
9. Tendances clés : noyaux malins plus grands (area +78 %, perimeter +37 %, AUC ≈ 0,88–0,89) et plus irréguliers (compactness +74 %, AUC 0,84) ; texture et fractal_dimension inutiles
10. Corrélations / ACP : perimeter–area r = 0,98 ; bloc « forme » ; séparation B/M sur l'ACP
11. Prétraitement : 6 variables, log + standardisation en pipeline, split stratifié 75/25
12. Comparaison de 8 modèles (CV 5×10) : SVM 0,915 ; RF 0,896 ; Rég. log. 0,893 ; KNN 0,884 ; GB 0,883 ; Arbre 0,814 ; Référence 0,50 → modèles simples suffisent
13. Modèle final : régression logistique Lasso (C = 0,3), AUC CV 0,908 ; choisie pour performance + interprétabilité
14. Résultats sur le test : AUC 0,947 ; accuracy 88 % ; matrice de confusion au seuil 0,5 (1 cancer raté / 15, 2 biopsies inutiles / 10)
15. Seuil clinique 0,37 : test 0 cancer raté / 15, 7 biopsies évitées / 10 ; en CV : sensibilité 96 %, spécificité 68 % → « ≈ 2 biopsies inutiles sur 3 évitées »
16. Interprétation : seulement 2 variables gardées — area (odds ratio 2,8) et compactness (odds ratio 2,3) = taille + forme
17. Déploiement et automatisation : schéma d'architecture (données → src/train.py → contrôle qualité → models/model.joblib → app Streamlit → médecin, + boucle « cas confirmés → réentraînement ») ; réentraînement planifié chaque lundi 03:00 UTC via GitHub Actions ; contrôle qualité (AUC ≥ 0,80, pas de baisse > 0,03) ; historique des versions
18. Démonstration de l'application Streamlit (3 pages) : [Capture : page Prédiction — cas bénin → « Biopsie probablement évitable »] ; [Capture : cas malin → « Biopsie recommandée » + graphique des contributions] ; [Capture : page Performances] ; [Capture : page Ajouter un cas confirmé]. Prévoir une démo en direct : streamlit run app/streamlit_app.py
19. Limites : 100 patients seulement, provenance douteuse (variables du Breast Cancer Wisconsin), pas de validation externe ni de données africaines (recalibration nécessaire), bénin/malin ≠ indolent/agressif, aide à la décision et non remplacement du médecin
20. Conclusion et perspectives + questions

DÉTAILS DU DÉPLOIEMENT (ne pas mentionner Docker)
- Application : Streamlit, 3 pages — Prédiction (6 mesures → probabilité + décision au seuil + contributions des variables), Performances du modèle (métriques, matrice de confusion, historique), Ajouter un cas confirmé (alimente le réentraînement).
- Réentraînement automatique : src/train.py (GridSearchCV, CV 5×10, seuil clinique sensibilité ≥ 95 %, contrôle qualité, sauvegarde + historique) planifié par GitHub Actions chaque lundi à 03:00 UTC.
- Modèle en production (100 patients) : Lasso C = 0,3 ; AUC CV 0,913 ; seuil 0,42 → sensibilité 95 % (3 cancers ratés / 62), spécificité 76 % (29 biopsies évitées / 38).
- Tests : 4 tests automatiques réussis + boucle « ajout de cas → réentraînement » vérifiée.
- URL de démo : [À COMPLÉTER si mise en ligne, sinon démo locale]
```
