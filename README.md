# Future404: AI-Reshaped Banking

**Challenge question:** How can AI reshape the way customers interact with their bank, and how banks deliver products and services?

This prototype shows four AI-driven experiences, all built on one shared customer data model:

| Experience | What changes for the customer | Module |
|---|---|---|
| 💬 Conversational banking | Ask questions in plain English instead of navigating menus | `src/future404/ai/assistant.py` |
| 📊 Personalised insights | The bank explains your money and nudges you toward better habits | `src/future404/services/insights.py` |
| 🎯 Next-best product | Products come to you, matched to your goals, with a reason for each | `src/future404/services/recommender.py` |
| 🚨 Proactive protection | Unusual transactions get flagged before you notice them | `src/future404/services/fraud.py` |

## Project structure

```
src/future404/
  config.py            settings from env / .env
  models.py            Customer, Account, Transaction, Product
  data/
    synthetic.py       fake customer and transaction generator (no real data)
    products.py        fictional product catalogue
  services/            plain-Python business logic (testable, no AI needed)
    insights.py
    recommender.py
    fraud.py
  ai/
    tools.py           services exposed to Claude as tools
    assistant.py       Claude tool-use loop + offline fallback
app/streamlit_app.py   demo UI
tests/                 pytest suite
```

**Design idea:** services hold the logic, and the AI layer only *calls* them through tools. The assistant can't make up balances, and every action can be audited. That's a key point for a bank.

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt

copy .env.example .env          # then add your ANTHROPIC_API_KEY (optional)
streamlit run app/streamlit_app.py
pytest
```

Without an API key, the assistant runs in **offline mode** (keyword-based answers), so everyone can develop and demo it.

## Suggested next steps / team split

- **Data:** richer synthetic personas (student, family, retiree, small business), or the CDR / Open Banking sample data
- **ML:** replace the z-score fraud check with an IsolationForest; add ML-based transaction categorisation
- **AI:** add goal planning ("save $20k for a house by 2028"), voice input, multilingual support
- **Product:** add a bank-side view (relationship-manager dashboard and product-uptake analytics)
- **Responsible AI:** explainability, human handoff, privacy, and the line between general information and financial advice
