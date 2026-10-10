"""Teacher fixture inventory and the reference for the one missing answer.

The original resource names and contents are preserved. Teacher answers may
omit their final newline, so their comparisons normalize CRLF and exactly one
optional terminal LF. Every other character and blank line is significant.
"""

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TeacherCase:
    name: str
    problem: int
    program: str
    input_path: Path
    expected_path: Path

    @property
    def run_id(self):
        return "teacher_" + self.input_path.stem


def normalize_newlines(data):
    """Keep all output bytes significant except Windows newline encoding."""
    return data.replace(b"\r\n", b"\n")


def comparable_teacher_output(data):
    """Ignore exactly one optional final newline, never other whitespace."""
    return normalize_newlines(data).removesuffix(b"\n")


def teacher_cases(root=ROOT):
    resources = root / "tests" / "teacher_resources"
    cases = []
    for number in range(5):
        for suffix in ("", "L", "S"):
            label = str(number) + suffix
            cases.append(TeacherCase(
                "palendrome_" + label, 1, "palindrome.py",
                resources / ("palendrome_" + label + ".txt"),
                resources / ("palendrome_ans_" + label + ".txt"),
            ))
    for number in range(3):
        cases.append(TeacherCase(
            "unique_substrings_" + str(number), 2, "substrings.py",
            resources / (f"unique_substrings_input_{number}.txt"),
            resources / (f"unique_substrings_ans_{number}.txt"),
        ))
    for number in range(11):
        cases.append(TeacherCase(
            "ghostbusters_" + str(number), 4, "ghostbusters.py",
            resources / (f"ghostbusters_input_{number}.txt"),
            resources / (f"ghostbusters_ans_{number}.txt"),
        ))
    return cases


def reference_palindrome_output(input_bytes):
    """Check mirrored character pairs without importing the submitted code."""
    results = []
    count = 0
    for line in normalize_newlines(input_bytes).decode("utf-8").splitlines():
        characters = [character for character in line if character != " "]
        left, right = 0, len(characters) - 1
        palindrome = True
        while left < right:
            if characters[left] != characters[right]:
                palindrome = False
                break
            left += 1
            right -= 1
        results.append(str(palindrome))
        count += int(palindrome)
    return ("\n".join([*results, str(count)]) + "\n").encode("utf-8")


def expectation(case):
    """Return bytes and an explicit origin; never invent a teacher answer."""
    if case.expected_path.is_file():
        return case.expected_path.read_bytes(), "teacher"
    if case.name != "palendrome_4S":
        raise FileNotFoundError(f"Missing teacher answer: {case.expected_path}")
    return reference_palindrome_output(case.input_path.read_bytes()), "independent"


def comparison_description(case, provenance):
    if provenance == "teacher":
        return ("PASS — matches teacher answer: " + case.expected_path.name
                + " (CRLF and one optional final newline normalized)")
    return ("PASS — matches an independent mirrored-character reference; "
            "teacher answer " + case.expected_path.name + " was not supplied")
