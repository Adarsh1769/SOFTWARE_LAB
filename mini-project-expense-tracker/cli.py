"""Command-line interface for the personal expense tracker."""

import argparse
from datetime import date
from decimal import Decimal
from pathlib import Path

from models import Expense, parse_amount, parse_expense_date
from storage import load_expenses, save_expenses


DEFAULT_DATA_FILE = Path.home() / ".expense-tracker" / "expenses.json"


def build_parser():
    parser = argparse.ArgumentParser(description="Track personal expenses locally.")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"JSON storage path (default: {DEFAULT_DATA_FILE})",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="record an expense")
    add_command.add_argument("--amount", required=True)
    add_command.add_argument("--category", required=True)
    add_command.add_argument("--description", required=True)
    add_command.add_argument("--date", dest="expense_date")

    commands.add_parser("list", help="list recorded expenses")
    commands.add_parser("summary", help="show totals by category")
    return parser


def format_money(amount):
    """Format a Decimal amount to two places."""
    return f"{amount:.2f}"


def run(args):
    expenses = load_expenses(args.data_file)

    if args.command == "add":
        amount = parse_amount(args.amount)
        if not args.category.strip():
            raise ValueError("category must not be blank")
        if not args.description.strip():
            raise ValueError("description must not be blank")
        expense_date = (
            parse_expense_date(args.expense_date)
            if args.expense_date
            else date.today()
        )
        expense = Expense(
            amount=amount,
            category=args.category,
            description=args.description,
            date=expense_date,
        )
        expenses.append(expense)
        save_expenses(args.data_file, expenses)
        print(
            f"Added {format_money(expense.amount)} "
            f"for {expense.description} ({expense.category}) on {expense.date}."
        )
        return 0

    if args.command == "list":
        if not expenses:
            print("No expenses recorded.")
            return 0
        for expense in expenses:
            print(
                f"{expense.date} | {format_money(expense.amount)} | "
                f"{expense.category} | {expense.description}"
            )
        return 0

    if args.command == "summary":
        totals = {}
        for expense in expenses:
            totals[expense.category] = (
                totals.get(expense.category, Decimal("0")) + expense.amount
            )
        grand_total = sum(totals.values(), Decimal("0"))
        print(f"Total: {format_money(grand_total)}")
        if totals:
            print("By category:")
            for category in sorted(totals):
                print(f"  {category}: {format_money(totals[category])}")
        else:
            print("No expenses recorded.")
        return 0

    raise ValueError(f"unsupported command: {args.command}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
