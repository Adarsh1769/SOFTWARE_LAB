"""Validated expense data model and JSON conversion."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import re


ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class Expense:
    amount: Decimal
    category: str
    description: str
    date: date

    def __post_init__(self):
        if not self.amount.is_finite() or self.amount <= 0:
            raise ValueError("amount must be a finite number greater than zero")
        if not self.category.strip():
            raise ValueError("category must not be blank")
        if not self.description.strip():
            raise ValueError("description must not be blank")

    def to_dict(self):
        """Convert this expense to its JSON-compatible representation."""
        return {
            "amount": str(self.amount),
            "category": self.category.strip(),
            "description": self.description.strip(),
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        """Build an expense from validated stored JSON fields."""
        if not isinstance(data, dict):
            raise ValueError("each stored expense must be a JSON object")
        expected = {"amount", "category", "description", "date"}
        if set(data) != expected:
            raise ValueError(
                "stored expense must contain exactly amount, category, "
                "description, and date"
            )
        if not all(isinstance(data[field], str) for field in expected):
            raise ValueError("all stored expense fields must be strings")
        try:
            amount = Decimal(data["amount"])
            expense_date = date.fromisoformat(data["date"])
        except (InvalidOperation, ValueError) as error:
            raise ValueError(f"stored expense has invalid amount or date: {error}") from error
        return cls(
            amount=amount,
            category=data["category"],
            description=data["description"],
            date=expense_date,
        )


def parse_amount(value):
    """Parse a positive finite monetary amount from command-line text."""
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise ValueError("amount must be a valid decimal number") from error
    if not amount.is_finite() or amount <= 0:
        raise ValueError("amount must be a finite number greater than zero")
    return amount


def parse_expense_date(value):
    """Parse an ISO calendar date."""
    if not ISO_DATE_PATTERN.fullmatch(value):
        raise ValueError("date must be a valid YYYY-MM-DD date")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("date must be a valid YYYY-MM-DD date") from error
