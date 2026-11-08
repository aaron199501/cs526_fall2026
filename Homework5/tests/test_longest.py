"""Independent checks for Problem 3, including the cross-array index rule."""

import itertools
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from longestSequence import (  # noqa: E402
    longest_alternating_sequence,
    longest_sequence_length,
    parse_input,
    read_input_file,
)


def quadratic_reference(array_a, array_b):
    """Longest path in the explicit DAG of legal endpoint transitions.

    This independent O(N squared) oracle enumerates every predecessor instead
    of using the implementation's coordinate compression or Fenwick trees.
    """
    vertices = sorted(
        [(index, "A", value) for index, value in enumerate(array_a)]
        + [(index, "B", value) for index, value in enumerate(array_b)]
    )
    lengths = []
    for current, (index, source, value) in enumerate(vertices):
        best = 1
        for previous in range(current):
            other_index, other_source, other_value = vertices[previous]
            if other_index < index and other_source != source and other_value < value:
                best = max(best, lengths[previous] + 1)
        lengths.append(best)
    return max(lengths, default=0)


class LongestSequenceTests(unittest.TestCase):
    def assert_witness(self, array_a, array_b, sequence):
        for item in sequence:
            self.assertIn(item.source, ("A", "B"))
            original = array_a if item.source == "A" else array_b
            self.assertGreaterEqual(item.position, 1)
            self.assertLessEqual(item.position, len(original))
            self.assertEqual(item.value, original[item.position - 1])
        for previous, current in zip(sequence, sequence[1:]):
            self.assertNotEqual(previous.source, current.source)
            self.assertLess(previous.position, current.position)
            self.assertLess(previous.value, current.value)

    def check_case(self, array_a, array_b, expected=None):
        sequence = longest_alternating_sequence(array_a, array_b)
        self.assert_witness(array_a, array_b, sequence)
        if expected is None:
            expected = quadratic_reference(array_a, array_b)
        self.assertEqual(len(sequence), expected, (array_a, array_b, sequence))
        return sequence

    def test_assignment_explanation(self):
        sequence = self.check_case([1, 7, 2], [4, 8, 3, 9], 3)
        self.assertEqual([item.value for item in sequence], [4, 7, 9])
        self.assertEqual([item.position for item in sequence], [1, 2, 4])

    def test_same_position_cannot_be_used_twice(self):
        self.check_case([1], [2], 1)
        self.check_case([2], [1], 1)
        self.check_case([1, 3], [2, 4], 2)

    def test_empty_negative_equal_and_unequal_lengths(self):
        for array_a, array_b, expected in (
            ([], [], 0),
            ([], [1, 2, 3], 1),
            ([1, 2, 3], [], 1),
            ([5, 5, 5], [5, 5, 5], 1),
            ([-5, -3, -1], [-6, -4, -2], 3),
            ([8, 2, 9, 1, 4], [4, 1, 5, 3, 2, 6], 4),
        ):
            with self.subTest(array_a=array_a, array_b=array_b):
                self.check_case(array_a, array_b, expected)

    def test_all_small_arrays_against_independent_oracle(self):
        arrays = [
            list(values)
            for length in range(4)
            for values in itertools.product((-1, 0, 1), repeat=length)
        ]
        for array_a in arrays:
            for array_b in arrays:
                self.check_case(array_a, array_b)

    def test_random_arrays_against_independent_oracle(self):
        rng = random.Random(526)
        for _ in range(750):
            array_a = [rng.randrange(-7, 8) for _ in range(rng.randrange(10))]
            array_b = [rng.randrange(-7, 8) for _ in range(rng.randrange(10))]
            self.check_case(array_a, array_b)

    def test_all_provided_inputs(self):
        for number, expected in enumerate((4, 7, 10, 39, 192, 1), 1):
            with self.subTest(file=number):
                array_a, array_b = read_input_file(ROOT / "inputs" / "longest_seq{}.txt".format(number))
                self.check_case(array_a, array_b, expected)

    def test_ten_thousand_positions(self):
        array_a = list(range(0, 20000, 2))
        array_b = list(range(1, 20001, 2))
        self.check_case(array_a, array_b, 10000)

    def test_length_convenience_function(self):
        self.assertEqual(longest_sequence_length([1, 7, 2], [4, 8, 3, 9]), 3)

    def test_valid_four_line_input(self):
        self.assertEqual(parse_input("2\r\n3\r\n-1 +2\r\n3 4 5\r\n"), ([-1, 2], [3, 4, 5]))
        self.assertEqual(parse_input("0\n0\n\n\n"), ([], []))
        self.assertEqual(parse_input("0\n1\n\n7\n"), ([], [7]))
        self.assertEqual(parse_input("1\n0\n7\n\n"), ([7], []))

    def test_invalid_file_shapes_and_tokens(self):
        examples = (
            ("1\n1\n1\n", "4 input lines"),
            ("1\n1\n1\n2\nextra", "4 input lines"),
            ("-1\n1\n1\n2", "nonnegative"),
            ("1 2\n1\n1\n2", "one nonnegative"),
            ("hello\n1\n1\n2", "only integers"),
            ("1\n2\n1\n2", "declares 2"),
            ("2\n1\n1\n2", "declares 2"),
            ("1\n1\n1.0\n2", "only integers"),
            ("1\n1\n1_0\n2", "only integers"),
        )
        for text, message in examples:
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, message):
                    parse_input(text)

    def test_cli_exact_output_and_optional_witness(self):
        input_file = ROOT / "inputs" / "longest_seq1.txt"
        command = [sys.executable, str(ROOT / "longestSequence.py"), str(input_file)]
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(completed.stdout, "File Input: longest_seq1.txt\nLongest Sequence: 4\n")
        self.assertEqual(completed.stderr, "")
        completed = subprocess.run(command + ["--show-sequence"], capture_output=True, text=True, check=True)
        self.assertIn("Sequence Values:", completed.stdout)
        self.assertIn("Sequence Witness:", completed.stdout)
        self.assertRegex(completed.stdout, r"[AB]\[[0-9]+\]=")

    def test_cli_reports_invalid_input_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            bad_input = Path(temporary) / "bad.txt"
            bad_input.write_text("1\n1\n1\nnot-an-integer\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "longestSequence.py"), str(bad_input)],
                capture_output=True, text=True,
            )
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("array B must contain only integers", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
