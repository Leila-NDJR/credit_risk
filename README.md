# Système de Scoring Crédit – Banque & Fintech Afrique Centrale

Projet End-to-End Data Science | M1 Data Science
Auteur : K. Jessy Leila
Date : Janvier 2026

## Description du projet

Ce projet est une solution de scoring crédit destinée aux banques et institutions financières opérant en Afrique Centrale.

L’objectif est de prédire le risque de défaut de paiement d’un client, puis de transformer cette prédiction en une décision d’octroi rentable, en intégrant une fonction de coût métier (profit / perte).

Le système permet de :

Analyser les données historiques de crédit pour identifier les facteurs de risque.

Prédire la probabilité de défaut via un modèle Machine Learning avancé (LightGBM).

Optimiser le seuil de décision pour maximiser le profit bancaire.

Déployer le modèle via une API FastAPI.

Visualiser les décisions et la rentabilité sur un dashboard Streamlit.

## Architecture générale

Le système repose sur :

Modèle ML : LightGBM (classification binaire défaut / non-défaut)

Backend : FastAPI (scoring en temps réel)

Base de données : SQLite (scoring.db)

Dashboard : Streamlit (pilotage du risque et du profit)

Explicabilité : SHAP (justification des décisions)


## Performances du modèle

Modèle retenu : LightGBM

AUC-ROC : 0.95

Recall (détection des défauts) : 79.7 %

Seuil standard : 0.50

Seuil optimisé (business) : 0.29

### Résultats business
Scénario	Profit simulé
Seuil 0.50	1,49 milliard FCFA
Seuil optimisé 0.29	1,84 milliard FCFA

Gain estimé : +23 % de rentabilité

## Exécution rapide
Lancer l’API
py -m uvicorn api.main:app --reload

Documentation : http://localhost:8000/docs

Lancer le dashboard
streamlit run dashboard/app.py


## Fonction de profit (résumé)

Hypothèses :

Montant du prêt : 5 000 000 FCFA

Taux d’intérêt : 12 %

Formule :
Gain = intérêts si client sain accepté
Perte = capital si défaut accepté
Refus = 0

Le seuil est choisi pour maximiser le profit total, pas l’accuracy.

## API FastAPI
Endpoint principal

POST /predict

Entrée :

{
  "person_age": 35,
  "person_income": 450000,
  "loan_amnt": 2000000,
  ...
}


Sortie :

{
  "probability_default": 0.23,
  "decision": "APPROVED",
  "threshold_used": 0.29,
  "explanation": {...}
}

## Explicabilité

SHAP TreeExplainer

Explications globales et locales

Justification individuelle des refus

## Dashboard Streamlit

Décisions crédit (pourcentages)

Distribution des probabilités

Profit total simulé

Comparaison seuil standard vs seuil optimisé

Simulation portefeuille (1 000 clients)

## Dépendances principales

Python 3.10+

scikit-learn

lightgbm

shap

fastapi

uvicorn

streamlit

pandas, numpy, sqlalchemy

