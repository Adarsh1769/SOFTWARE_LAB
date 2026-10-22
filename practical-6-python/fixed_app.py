"""Calculator that accepts only a small, allowlisted arithmetic syntax."""

import ast
import math
import operator
from typing import TypeAlias

Number: TypeAlias = int | float
MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 50
MAX_ABSOLUTE_VALUE = 1_000_000_000_000

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_node(node: ast.AST) -> Number:
    """Evaluate one already-parsed expression node from the arithmetic allowlist."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("only numeric literals are allowed")
        return _check_result(node.value)

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("unsupported arithmetic operator")
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        return _check_result(operation(left, right))

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("unsupported unary operator")
        return _check_result(operation(_evaluate_node(node.operand)))

    raise ValueError("only numeric arithmetic expressions are allowed")


def _check_result(value: Number) -> Number:
    """Reject non-finite results and values outside the calculator's size limit."""
    if not math.isfinite(value) or abs(value) > MAX_ABSOLUTE_VALUE:
        raise ValueError("result is outside the supported range")
    return value


def calculate(expression: str) -> Number:
    """Evaluate bounded arithmetic using numbers and +, -, *, and / only.

    Args:
        expression: An arithmetic expression no longer than 200 characters.

    Returns:
        The numeric result of the expression.

    Raises:
        TypeError: If expression is not a string.
        ValueError: If the expression is too long, too complex, unsupported,
            or produces a result outside the supported range.
        ZeroDivisionError: If the expression divides by zero.
    """
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("expression is too long")

    parsed = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(parsed)) > MAX_AST_NODES:
        raise ValueError("expression is too complex")
    return _evaluate_node(parsed.body)


if __name__ == "__main__":
    print(calculate("2 + 3 * 4"))
