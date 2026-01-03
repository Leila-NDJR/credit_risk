import streamlit as st
import pandas as pd
import sqlite3
import json

st.set_page_config(
    page_title="Credit Scoring Dashboard",
    layout="wide"
)

st.title("Credit Scoring Dashboard")

conn = sqlite3.connect("data/scoring.db")
df = pd.read_sql("SELECT * FROM scoring_events", conn)

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Nombre total de clients", len(df))
col2.metric(
    "Taux d'acceptation",
    f"{(df['decision'] == 'APPROVED').mean() * 100:.1f}%"
)
col3.metric(
    "Risque moyen",
    f"{df['probability_default'].mean():.2f}"
)

st.divider()

# Distribution
st.subheader("Distribution des probabilités de défaut")
st.bar_chart(df["probability_default"])

# Décisions (%)
st.subheader("Décisions crédit (%)")
decision_pct = (
    df["decision"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)
st.bar_chart(decision_pct)


def generate_decision_explanation(row):
    shap_raw = row.get("shap_values")

    if not shap_raw:
        return "Décision basée sur le score global du client."

    shap = json.loads(shap_raw) if isinstance(shap_raw, str) else shap_raw

    drivers = [
        feature.replace("_", " ")
        for feature, value in shap.items()
        if value > 0
    ]

    if not drivers:
        return "Profil globalement peu risqué selon le modèle."

    return (
        "Décision influencée principalement par : "
        + ", ".join(drivers[:3])
    )


df["justification"] = df.apply(generate_decision_explanation, axis=1)

st.subheader("Historique des décisions")
st.dataframe(
    df[[
        "timestamp",
        "decision",
        "probability_default",
        "justification"
    ]].sort_values("timestamp", ascending=False),
    use_container_width=True
)
