# CS526 Homework Assignment 3

Boston University Metropolitan College

## Introduction

This homework implements palindrome detection, recursive enumeration of unique
substrings, recursive in-place reversal of three stack implementations, and
intersection checking for fixed Ghostbuster/ghost pairs. The programs use only
the Python standard library and require Python 3.9 or later.

Problems 1, 2, and 4 read standard input. Problem 3 follows the assignment's
instruction to push the numbers 1 through 10 onto each stack and requires no
input file.

| File or folder | Purpose |
| --- | --- |
| `palindrome.py` | Problem 1 |
| `palindrome_input.txt` | Problem 1 sample input, matching the assignment example |
| `substrings.py` | Problem 2 |
| `substrings_input.txt` | Problem 2 sample input |
| `stacks.py` | Problem 3 |
| `ghostbusters.py` | Problem 4 |
| `tests/test_homework.py` | Automated correctness, structure, and output tests |
| `tests/record_runs.py` | Runs and verifies the programs; optionally serves a local execution viewer |
| `tests/data/` | Saved automated-test inputs and expected-output fixtures |
| `screenshot/` | Six representative VS Code terminal screenshots: Problems 1-3, two Problem 4 outcomes, and the automated tests |
| `Homework3.txt` | Original assignment requirements |

## Files and repository layout

Use the assignment's folder option by placing this entire `Homework3/` folder
in your Git repository. A suitable repository layout is:

```text
<your-repository>/
`-- Homework3/
    |-- .gitignore
    |-- Homework3.txt
    |-- README.md
    |-- palindrome.py
    |-- palindrome_input.txt
    |-- substrings.py
    |-- substrings_input.txt
    |-- stacks.py
    |-- ghostbusters.py
    |-- tests/
    |   |-- __init__.py
    |   |-- test_homework.py
    |   |-- record_runs.py
    |   `-- data/
    |       |-- *_input.txt
    |       `-- *_expected.txt
    `-- screenshot/
        |-- p1_sample.png
        |-- p2_sample.png
        |-- p3_stacks.png
        |-- p4_example1.png
        |-- p4_example2.png
        `-- tests_unittest.png
