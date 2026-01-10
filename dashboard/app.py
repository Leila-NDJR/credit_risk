import streamlit as st
import pandas as pd
import sqlite3
import json
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================

st.set_page_config(
    page_title="Credit Scoring – Risk & Profit Dashboard",
    layout="wide"
)

st.title("Credit Scoring Dashboard – Vision Risque & Rentabilité")

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

# Base de données des décisions
conn = sqlite3.connect("data/scoring.db")
df = pd.read_sql("SELECT * FROM scoring_events", conn)

# Paramètres Risk (issus de la Business Validation)
with open("data/models/risk_config.json", "r") as f:
    risk_config = json.load(f)

OPTIMAL_THRESHOLD = risk_config["optimal_threshold"]
LOAN_AMOUNT = risk_config["loan_amount"]
INTEREST_RATE = risk_config["interest_rate"]

# ============================================================
# FONCTION PROFIT MÉTIER
# ============================================================

def compute_profit_from_df(df, threshold, interest_rate):
    profit = 0

    for _, row in df.iterrows():
        proba = row["probability_default"]
        true = row.get("true_label", None)  # facultatif en prod

        decision_refus = proba >= threshold

        # En production, true_label n'existe pas :
        # on fait ici une simulation pédagogique
        if true is None:
            continue

        if not decision_refus and true == 0:
            profit += LOAN_AMOUNT * interest_rate
        elif not decision_refus and true == 1:
            profit -= LOAN_AMOUNT

    return profit

# ============================================================
# KPI PRINCIPAUX – VUE COMITÉ DE RISQUE
# ============================================================

st.subheader("Indicateurs Clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Nombre total de clients", len(df))

col2.metric(
    "Taux d'acceptation",
    f"{(df['decision'] == 'APPROVED').mean() * 100:.1f}%"
)

col3.metric(
    "Risque moyen (PD)",
    f"{df['probability_default'].mean():.2f}"
)

col4.metric(
    "Seuil optimal utilisé",
    f"{OPTIMAL_THRESHOLD:.2f}"
)

st.divider()

# ============================================================
# DISTRIBUTION DU RISQUE
# ============================================================

st.subheader("Distribution des Probabilités de Défaut")
st.bar_chart(df["probability_default"])

# ============================================================
# DÉCISIONS CRÉDIT – EN POURCENTAGE
# ============================================================

st.subheader("Décisions Crédit (%)")

decision_pct = (
    df["decision"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

st.bar_chart(decision_pct)

st.divider()

# ============================================================
# PROFIT : SEUIL 0.5 VS SEUIL OPTIMISÉ
# ============================================================

st.subheader("Analyse de Rentabilité")

if "true_label" in df.columns:

    profit_05 = compute_profit_from_df(df, 0.5, INTEREST_RATE)
    profit_opt = compute_profit_from_df(df, OPTIMAL_THRESHOLD, INTEREST_RATE)

    col1, col2 = st.columns(2)

    col1.metric(
        "Profit – Seuil 0.5",
        f"{profit_05:,.0f} XAF"
    )

    col2.metric(
        "Profit – Seuil Optimisé",
        f"{profit_opt:,.0f} XAF",
        delta=f"{profit_opt - profit_05:,.0f} XAF"
    )

else:
    st.info(
        "Les profits sont illustratifs. "
        "Les labels réels ne sont pas disponibles en production."
    )

# ============================================================
# SIMULATION PORTEFEUILLE – 1 000 CLIENTS
# ============================================================

st.subheader("Simulation Portefeuille – 1 000 Clients")

df_sim = df.sample(
    n=min(1000, len(df)),
    replace=True,
    random_state=42
)

if "true_label" in df_sim.columns:
    sim_profit = compute_profit_from_df(
        df_sim,
        OPTIMAL_THRESHOLD,
        INTEREST_RATE
    )
    st.write(f"**Profit simulé** : {sim_profit:,.0f} XAF")
else:
    st.write("Simulation indicative (sans labels réels).")

# ============================================================
# STRESS TEST – BEAC +1%
# ============================================================

st.subheader("Stress Test – Hausse BEAC +1%")

new_rate = INTEREST_RATE + 0.01

if "true_label" in df_sim.columns:
    stress_profit = compute_profit_from_df(
        df_sim,
        OPTIMAL_THRESHOLD,
        new_rate
    )
    st.write(f"Taux initial : {INTEREST_RATE*100:.1f}%")
    st.write(f"Nouveau taux : {new_rate*100:.1f}%")
    st.write(f"**Profit après choc BEAC** : {stress_profit:,.0f} XAF")
else:
    st.write("Analyse qualitative : hausse des taux améliore la rentabilité des clients sains.")

st.divider()

# ============================================================
# JUSTIFICATION MÉTIER DES DÉCISIONS (SHAP → TEXTE)
# ============================================================

def generate_decision_explanation(row):
    shap_raw = row.get("shap_values")

    if not shap_raw:
        return "Décision fondée sur le profil de risque global du client."

    shap_dict = json.loads(shap_raw) if isinstance(shap_raw, str) else shap_raw

    # Variables les plus contributives au risque
    drivers = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]

    explanations = [
        feature.replace("num__", "").replace("_", " ")
        for feature, value in drivers
        if value > 0
    ]

    if not explanations:
        return "Profil globalement peu risqué selon le modèle."

    return (
        "Décision principalement expliquée par : "
        + ", ".join(explanations)
    )

df["justification"] = df.apply(generate_decision_explanation, axis=1)

# ============================================================
# HISTORIQUE DES DÉCISIONS
# ============================================================

st.subheader("Historique des Décisions Client")

st.dataframe(
    df[[
        "timestamp",
        "decision",
        "probability_default",
        "justification"
    ]].sort_values("timestamp", ascending=False),
    use_container_width=True
)

# ============================================================
# MESSAGE FINAL
# ============================================================

st.success(
    "Le système de scoring est terminé "
)
