"""Compute each running median using two instances of the Problem 2 heap."""

import argparse
import sys

from input_utils import parse_integer_list, read_source
from linkedHeap import BinaryMinHeap


class RunningMedian:
    """Keep the lower half in a negated min-heap and upper half in a min-heap.

    After every addition, lower has either the same size as upper or one
    extra value. Every lower-half value is at most every upper-half value.
    These two conditions make the median available from the roots in O(1).
    """

    def __init__(self):
        self.lower = BinaryMinHeap()
        self.upper = BinaryMinHeap()

    def add(self, value):
        """Insert an integer amount, rebalance, and return the current median."""
        if type(value) is not int:
            raise ValueError("Sale amounts must be integers.")
        if self.lower.is_empty() or value <= -self.lower.peek():
            self.lower.insert(-value)
        else:
            self.upper.insert(value)

        if len(self.lower) > len(self.upper) + 1:
            self.upper.insert(-self.lower.extract_min())
        elif len(self.upper) > len(self.lower):
            self.lower.insert(-self.upper.extract_min())
        return self.median()

    def median(self):
        """Return the median in O(1); an empty stream has no median."""
        if self.lower.is_empty():
            raise IndexError("The median of an empty stream is undefined.")
        if len(self.lower) == len(self.upper):
            return (-self.lower.peek() + self.upper.peek()) / 2.0
        return float(-self.lower.peek())


def running_medians(values):
    """Return one median for each prefix, preserving the arrival order."""
    stream = RunningMedian()
    return [stream.add(value) for value in values]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="optional file; default: standard input")
    args = parser.parse_args(argv)
    try:
        values = parse_integer_list(read_source(args.input_file), "Sale amounts")
        medians = running_medians(values)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(medians)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
