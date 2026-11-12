"""Run supplied examples through stdin and retain their real console output."""

import argparse
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
PROGRAMS = {"merge": "mergeLogs.py", "heap": "linkedHeap.py", "median": "runningMedian.py"}


def case_number(path):
    return int(re.search(r"input(\d+)", path.stem).group(1))


def run_case(kind, input_path, show_output=False):
    """Use a pipe to test the assignment's required standard-input interface."""
    program = PROGRAMS[kind]
    started = time.perf_counter()
    result = subprocess.run(
        [sys.executable, "-B", program], input=input_path.read_bytes(),
        cwd=ROOT, capture_output=True, check=False,
    )
    elapsed = time.perf_counter() - started
    output = result.stdout.decode("utf-8").replace("\r\n", "\n")
    errors = result.stderr.decode("utf-8").replace("\r\n", "\n")
    expected_path = ROOT / "tests" / "expected" / input_path.name.replace("_input", "_output")
    expected = expected_path.read_text(encoding="utf-8-sig")
    if kind == "heap":
        # The assignment permits different spaces, but not different tree positions.
        from test_homework6 import heap_output_signature
        matches = heap_output_signature(output) == heap_output_signature(expected)
    else:
        matches = output.split() == expected.split()
    passed = result.returncode == 0 and matches
    record = (
        f"Program: python {program}\nStandard input: inputs/{input_path.name}\n\n"
        + output + ("\nStandard error:\n" + errors if errors else "")
        + f"\nExit code: {result.returncode}\nExpected result: {'PASS' if matches else 'FAIL'}\n"
        + f"Elapsed seconds: {elapsed:.6f}\n"
    )
    (ROOT / "results" / (input_path.stem + ".txt")).write_text(record, encoding="utf-8")
    if show_output:
        print(record, end="", flush=True)
    else:
        print(f"{'PASS' if passed else 'FAIL'} {input_path.name:20s} {elapsed:.3f} s", flush=True)
    return passed


def run_group(kind):
    paths = list((ROOT / "inputs").glob(kind + "_input*.txt"))
    paths.sort(key=case_number)
    print(f"\n{kind.upper()} supplied examples ({len(paths)})", flush=True)
    outcomes = [run_case(kind, path) for path in paths]
    print(f"{sum(outcomes)}/{len(outcomes)} expected results matched.", flush=True)
    return all(outcomes)


def run_tests():
    command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"]
    print("\npython -m unittest discover -s tests -v", flush=True)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    record = result.stdout + result.stderr + f"\nExit code: {result.returncode}\n"
    (ROOT / "results" / "tests.txt").write_text(record, encoding="utf-8")
    print(record, end="", flush=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["all", "resources", "merge", "heap", "median", "merge_demo", "heap_demo", "median_demo", "tests"])
    selected = parser.parse_args().case
    (ROOT / "results").mkdir(exist_ok=True)
    print("CS526 Homework Assignment 6", flush=True)
    print("Interpreter: " + sys.version.split()[0], flush=True)
    if selected.endswith("_demo"):
        kind = selected.removesuffix("_demo")
        passed = run_case(kind, ROOT / "inputs" / (kind + "_input1.txt"), show_output=True)
    elif selected == "tests":
        passed = run_tests()
    elif selected in {"all", "resources"}:
        outcomes = [run_group(kind) for kind in PROGRAMS]
        if selected == "all":
            outcomes.append(run_tests())
        passed = all(outcomes)
    else:
        passed = run_group(selected)
    print("\nOverall: " + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
