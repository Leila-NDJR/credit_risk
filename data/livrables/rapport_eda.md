## 1. Contexte et objectif de l’analyse

L’analyse exploratoire des données (EDA) a été réalisée dans le but de comprendre la structure du portefeuille de crédits d’AfriCash Solutions et d’identifier les principaux facteurs associés au défaut de paiement.

Le jeu de données contient plusieurs dizaines de milliers de demandes de crédit, décrivant à la fois :

les caractéristiques socio-économiques des emprunteurs,
les paramètres du prêt,
et l’issue du crédit (remboursé ou en défaut).

Cette étape est essentielle afin de poser les bases d’un système de credit scoring fiable, orienté vers la réduction du risque et l’amélioration de la prise de décision.

## 2. Structure et qualité des données

L’analyse de la structure des données montre :

un nombre élevé d’observations, garantissant une bonne puissance statistique ;
un mélange de variables numériques (âge, revenu, montant du prêt, taux d’intérêt) et catégorielles (statut de logement, motif du prêt, historique de défaut) ;
la présence de valeurs manquantes sur certaines variables, ce qui justifie une phase rigoureuse de nettoyage et d’imputation dans l’étape suivante.

Les statistiques descriptives révèlent également :

une forte hétérogénéité des revenus,
des montants de prêts très dispersés,
et la présence de valeurs extrêmes, typiques des données financières réelles.

Ces éléments confirment que le recours à un simple modèle naïf serait insuffisant, et qu’un preprocessing structuré est indispensable.

## 3. Analyse de la variable cible : le défaut de paiement

La variable cible loan_status permet d’identifier les crédits en défaut.

L’analyse montre que :
le taux de défaut global est significatif, supérieur aux standards attendus dans un portefeuille sain ;
la distribution des classes est déséquilibrée, avec une majorité de crédits remboursés.

D’un point de vue métier, cela implique que :
la métrique de performance principale ne devra pas être l’accuracy,
mais des indicateurs sensibles au risque, notamment le recall sur les défauts.

## 4. Analyse des facteurs de risque
### 4.1 Âge de l’emprunteur

L’étude du taux de défaut par âge met en évidence :

une variabilité du risque selon les tranches d’âge ;
un risque généralement plus élevé chez les emprunteurs les plus jeunes, et parfois chez les plus âgés.

Cela suggère que l’âge n’agit pas de manière linéaire et devra être traité avec prudence (binning, interactions).

### 4.2 Revenu

Le revenu apparaît comme un facteur discriminant majeur :

les emprunteurs appartenant aux quintiles de revenu les plus faibles présentent des taux de défaut nettement plus élevés ;
le risque décroît globalement avec le niveau de revenu.

Cette relation valide un principe fondamental du credit scoring :

la capacité de remboursement est un déterminant central du risque de crédit.

### 4.3 Historique de défaut

L’historique de défaut (cb_person_default_on_file) est l’un des signaux les plus puissants observés :

les clients ayant déjà fait défaut présentent un taux de défaut largement supérieur aux autres.

Ce résultat est cohérent avec les pratiques bancaires et confirme que cette variable devra être fortement pondérée dans le modèle.

### 4.4 Montant du prêt

L’analyse du montant du prêt montre que :

les crédits en défaut sont souvent associés à des montants plus élevés,
suggérant un effet de surendettement potentiel.

Cependant, cette variable devra être analysée relativement au revenu, ce qui justifie la création de ratios lors du feature engineering.

## 5. Corrélations et limites de l’analyse

La matrice de corrélation met en évidence certaines relations entre variables numériques, mais :

aucune corrélation linéaire forte ne suffit à elle seule à expliquer le défaut ;

cela confirme la nécessité de modèles non linéaires capables de capturer des interactions complexes.

Il est important de rappeler que :

corrélation ≠ causalité
Les résultats observés doivent être interprétés comme des signaux de risque, et non comme des relations causales strictes.

## 6. Conclusion de l’EDA (vision métier)

En synthèse :

le portefeuille présente un niveau de risque non négligeable ;
plusieurs variables clés (revenu, historique de défaut, montant du prêt) se démarquent comme fortement associées au défaut ;

certains segments de clients présentent un risque structurellement plus élevé.

Ces résultats justifient pleinement la mise en place d’un système de credit scoring automatisé, permettant :

une meilleure sélection des emprunteurs,
une réduction du taux de défaut,
et une prise de décision plus rapide et plus objective.


### TRANSITION LOGIQUE VERS LE NOTEBOOK 02

À ce stade, le problème est clair, mais :

les données ne sont pas encore prêtes pour un modèle,
les variables catégorielles ne sont pas exploitables,
les valeurs manquantes et les échelles hétérogènes posent problème.

Objectif du notebook 02 :
Transformer ces données brutes en un jeu de données propre, cohérent et modélisable, sans fuite d’information.