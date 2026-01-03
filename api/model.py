import joblib
import pandas as pd
import os

# --- Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "final_model_lgbm.pkl")

# --- Load model
model = joblib.load(MODEL_PATH)

# --- Business threshold (issu de l'optimisation profit)
OPTIMAL_THRESHOLD = 0.4


def predict_proba(client_dict: dict) -> float:
    """
    Retourne la probabilité de défaut (PD)
    """
    X = pd.DataFrame([client_dict])
    proba = model.predict_proba(X)[0, 1]
    return float(proba)


def make_decision(proba: float) -> str:
    """
    Applique la politique risque
    """
    return "REJECTED" if proba >= OPTIMAL_THRESHOLD else "APPROVED"


def predict(client_dict: dict):
    """
    Fonction utilisée par l'API
    """
    proba = predict_proba(client_dict)
    decision = make_decision(proba)

    return {
        "probability_default": proba,
        "decision": decision,
        "threshold_used": OPTIMAL_THRESHOLD
    }
