from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_valid_client():
    payload = {
        "person_age": 35,
        "person_income": 450000,
        "person_home_ownership": "RENT",
        "person_emp_length": 5,
        "loan_intent": "EDUCATION",
        "loan_grade": "C",
        "loan_amnt": 200000,
        "loan_int_rate": 12.5,
        "loan_percent_income": 0.25,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 48
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "probability_default" in data
    assert "decision" in data
    assert data["decision"] in ["APPROVED", "REJECTED"]
    assert "explanation" in data


def test_predict_batch():
    payload = {
        "clients": [
            {
                "person_age": 30,
                "person_income": 300000,
                "person_home_ownership": "RENT",
                "person_emp_length": 2,
                "loan_intent": "MEDICAL",
                "loan_grade": "D",
                "loan_amnt": 150000,
                "loan_int_rate": 14.0,
                "loan_percent_income": 0.3,
                "cb_person_default_on_file": "N",
                "cb_person_cred_hist_length": 24
            },
            {
                "person_age": 55,
                "person_income": 900000,
                "person_home_ownership": "OWN",
                "person_emp_length": 15,
                "loan_intent": "DEBTCONSOLIDATION",
                "loan_grade": "B",
                "loan_amnt": 400000,
                "loan_int_rate": 9.5,
                "loan_percent_income": 0.18,
                "cb_person_default_on_file": "Y",
                "cb_person_cred_hist_length": 120
            }
        ]
    }

    response = client.post("/predict_batch", json=payload)
    assert response.status_code == 200

    results = response.json()["results"]
    assert len(results) == 2
