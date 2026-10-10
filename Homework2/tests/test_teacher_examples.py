"""Regression checks for teacher output, input recovery and staircase CLI."""
import ast
import inspect
import itertools
import os
import subprocess
import sys
import unittest
from pathlib import Path

from problem3 import combinations, ways
from teacher_cases import load_teacher_cases, normalize_newlines, staircase_transcript

ROOT = Path(__file__).resolve().parents[1]


def run_program(args, input_text=""):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, "-B", *args], input=input_text, text=True,
        capture_output=True, cwd=ROOT, env=environment, timeout=30,
    )
    return result


class TeacherExampleTests(unittest.TestCase):
    def test_all_19_teacher_outputs(self):
        cases = load_teacher_cases(ROOT)
        self.assertEqual(len(cases), 19)
        for case in cases:
            with self.subTest(case=case["id"]):
                input_text = (ROOT / case["input_path"]).read_text(encoding="utf-8") if case["input_path"] else ""
                result = run_program(case["args"], input_text)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(normalize_newlines(result.stdout), case["expected_stdout"])
                self.assertFalse(case["reference"]["independently_derived"])

    def test_combined_teacher_staircase_output(self):
        result = run_program(["problem3.py", "--teacher-examples"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(normalize_newlines(result.stdout), staircase_transcript(ROOT))

    def test_default_staircase_demo_keeps_pdf_examples(self):
        result = run_program(["problem3.py"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, "ways(3) = 4\nways(5) = 13\nways(10) = 274\n")


class DriverBoundaryTests(unittest.TestCase):
    def test_empty_input_finishes_cleanly(self):
        for driver in ("problem2_driver.py", "problem4_driver.py"):
            with self.subTest(driver=driver):
                result = run_program([driver], "\n# comment only\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(result.stdout, "Final list: (empty)\n")

    def test_original_inputs_are_retained_and_processed(self):
        expected_final = {
            "tests/original_resources/problem2_basic.txt": "Final list: 8 -> 12 -> 5 -> 7\n",
            "tests/original_resources/problem2_errors.txt": "Final list: 7 -> 8\n",
            "problem2Resources/problem2_all_operations.txt": "Final list: 5 -> 8\n",
            "problem2Resources/problem2_empty_single.txt": "Final list: (empty)\n",
        }
        for path, final_line in expected_final.items():
            with self.subTest(path=path):
                result = run_program(["problem2_driver.py"], (ROOT / path).read_text(encoding="utf-8"))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertTrue(result.stdout.endswith(final_line), result.stdout)

    def test_non_finite_values_cannot_break_sorted_order(self):
        result = run_program(["problem4_driver.py"], "add nan\nadd inf\nadd -inf\nadd 2\nadd 1\nprint_list\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, "line 1: value must be a number, got 'add nan'\nline 2: value must be a number, got 'add inf'\nline 3: value must be a number, got 'add -inf'\nadd(2)\nadd(1)\n1 <-> 2\nFinal list: 1 <-> 2\n")


class StaircaseCliTests(unittest.TestCase):
    def test_zero_step_path_and_count(self):
        self.assertEqual(list(combinations(0)), [()])
        self.assertEqual(list(combinations(-1)), [])
        result = run_program(["problem3.py", "--steps", "0", "--count-only"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Step Combinations for an input of 0 steps:  1 \n")

    def test_invalid_cli_is_rejected(self):
        for args, message in (
            (["--steps", "-1"], "--steps must be non-negative"),
            (["--steps", "x"], "invalid int value"),
            (["--count-only"], "--count-only requires --steps"),
            (["--teacher-examples", "--count-only"], "--count-only requires --steps"),
            (["--teacher-examples", "--steps", "3"], "not allowed with argument"),
        ):
            with self.subTest(args=args):
                result = run_program(["problem3.py", *args])
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn(message, result.stderr)

    def test_recursive_paths_match_independent_enumeration(self):
        for steps in range(1, 8):
            with self.subTest(steps=steps):
                expected = {
                    path
                    for length in range(1, steps + 1)
                    for path in itertools.product((1, 2, 3), repeat=length)
                    if sum(path) == steps
                }
                actual = list(combinations(steps))
                self.assertEqual(len(actual), len(set(actual)))
                self.assertEqual(set(actual), expected)
                self.assertEqual(actual, sorted(actual))
                self.assertEqual(len(actual), ways(steps))

    def test_recursive_functions_have_no_loops(self):
        for function in (ways, combinations):
            with self.subTest(function=function.__name__):
                tree = ast.parse(inspect.getsource(function))
                self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.AsyncFor, ast.comprehension)) for node in ast.walk(tree)))
                self.assertTrue(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function.__name__ for node in ast.walk(tree)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
