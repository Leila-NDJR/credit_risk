import random
import requests

API_URL = "http://127.0.0.1:8000/predict"


def generate_client():
    return {
        "person_age": random.randint(21, 65),
        "person_income": random.randint(200_000, 1_500_000),
        "person_home_ownership": random.choice(["RENT", "OWN", "MORTGAGE"]),
        "loan_intent": random.choice(["PERSONAL", "EDUCATION", "VENTURE", "MEDICAL"]),
        "loan_amnt": random.randint(50_000, 800_000),
        "loan_int_rate": round(random.uniform(5, 25), 2),
        "loan_percent_income": round(random.uniform(0.05, 0.6), 2),
        "cb_person_default_on_file": random.choice(["Y", "N"]),
        "cb_person_cred_hist_length": random.randint(12, 300),
        "loan_grade": random.choice(["A", "B", "C", "D", "E"]),
        "person_emp_length": random.randint(0, 40)
    }


def simulate_clients(n=100):
    for i in range(n):
        client = generate_client()
        r = requests.post(API_URL, json=client)
        if r.status_code == 200:
            print(f"Client {i+1} scored")
        else:
            print(f"Error on client {i+1}")


if __name__ == "__main__":
    simulate_clients(200)
