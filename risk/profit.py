def compute_profit(
    y_true,
    y_proba,
    threshold,
    loan_amount=5_000_000,
    interest_rate=0.12
):
    profit = 0

    for true, proba in zip(y_true, y_proba):
        if proba < threshold:
            if true == 0:
                profit += loan_amount * interest_rate
            else:
                profit -= loan_amount

    return profit
