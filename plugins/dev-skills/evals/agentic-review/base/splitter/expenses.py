from dataclasses import dataclass

from .money import parse_amount


@dataclass
class Expense:
    payer: str
    amount_cents: int
    description: str


def load_expenses(rows):
    """rows: iterable of (payer, amount text, description) as typed by trip members."""
    return [Expense(payer, parse_amount(amount), description) for payer, amount, description in rows]


def total_paid(expenses):
    """How much each payer has paid, in cents."""
    totals = {}
    for expense in expenses:
        totals[expense.payer] = totals.get(expense.payer, 0) + expense.amount_cents
    return totals
