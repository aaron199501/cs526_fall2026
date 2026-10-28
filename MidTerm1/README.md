# CS526 Mid-Term 1

Boston University Metropolitan College

## Introduction

This midterm implements three algorithms: finding a three-day snowfall window
that exceeds half the total, simulating synchronous infection on a square grid,
and validating a partially filled symbol puzzle. The programs require Python
3.9 or later and use only the standard library. No package installation is
required. Inputs are assumed to be well formed, as the assignment permits.

All three programs are at the assignment root, following the layout of the
other homework folders. Each accepts an input filename or standard input.
All eleven supplied input files are preserved unchanged. The assignment lists
snowfall inputs 1-4, pandemic inputs 1-2, and puzzle inputs 1-2; the supplied
folder also includes snowfall input 5 and puzzle inputs 3-4.

| File or folder | Purpose |
| --- | --- |
| `snowfall.py` | Problem 1: Snowfall (35 points) |
| `pandemic.py` | Problem 2: Pandemic (35 points) |
| `puzzle_game.py` | Problem 3: Symbol Puzzle Game (30 points) |
| `inputs/` | All eleven original input files, unchanged |
| `tests/test_midterm.py` | 27 automated tests, including 950 deterministic random cases |
| `tests/run_examples.py` | Runs demonstrations and reports actual commands and output |
| `tests/input_sha256.json` | SHA-256 hashes of the eleven supplied inputs |
| `tests/screenshot_sha256.json` | SHA-256 hashes of the twelve current screenshots |
| `example_executions/` | Saved commands and actual execution output |
| `screenshot/` | Twelve VS Code integrated terminal screenshots |

## Algorithm

### Problem 1: Snowfall

The input contains `n`, followed by the `n` cumulative snowfall totals. The
last cumulative value is the total snowfall. Scan every three-day window,
including days 1, 2, and 3. For a window ending at zero-based index `end`, its
snowfall is `cumulative[end] - cumulative[end - 3]`; use zero as the subtracted
value for the first window.

Return `YES` as soon as `2 * window_total > total`. If no window qualifies,
return `NO`. Fewer than three days also returns `NO`. The strict comparison
rejects a window containing exactly half the total. `Fraction` reads numeric
tokens exactly, including decimal tokens, so rounding cannot change this
boundary. The output preserves the input's numeric spelling and has the form
`<cumulative values> solution: YES` or `<cumulative values> solution: NO`.

**Correctness.** Subtracting the cumulative total before a window removes
exactly the snowfall on earlier days, leaving the sum on its three days. The
loop considers every possible ending index from 2 through `n - 1`, so it
checks every three-day window once. It returns `YES` only when a window meets
the strict inequality. If none does, or no three-day window exists, `NO` is
correct.

**Code.** `read_input(text)` returns the cumulative values as exact `Fraction`
objects and handles a leading UTF-8 byte-order mark.
`has_heavy_three_days(cumulative)` performs the scan and returns a Boolean.
`main()` reads the optional file or standard input and prints the original
numeric tokens followed by the answer.

**Complexity.** The scan performs O(n) arithmetic operations and uses O(1)
additional numeric values beyond the input list. Parsing and storing the input
require O(n) entries, giving O(n) time and O(n) total space under the usual
fixed-size-number model. With unbounded-length numbers, `Fraction` arithmetic
and storage also depend on their bit lengths.

### Problem 2: Pandemic

The input begins with the side length `N`. Each remaining line gives the
zero-based row and column of an initially infected county. Represent the state
with an `N` by `N` Boolean grid, where `True` means infected.

For each day, scan the healthy counties. Count infected neighbors above,
below, left, and right, using only positions inside the grid. Diagonals do not
count. Save counties with at least two infected neighbors in a separate list.
After the whole scan, mark all listed counties infected together. An infected
county stays infected. Repeat until the list is empty, then check for a healthy
county in the final grid.

**Correctness.** The initial grid represents Day 1. Assume a grid represents
the current day correctly. Because the grid is unchanged during the scan, the
pending list contains exactly the healthy counties with at least two neighbors
infected on that day. Applying the entire list produces the correct next-day
state. Induction therefore proves that every simulated state is correct. Each
nonterminal round infects at least one new county, so there can be at most
`N^2` such rounds. An empty list means that no further infection is possible.
Checking the final grid then gives the required healthy-county answer.

