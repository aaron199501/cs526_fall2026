"""Read the assignment's integer-list input without evaluating Python code."""

import ast
from pathlib import Path
import sys


def read_source(filename=None):
    """Read standard input by default, or a UTF-8 input file when supplied."""
    if filename is None:
        return sys.stdin.read().lstrip("\ufeff")
    return Path(filename).read_text(encoding="utf-8-sig")


def validate_integer_list(values, label="Input"):
    """Require a list of integers; booleans are not sale amounts or times."""
    if not isinstance(values, list):
        raise ValueError(f"{label} must be a list such as [8, 3, 5, 1].")
    if any(type(value) is not int for value in values):
        raise ValueError(f"{label} must contain only integers.")
    return values


def parse_integer_list(text, label="Input"):
    """Parse bracketed input safely, retaining its original element order."""
    try:
        values = ast.literal_eval(text.strip())
    except (SyntaxError, ValueError) as error:
        raise ValueError(f"{label} must be a list such as [8, 3, 5, 1].") from error
    return validate_integer_list(values, label)
