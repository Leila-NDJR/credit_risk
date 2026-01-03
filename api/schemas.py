
from pydantic import BaseModel
from typing import Literal, List, Dict

class ClientData(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: Literal["RENT", "OWN", "MORTGAGE", "OTHER"]
    person_emp_length: float
    loan_intent: Literal[
        "EDUCATION", "MEDICAL", "VENTURE",
        "PERSONAL", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"
    ]
    loan_grade: Literal["A", "B", "C", "D", "E", "F", "G"]
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: Literal["Y", "N"]
    cb_person_cred_hist_length: float



class PredictionResponse(BaseModel):
    probability_default: float
    decision: str
    threshold_used: float
    explanation: dict



class BatchClientData(BaseModel):
    clients: List[ClientData]


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]