**Code.** `read_input(text)` returns the grid size and initial coordinate pairs.
`simulate(n, initial, show_days=False)` returns the final Boolean grid.
`print_board(board, day)` displays infected cells as `X` and healthy cells as
`.`. `main()` selects file or standard input, runs the simulation, and prints
exactly one of these final messages:

```text
There are healthy counties left
There are no healthy counties left
```

The optional `--show-days` flag prints the initial board as Day 1 and each
changed board. The unchanged terminating board is not printed a second time.
The required message remains the final output line.

**Complexity.** Let `K` be the number of input coordinate pairs and `D` the
number of full-grid scans, including the final scan. Each scan checks at most
four neighbors per cell, so time is O(K + D*N^2). Since `D <= N^2 + 1`, a
conservative worst-case bound is O(K + N^4). The board and pending list use
O(N^2) auxiliary space. Including the parsed coordinates, stored data uses
O(K + N^2) space. The program works for any supplied grid size `N`.

### Problem 3: Symbol Puzzle Game

The input contains `n`, a comma-separated list of `n` distinct allowed symbols,
and `n` comma-separated board rows. The assignment guarantees that the square
root of `n` is an integer. A dot (`.`) is an empty cell. Commas are separators.

Scan the board once, maintaining a set for each row, column, and square
sub-board. Skip dots. For every other value, check that it belongs to the
allowed symbols and has not appeared in its row, column, or sub-board. A failed
check makes the board invalid; otherwise, add the symbol to all three sets.
If the scan finishes, the board is valid.

Let `k = sqrt(n)`. The sub-board index is
`(row // k) * k + column // k`. This divides the board into `n` non-overlapping
`k` by `k` sub-boards starting at the top-left corner.

**Correctness.** Before a cell is processed, each set contains exactly the
non-empty symbols already visited in that region. A repeated symbol is found
when its later occurrence is visited. A non-empty symbol outside the allowed
list is rejected immediately. If the scan finishes, every non-empty value is
allowed and every row, column, and sub-board has no repetitions, which are
exactly the required conditions. Empty cells are skipped and never make the
board invalid. This checks the current state; it does not require a completed
board or test whether it can later be solved.

**Code.** `read_input(text)` returns `(symbols, board)`, splitting values on
commas and removing surrounding whitespace. `is_valid_board(symbols, board)`
uses `math.isqrt` and the sets to return a Boolean. `main()` reads the file or
standard input and prints exactly `The board is valid` or
`The board is invalid`.

**Complexity.** For an `n` by `n` board, expected time is O(n^2) under the usual
hash-set model. The region sets store at most three entries per non-empty
cell, so auxiliary space is O(n^2). The parsed board also uses O(n^2) space.
These bounds treat symbols as fixed-size values.

## How to run

Open the `MidTerm1/` folder in the standard VS Code application and open its
integrated terminal. Run every command below from that folder. The examples
use `python`; use `python3` on systems with that command, or `py` on Windows
when using the Python launcher. The optional `-B` flag prevents bytecode cache
files and does not change program output.

### All supplied inputs

```sh
python -B snowfall.py inputs/snowfall_input1.txt
python -B snowfall.py inputs/snowfall_input2.txt
python -B snowfall.py inputs/snowfall_input3.txt
python -B snowfall.py inputs/snowfall_input4.txt
python -B snowfall.py inputs/snowfall_input5.txt

python -B pandemic.py inputs/pandemic_input1.txt
python -B pandemic.py inputs/pandemic_input2.txt

python -B puzzle_game.py inputs/puzzle_game_input1.txt
python -B puzzle_game.py inputs/puzzle_game_input2.txt
python -B puzzle_game.py inputs/puzzle_game_input3.txt
python -B puzzle_game.py inputs/puzzle_game_input4.txt
```

The five snowfall results, in order, are:

```text
1 4 10 14 15 17 17 23 solution: YES
44 127 166 231 238 320 363 429 500 511 577 642 689 764 812 886 solution: NO
3 8 14 19 21 24 25 25 32 solution: NO
1 2 3 4 5 solution: YES
1 2 3 solution: YES
```

