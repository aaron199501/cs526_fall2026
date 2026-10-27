"""Simulate the synchronous spread of infection on a square grid."""

import argparse
from pathlib import Path
import sys


def read_input(text):
    """Return the grid size and the initially infected (row, column) pairs."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    n = int(lines[0])
    initial = [tuple(map(int, line.split())) for line in lines[1:]]
    return n, initial


def print_board(board, day):
    """Display one day; X means infected and . means healthy."""
    print(f"Day {day}")
    for row in board:
        print(" ".join("X" if cell else "." for cell in row))
    print()


def simulate(n, initial, show_days=False):
    """Return the final Boolean grid, applying every day's changes together.

    True means infected. The initial configuration is Day 1. When show_days
    is True, print the initial board and each subsequent changed board.
    """
    board = [[False] * n for _ in range(n)]
    for row, column in initial:
        board[row][column] = True

    day = 1
    if show_days:
        print_board(board, day)

    while True:
        newly_infected = []
        for row in range(n):
            for column in range(n):
                if board[row][column]:
                    continue

                infected_neighbors = 0
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    neighbor_row = row + dr
                    neighbor_column = column + dc
                    if (0 <= neighbor_row < n
                            and 0 <= neighbor_column < n
                            and board[neighbor_row][neighbor_column]):
                        infected_neighbors += 1

                if infected_neighbors >= 2:
                    newly_infected.append((row, column))

        if not newly_infected:
            return board

        # No board cell changes during the scan above. Thus, counties added
        # here cannot contribute to another county's count until the next day.
        for row, column in newly_infected:
            board[row][column] = True

        day += 1
        if show_days:
            print_board(board, day)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="input filename; omit for stdin")
    parser.add_argument("--show-days", action="store_true", help="print daily boards")
    args = parser.parse_args()

    if args.input_file:
        text = Path(args.input_file).read_text(encoding="utf-8-sig")
    else:
        text = sys.stdin.read().lstrip("\ufeff")

    n, initial = read_input(text)
    board = simulate(n, initial, args.show_days)
    if any(not cell for row in board for cell in row):
        print("There are healthy counties left")
    else:
        print("There are no healthy counties left")


if __name__ == "__main__":
    main()