```

The four source programs and the two sample input files are at the homework
root. All automated tests and their input/output fixtures remain in `tests/`.
The assignment's Code, README, Test files, and Example executions labels
describe required contents; they do not require folders with those names.

The Problem 1 sample can be run exactly as shown in the assignment on
Linux/macOS:

```sh
python3 palindrome.py < palindrome_input.txt
```

## Algorithm

### Problem 1: palindrome detection

A string is a palindrome when its character sequence is identical in forward
and reverse order. Remove the literal spaces permitted as character separators
before making this comparison; keep uppercase and lowercase letters distinct.
`is_palindrome` implements this definition by comparing the cleaned string with
its reversed slice.

The driver reads one string per line and removes only line-ending characters.
It prints one Boolean per string, counts the palindromes, and prints the count
on the final line. A line of length L takes O(L) time and additional space; input
lines are processed individually.

### Problem 2: recursive unique substrings

Every nonempty substring is an interval `text[start:end]`, where
`0 <= start < end <= n`. `unique_substrings` enumerates these intervals with
two recursive helpers:

1. `search_starts(low, high)` splits a half-open range of start indices into
   halves until a single start index remains.
2. For that start, `search_ends(start, low, high)` recursively splits the range
   of valid exclusive end indices. At a single-index range, it inserts the
   corresponding slice into a set.

Empty ranges return immediately. The initial start range is `[0, n)` and each
end range is `[start+1, n+1)`. These ranges reach every contiguous, nonempty
substring. The set removes duplicates. The driver sorts the set using Python's
case-sensitive lexicographic order, prints each substring, and prints the count.

The search uses recursion without loops. Balanced splitting limits call depth
to O(log n), with O(n²) interval visits. Copying and hashing slices can require
O(n³) total character work and storage in the worst case. Sorting m distinct
substrings uses O(m log m) comparisons, each potentially examining O(n)
characters.

### Problem 3: recursive in-place stack reversal

All three stacks implement `push`, `pop`, `peek`, and `is_empty`. Empty `pop`
and `peek` operations raise `IndexError`. Each reversal modifies the existing
stack and returns `None`; it neither constructs a replacement stack nor
allocates replacement linked nodes.

**Array stack.** The final array element is the top. Push appends and pop removes
that element. `_reverse_array` swaps the left and right elements, then recurses
on the inner interval. The base case is `left >= right`. The original array
object is preserved.

**Singly linked stack.** `head` is the top and `next` points toward the bottom.
Push inserts a new head; pop advances the head. `_reverse_singly_nodes` returns
for an empty or one-node list. Otherwise, it reverses the suffix recursively,
links the original next node back to the current node, and clears the current
node's old `next` link to prevent a cycle. The original bottom becomes the head.

**Doubly linked stack.** `head` is the top and `tail` is the bottom; `next` points
downward and `prev` points upward. Push and pop maintain both link directions
and handle transitions to and from an empty stack. `_reverse_doubly_nodes`
saves the original next node, swaps the current node's `next` and `prev`, and
recurses on the saved node. A null node is the base case. The wrapper swaps
`head` and `tail` after reversing the links.

All reversal helpers use recursion and no loops. Loops used to initialize the
demonstration and format its output are outside reversal. Each reversal takes
O(n) time and O(n) recursive call space. Push, pop, peek, and empty checks take
O(1), except array push is amortized O(1). Display order is bottom to top.

### Problem 4: infinite Ghostbuster streams

The given pairings cannot change. Two nonparallel infinite lines always
intersect, including beyond their endpoint segments. Coincident lines also
count as crossing. Therefore, all streams can fire together exactly when they
are parallel and lie on distinct lines.

For endpoints `(bx, by)` and `(gx, gy)`, set `A = gy - by` and `B = bx - gx`.
Divide both by `gcd(A, B)` and normalize the sign so A is positive, or B is
positive when A is zero. Then set `C = A*bx + B*by`. This gives the exact integer
line equation `A*x + B*y = C`. Distinct endpoints guarantee a nonzero divisor.

The program remembers the first normalized `(A, B)` and stores offsets C in
a set. A different `(A, B)` identifies intersecting nonparallel lines. With
the same `(A, B)`, a repeated C identifies coincident lines. If every direction
matches and every C is distinct, all lines are parallel and separate. This
condition is both necessary and sufficient, including the single-pair case.

Vertical and horizontal streams require no special slope handling. Integer
arithmetic avoids floating-point rounding. The algorithm performs expected
O(n) set operations and uses O(n) space. Gcd calculation adds O(log M) work
per pair under the unit-cost integer model, where M bounds coordinate
differences; very large integers also incur bit-operation costs.

## Interesting aspects

- Problem 1 ignores literal spaces while preserving case, tabs, and punctuation.
  Problem 2 preserves spaces within its input string.
- Balanced recursive index ranges keep substring enumeration shallow even when
  there are many substrings.
- Stack tests check object identity, linked node identity, and both directions
  of doubly linked pointers. Recursive linked reversal remains subject to
  Python's recursion depth limit for very large stacks.
- Geometry tests include intersecting extensions of disjoint segments,
  coincident lines, opposite directions, negative coordinates, vertical lines,
  and large integer coordinates.
- The tests cover saved input/output fixtures, exhaustive short-string cases,
  stack edge cases, and 1,000 reproducible geometry comparisons against an
  independent pairwise determinant algorithm with random seed 526.
- Six representative example executions are provided as VS Code integrated-terminal
  PNG screenshots in `screenshot/`. All test scripts, input files, and expected
  output files are retained, including cases without individual screenshots.

## How to run

Run these commands inside `Homework3/`. No additional packages are needed.
On Linux/macOS, use `python3`; the Windows commands below use the Python
launcher `py`. You can also use an
installed `python`.

### Linux/macOS

```sh
python3 -B palindrome.py < palindrome_input.txt
python3 -B substrings.py < substrings_input.txt
python3 -B stacks.py
python3 -B ghostbusters.py < tests/data/p4_example1_input.txt
python3 -B ghostbusters.py < tests/data/p4_example2_input.txt
python3 -B ghostbusters.py < tests/data/p4_example3_input.txt
python3 -B ghostbusters.py < tests/data/p4_example4_input.txt
```

### Windows PowerShell

PowerShell does not support `<` redirection. Pipe each input file to Python:

```powershell
Get-Content .\palindrome_input.txt | py -B .\palindrome.py
Get-Content .\substrings_input.txt | py -B .\substrings.py
py -B .\stacks.py
Get-Content .\tests\data\p4_example1_input.txt | py -B .\ghostbusters.py
Get-Content .\tests\data\p4_example2_input.txt | py -B .\ghostbusters.py
Get-Content .\tests\data\p4_example3_input.txt | py -B .\ghostbusters.py
Get-Content .\tests\data\p4_example4_input.txt | py -B .\ghostbusters.py
```

Replace `py` with `python` if that is your installed Python command. Other saved input
cases can be run by substituting their matching files from `tests/data/`.

### Automated tests

The suite runs all saved cases and additional algorithm and structure checks:

```sh
python3 -B -m unittest discover -s tests -v
```

On Windows:

```powershell
py -B -m unittest discover -s tests -v
```

The `-B` option keeps bytecode cache files out of the submission folder.
Actual VS Code integrated-terminal screenshots are in `screenshot/`.

To run and verify every saved execution without starting the optional viewer:

```sh
python3 -B tests/record_runs.py --verify-only
```

On Windows PowerShell:

```powershell
py -B .\tests\record_runs.py --verify-only
```

### Execution screenshots

| Program | Screenshot |
| --- | --- |
| Problem 1 | [Sample](screenshot/p1_sample.png) |
| Problem 2 | [Sample](screenshot/p2_sample.png) |
| Problem 3 | [All three stacks](screenshot/p3_stacks.png) |
| Problem 4: ghosts were not eliminated | [Example 1](screenshot/p4_example1.png) |
| Problem 4: ghosts were eliminated | [Example 2](screenshot/p4_example2.png) |
| Automated tests | [Full test execution](screenshot/tests_unittest.png) |

The six supplied PNG files show the execution commands and outputs in the VS Code integrated terminal. The screenshots use the equivalent saved samples in `tests/data/`, which remain available. All test cases are retained in the root sample files and `tests/`; individual screenshots are provided for representative examples.
To optionally rerun all cases and open the local execution viewer:

```sh
python3 -B tests/record_runs.py
```

On Windows, replace `python3` with `py` or `python`. Open
`http://127.0.0.1:8765/` in a browser. Press Ctrl+C to stop the viewer. The helper keeps actual output in
memory and writes no result text files.

### Repository submission

Place this entire `Homework3/` folder in your Git repository, commit it, and
push it. Keeping the folder name satisfies the assignment's folder option.
Confirm that the source files, sample input files, README, `tests/`, and `screenshot/` are visible
in the repository, then submit the repository link on Brightspace.
