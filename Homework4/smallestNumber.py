"""Problem 2: fewest array elements with sum strictly greater than a target."""

import argparse
from fractions import Fraction
from pathlib import Path


def _number(token):
    """Keep integer inputs fast; accept exact finite decimal inputs as well."""
    try:
        return int(token)
    except ValueError:
        return Fraction(token)


def read_input(path):
    tokens = Path(path).read_text(encoding="utf-8-sig").split()
    if len(tokens) < 2:
        raise ValueError("expected an element count, target, and array values")
    n = int(tokens[0])
    if n < 0 or len(tokens) != n + 2:
        raise ValueError("element count does not match the array")
    return [_number(value) for value in tokens[2:]], _number(tokens[1])


def smallest_number(values, target):
    """Return the minimum size of a nonempty selection, or None if impossible.

    Elements need not be adjacent. Sorting a copy preserves the original array.
    For each k, the k largest elements have the greatest sum of any k elements.
    """
    total = 0
    for count, value in enumerate(sorted(values, reverse=True), start=1):
        total += value
        if total > target:
            return count
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="file containing n, target, and n values")
    args = parser.parse_args(argv)
    try:
        values, target = read_input(args.input_file)
    except (OSError, ValueError, ZeroDivisionError) as error:
        parser.error(str(error))
    answer = smallest_number(values, target)
    displayed_answer = answer if answer is not None else "No solution"
    print(f"Input: {','.join(map(str, values))} Target: {target} Answer: {displayed_answer}")


if __name__ == "__main__":
    main()
