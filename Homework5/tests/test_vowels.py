"""Independent enumeration, supplied cases, and input/CLI checks for Problem 2."""

from collections import Counter
import itertools
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from vowelCombinations import count_vowel_combinations, read_input


ROOT = Path(__file__).resolve().parents[1]


class VowelCombinationTests(unittest.TestCase):
    def test_all_short_inputs_against_word_enumeration(self):
        # Enumerate actual vowel words, encode them, and count equal encodings.
        # Every encoding of at most six symbols has at most six letters.
        code_for_letter = {"A": ".-", "E": ".", "I": "..", "O": "---", "U": "..-"}
        expected = Counter()
        for word_length in range(7):
            for letters in itertools.product("AEIOU", repeat=word_length):
                encoding = "".join(code_for_letter[letter] for letter in letters)
                if len(encoding) <= 6:
                    expected[encoding] += 1
        for length in range(7):
            for symbols in itertools.product(".-", repeat=length):
                sequence = "".join(symbols)
                with self.subTest(sequence=sequence):
                    self.assertEqual(count_vowel_combinations(sequence), expected[sequence])

    def test_supplied_inputs(self):
        for number, expected in enumerate((6, 8, 0, 193050000), 1):
            with self.subTest(number=number):
                sequence = read_input(ROOT / "inputs" / "vowel_input{}.txt".format(number))
                self.assertEqual(count_vowel_combinations(sequence), expected)

    def test_empty_input_has_one_decoding(self):
        self.assertEqual(count_vowel_combinations(""), 1)

    def test_single_symbols_and_dash_groups(self):
        for sequence, expected in ((".", 1), ("-", 0), ("--", 0), ("---", 1), ("------", 1)):
            with self.subTest(sequence=sequence):
                self.assertEqual(count_vowel_combinations(sequence), expected)

    def test_count_exceeds_fixed_width_integer(self):
        # A dot-only string has Fibonacci(n+1) partitions into E and I.
        previous, current = 1, 1
        for _ in range(100):
            previous, current = current, previous + current
        answer = count_vowel_combinations("." * 100)
        self.assertEqual(answer, previous)
        self.assertGreater(answer, 2 ** 64)

    def test_function_rejects_invalid_symbols(self):
        for sequence in ("a", ". -", ".\n", "_", "…"):
            with self.subTest(sequence=sequence):
                with self.assertRaises(ValueError):
                    count_vowel_combinations(sequence)

    def read_temporary_input(self, text):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "input.txt"
            with filename.open("w", encoding="utf-8", newline="") as output:
                output.write(text)
            return read_input(filename)

    def test_reader_accepts_bom_crlf_and_trailing_blank_lines(self):
        self.assertEqual(self.read_temporary_input("\ufeff3\r\n .-. \r\n\r\n"), ".-.")

    def test_reader_accepts_zero_length(self):
        for text in ("0\n", "0\n\n", "0\n   \n\n"):
            with self.subTest(text=text):
                self.assertEqual(self.read_temporary_input(text), "")

    def test_reader_rejects_bad_input(self):
        for text in ("", "abc\n.\n", "-1\n\n", "3\n", "4\n...\n", "1\nx\n", "2\n. -\n", "1\n.\n-\n"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    self.read_temporary_input(text)

    def test_cli_exact_required_output(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "vowelCombinations.py"), str(ROOT / "inputs" / "vowel_input1.txt")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, "File Input: vowel_input1.txt\nThe Number of Vowel combinations is:\n    6\n")

    def test_cli_reports_missing_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "vowelCombinations.py"), str(Path(directory) / "missing.txt")],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
