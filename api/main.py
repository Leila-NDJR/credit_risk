from fastapi import FastAPI, HTTPException
from api.schemas import ClientData, BatchClientData, PredictionResponse
from api.model import predict
from api.explain import explain
from config.risk_config import OPTIMAL_THRESHOLD
from api.mqtt.publisher import publish_scoring_event

app = FastAPI(
    title="Credit Scoring API",
    version="1.0"
)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict_credit(client: ClientData):

    try:
        client_dict = client.model_dump()

        # 1️⃣ Prédiction (PD + décision + seuil)
        result = predict(client_dict)

        # 2️⃣ Explicabilité
        explanation = explain(client_dict)

        # 3️⃣ Event (traçabilité / audit)
        publish_scoring_event({
            "probability_default": round(result["probability_default"], 4),
            "decision": result["decision"],
            "threshold_used": OPTIMAL_THRESHOLD,
            "features": client_dict,
            "shap_values": explanation
        })

        return {
            "probability_default": round(result["probability_default"], 4),
            "decision": result["decision"],
            "threshold_used": OPTIMAL_THRESHOLD,
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
