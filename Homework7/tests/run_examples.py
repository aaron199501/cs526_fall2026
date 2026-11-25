"""Run the required command-line examples and preserve their complete outputs."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = []
for algorithm in ("merge", "quick", "insertion", "radix"):
    for size in ("small", "medium", "large"):
        filename = f"radix_{size}.txt" if algorithm == "radix" else f"{size}.txt"
        CASES.append((f"{algorithm}_{size}", [f"{algorithm}_sort.py", f"inputs/{filename}"], 0))
CASES += [
    ("matching_ten", ["stable_matching.py", "inputs/marraige_ten.txt"], 0),
    ("matching_hundred", ["stable_matching.py", "inputs/marriage_hundred.txt", "--allow-shared-names"], 0),
    ("matching_thousand", ["stable_matching.py", "inputs/marraige_thousand.txt", "--allow-shared-names"], 0),
    ("matching_invalid", ["stable_matching.py", "inputs/badInput.txt"], 1),
]


def run_case(case, preview=False):
    name, arguments, expected = case
    command = "python " + " ".join(arguments)
    process = subprocess.run(
        [sys.executable, "-B", *arguments], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", timeout=60,
    )
    output = process.stdout
    target = ROOT / "results" / f"{name}.txt"
    target.parent.mkdir(exist_ok=True)
    target.write_text(output, encoding="utf-8")
    print(f"Command: {command}", flush=True)
    lines = output.splitlines()
    if preview and len(lines) > 39:
        print(f"Complete output saved to results/{name}.txt ({len(lines)} lines).")
        print("--- Start of actual output (long lines wrapped by the terminal) ---")
        for line in lines[:5 if name.startswith("matching") else 15]:
            # Preference records contain thousands of names on one line.
            # Only the preview is shortened; the saved program output is exact.
            print(line if len(line) <= 120 else line[:120] + " ... [line continues in saved output]")
        print("--- Middle omitted from this preview; see the complete output file ---")
        print("--- End of actual output ---")
        for line in lines[-12:]:
            print(line)
    else:
        print(output, end="" if output.endswith("\n") else "\n")
    passed = process.returncode == expected
    print(f"Exit code: {process.returncode} (expected {expected})")
    print("Execution: " + ("PASS" if passed else "FAIL"), flush=True)
    if not passed:
        raise RuntimeError(f"Unexpected exit code in {name}")
    return {"case": name, "command": command, "exit_code": process.returncode, "expected_exit_code": expected, "output": f"results/{name}.txt"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", default="all", choices=["all"] + [case[0] for case in CASES])
    parser.add_argument("--preview", action="store_true", help="display excerpts while saving complete output")
    args = parser.parse_args()
    selected = CASES if args.case == "all" else [case for case in CASES if case[0] == args.case]
    summary = [run_case(case, preview=args.preview) for case in selected]
    if args.case == "all":
        (ROOT / "results" / "execution_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