Pandemic inputs 1 and 2 print `There are healthy counties left` and
`There are no healthy counties left`, respectively. Puzzle inputs 1-4 print
valid, invalid, valid, and invalid, using the exact messages above. Snowfall
input 3 has maximum three-day snowfall 16 out of 32, so it correctly returns
`NO`. Puzzle inputs 1-2 are 9 by 9 and inputs 3-4 are 4 by 4.

### Standard input and daily boards

In Command Prompt, Bash, or another shell supporting input redirection:

```sh
python -B snowfall.py < inputs/snowfall_input1.txt
python -B pandemic.py < inputs/pandemic_input1.txt
python -B puzzle_game.py < inputs/puzzle_game_input1.txt
```

In Windows PowerShell:

```powershell
Get-Content -Raw inputs/snowfall_input1.txt | python -B snowfall.py
Get-Content -Raw inputs/pandemic_input1.txt | python -B pandemic.py
Get-Content -Raw inputs/puzzle_game_input1.txt | python -B puzzle_game.py
```

To display the synchronous daily infection states:

```sh
python -B pandemic.py inputs/pandemic_input1.txt --show-days
```

### Automated verification

```sh
python -B -m unittest discover -s tests -v
python -B tests/run_examples.py all
```

The 27 tests check all original inputs, exact output messages, filename and
standard input, snowfall boundaries, synchronous infection updates, and puzzle
row, column, sub-board, and symbol rules. They include 950 deterministic random
cases checked against independent reference algorithms. The saved
[test execution](example_executions/tests.txt) records an actual test run.

To reproduce an individual recorded demonstration:

```sh
python -B tests/run_examples.py snowfall_1
python -B tests/run_examples.py pandemic_2
python -B tests/run_examples.py puzzle_4
python -B tests/run_examples.py pandemic_days
```

## Example executions

The execution records show the command, Python version, exit status, elapsed
time, and real program output. Each assignment program prints the required
answer format. To reproduce an execution, use the direct program commands
listed in How to run above.

The following table links twelve saved text executions and their VS Code
integrated terminal screenshots. Each screenshot shows the relevant source
code on the left and its actual execution command and output on the right.
The daily-board screenshot includes every printed board and the final answer.
The eleven original input cases include all
four Snowfall demonstrations required by the assignment; the additional
demonstration displays the synchronous daily infection states.

| Demonstration | Actual execution | Screenshot |
| --- | --- | --- |
| Snowfall input 1: YES | [Run](example_executions/snowfall_1.txt) | [Image](screenshot/snowfall_1.jpg) |
| Snowfall input 2: NO | [Run](example_executions/snowfall_2.txt) | [Image](screenshot/snowfall_2.jpg) |
| Snowfall input 3: NO | [Run](example_executions/snowfall_3.txt) | [Image](screenshot/snowfall_3.jpg) |
| Snowfall input 4: YES | [Run](example_executions/snowfall_4.txt) | [Image](screenshot/snowfall_4.jpg) |
| Snowfall input 5: YES | [Run](example_executions/snowfall_5.txt) | [Image](screenshot/snowfall_5.jpg) |
| Pandemic input 1: healthy counties remain | [Run](example_executions/pandemic_1.txt) | [Image](screenshot/pandemic_1.jpg) |
| Pandemic input 2: no healthy counties remain | [Run](example_executions/pandemic_2.txt) | [Image](screenshot/pandemic_2.jpg) |
| Puzzle input 1: valid | [Run](example_executions/puzzle_1.txt) | [Image](screenshot/puzzle_1.jpg) |
| Puzzle input 2: invalid | [Run](example_executions/puzzle_2.txt) | [Image](screenshot/puzzle_2.jpg) |
| Puzzle input 3: valid | [Run](example_executions/puzzle_3.txt) | [Image](screenshot/puzzle_3.jpg) |
| Puzzle input 4: invalid | [Run](example_executions/puzzle_4.txt) | [Image](screenshot/puzzle_4.jpg) |
| Pandemic synchronous daily boards | [Run](example_executions/pandemic_days.txt) | [Image](screenshot/pandemic_days.jpg) |

The [combined supplied-input log](example_executions/supplied_runs.txt) records
all eleven original cases.

Keep this complete `MidTerm1/` folder in the Git repository. The assignment
folder is [MidTerm1 on GitHub](https://github.com/aaron199501/cs526_fall2026/tree/main/MidTerm1).
Submit the GitHub repository or assignment-folder link in Blackboard.
