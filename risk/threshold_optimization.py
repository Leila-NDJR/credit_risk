import numpy as np
from risk.profit import compute_profit


def find_optimal_threshold(
    y_true,
    y_proba,
    thresholds=np.linspace(0, 1, 101),
    loan_amount=5_000_000,
    interest_rate=0.12
):
    profits = []

    for t in thresholds:
        p = compute_profit(
            y_true,
            y_proba,
            t,
            loan_amount,
            interest_rate
        )
        profits.append(p)

    best_idx = int(np.argmax(profits))

    return thresholds[best_idx], profits
