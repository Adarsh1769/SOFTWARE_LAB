"""Compare the legacy and refactored order summaries on the same sample."""

from clean import summarize_orders
from messy import process


def main() -> None:
    orders = [
        ("Notebook", 2, 25.00),
        ("Desk", 1, 150.00),
        ("Invalid quantity", 0, 12.00),
        ("Invalid price", 1, -5.00),
        ("Incomplete row", 10),
    ]
    original_result = process(orders)
    refactored_result = summarize_orders(orders)

    print(f"Original:   {original_result}")
    print(f"Refactored: {refactored_result}")
    print(f"Behavior preserved: {original_result == refactored_result}")


if __name__ == "__main__":
    main()
