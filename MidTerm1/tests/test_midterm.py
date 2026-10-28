"""Independent examples, boundary cases, and reference comparisons."""

import contextlib
from collections import deque
from fractions import Fraction
import importlib.util
import io
from itertools import accumulate
from pathlib import Path
import random
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snowfall = load_module("snowfall", "snowfall.py")
pandemic = load_module("pandemic", "pandemic.py")
puzzle = load_module("puzzle_game", "puzzle_game.py")


def run_program(relative, filename=None, text=None, extra=()):
    command = [sys.executable, "-B", str(ROOT / relative)]
    if filename is not None:
        command.append(str(ROOT / filename))
    command.extend(extra)
    result = subprocess.run(command, input=text, text=True,
                            capture_output=True, cwd=ROOT, check=True)
    if result.stderr:
        raise AssertionError(result.stderr)
    return result.stdout


def infection_closure(n, initial):
    """Independent event-driven oracle for the final monotone closure.

    This oracle does not simulate daily scans. Daily synchrony is tested
    separately against the explicit assignment boards.
    """
    infected = set(initial)
    pending = deque(infected)
    counts = {}
    while pending:
        row, column = pending.popleft()
        for neighbor in ((row - 1, column), (row + 1, column),
                         (row, column - 1), (row, column + 1)):
            r, c = neighbor
            if 0 <= r < n and 0 <= c < n and neighbor not in infected:
                counts[neighbor] = counts.get(neighbor, 0) + 1
                if counts[neighbor] == 2:
                    infected.add(neighbor)
                    pending.append(neighbor)
    return [[(r, c) in infected for c in range(n)] for r in range(n)]


def puzzle_reference(symbols, board):
    """Collect complete regions and compare every pair of filled cells."""
    n = len(board)
    width = int(n ** 0.5)
    if any(value != "." and value not in symbols
           for row in board for value in row):
        return False
    regions = [list(row) for row in board]
    regions.extend(list(column) for column in zip(*board))
    for top in range(0, n, width):
        for left in range(0, n, width):
            regions.append([board[r][c]
                            for r in range(top, top + width)
                            for c in range(left, left + width)])
    for region in regions:
        values = [value for value in region if value != "."]
        for first in range(len(values)):
            for second in range(first + 1, len(values)):
                if values[first] == values[second]:
                    return False
    return True


class SnowfallTests(unittest.TestCase):
    def test_all_five_original_files(self):
        for number, answer in enumerate(("YES", "NO", "NO", "YES", "YES"), 1):
            relative = f"inputs/snowfall_input{number}.txt"
            tokens = (ROOT / relative).read_text().split()
            expected = " ".join(tokens[1:]) + f" solution: {answer}\n"
            with self.subTest(number=number):
                self.assertEqual(run_program("snowfall.py",
                                             relative), expected)

    def test_fewer_than_three_days(self):
        for values in ([], [7], [7, 15]):
            self.assertFalse(snowfall.has_heavy_three_days(values))

    def test_first_window_only(self):
        self.assertTrue(snowfall.has_heavy_three_days([6, 7, 8, 8, 8, 10]))

    def test_last_window_only(self):
        self.assertTrue(snowfall.has_heavy_three_days([0, 0, 0, 0, 0, 10]))

    def test_exact_half_and_zero(self):
        self.assertFalse(snowfall.has_heavy_three_days([3, 8, 14, 19, 21, 24, 25, 25, 32]))
        self.assertFalse(snowfall.has_heavy_three_days([0, 0, 0, 0]))

    def test_decimal_exactness_and_original_output(self):
        for tokens, answer in (("0.1 0.3 0.3 0.4 0.6 0.6", "NO"),
                               ("0.1 0.310 0.310 0.4 0.6 0.6", "YES")):
            self.assertEqual(run_program("snowfall.py",
                                         text="6\n" + tokens + "\n"),
                             tokens + f" solution: {answer}\n")
        self.assertEqual(snowfall.read_input("\ufeff3\n1.50 2.0 3.0\n")[0],
                         Fraction(3, 2))

    def test_large_integers(self):
        large = 10 ** 100
        self.assertFalse(snowfall.has_heavy_three_days([large] * 3 + [2 * large]))
        self.assertTrue(snowfall.has_heavy_three_days([large + 1] * 3 + [2 * large + 1]))

    def test_300_random_daily_arrays_against_direct_sums(self):
        randomizer = random.Random(52601)
        for _ in range(300):
            daily = [randomizer.randrange(20)
                     for _ in range(randomizer.randrange(21))]
            expected = any(2 * sum(daily[start:start + 3]) > sum(daily)
                           for start in range(len(daily) - 2))
            self.assertEqual(snowfall.has_heavy_three_days(list(accumulate(daily))),
                             expected, daily)


