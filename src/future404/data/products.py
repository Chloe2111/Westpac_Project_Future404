"""Illustrative product catalogue (fictional products and rates)."""

from future404.models import Product

PRODUCTS: list[Product] = [
    Product("P01", "Smart Saver", "savings",
            "High-interest savings that rewards growing your balance each month.",
            4.75, {"min_age": 14, "min_income": 0}, ["save", "emergency_fund", "travel"]),
    Product("P02", "First Home Saver", "savings",
            "Bonus interest for customers saving toward a home deposit.",
            5.10, {"min_age": 18, "max_age": 45, "min_income": 30000}, ["home", "save"]),
    Product("P03", "Low Rate Card", "credit_card",
            "Low ongoing purchase rate for customers who sometimes carry a balance.",
            12.99, {"min_age": 18, "min_income": 25000}, ["debt", "credit"]),
    Product("P04", "Rewards Card", "credit_card",
            "Points on everyday spend and complimentary travel insurance.",
            20.99, {"min_age": 18, "min_income": 60000}, ["travel", "rewards"]),
    Product("P05", "Green Home Loan", "home_loan",
            "Discounted variable rate for energy-efficient homes.",
            5.89, {"min_age": 18, "min_income": 50000}, ["home", "sustainability"]),
    Product("P06", "Micro-Invest", "investment",
            "Round up everyday purchases and invest the spare change.",
            0.0, {"min_age": 18, "min_income": 0}, ["invest", "save"]),
]
