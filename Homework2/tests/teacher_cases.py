"""Extract expected outputs from the supplied teacher execution transcripts."""
import re
from pathlib import Path


def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def homework_root(root=None):
    return Path(root) if root is not None else Path(__file__).resolve().parents[1]


def read_transcript(path):
    return normalize_newlines(path.read_text(encoding="utf-8-sig"))


def staircase_transcript(root=None):
    return read_transcript(homework_root(root) / "tests/teacher_resources/problem3Excutions.txt")


def load_teacher_cases(root=None):
    """Return 19 cases with relative paths, commands, output and provenance."""
    root = homework_root(root)
    cases = []
    for problem, filename in ((2, "problem2Executions.txt"), (4, "problem4Executions.txt")):
        relative_reference = f"tests/teacher_resources/{filename}"
        text = read_transcript(root / relative_reference)
        sections = list(re.finditer(r"(?m)^===== (?P<input>[^\n]+)\n\$ (?P<command>[^\n]+)\n", text))
        for position, section in enumerate(sections):
            end = sections[position + 1].start() if position + 1 < len(sections) else len(text)
            expected = text[section.end():end].rstrip("\n") + "\n"
            input_path = section.group("input")
            if not (root / input_path).is_file():
                raise FileNotFoundError(root / input_path)
            output_line = text[:section.end()].count("\n") + 1
            cases.append({
                "id": Path(input_path).stem,
                "title": f"Problem {problem} — {Path(input_path).stem}",
                "problem": problem,
                "args": [f"problem{problem}_driver.py"],
                "input_path": input_path,
                "expected_stdout": expected,
                "teacher_command": section.group("command"),
                "reference": {
                    "path": relative_reference,
                    "section_line": text[:section.start()].count("\n") + 1,
                    "output_first_line": output_line,
                    "output_last_line": output_line + len(expected.splitlines()) - 1,
                    "independently_derived": False,
                },
            })
    relative_reference = "tests/teacher_resources/problem3Excutions.txt"
    text = staircase_transcript(root)
    sections = list(re.finditer(r"(?m)^Step Combinations for an input of (?P<steps>\d+) steps:[^\n]*\n", text))
    for position, section in enumerate(sections):
        end = sections[position + 1].start() if position + 1 < len(sections) else len(text)
        expected = text[section.start():end].rstrip("\n") + "\n"
        steps = int(section.group("steps"))
        count_only = "Total Step Combinations:" not in expected
        args = ["problem3.py", "--steps", str(steps)]
        if count_only:
            args.append("--count-only")
        count_match = re.search(r"(?:Total Step Combinations:|steps:)\s+(\d+)\s*\n?$", expected)
        output_line = text[:section.start()].count("\n") + 1
        cases.append({
            "id": f"problem3_steps_{steps}",
            "title": f"Problem 3 — {steps} steps" + (" (count only)" if count_only else ""),
            "problem": 3,
            "args": args,
            "input_path": None,
            "expected_stdout": expected,
            "expected_count": int(count_match.group(1)),
            "lists_combinations": not count_only,
            "teacher_command": None,
            "reference": {
                "path": relative_reference,
                "section_line": output_line,
                "output_first_line": output_line,
                "output_last_line": output_line + len(expected.splitlines()) - 1,
                "independently_derived": False,
            },
        })
    if len(cases) != 19:
        raise ValueError(f"Expected 19 teacher examples, found {len(cases)}")
    return sorted(cases, key=lambda case: (case["problem"], case["id"]))
