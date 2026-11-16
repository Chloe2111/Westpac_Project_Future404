"""Core domain objects shared by every module."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Transaction:
    id: str
    date: date
    description: str
    category: str
    amount: float  # negative = money out, positive = money in
    merchant_location: str = "Brisbane"


@dataclass
class Account:
    id: str
    type: str  # "everyday", "savings", "credit_card", "home_loan"
    balance: float
    transactions: list[Transaction] = field(default_factory=list)


@dataclass
class Customer:
    id: str
    name: str
    age: int
    annual_income: float
    goals: list[str]
    accounts: list[Account] = field(default_factory=list)

    def all_transactions(self) -> list[Transaction]:
        return [t for a in self.accounts for t in a.transactions]


@dataclass
class Product:
    id: str
    name: str
    type: str
    description: str
    interest_rate: float
    eligibility: dict  # e.g. {"min_age": 18, "min_income": 0}
    tags: list[str] = field(default_factory=list)
