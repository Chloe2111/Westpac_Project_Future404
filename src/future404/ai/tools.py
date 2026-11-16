"""Bank capabilities exposed to the AI assistant as tools.

The model never touches data directly - it can only call these functions,
which keeps behaviour auditable and easy to permission (e.g. read-only today,
transfers behind explicit confirmation later).
"""

import json

from future404.models import Customer
from future404.services import fraud, insights, recommender


def _obj(props: dict | None = None, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": props or {}, "required": required or [],
            "additionalProperties": False}


TOOL_DEFINITIONS: list[dict] = [
    {"name": "get_accounts", "description": "List the customer's accounts and current balances.",
     "input_schema": _obj()},
    {"name": "get_spending_by_category",
     "description": "Total spending per category over the last N days.",
     "input_schema": _obj({"days": {"type": "integer", "description": "Look-back window, default 30"}})},
    {"name": "get_cash_flow", "description": "Income, spend, net and savings rate over the last N days.",
     "input_schema": _obj({"days": {"type": "integer", "description": "Look-back window, default 30"}})},
    {"name": "get_savings_tips", "description": "Personalised tips to save money.",
     "input_schema": _obj()},
    {"name": "recommend_products",
     "description": "Suggest bank products that fit the customer's goals, with reasons.",
     "input_schema": _obj()},
    {"name": "get_fraud_alerts",
     "description": "Recent transactions flagged as unusual or potentially fraudulent.",
     "input_schema": _obj()},
    {"name": "search_transactions",
     "description": "Find transactions whose description or category contains a keyword.",
     "input_schema": _obj({"keyword": {"type": "string"}}, ["keyword"])},
]


def run_tool(name: str, args: dict, customer: Customer) -> str:
    """Execute a tool and return a JSON string result."""
    if name == "get_accounts":
        out = [{"id": a.id, "type": a.type, "balance": a.balance} for a in customer.accounts]
    elif name == "get_spending_by_category":
        out = insights.spending_by_category(customer, int(args.get("days", 30)))
    elif name == "get_cash_flow":
        out = insights.cash_flow_summary(customer, int(args.get("days", 30)))
    elif name == "get_savings_tips":
        out = insights.savings_tips(customer)
    elif name == "recommend_products":
        out = recommender.recommend_products(customer)
    elif name == "get_fraud_alerts":
        out = fraud.detect_anomalies(customer)
    elif name == "search_transactions":
        kw = str(args["keyword"]).lower()
        out = [{"date": t.date.isoformat(), "description": t.description, "amount": t.amount}
               for t in customer.all_transactions()
               if kw in t.description.lower() or kw in t.category.lower()][-20:]
    else:
        raise ValueError(f"Unknown tool: {name}")
    return json.dumps(out, default=str)
