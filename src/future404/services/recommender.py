"""Next-best-product recommendations based on customer profile and behaviour."""

from future404.data.products import PRODUCTS
from future404.models import Customer, Product
from future404.services.insights import cash_flow_summary


def _eligible(customer: Customer, p: Product) -> bool:
    e = p.eligibility
    return (customer.age >= e.get("min_age", 0)
            and customer.age <= e.get("max_age", 200)
            and customer.annual_income >= e.get("min_income", 0))


def recommend_products(customer: Customer, top_n: int = 3) -> list[dict]:
    """Score eligible products; return the best matches with an explanation.

    Explainability matters in banking: every recommendation carries a reason.
    """
    owned_types = {a.type for a in customer.accounts}
    flow = cash_flow_summary(customer)
    results = []
    for p in PRODUCTS:
        if not _eligible(customer, p):
            continue
        score, reasons = 0.0, []
        goal_hits = set(p.tags) & set(customer.goals)
        if goal_hits:
            score += 2 * len(goal_hits)
            reasons.append(f"matches your goal(s): {', '.join(sorted(goal_hits))}")
        if p.type not in owned_types:
            score += 0.5
        if p.type == "savings" and flow["net"] > 500:
            score += 1
            reasons.append("you have surplus cash each month")
        if score > 0:
            results.append({"product": p.name, "type": p.type, "rate": p.interest_rate,
                            "score": round(score, 2),
                            "why": "; ".join(reasons) or "a good fit for your profile"})
    return sorted(results, key=lambda r: -r["score"])[:top_n]
