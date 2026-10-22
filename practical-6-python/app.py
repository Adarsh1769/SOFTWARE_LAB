"""Intentionally vulnerable calculator example for the static-analysis lab."""


def calculate(expression: str) -> object:
    """Evaluate an expression unsafely; do not use this with user input."""
    return eval(expression)


if __name__ == "__main__":
    print(calculate("2 + 3 * 4"))