class PandemicTests(unittest.TestCase):
    def test_original_files_and_exact_final_lines(self):
        messages = ("There are healthy counties left\n",
                    "There are no healthy counties left\n")
        for number, expected in enumerate(messages, 1):
            with self.subTest(number=number):
                self.assertEqual(run_program("pandemic.py",
                                             f"inputs/pandemic_input{number}.txt"),
                                 expected)

    def test_empty_and_fully_infected(self):
        self.assertEqual(pandemic.simulate(3, []), [[False] * 3 for _ in range(3)])
        full = [(r, c) for r in range(3) for c in range(3)]
        self.assertEqual(pandemic.simulate(3, full), [[True] * 3 for _ in range(3)])

    def test_one_county_states(self):
        self.assertEqual(pandemic.simulate(1, []), [[False]])
        self.assertEqual(pandemic.simulate(1, [(0, 0)]), [[True]])

    def test_single_infection_cannot_spread(self):
        board = pandemic.simulate(4, [(1, 1)])
        self.assertEqual(sum(map(sum, board)), 1)

    def test_diagonals_do_not_count_as_neighbors(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            pandemic.simulate(3, [(0, 0), (2, 2)], show_days=True)
        self.assertEqual(output.getvalue(), "Day 1\nX . .\n. . .\n. . X\n\n")

    def test_daily_synchrony_matches_assignment(self):
        expected = (
            "Day 1\n. . . . .\n. . . X .\n. . X . .\n. . . . X\n. . . . .\n\n"
            "Day 2\n. . . . .\n. . X X .\n. . X X .\n. . . . X\n. . . . .\n\n"
            "Day 3\n. . . . .\n. . X X .\n. . X X X\n. . . X X\n. . . . .\n\n"
            "Day 4\n. . . . .\n. . X X X\n. . X X X\n. . X X X\n. . . . .\n\n"
            "There are healthy counties left\n"
        )
        self.assertEqual(run_program("pandemic.py",
                                     "inputs/pandemic_input1.txt",
                                     extra=("--show-days",)), expected)

    def test_all_two_by_two_initial_states(self):
        cells = [(r, c) for r in range(2) for c in range(2)]
        for mask in range(16):
            initial = [cell for i, cell in enumerate(cells) if mask & (1 << i)]
            self.assertEqual(pandemic.simulate(2, initial), infection_closure(2, initial))

    def test_250_random_grids_against_event_driven_closure(self):
        randomizer = random.Random(52602)
        for _ in range(250):
            n = randomizer.randrange(1, 8)
            initial = [(r, c) for r in range(n) for c in range(n)
                       if randomizer.random() < 0.3]
            self.assertEqual(pandemic.simulate(n, initial), infection_closure(n, initial))

    def test_standard_input(self):
        self.assertEqual(run_program("pandemic.py", text="1\n"),
                         "There are healthy counties left\n")


class PuzzleTests(unittest.TestCase):
    @staticmethod
    def blank(n=4):
        return [["."] * n for _ in range(n)]

    def test_all_four_original_files(self):
        for number, valid in enumerate((True, False, True, False), 1):
            with self.subTest(number=number):
                self.assertEqual(run_program("puzzle_game.py",
                                             f"inputs/puzzle_game_input{number}.txt"),
                                 "The board is valid\n" if valid else "The board is invalid\n")

    def test_empty_boards_and_single_cell(self):
        for n in (1, 4, 9, 16):
            self.assertTrue(puzzle.is_valid_board([str(i) for i in range(n)], self.blank(n)))
        self.assertTrue(puzzle.is_valid_board(["@"], [["@"]]))

    def test_row_only_duplicate(self):
        board = self.blank()
        board[0][0] = board[0][2] = "@"
        self.assertFalse(puzzle.is_valid_board(list("@#&*"), board))

    def test_column_only_duplicate(self):
        board = self.blank()
        board[0][0] = board[2][0] = "@"
        self.assertFalse(puzzle.is_valid_board(list("@#&*"), board))

    def test_box_only_duplicate(self):
        board = self.blank()
        board[0][0] = board[1][1] = "@"
        self.assertFalse(puzzle.is_valid_board(list("@#&*"), board))

    def test_unlisted_symbol(self):
        board = self.blank()
        board[2][3] = "?"
        self.assertFalse(puzzle.is_valid_board(list("@#&*"), board))
        self.assertEqual(run_program("puzzle_game.py",
                                     text="1\n@\n?\n"), "The board is invalid\n")

    def test_repetition_in_unrelated_regions_is_valid(self):
        board = self.blank()
        board[0][0] = board[2][2] = "@"
        self.assertTrue(puzzle.is_valid_board(list("@#&*"), board))

    def test_complete_valid_boards_and_200_partial_boards(self):
        randomizer = random.Random(52603)
        for n, width in ((4, 2), (9, 3), (16, 4)):
            symbols = [str(i) for i in range(n)]
            board = [[symbols[(r * width + r // width + c) % n]
                      for c in range(n)] for r in range(n)]
            self.assertTrue(puzzle.is_valid_board(symbols, board))
            for _ in range(67 if n != 16 else 66):
                partial = [[value if randomizer.random() < 0.45 else "."
                            for value in row] for row in board]
                self.assertTrue(puzzle.is_valid_board(symbols, partial))

    def test_200_random_boards_against_pairwise_region_oracle(self):
        randomizer = random.Random(52604)
        for _ in range(200):
            n = randomizer.choice((4, 9))
            symbols = [str(i) for i in range(n)]
            board = [[randomizer.choice(symbols + ["."] * 20 + ["?"])
                      for _ in range(n)] for _ in range(n)]
            self.assertEqual(puzzle.is_valid_board(symbols, board),
                             puzzle_reference(symbols, board))

    def test_parser_and_standard_input(self):
        symbols, board = puzzle.read_input("\ufeff1\n @ \n . \n\n")
        self.assertEqual((symbols, board), (["@"], [["."]]))
        self.assertEqual(run_program("puzzle_game.py",
                                     text="1\n@\n.\n"), "The board is valid\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
