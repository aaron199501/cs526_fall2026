# CS526 Homework Assignment 3

Boston University Metropolitan College

## Introduction

This homework implements palindrome detection, recursive enumeration of unique
substrings, recursive in-place reversal of three stack implementations, and
intersection checking for fixed Ghostbuster/ghost pairs. The programs use only
the Python standard library and require Python 3.9 or later.

The submission includes all 29 inputs and all 28 expected-output files supplied
by the instructor. Every supplied expected output matches the corresponding
program output. The remaining input, `palendrome_4S.txt`, has no answer file in
the supplied resources; it is checked against an independent palindrome
reference instead. Actual executions are saved as text and browser screenshots.

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
| `tests/test_homework.py` | Original correctness, structure, and output tests |
| `tests/test_teacher_examples.py` | Regression tests for all 29 instructor inputs |
| `tests/teacher_cases.py` | Maps instructor inputs to programs and answers; independently checks the input with no supplied answer |
| `tests/record_runs.py` | Runs and verifies the programs, exports actual execution transcripts, and optionally serves a local execution viewer |
| `tests/data/` | Original automated-test inputs and expected-output fixtures |
| `tests/teacher_resources/` | All 58 instructor files, preserving their original contents and names |
| `example_executions/` | Actual commands, outputs, and comparison results for all 29 instructor inputs, the stack demonstration, and the expanded test suite |
| `screenshot/` | Screenshots of all 29 instructor-input executions, fresh stack and test executions, and six retained terminal examples |

## Files and repository layout

Use the assignment's folder option by placing this entire `Homework3/` folder
in your Git repository. A suitable repository layout is:

```text
<your-repository>/
`-- Homework3/
    |-- .gitignore
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
    |   |-- test_teacher_examples.py
    |   |-- teacher_cases.py
    |   |-- record_runs.py
    |   |-- data/
    |   |   |-- *_input.txt
    |   |   `-- *_expected.txt
    |   `-- teacher_resources/
    |       |-- Homework3.txt
    |       |-- palendrome_*.txt
    |       |-- palendrome_ans_*.txt
    |       |-- unique_substrings_input_*.txt
    |       |-- unique_substrings_ans_*.txt
    |       |-- ghostbusters_input_*.txt
    |       `-- ghostbusters_ans_*.txt
    |-- example_executions/
    |   `-- *.txt
    `-- screenshot/
        |-- teacher_*.jpg
        |-- p3_stacks.jpg
        |-- tests_unittest.jpg
        |-- p1_sample.png
        |-- p2_sample.png
        |-- p3_stacks.png
        |-- p4_example1.png
        |-- p4_example2.png
        `-- tests_unittest.png
