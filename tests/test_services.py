import json

from future404.ai.assistant import BankingAssistant
from future404.ai.tools import TOOL_DEFINITIONS, run_tool
from future404.data.synthetic import generate_customer
from future404.services import fraud, insights, recommender


def make_customer():
    return generate_customer(seed=1)


def test_spending_is_positive_and_sorted():
    spend = insights.spending_by_category(make_customer())
    values = list(spend.values())
    assert values and all(v > 0 for v in values)
    assert values == sorted(values, reverse=True)


def test_cash_flow_net_matches():
    flow = insights.cash_flow_summary(make_customer())
    assert round(flow["income"] - flow["spend"], 2) == flow["net"]


def test_recommendations_have_reasons():
    recs = recommender.recommend_products(make_customer())
    assert 0 < len(recs) <= 3
    assert all(r["why"] for r in recs)


def test_fraud_flags_injected_transactions():
    merchants = {a["merchant"] for a in fraud.detect_anomalies(make_customer())}
    assert "Online Electronics LTD" in merchants


def test_every_tool_runs():
    c = make_customer()
    for tool in TOOL_DEFINITIONS:
        args = {"keyword": "coles"} if tool["name"] == "search_transactions" else {}
        json.loads(run_tool(tool["name"], args, c))


def test_offline_assistant_answers():
    bot = BankingAssistant(make_customer())
    bot.client = None  # force offline mode
    assert "unusual" in bot.ask("any suspicious activity?").lower()
