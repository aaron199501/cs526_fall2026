"""Recursively find unique nonempty substrings and print them in sorted order."""

import sys


def unique_substrings(text: str) -> set[str]:
    """Search every start/end pair recursively, removing duplicates with a set.

    Both index ranges are split in half recursively. This visits all consecutive
    substrings without loops in the search and keeps recursion depth logarithmic
    in the input length instead of creating one call per substring.
    """
    found: set[str] = set()

    def search_ends(start: int, low: int, high: int) -> None:
        """Visit every exclusive end index in the half-open range [low, high)."""
        if low >= high:
            return
        if high - low == 1:
            found.add(text[start:low])
            return
        middle = (low + high) // 2
        search_ends(start, low, middle)
        search_ends(start, middle, high)

    def search_starts(low: int, high: int) -> None:
        """Visit every start index in the half-open range [low, high)."""
        if low >= high:
            return
        if high - low == 1:
            search_ends(low, low + 1, len(text) + 1)
            return
        middle = (low + high) // 2
        search_starts(low, middle)
        search_starts(middle, high)

    search_starts(0, len(text))
    return found


def main() -> None:
    """Preserve spaces and case, then print sorted substrings and their count."""
    text = sys.stdin.readline().rstrip("\r\n")
    found = unique_substrings(text)
    for substring in sorted(found):
        print(substring)
    print(len(found))


if __name__ == "__main__":
    main()
