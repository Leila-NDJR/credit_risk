## 1.Objectif du notebook 04

L’objectif de ce notebook est de rendre explicable et défendable le modèle de credit scoring retenu (LightGBM), conformément aux exigences :
métier (comité crédit),
réglementaires (transparence des décisions),
opérationnelles (justification client).

Contrairement aux notebooks précédents, il ne s’agit plus d’optimiser la performance, mais de comprendre et justifier les décisions du modèle.

En finance :
Un modèle performant mais inexplicable est inutilisable.

## 2.Pourquoi SHAP ?
SHAP (SHapley Additive exPlanations) repose sur la théorie des jeux coopératifs.

Principe clé :
Chaque variable est vue comme un joueur qui contribue à faire monter ou descendre le score final.

Mathématiquement :

𝑓(𝑥)=base value +
∑SHAP𝑗
𝑗
base value : score moyen du modèle sur l’ensemble des données

SHAPᵢ : contribution de la variable i pour un client donné

## 3.Lecture du graphique SHAP individuel (force plot)

Nous analysons maintenant le graphique obtenu du shap

### 3.1 Structure générale du graphique

Sur le graphique, on observe :

une ligne horizontale représentant l’axe du score (log-odds),
une valeur de base (base value),
une valeur finale 
f(x)=−4.32,
des segments colorés (rouge / bleu).

### 3.2 Sens des couleurs (point fondamental)
Couleur	Signification
- Rouge	La variable augmente le risque de défaut
- Bleu	La variable réduit le risque de défaut

Ce n’est PAS la couleur de la variable, mais son effet sur le score.

### 3.3 Sens du déplacement

Les segments poussent vers la droite → risque élévé
Les segments poussent vers la gauche → risque faible

Le modèle part de la base value
et chaque variable déplace le score jusqu’à la valeur finale.

## 4.Analyse détaillée des contributions (variable par variable)

- Variables augmentant le risque (rouge)
. loan_intent_VENTURE = 0.0
Le client n’a pas un prêt à vocation “venture”
Cette situation est associée à un risque plus élevé dans les données

Lecture métier :
Certains types de prêts sont historiquement plus risqués que d’autres.

. person_home_ownership_OWN = 0.0
Le client ne possède pas son logement

Lecture métier :
L’absence de propriété immobilière est souvent un proxy de fragilité financière.

- Variables réduisant le risque (bleu)
. loan_int_rate = 11.89
Taux d’intérêt relativement élevé
Effet protecteur dans le modèle

Lecture métier (important) :
Ce n’est pas causal, mais sélectif :
les clients à taux élevé sont souvent déjà filtrés par la banque.

. person_income = 50000
Revenu relativement élevé
Forte contribution à la réduction du risque

Lecture métier :
Cohérent avec les fondamentaux du credit scoring :
plus de revenu → meilleure capacité de remboursement.

. loan_percent_income = 0.02
Le prêt représente une faible part du revenu

Lecture métier :
Faible charge financière → risque réduit.

. loan_grade_A = 0.0
Le client n’est pas de grade A
Effet néanmoins faible

Lecture métier :
Variable informative mais secondaire ici.

. person_home_ownership_RENT = 1.0
Le client est locataire
Effet négatif faible mais non nul

Lecture métier :
Le modèle différencie subtilement les profils non-propriétaires.

## 5.Reconstruction du raisonnement du modèle

On peut reformuler la décision du modèle en langage humain :

Le client présente plusieurs facteurs de risque liés à sa situation résidentielle et au type de prêt, mais ces éléments sont largement compensés par un revenu élevé et une charge de remboursement faible. Le score final reste inférieur au seuil de risque critique.

C’est exactement ce que demande un régulateur.

## 6.Justification d’un refus (version opérationnelle)

Si le score avait franchi le seuil de refus, la justification aurait été :

- client (simplifiée)

Votre demande n’a pas pu être acceptée en raison de plusieurs éléments défavorables liés à votre situation financière globale, malgré certains points positifs.

- Version comité crédit

La décision est principalement expliquée par des variables structurelles augmentant significativement la probabilité de défaut, insuffisamment compensées par les facteurs favorables.

## 7.Apport de SHAP pour l’institution

Grâce à SHAP, le modèle devient :

- Transparent (on sait pourquoi une décision est prise)

- Traçable (chaque score est justifié)

- Défendable (audit, régulation, contentieux)

- Actionnable (amélioration des politiques crédit)

Sans SHAP, LightGBM serait inutilisable en production bancaire.

### Conclusion générale du notebook 04

L’analyse SHAP démontre que le modèle LightGBM :
repose sur des variables économiquement pertinentes,
prend des décisions cohérentes avec les principes du credit scoring,
permet une justification individuelle claire et reproductible.
L’association performance prédictive + explicabilité fait de ce modèle un système de credit scoring exploitable en environnement Fintech réel.