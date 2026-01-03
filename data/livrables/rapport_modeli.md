## 1. Objectif métier de la modélisation

L’objectif de cette phase est de développer un modèle de credit scoring binaire capable d’identifier les emprunteurs présentant un risque élevé de défaut, afin de réduire les pertes financières liées aux mauvais crédits.

Dans ce contexte, la performance du modèle n’est pas évaluée uniquement sur sa capacité prédictive globale, mais sur sa capacité à limiter les erreurs les plus coûteuses, en particulier les faux négatifs (clients défaillants acceptés).

## 2. Modèles testés

Quatre modèles ont été implémentés et évalués selon une méthodologie homogène :

Régression logistique : Modèle de référence réglementaire
Interprétable mais limité dans la capture de non-linéarités

Random Forest : Modèle d’ensemble robuste
Capte des interactions mais performance encore limitée sur la détection du défaut

XGBoost : Modèle de boosting performant
Très bon compromis global entre AUC et précision

LightGBM : Modèle de boosting optimisé
Excellente capacité de détection des défauts

Tous les modèles ont été intégrés dans un pipeline unique incluant le preprocessing, garantissant la comparabilité et l’absence de fuite de données.

## 3. Méthodologie d’évaluation

Les modèles ont été évalués sur un jeu de test indépendant à l’aide des métriques suivantes :

ROC-AUC : capacité discriminante globale
Recall (classe défaut) : capacité à détecter les clients à risque
Precision : proportion de défauts parmi les clients refusés
F1-score : compromis précision / rappel
Matrices de confusion : lecture directe des erreurs métier

Le recall a été considéré comme métrique prioritaire, conformément aux pratiques du credit scoring, où le coût d’un faux négatif est nettement supérieur à celui d’un faux positif.

## 4. Analyse comparative des résultats

### Régression logistique

Recall insuffisant
Nombre élevé de faux négatifs
Performance globale limitée

Modèle non retenu pour un usage opérationnel.

### Random Forest
Amélioration par rapport à la logistique
Recall encore instable
Peu d’avantage par rapport aux modèles de boosting

Modèle intermédiaire, mais dominé par XGBoost et LightGBM.

### XGBoost

Excellente AUC
Bon équilibre précision / recall
Faux négatifs encore légèrement supérieurs à LightGBM

Modèle performant mais non optimal pour une stratégie de risque conservatrice.

### LightGBM

Recall le plus élevé
Réduction maximale des faux négatifs
AUC compétitive

Faux positifs acceptables au regard du gain en protection contre le défaut

Meilleur modèle selon l’objectif métier retenu.

## 5. Choix du modèle final

Le modèle LightGBM est retenu comme modèle final de scoring, car il :

minimise les faux négatifs,
réduit le risque de pertes financières,
offre une performance globale satisfaisante,
reste compatible avec des techniques d’explicabilité avancées.

Ce choix correspond à une stratégie de gestion du risque prudente, typique :
d’une Fintech en phase de croissance,
d’un contexte économique incertain,
d’un portefeuille à risque modéré à élevé.

## 6. Industrialisation et traçabilité

Le pipeline LightGBM complet a été sauvegardé, garantissant :

la reproductibilité des résultats,
l’absence de fuite de preprocessing,
la possibilité d’un déploiement direct en environnement de production,
la compatibilité avec les outils d’interprétabilité (SHAP).

La phase de modélisation est considérée comme terminée et conforme aux standards Fintech.

