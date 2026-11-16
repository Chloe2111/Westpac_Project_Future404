"""Personalised spending insights - turning raw transactions into advice."""

from collections import defaultdict
from datetime import date, timedelta

from future404.models import Customer


def spending_by_category(customer: Customer, days: int = 30) -> dict[str, float]:
    cutoff = date.today() - timedelta(days=days)
    totals: dict[str, float] = defaultdict(float)
    for t in customer.all_transactions():
        if t.amount < 0 and t.date >= cutoff:
            totals[t.category] += -t.amount
    return dict(sorted(((k, round(v, 2)) for k, v in totals.items()), key=lambda kv: -kv[1]))


def cash_flow_summary(customer: Customer, days: int = 30) -> dict[str, float]:
    cutoff = date.today() - timedelta(days=days)
    recent = [t for t in customer.all_transactions() if t.date >= cutoff]
    income = sum(t.amount for t in recent if t.amount > 0)
    spend = -sum(t.amount for t in recent if t.amount < 0)
    return {
        "income": round(income, 2),
        "spend": round(spend, 2),
        "net": round(income - spend, 2),
        "savings_rate_pct": round((income - spend) / income * 100, 1) if income else 0.0,
    }


def savings_tips(customer: Customer) -> list[str]:
    """Simple rule-based nudges. Replace/extend with ML or LLM-generated tips."""
    spend = spending_by_category(customer)
    flow = cash_flow_summary(customer)
    tips: list[str] = []
    if spend.get("dining", 0) > 300:
        tips.append(f"You spent ${spend['dining']:.0f} on dining this month. "
                    f"Cutting 25% would save about ${spend['dining'] * 0.25 * 12:.0f} a year.")
    if spend.get("subscriptions", 0) > 50:
        tips.append("Review your subscriptions - are you using all of them?")
    if flow["savings_rate_pct"] < 20:
        tips.append(f"Your savings rate is {flow['savings_rate_pct']}%. "
                    "Try an automatic transfer on payday to reach 20%.")
    if not tips:
        tips.append("Great work - your spending looks well balanced this month.")
    return tips
