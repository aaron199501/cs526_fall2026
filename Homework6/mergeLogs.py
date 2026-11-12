"""Merge sorted register logs with the linked priority queue from Problem 2."""

import argparse
import sys

from input_utils import parse_integer_list, read_source, validate_integer_list
from linkedHeap import BinaryMinHeap


def read_logs(text):
    """Read one register per line, retaining empty logs and their register IDs."""
    return [
        parse_integer_list(line, f"Register {number}")
        for number, line in enumerate(text.splitlines(), start=1)
    ]


def merge_logs(logs):
    """Return (time, register) pairs, ordered by time and then register ID.

    Only the earliest unprocessed sale from each nonempty register is in
    the queue. Extracting it frees that register's place before its next
    sale is inserted, so the queue never contains more than k entries.
    """
    queue = BinaryMinHeap()
    for register, log in enumerate(logs, start=1):
        validate_integer_list(log, f"Register {register}")
        for index in range(1, len(log)):
            if log[index] < log[index - 1]:
                raise ValueError(f"Register {register} must be in increasing order.")
        if log:
            queue.insert((log[0], register, 0))

    merged = []
    while not queue.is_empty():
        time, register, index = queue.extract_min()
        merged.append((time, register))
        next_index = index + 1
        log = logs[register - 1]
        if next_index < len(log):
            queue.insert((log[next_index], register, next_index))
    return merged


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="optional file; default: standard input")
    args = parser.parse_args(argv)
    try:
        logs = read_logs(read_source(args.input_file))
        merged = merge_logs(logs)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Registers: {len(logs)}")
    print(f"Total sales: {len(merged)}")
    print(f"Merged log: {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
