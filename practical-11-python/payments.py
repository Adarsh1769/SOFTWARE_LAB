"""Small payment total helper used by the Practical 11 CI example."""


def calculate_total(subtotal: float, tax_rate: float) -> float:
    """Return the amount payable after applying a fractional tax rate."""
    tax = subtotal * tax_rate
    return round(subtotal + tax, 2)
