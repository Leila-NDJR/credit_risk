import numpy as np

def optimize_threshold(
    y_true,
    y_proba,
    loan_amount,
    interest_rate,
    reject_cost=0
):
    """
    Retourne le seuil maximisant le profit bancaire
    """

    gain_tn = loan_amount * interest_rate
    cost_fn = loan_amount

    thresholds = np.linspace(0, 1, 101)
    profits = []

    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)

        profit = 0
        for yt, yp in zip(y_true, y_pred):
            if yt == 0 and yp == 0:
                profit += gain_tn
            elif yt == 1 and yp == 0:
                profit -= cost_fn
            else:
                profit += reject_cost

        profits.append(profit)

    best_idx = int(np.argmax(profits))

    return {
        "best_threshold": thresholds[best_idx],
        "best_profit": profits[best_idx],
        "thresholds": thresholds,
        "profits": profits
    }
