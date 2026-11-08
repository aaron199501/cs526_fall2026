"""Find a longest increasing sequence alternating between A and B.

Both values and original array positions must strictly increase, including
when moving from one array to the other. Positions printed by this program
are one-based, as in the assignment's example.

Usage: python longestSequence.py inputs/longest_seq1.txt
       python longestSequence.py inputs/longest_seq1.txt --show-sequence
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SequenceItem:
    """One selected input element, with its original one-based position."""

    source: str
    position: int
    value: int


class _FenwickMaximum:
    """Prefix maxima of (sequence length, endpoint ID), indexed from one."""

    def __init__(self, size: int) -> None:
        self._tree = [(0, -1)] * (size + 1)

    def query(self, rank: int) -> Tuple[int, int]:
        best = (0, -1)
        while rank > 0:
            if self._tree[rank][0] > best[0]:
                best = self._tree[rank]
            rank -= rank & -rank
        return best

    def update(self, rank: int, candidate: Tuple[int, int]) -> None:
        while rank < len(self._tree):
            if candidate[0] > self._tree[rank][0]:
                self._tree[rank] = candidate
            rank += rank & -rank


def longest_alternating_sequence(
    array_a: Sequence[int], array_b: Sequence[int]
) -> List[SequenceItem]:
    """Return an optimal sequence, including a witness of all three rules.

    With N = len(A) + len(B), time is O(N log N), including coordinate
    compression; storage is O(N). Either array may supply the first item.

    At position k, the best sequence ending at A[k] is one plus the best
    earlier B endpoint with a smaller value, and conversely for B[k]. Two
    Fenwick trees answer those prefix-maximum queries. Both candidates at k
    are computed before either is inserted, so an equal-position transition
    is impossible. Endpoint backpointers reconstruct an actual solution.
    """
    if not array_a and not array_b:
        return []

    distinct_values = sorted(set(array_a).union(array_b))
    ranks = {value: rank for rank, value in enumerate(distinct_values, 1)}
    trees = [_FenwickMaximum(len(ranks)), _FenwickMaximum(len(ranks))]
    # Each endpoint stores its input element and the preceding endpoint ID.
    endpoints: List[Tuple[SequenceItem, int]] = []
    best_length, best_endpoint = 0, -1

    for index in range(max(len(array_a), len(array_b))):
        pending = []
        for source_id, array in enumerate((array_a, array_b)):
            if index >= len(array):
                continue
            value = array[index]
            rank = ranks[value]
            previous_length, previous_endpoint = trees[1 - source_id].query(
                rank - 1
            )
            length = previous_length + 1
            endpoint_id = len(endpoints)
            item = SequenceItem("A" if source_id == 0 else "B", index + 1, value)
            endpoints.append((item, previous_endpoint))
            pending.append((source_id, rank, length, endpoint_id))
            if length > best_length:
                best_length, best_endpoint = length, endpoint_id

        # Delay both updates until both queries have excluded this position.
        for source_id, rank, length, endpoint_id in pending:
            trees[source_id].update(rank, (length, endpoint_id))

    result = []
    while best_endpoint != -1:
        item, best_endpoint = endpoints[best_endpoint]
        result.append(item)
    result.reverse()
    return result


def longest_sequence_length(array_a: Sequence[int], array_b: Sequence[int]) -> int:
    """Return the length required by the assignment's output format."""
    return len(longest_alternating_sequence(array_a, array_b))


def _integer_tokens(line: str, description: str) -> List[int]:
    tokens = line.split()
    if any(re.fullmatch(r"[+-]?[0-9]+", token) is None for token in tokens):
        raise ValueError("{} must contain only integers".format(description))
    try:
        return [int(token) for token in tokens]
    except ValueError as error:
        raise ValueError("{} contains an invalid integer".format(description)) from error


def parse_input(text: str) -> Tuple[List[int], List[int]]:
    """Validate the required four-line input, allowing blank empty arrays."""
    lines = text.splitlines()
    if len(lines) != 4:
        raise ValueError("expected exactly 4 input lines; found {}".format(len(lines)))

    sizes = []
    for number, source in enumerate(("A", "B")):
        tokens = _integer_tokens(lines[number], "size of {}".format(source))
        if len(tokens) != 1 or tokens[0] < 0:
            raise ValueError("size of {} must be one nonnegative integer".format(source))
        sizes.append(tokens[0])

    arrays = []
    for number, source in enumerate(("A", "B")):
        values = _integer_tokens(lines[number + 2], "array {}".format(source))
        if len(values) != sizes[number]:
            raise ValueError(
                "array {} declares {} values but contains {}".format(
                    source, sizes[number], len(values)
                )
            )
        arrays.append(values)
    return arrays[0], arrays[1]


def read_input_file(path: Path) -> Tuple[List[int], List[int]]:
    """Read UTF-8 input; a UTF-8 byte-order mark is accepted."""
    return parse_input(Path(path).read_text(encoding="utf-8-sig"))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_files", nargs="+", type=Path, help="four-line input file(s)")
    parser.add_argument(
        "--show-sequence", action="store_true", help="also show values and source/position witnesses"
    )
    arguments = parser.parse_args(argv)
    for number, path in enumerate(arguments.input_files):
        try:
            array_a, array_b = read_input_file(path)
            sequence = longest_alternating_sequence(array_a, array_b)
        except (OSError, UnicodeError, ValueError) as error:
            parser.exit(2, "error: {}: {}\n".format(path, error))
        if number:
            print()
        print("File Input: {}".format(path.name))
        print("Longest Sequence: {}".format(len(sequence)))
        if arguments.show_sequence:
            print("Sequence Values: {}".format(" ".join(str(item.value) for item in sequence)))
            print(
                "Sequence Witness: {}".format(
                    " -> ".join(
                        "{}[{}]={}".format(item.source, item.position, item.value)
                        for item in sequence
                    )
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
