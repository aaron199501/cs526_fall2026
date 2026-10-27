"""Run the real programs with reproducible commands and captured output."""

import argparse
from pathlib import Path
import platform
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
CASES = {}
for number, answer in enumerate(("YES", "NO", "NO", "YES", "YES"), 1):
    CASES[f"snowfall_{number}"] = (
        "Problem1_Snowfall", ["snowfall.py", f"inputs/snowfall_input{number}.txt"],
        f"solution: {answer}", "snowfall.py")
for number, answer in enumerate(("There are healthy counties left",
                               "There are no healthy counties left"), 1):
    CASES[f"pandemic_{number}"] = (
        "Problem2_Pandemic", ["pandemic.py", f"inputs/pandemic_input{number}.txt"],
        answer, "pandemic.py")
for number, answer in enumerate(("valid", "invalid", "valid", "invalid"), 1):
    CASES[f"puzzle_{number}"] = (
        "Problem3_SymbolPuzzle", ["puzzle_game.py", f"inputs/puzzle_game_input{number}.txt"],
        f"The board is {answer}", "puzzle_game.py")
CASES["pandemic_days"] = (
    "Problem2_Pandemic", ["pandemic.py", "inputs/pandemic_input1.txt", "--show-days"],
    "There are healthy counties left", "pandemic.py")
CASES["tests"] = (".", ["-m", "unittest", "discover", "-s", "tests", "-v"],
                  "OK", "tests/test_midterm.py")


def run_case(name):
    folder, arguments, expected, _ = CASES[name]
    print(f"=== {name} ===", flush=True)
    print(f"Working directory: {folder}", flush=True)
    print("Command: python -B " + " ".join(arguments), flush=True)
    start = time.perf_counter()
    result = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT / folder,
                            capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    output = result.stdout + result.stderr
    passed = result.returncode == 0 and output.rstrip().endswith(expected)
    print(f"Exit status: {result.returncode}; elapsed: {elapsed:.4f} seconds; "
          f"expected result: {'PASS' if passed else 'FAIL'}", flush=True)
    print("Program output:", flush=True)
    print(output, end="" if output.endswith("\n") else "\n", flush=True)
    if not passed:
        raise RuntimeError(f"Unexpected output for {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=[*CASES, "all", "snowfall", "pandemic", "puzzle"])
    parser.add_argument("--show-interpreter", action="store_true",
                        help="show the exact path of the running Python interpreter")
    args = parser.parse_args()
    print("CS526 Mid-Term: actual program execution", flush=True)
    print(f"Python {platform.python_version()}", flush=True)
    if args.show_interpreter:
        print(f"Interpreter: {sys.executable}", flush=True)
    print("In the commands below, python denotes this interpreter.\n", flush=True)
    if args.case == "all":
        names = list(CASES)[:11]
    elif args.case in ("snowfall", "pandemic", "puzzle"):
        names = [name for name in CASES
                 if name.startswith(args.case + "_") and name != "pandemic_days"]
    else:
        names = [args.case]
    for index, name in enumerate(names):
        if index:
            print()
        run_case(name)


if __name__ == "__main__":
    main()
