"""Refactored and documented order-summary implementation."""

from collections.abc import Iterable, Sequence

DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.10


def _calculate_line_total(quantity: float, unit_price: float) -> float:
    """Calculate a line total and apply the legacy discount when eligible."""
    line_total = quantity * unit_price
    if line_total > DISCOUNT_THRESHOLD:
        line_total *= 1 - DISCOUNT_RATE
    return line_total


def summarize_orders(
    orders: Iterable[Sequence[float | str]],
) -> dict[str, float]:
    """Summarize valid order rows using the original pricing rules.

    Each row must contain at least three values: an item label, quantity, and
    unit price. Rows with a non-positive quantity or negative price are ignored.
    A 10% discount applies to a line total strictly greater than 100.

    Args:
        orders: Iterable of order rows containing label, quantity, and price.

    Returns:
        A dictionary with the rounded total, units sold, and average price
        per sold unit. The average is zero when no valid units are sold.
    """
    total = 0.0
    units_sold = 0

    for order in orders:
        if len(order) <= 2:
            continue

        quantity = order[1]
        unit_price = order[2]
        if quantity > 0 and unit_price >= 0:
            total += _calculate_line_total(quantity, unit_price)
            units_sold += quantity

    average_price = total / units_sold if units_sold > 0 else 0
    return {
        "total": round(total, 2),
        "units": units_sold,
        "average": round(average_price, 2),
    }


if __name__ == "__main__":
    sample_orders = [
        ("Notebook", 2, 25.00),
        ("Desk", 1, 150.00),
        ("Invalid quantity", 0, 12.00),
    ]
    print(summarize_orders(sample_orders))
