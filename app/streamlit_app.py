"""Demo UI. Run with:  streamlit run app/streamlit_app.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from future404.ai.assistant import BankingAssistant  # noqa: E402
from future404.data.synthetic import generate_customer  # noqa: E402
from future404.services import fraud, insights, recommender  # noqa: E402

st.set_page_config(page_title="Future404 Bank", page_icon="🏦", layout="wide")

if "customer" not in st.session_state:
    st.session_state.customer = generate_customer()
    st.session_state.assistant = BankingAssistant(st.session_state.customer)
    st.session_state.chat = []

customer = st.session_state.customer
assistant: BankingAssistant = st.session_state.assistant

st.title("🏦 Future404 - AI-powered banking")
st.caption(f"Signed in as {customer.name} · "
           f"{'Claude AI online' if assistant.online else 'Offline mode (no API key)'}")

cols = st.columns(len(customer.accounts) + 1)
for col, acct in zip(cols, customer.accounts):
    col.metric(acct.type.title(), f"${acct.balance:,.2f}")
flow = insights.cash_flow_summary(customer)
cols[-1].metric("Savings rate (30d)", f"{flow['savings_rate_pct']}%")

tab_chat, tab_insights, tab_products, tab_alerts = st.tabs(
    ["💬 Assistant", "📊 Insights", "🎯 For you", "🚨 Alerts"])

with tab_chat:
    for role, text in st.session_state.chat:
        st.chat_message(role).markdown(text)
    if prompt := st.chat_input("Ask about your money, e.g. 'Where did my money go this month?'"):
        st.chat_message("user").markdown(prompt)
        with st.spinner("Thinking..."):
            reply = assistant.ask(prompt)
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat += [("user", prompt), ("assistant", reply)]

with tab_insights:
    spend = insights.spending_by_category(customer)
    st.subheader("Spending by category (last 30 days)")
    st.bar_chart(pd.Series(spend, name="AUD"))
    st.subheader("Personalised tips")
    for tip in insights.savings_tips(customer):
        st.info(tip)

with tab_products:
    st.subheader("Recommended for your goals")
    for rec in recommender.recommend_products(customer):
        st.success(f"**{rec['product']}** ({rec['type']}, {rec['rate']}%) - {rec['why']}")
    st.caption("General information only - not financial advice.")

with tab_alerts:
    alerts = fraud.detect_anomalies(customer)
    if not alerts:
        st.write("No unusual activity. ✅")
    for a in alerts:
        box = st.error if a["risk"] == "high" else st.warning
        box(f"**{a['merchant']}** ${a['amount']:,.2f} on {a['date']} - {'; '.join(a['reasons'])}")
