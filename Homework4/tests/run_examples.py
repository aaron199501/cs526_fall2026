"""Run screenshot demonstrations with the real command, output, and elapsed time."""

import argparse
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "trees": ["treeTraversals.py"],
    "fewest_sample": ["smallestNumber.py", "tests/data/smallest_input.txt"],
    "fewest_1": ["smallestNumber.py", "Fewest_Resourses/fewest_1.txt"],
    "fewest_2": ["smallestNumber.py", "Fewest_Resourses/fewest_2.txt"],
    "fewest_3": ["smallestNumber.py", "Fewest_Resourses/fewest_3.txt"],
    "angles_1": ["rightTriangles.py", "Angles_Resourses/rightangles_1.txt"],
    "angles_2": ["rightTriangles.py", "Angles_Resourses/rightangles_2.txt"],
    "angles_3": ["rightTriangles.py", "Angles_Resourses/rightangles_3.txt"],
    "strict_greater": ["smallestNumber.py", "tests/data/strict_greater.txt"],
    "rotated_triangle": ["rightTriangles.py", "tests/data/rotated_triangle.txt"],
    "square": ["rightTriangles.py", "tests/data/square.txt"],
    "opposite_rays": ["rightTriangles.py", "tests/data/opposite_rays.txt"],
    "tests_unittest": ["-m", "unittest", "discover", "-s", "tests"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    args = parser.parse_args()
    command = [sys.executable, "-B", *CASES[args.case]]
    print(f"CS526 Homework 4 | {args.case}", flush=True)
    print("$ python " + " ".join(CASES[args.case]), flush=True)
    print(flush=True)
    start = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT)
    elapsed = time.perf_counter() - start
    print("\nCommand: python " + " ".join(CASES[args.case]), flush=True)
    print(f"\nExit status: {completed.returncode} | Elapsed: {elapsed:.3f} seconds", flush=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
