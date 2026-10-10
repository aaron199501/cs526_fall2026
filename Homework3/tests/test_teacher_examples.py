"""Run every teacher input and compare its complete command-line output."""

import os
from pathlib import Path
import subprocess
import sys
import unittest

try:
    from .teacher_cases import comparable_teacher_output, expectation, teacher_cases
except ImportError:  # unittest discover -s tests imports modules by filename.
    from teacher_cases import comparable_teacher_output, expectation, teacher_cases


ROOT = Path(__file__).resolve().parents[1]


class TeacherExampleTests(unittest.TestCase):
    def test_all_teacher_examples(self):
        cases = teacher_cases(ROOT)
        self.assertEqual(len(cases), 29)
        resources = ROOT / "tests" / "teacher_resources"
        supplied_inputs = {
            path.name for path in resources.glob("*.txt")
            if (path.name.startswith("palendrome_") and "_ans_" not in path.name)
            or path.name.startswith(("unique_substrings_input_", "ghostbusters_input_"))
        }
        self.assertEqual(supplied_inputs, {case.input_path.name for case in cases},
                         "A teacher input was added, omitted, or renamed")
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        for case in cases:
            with self.subTest(teacher_input=case.input_path.name):
                self.assertTrue(case.input_path.is_file(), str(case.input_path))
                expected, provenance = expectation(case)
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / case.program)],
                    input=case.input_path.read_bytes(), capture_output=True,
                    cwd=ROOT, env=environment, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
                self.assertEqual(result.stderr, b"", "Unexpected standard error")
                self.assertEqual(comparable_teacher_output(result.stdout),
                                 comparable_teacher_output(expected),
                                 f"Output differs from {provenance} expectation")


if __name__ == "__main__":
    unittest.main()
