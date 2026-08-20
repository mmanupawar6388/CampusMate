import ast
import operator
import re
from datetime import datetime, timedelta


# ---------------------------------------------------------
# SAFE CALCULATOR
# ---------------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid value")

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Operator not allowed")

        left = _eval_node(node.left)
        right = _eval_node(node.right)

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Operator not allowed")

        return operation(_eval_node(node.operand))

    raise ValueError("Invalid expression")


def calculate(expression):
    expression = expression.strip()

    if not expression:
        return "Please enter a calculation."

    if len(expression) > 100:
        return "Calculation is too long."

    tree = ast.parse(expression, mode="eval")

    result = _eval_node(tree.body)

    return str(result)


# ---------------------------------------------------------
# PERCENTAGE
# ---------------------------------------------------------

def percentage(value, total):
    if total == 0:
        return "Total cannot be zero."

    result = (value / total) * 100

    return f"{result:.2f}%"


# ---------------------------------------------------------
# STUDY PLAN
# ---------------------------------------------------------

def create_study_plan(subjects, days, hours_per_day):
    subjects = [s.strip() for s in subjects.split(",") if s.strip()]

    if not subjects:
        return "Please provide subjects separated by commas."

    try:
        days = int(days)
        hours_per_day = float(hours_per_day)
    except ValueError:
        return "Days and study hours must be numbers."

    if days <= 0:
        return "Days must be greater than zero."

    if hours_per_day <= 0:
        return "Study hours must be greater than zero."

    plan = []

    for day in range(1, days + 1):

        subject = subjects[(day - 1) % len(subjects)]

        next_subject = subjects[day % len(subjects)]

        plan.append(
            f"DAY {day}\n"
            f"• {subject}: {hours_per_day / 2:.1f} hours\n"
            f"• {next_subject}: {hours_per_day / 2:.1f} hours\n"
            f"• 15-minute revision at the end"
        )

    return "\n\n".join(plan)


# ---------------------------------------------------------
# DEADLINE HELPER
# ---------------------------------------------------------

def deadline_info(days):
    try:
        days = int(days)
    except ValueError:
        return "Enter the number of remaining days."

    if days < 0:
        return "Days cannot be negative."

    target = datetime.now() + timedelta(days=days)

    return (
        f"Approximate target date: "
        f"{target.strftime('%d %B %Y')}"
    )
