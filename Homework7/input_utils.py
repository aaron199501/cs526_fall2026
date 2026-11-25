"""File input and terminal output shared by the four sorting programs."""

import argparse
from pathlib import Path
import re
import sys


def read_integers(path, non_negative=False):
    """Read exactly one integer per line and report the offending line on error."""
    values = []
    with Path(path).open(encoding="utf-8-sig") as source:
        for number, line in enumerate(source, start=1):
            token = line.strip()
            if re.fullmatch(r"[+-]?[0-9]+", token) is None:
                raise ValueError(f"line {number}: expected one integer")
            value = int(token)
            if non_negative and value < 0:
                raise ValueError(f"line {number}: radix sort requires a non-negative integer")
            values.append(value)
    return values


def print_values(label, values):
    """Print every value; wrapping is for readability and never truncates data."""
    print(f"{label} ({len(values)} values):")
    if not values:
        print("(empty)")
    for start in range(0, len(values), 20):
        print(" ".join(str(value) for value in values[start:start + 20]))


def run_sort_cli(sort_function, description, non_negative=False):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_file", help="text file containing one integer per line")
    args = parser.parse_args()
    try:
        values = read_integers(args.input_file, non_negative=non_negative)
        result = sort_function(values)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print_values("Input", values)
    print_values("Sorted", result)
    return 0