```

The four source programs and the two original sample input files are at the
homework root. All automated tests and their input/output fixtures remain in
`tests/`. The instructor's spelling `palendrome` is preserved in the resource
filenames; the Problem 1 program is named `palindrome.py`.
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
- Instructor resources cover 15 palindrome inputs, three substring inputs, and
  11 Ghostbuster inputs. Problem 3 has no instructor input file because its
  required input is the fixed sequence 1 through 10.
- Output comparison checks every line. It treats Windows CRLF and Unix LF as
  equivalent and allows one optional final newline; it does not ignore spaces,
  capitalization, or extra output lines.
- `palendrome_ans_4S.txt` was not supplied. The independent reference compares
  characters from both ends after removing literal spaces. This case produces
  ten Boolean results and a final palindrome count of 4. Its transcript and
  screenshot explicitly identify this independent check.
- All 29 instructor-input executions have individual screenshots in
  `screenshot/`. The JPEG files are captures of the local execution viewer
  displaying real subprocess output. Six original VS Code terminal PNG files
  are retained as earlier examples; the old test PNG shows the earlier
  32-test suite, while the fresh JPEG shows the expanded suite.

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

### Instructor inputs

Run an individual instructor case by selecting its input file. For example:

```sh
python3 -B palindrome.py < tests/teacher_resources/palendrome_0.txt
python3 -B substrings.py < tests/teacher_resources/unique_substrings_input_0.txt
python3 -B ghostbusters.py < tests/teacher_resources/ghostbusters_input_0.txt
```

On Windows PowerShell:

```powershell
Get-Content .\tests\teacher_resources\palendrome_0.txt | py -B .\palindrome.py
Get-Content .\tests\teacher_resources\unique_substrings_input_0.txt | py -B .\substrings.py
Get-Content .\tests\teacher_resources\ghostbusters_input_0.txt | py -B .\ghostbusters.py
```

Substitute any input linked in the tables below to run another case. The
automated commands in the next section run every instructor case together.

### Automated tests

The suite runs all original cases, all 29 instructor inputs, and the algorithm
and structure checks:

```sh
python3 -B -m unittest discover -s tests -v
```

On Windows:

```powershell
py -B -m unittest discover -s tests -v
```

The `-B` option keeps bytecode cache files out of the submission folder.

To run and verify all 48 saved executions, including the complete test suite,
without starting the optional viewer:

```sh
python3 -B tests/record_runs.py --verify-only
```

On Windows PowerShell:

```powershell
py -B .\tests\record_runs.py --verify-only
```

To regenerate the 31 actual execution transcripts in `example_executions/`:

```sh
python3 -B tests/record_runs.py --export --verify-only
```

On Windows PowerShell:

```powershell
py -B .\tests\record_runs.py --export --verify-only
```

Each transcript records the command, input, actual output, and comparison
result. The recorded commands use Linux/macOS redirection syntax; use the
PowerShell equivalents above on Windows. Exporting reruns the programs and
updates the transcripts. Screenshots are captured separately from the viewer.

### Instructor example executions

All 28 cases with supplied answers passed comparison. The remaining case
passed the independent reference check. Each row links to the original input,
its expected output when supplied, the actual execution, and its screenshot.

#### Problem 1

| Input | Instructor answer | Actual execution | Screenshot |
| --- | --- | --- | --- |
| [palendrome_0.txt](tests/teacher_resources/palendrome_0.txt) | [Answer](tests/teacher_resources/palendrome_ans_0.txt) | [Run](example_executions/teacher_palendrome_0.txt) | [Image](screenshot/teacher_palendrome_0.jpg) |
| [palendrome_0L.txt](tests/teacher_resources/palendrome_0L.txt) | [Answer](tests/teacher_resources/palendrome_ans_0L.txt) | [Run](example_executions/teacher_palendrome_0L.txt) | [Image](screenshot/teacher_palendrome_0L.jpg) |
| [palendrome_0S.txt](tests/teacher_resources/palendrome_0S.txt) | [Answer](tests/teacher_resources/palendrome_ans_0S.txt) | [Run](example_executions/teacher_palendrome_0S.txt) | [Image](screenshot/teacher_palendrome_0S.jpg) |
| [palendrome_1.txt](tests/teacher_resources/palendrome_1.txt) | [Answer](tests/teacher_resources/palendrome_ans_1.txt) | [Run](example_executions/teacher_palendrome_1.txt) | [Image](screenshot/teacher_palendrome_1.jpg) |
| [palendrome_1L.txt](tests/teacher_resources/palendrome_1L.txt) | [Answer](tests/teacher_resources/palendrome_ans_1L.txt) | [Run](example_executions/teacher_palendrome_1L.txt) | [Image](screenshot/teacher_palendrome_1L.jpg) |
| [palendrome_1S.txt](tests/teacher_resources/palendrome_1S.txt) | [Answer](tests/teacher_resources/palendrome_ans_1S.txt) | [Run](example_executions/teacher_palendrome_1S.txt) | [Image](screenshot/teacher_palendrome_1S.jpg) |
| [palendrome_2.txt](tests/teacher_resources/palendrome_2.txt) | [Answer](tests/teacher_resources/palendrome_ans_2.txt) | [Run](example_executions/teacher_palendrome_2.txt) | [Image](screenshot/teacher_palendrome_2.jpg) |
| [palendrome_2L.txt](tests/teacher_resources/palendrome_2L.txt) | [Answer](tests/teacher_resources/palendrome_ans_2L.txt) | [Run](example_executions/teacher_palendrome_2L.txt) | [Image](screenshot/teacher_palendrome_2L.jpg) |
| [palendrome_2S.txt](tests/teacher_resources/palendrome_2S.txt) | [Answer](tests/teacher_resources/palendrome_ans_2S.txt) | [Run](example_executions/teacher_palendrome_2S.txt) | [Image](screenshot/teacher_palendrome_2S.jpg) |
| [palendrome_3.txt](tests/teacher_resources/palendrome_3.txt) | [Answer](tests/teacher_resources/palendrome_ans_3.txt) | [Run](example_executions/teacher_palendrome_3.txt) | [Image](screenshot/teacher_palendrome_3.jpg) |
| [palendrome_3L.txt](tests/teacher_resources/palendrome_3L.txt) | [Answer](tests/teacher_resources/palendrome_ans_3L.txt) | [Run](example_executions/teacher_palendrome_3L.txt) | [Image](screenshot/teacher_palendrome_3L.jpg) |
| [palendrome_3S.txt](tests/teacher_resources/palendrome_3S.txt) | [Answer](tests/teacher_resources/palendrome_ans_3S.txt) | [Run](example_executions/teacher_palendrome_3S.txt) | [Image](screenshot/teacher_palendrome_3S.jpg) |
| [palendrome_4.txt](tests/teacher_resources/palendrome_4.txt) | [Answer](tests/teacher_resources/palendrome_ans_4.txt) | [Run](example_executions/teacher_palendrome_4.txt) | [Image](screenshot/teacher_palendrome_4.jpg) |
| [palendrome_4L.txt](tests/teacher_resources/palendrome_4L.txt) | [Answer](tests/teacher_resources/palendrome_ans_4L.txt) | [Run](example_executions/teacher_palendrome_4L.txt) | [Image](screenshot/teacher_palendrome_4L.jpg) |
| [palendrome_4S.txt](tests/teacher_resources/palendrome_4S.txt) | Not supplied; independent reference | [Run](example_executions/teacher_palendrome_4S.txt) | [Image](screenshot/teacher_palendrome_4S.jpg) |

#### Problem 2

| Input | Instructor answer | Actual execution | Screenshot |
| --- | --- | --- | --- |
| [unique_substrings_input_0.txt](tests/teacher_resources/unique_substrings_input_0.txt) | [Answer](tests/teacher_resources/unique_substrings_ans_0.txt) | [Run](example_executions/teacher_unique_substrings_input_0.txt) | [Image](screenshot/teacher_unique_substrings_input_0.jpg) |
| [unique_substrings_input_1.txt](tests/teacher_resources/unique_substrings_input_1.txt) | [Answer](tests/teacher_resources/unique_substrings_ans_1.txt) | [Run](example_executions/teacher_unique_substrings_input_1.txt) | [Image](screenshot/teacher_unique_substrings_input_1.jpg) |
| [unique_substrings_input_2.txt](tests/teacher_resources/unique_substrings_input_2.txt) | [Answer](tests/teacher_resources/unique_substrings_ans_2.txt) | [Run](example_executions/teacher_unique_substrings_input_2.txt) | [Image](screenshot/teacher_unique_substrings_input_2.jpg) |

#### Problem 3

The fixed stack demonstration is included as a [text execution](example_executions/p3_stacks.txt)
and a [fresh screenshot](screenshot/p3_stacks.jpg). It shows all three stack
implementations before and after reversing the numbers 1 through 10.

#### Problem 4

| Input | Instructor answer | Actual execution | Screenshot |
| --- | --- | --- | --- |
| [ghostbusters_input_0.txt](tests/teacher_resources/ghostbusters_input_0.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_0.txt) | [Run](example_executions/teacher_ghostbusters_input_0.txt) | [Image](screenshot/teacher_ghostbusters_input_0.jpg) |
| [ghostbusters_input_1.txt](tests/teacher_resources/ghostbusters_input_1.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_1.txt) | [Run](example_executions/teacher_ghostbusters_input_1.txt) | [Image](screenshot/teacher_ghostbusters_input_1.jpg) |
| [ghostbusters_input_2.txt](tests/teacher_resources/ghostbusters_input_2.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_2.txt) | [Run](example_executions/teacher_ghostbusters_input_2.txt) | [Image](screenshot/teacher_ghostbusters_input_2.jpg) |
| [ghostbusters_input_3.txt](tests/teacher_resources/ghostbusters_input_3.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_3.txt) | [Run](example_executions/teacher_ghostbusters_input_3.txt) | [Image](screenshot/teacher_ghostbusters_input_3.jpg) |
| [ghostbusters_input_4.txt](tests/teacher_resources/ghostbusters_input_4.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_4.txt) | [Run](example_executions/teacher_ghostbusters_input_4.txt) | [Image](screenshot/teacher_ghostbusters_input_4.jpg) |
| [ghostbusters_input_5.txt](tests/teacher_resources/ghostbusters_input_5.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_5.txt) | [Run](example_executions/teacher_ghostbusters_input_5.txt) | [Image](screenshot/teacher_ghostbusters_input_5.jpg) |
| [ghostbusters_input_6.txt](tests/teacher_resources/ghostbusters_input_6.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_6.txt) | [Run](example_executions/teacher_ghostbusters_input_6.txt) | [Image](screenshot/teacher_ghostbusters_input_6.jpg) |
| [ghostbusters_input_7.txt](tests/teacher_resources/ghostbusters_input_7.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_7.txt) | [Run](example_executions/teacher_ghostbusters_input_7.txt) | [Image](screenshot/teacher_ghostbusters_input_7.jpg) |
| [ghostbusters_input_8.txt](tests/teacher_resources/ghostbusters_input_8.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_8.txt) | [Run](example_executions/teacher_ghostbusters_input_8.txt) | [Image](screenshot/teacher_ghostbusters_input_8.jpg) |
| [ghostbusters_input_9.txt](tests/teacher_resources/ghostbusters_input_9.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_9.txt) | [Run](example_executions/teacher_ghostbusters_input_9.txt) | [Image](screenshot/teacher_ghostbusters_input_9.jpg) |
| [ghostbusters_input_10.txt](tests/teacher_resources/ghostbusters_input_10.txt) | [Answer](tests/teacher_resources/ghostbusters_ans_10.txt) | [Run](example_executions/teacher_ghostbusters_input_10.txt) | [Image](screenshot/teacher_ghostbusters_input_10.jpg) |

The expanded automated test run is included as a [text execution](example_executions/tests_unittest.txt)
and a [fresh screenshot](screenshot/tests_unittest.jpg).

### Retained terminal examples

| Program | Screenshot |
| --- | --- |
| Problem 1 | [Sample](screenshot/p1_sample.png) |
| Problem 2 | [Sample](screenshot/p2_sample.png) |
| Problem 3 | [All three stacks](screenshot/p3_stacks.png) |
| Problem 4: ghosts were not eliminated | [Example 1](screenshot/p4_example1.png) |
| Problem 4: ghosts were eliminated | [Example 2](screenshot/p4_example2.png) |
| Earlier automated tests | [Original 32-test execution](screenshot/tests_unittest.png) |

These six PNG files show earlier commands and outputs in the VS Code integrated
terminal. Their corresponding original input files remain available. The fresh
JPEG captures and text executions above show the instructor inputs and the
expanded tests.

### Local execution viewer

To rerun all cases and open the local execution viewer:

```sh
python3 -B tests/record_runs.py
```

On Windows, replace `python3` with `py` or `python`. Open
`http://127.0.0.1:8765/` in a browser. Each page displays a real captured
execution, its input, actual output, and verification result. Press Ctrl+C to
stop the viewer. Without `--export`, the helper keeps results in memory and
writes no execution text files.

### Repository submission

Place this entire `Homework3/` folder in your Git repository, commit it, and
push it. Keeping the folder name satisfies the assignment's folder option.
Confirm that the source files, sample input files, README, `tests/`,
`example_executions/`, and `screenshot/` are visible in the repository, then
submit the repository link on Brightspace.
