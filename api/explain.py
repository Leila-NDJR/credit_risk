import shap
import pandas as pd
from api.model import model

explainer = shap.TreeExplainer(
    model.named_steps["model"]
)

def explain(client_dict: dict):
    X = pd.DataFrame([client_dict])

    X_processed = model.named_steps["preprocessor"].transform(X)

    shap_values = explainer.shap_values(X_processed)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    feature_names = model.named_steps["preprocessor"].get_feature_names_out()

    shap_dict = dict(zip(feature_names, shap_values[0]))

    explanation = dict(
        sorted(
            shap_dict.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:3]
    )

    return explanation
