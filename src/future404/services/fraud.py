"""Proactive fraud / anomaly alerts.

Baseline: z-score on amount + unusual location. Upgrade path: scikit-learn
IsolationForest or a trained classifier on labelled data.
"""

from statistics import mean, pstdev

from future404.models import Customer

HOME_LOCATIONS = {"Brisbane"}


def detect_anomalies(customer: Customer, z_threshold: float = 3.0) -> list[dict]:
    debits = [t for t in customer.all_transactions() if t.amount < 0 and t.category != "rent"]
    if len(debits) < 10:
        return []
    amounts = [-t.amount for t in debits]
    mu, sigma = mean(amounts), pstdev(amounts) or 1.0
    alerts = []
    for t in debits:
        z = (-t.amount - mu) / sigma
        reasons = []
        if z >= z_threshold:
            reasons.append(f"amount is {z:.1f} std devs above your usual spend")
        if t.merchant_location not in HOME_LOCATIONS:
            reasons.append(f"unusual location: {t.merchant_location}")
        if reasons:
            alerts.append({"id": t.id, "date": t.date.isoformat(), "merchant": t.description,
                           "amount": -t.amount, "risk": "high" if len(reasons) > 1 else "medium",
                           "reasons": reasons})
    return sorted(alerts, key=lambda a: a["date"], reverse=True)
