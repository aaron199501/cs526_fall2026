"""Check the current state of a symbol puzzle without filling its empty cells."""

import argparse
from math import isqrt
from pathlib import Path
import sys


def read_input(text: str) -> tuple[list[str], list[list[str]]]:
    """Read the listed symbols and n comma-separated board rows."""
    lines = text.lstrip("\ufeff").splitlines()
    n = int(lines[0])
    symbols = [value.strip() for value in lines[1].split(",")]
    board = [
        [value.strip() for value in line.split(",")]
        for line in lines[2:n + 2]
    ]
    return symbols, board


def is_valid_board(symbols: list[str], board: list[list[str]]) -> bool:
    """Check allowed symbols and uniqueness in every row, column, and box."""
    n = len(board)
    box_size = isqrt(n)
    allowed = set(symbols)
    rows = [set() for _ in range(n)]
    columns = [set() for _ in range(n)]
    boxes = [set() for _ in range(n)]

    for row in range(n):
        for column in range(n):
            symbol = board[row][column]
            if symbol == ".":
                continue

            box = (row // box_size) * box_size + column // box_size
            if (symbol not in allowed
                    or symbol in rows[row]
                    or symbol in columns[column]
                    or symbol in boxes[box]):
                return False

            rows[row].add(symbol)
            columns[column].add(symbol)
            boxes[box].add(symbol)

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_file", nargs="?",
        help="input filename; omit it to read from standard input",
    )
    args = parser.parse_args()
    text = (Path(args.input_file).read_text(encoding="utf-8-sig")
            if args.input_file else sys.stdin.read())
    symbols, board = read_input(text)
    print("The board is valid" if is_valid_board(symbols, board)
          else "The board is invalid")


if __name__ == "__main__":
    main()
