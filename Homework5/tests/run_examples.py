"""Run the real homework programs and save their console output."""

from pathlib import Path
import argparse
import shlex
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "bst": ["binarySearchTree.py", "--size", "5", "--seed", "526"],
    **{f"vowels_{i}": ["vowelCombinations.py", f"inputs/vowel_input{i}.txt"]
       for i in range(1, 5)},
    **{f"longest_{i}": ["longestSequence.py", f"inputs/longest_seq{i}.txt"]
       for i in range(1, 7)},
    "tests": ["-m", "unittest", "discover", "-s", "tests"],
}
GROUPS = {
    "vowels": [f"vowels_{i}" for i in range(1, 5)],
    "longest": [f"longest_{i}" for i in range(1, 7)],
    "longest_small": [f"longest_{i}" for i in (1, 2, 3)],
    "longest_large": [f"longest_{i}" for i in (4, 5, 6)],
    "all": list(CASES),
}


def run_case(case):
    arguments = CASES[case]
    display_command = "python " + shlex.join(arguments)
    print(f"> {display_command}", flush=True)
    started = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, "-B", *arguments], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding="utf-8", errors="strict",
    )
    elapsed = time.perf_counter() - started
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n",
          flush=True)
    footer = f"Exit code: {completed.returncode}; elapsed: {elapsed:.3f} s\n"
    print(footer, flush=True)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / f"{case}.txt").write_text(
        f"> {display_command}\n{completed.stdout}{footer}", encoding="utf-8",
    )
    return completed.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=sorted([*CASES, *GROUPS]), default="all",
                        nargs="?")
    options = parser.parse_args()
    cases = GROUPS.get(options.case, [options.case])
    failures = sum(run_case(case) != 0 for case in cases)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
