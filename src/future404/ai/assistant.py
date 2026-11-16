"""Conversational banking assistant powered by Claude, with an offline fallback."""

from __future__ import annotations

from future404.ai.tools import TOOL_DEFINITIONS, run_tool
from future404.config import settings
from future404.models import Customer
from future404.services import fraud, insights, recommender

SYSTEM_PROMPT = """You are Future404, a friendly digital banking assistant for an Australian bank.
Help the customer understand their money, spot risks, and find products that fit their goals.

- Use the tools to fetch facts; never invent balances, transactions or rates.
- Keep answers short, plain-English, and in AUD.
- When suggesting products, explain why they fit. This is general information, not financial advice.
- You cannot move money. If asked, explain the customer can do it in the app.
- If a transaction looks fraudulent, advise them to lock their card and contact the bank."""

MAX_TOOL_ROUNDS = 8


class BankingAssistant:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.messages: list[dict] = []
        self.client = None
        if settings.ai_enabled:
            import anthropic

            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    @property
    def online(self) -> bool:
        return self.client is not None

    def ask(self, user_text: str) -> str:
        if not self.online:
            return self._offline_answer(user_text)
        self.messages.append({"role": "user", "content": user_text})
        return self._run_loop()

    # ---- Claude tool-use loop -------------------------------------------------
    def _run_loop(self) -> str:
        for _ in range(MAX_TOOL_ROUNDS):
            response = self.client.beta.messages.create(
                model=settings.model,
                max_tokens=16000,
                system=f"{SYSTEM_PROMPT}\n\nCustomer name: {self.customer.name}",
                tools=TOOL_DEFINITIONS,
                messages=self.messages,
                output_config={"effort": "medium"},
                # If a safety classifier declines, the API retries on a fallback model.
                betas=["server-side-fallback-2026-07-01"],
                extra_body={"fallbacks": "default"},
            )
            # Keep the full content (incl. thinking blocks) so the history stays valid.
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "refusal":
                return "Sorry, I can't help with that request."
            if response.stop_reason == "pause_turn":
                continue
            if response.stop_reason != "tool_use":
                return "".join(b.text for b in response.content if b.type == "text").strip()

            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                try:
                    content = run_tool(block.name, block.input, self.customer)
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": content})
                except Exception as exc:  # report tool errors back to the model
                    results.append({"type": "tool_result", "tool_use_id": block.id,
                                    "content": f"Error: {exc}", "is_error": True})
            self.messages.append({"role": "user", "content": results})
        return "Sorry, that took too many steps. Could you rephrase?"

    # ---- Offline fallback (no API key) -----------------------------------------
    def _offline_answer(self, text: str) -> str:
        t = text.lower()
        c = self.customer
        if any(w in t for w in ("fraud", "suspicious", "scam", "unusual")):
            alerts = fraud.detect_anomalies(c)
            if not alerts:
                return "No unusual activity found."
            lines = [f"- {a['date']} {a['merchant']} ${a['amount']:.2f} ({a['risk']} risk)" for a in alerts]
            return "I found these unusual transactions:\n" + "\n".join(lines)
        if any(w in t for w in ("spend", "spent", "category", "budget")):
            s = insights.spending_by_category(c)
            return "Last 30 days spending:\n" + "\n".join(f"- {k}: ${v:,.2f}" for k, v in s.items())
        if any(w in t for w in ("save", "saving", "tip")):
            return "\n".join(f"- {tip}" for tip in insights.savings_tips(c))
        if any(w in t for w in ("product", "recommend", "card", "loan")):
            recs = recommender.recommend_products(c)
            return "\n".join(f"- {r['product']} ({r['rate']}%): {r['why']}" for r in recs)
        if any(w in t for w in ("balance", "how much", "accounts")):
            return "\n".join(f"- {a.type}: ${a.balance:,.2f}" for a in c.accounts)
        return ("(Offline mode - set ANTHROPIC_API_KEY for full AI.) "
                "Try asking about your balance, spending, savings tips, products, or suspicious activity.")
