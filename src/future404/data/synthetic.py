"""Generates realistic-looking but entirely fake customers and transactions.

Never use real customer data in this prototype. Swap this module for a real
data source (e.g. an open-banking / CDR feed) later without changing services.
"""

import random
from datetime import date, timedelta

from future404.config import settings
from future404.models import Account, Customer, Transaction

# category -> (merchants, typical amount range)
SPEND_PATTERNS: dict[str, tuple[list[str], tuple[float, float]]] = {
    "groceries": (["Woolworths", "Coles", "Aldi"], (20, 180)),
    "dining": (["Guzman y Gomez", "Local Cafe", "Sushi Train"], (12, 90)),
    "transport": (["Translink", "Uber", "BP Fuel"], (5, 80)),
    "subscriptions": (["Netflix", "Spotify", "Gym Membership"], (12, 60)),
    "shopping": (["Kmart", "JB Hi-Fi", "Amazon AU"], (15, 150)),
    "utilities": (["Origin Energy", "Telstra", "Urban Utilities"], (60, 250)),
    "rent": (["Rent Payment"], (1800, 1800)),
}


def _make_transactions(rng: random.Random, days: int, income: float) -> list[Transaction]:
    txns: list[Transaction] = []
    start = date.today() - timedelta(days=days)
    counter = 0
    for d in range(days):
        day = start + timedelta(days=d)
        # fortnightly salary
        if d % 14 == 0:
            counter += 1
            txns.append(Transaction(f"T{counter:05d}", day, "Salary", "income", round(income / 26, 2)))
        if day.day == 1:
            counter += 1
            txns.append(Transaction(f"T{counter:05d}", day, "Rent Payment", "rent", -1800.0))
        for category, (merchants, (lo, hi)) in SPEND_PATTERNS.items():
            if category == "rent":
                continue
            if rng.random() < {"groceries": 0.35, "dining": 0.3, "transport": 0.5,
                               "subscriptions": 0.03, "shopping": 0.08, "utilities": 0.03}[category]:
                counter += 1
                txns.append(Transaction(
                    f"T{counter:05d}", day, rng.choice(merchants), category,
                    -round(rng.uniform(lo, hi), 2),
                ))
    # inject a couple of suspicious transactions for the fraud demo
    for desc, amt, loc in [("Online Electronics LTD", -2499.0, "Lagos"), ("Crypto Exchange XYZ", -1350.0, "Unknown")]:
        counter += 1
        txns.append(Transaction(f"T{counter:05d}", date.today() - timedelta(days=rng.randint(1, 5)),
                                desc, "shopping", amt, loc))
    return sorted(txns, key=lambda t: t.date)


def generate_customer(seed: int | None = None, name: str = "Alex Chen", age: int = 27,
                      income: float = 95000, goals: list[str] | None = None) -> Customer:
    rng = random.Random(settings.random_seed if seed is None else seed)
    everyday = Account("A1", "everyday", round(rng.uniform(1500, 6000), 2),
                       _make_transactions(rng, days=90, income=income))
    savings = Account("A2", "savings", round(rng.uniform(5000, 25000), 2))
    return Customer("C001", name, age, income, goals or ["home", "travel"], [everyday, savings])
