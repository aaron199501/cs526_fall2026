"""Determine whether three consecutive days contain over half the snowfall."""

import argparse
from fractions import Fraction
from pathlib import Path
import sys


def has_heavy_three_days(cumulative):
    """Return whether any three-day total is strictly over half the total."""
    if len(cumulative) < 3:
        return False

    total = cumulative[-1]
    for end in range(2, len(cumulative)):
        # Subtract the cumulative amount just before this three-day window.
        before_window = cumulative[end - 3] if end >= 3 else 0
        window_total = cumulative[end] - before_window
        if 2 * window_total > total:
            return True
    return False


def read_input(text):
    """Read the day count and its cumulative snowfall values from input text."""
    values = text.lstrip("\ufeff").split()
    number_of_days = int(values[0])
    return [Fraction(value) for value in values[1:number_of_days + 1]]


def main():
    """Read a file or standard input, then print the required result line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="input file; omit to use stdin")
    args = parser.parse_args()

    if args.input_file:
        text = Path(args.input_file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    cumulative = read_input(text)
    answer = "YES" if has_heavy_three_days(cumulative) else "NO"
    # Keep the input's numeric spelling, such as 1.50, in the output.
    original_values = text.lstrip("\ufeff").split()[1:len(cumulative) + 1]
    input_values = " ".join(original_values)
    print(f"{input_values} solution: {answer}")


if __name__ == "__main__":
    main()
