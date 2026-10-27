CS526 Mid-Term 1
Boston University Metropolitan College

Submission
----------
Repository: https://github.com/aaron199501/cs526_fall2026
Assignment folder: MidTerm1/
Latest folder link: https://github.com/aaron199501/cs526_fall2026/tree/main/MidTerm1

Submit the GitHub folder link in Blackboard, as for the homeworks. A folder
link using a full commit hash preserves the exact submitted version.
This folder contains all program source code, supplied inputs, running
examples, and algorithm descriptions. Each problem has its own readme with
its algorithm and exact run commands. Saved execution output is in results/;
screenshots are in screenshot/.
MidTerm1.zip is provided separately as a local archive of this folder.
Uploading files to GitHub does not submit the link in Blackboard.

Contents
--------
MidTerm1.code-workspace             Portable VS Code folder and layout settings
Problem1_Snowfall/snowfall.py        Problem 1 (35 points)
Problem1_Snowfall/readme.txt         Algorithm, correctness, code, run commands
Problem1_Snowfall/inputs/            Five unchanged supplied inputs
Problem2_Pandemic/pandemic.py        Problem 2 (35 points)
Problem2_Pandemic/readme.txt         Algorithm, correctness, code, run commands
Problem2_Pandemic/inputs/            Two unchanged supplied inputs
Problem3_SymbolPuzzle/puzzle_game.py Problem 3 (30 points)
Problem3_SymbolPuzzle/readme.txt     Algorithm, correctness, code, run commands
Problem3_SymbolPuzzle/inputs/        Four unchanged supplied inputs
tests/test_midterm.py               Independent automated verification
tests/run_examples.py               Reproducible real execution demonstrations
results/                           Saved execution logs and input SHA-256 hashes
screenshot/                        Original VS Code window captures

Requirements and execution
--------------------------
Python 3.9 or later; no third-party packages are required.
In the standard VS Code application, open MidTerm1.code-workspace or open the
folder containing this readme, then open its integrated terminal. The portable
workspace file configures the project folder and editor layout. All commands
in this root readme are run from that folder. Each problem's own readme also
provides commands to run directly from that problem's directory.

    python Problem1_Snowfall/snowfall.py Problem1_Snowfall/inputs/snowfall_input1.txt
    python Problem2_Pandemic/pandemic.py Problem2_Pandemic/inputs/pandemic_input1.txt
    python Problem3_SymbolPuzzle/puzzle_game.py Problem3_SymbolPuzzle/inputs/puzzle_game_input1.txt

Each program accepts a filename argument or, if it is omitted, standard input.
For example, in PowerShell:

    Get-Content -Raw Problem1_Snowfall/inputs/snowfall_input1.txt | python Problem1_Snowfall/snowfall.py

The commands assume that python selects an installed Python 3 interpreter.
On Windows, py can be used instead; on systems using python3, substitute
python3. The refreshed saved runs use the locally installed Python 3.14.7.
These exact PowerShell commands use that interpreter on this computer:

    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B tests/run_examples.py all
    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B tests/run_examples.py pandemic_days
    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B -m unittest discover -s tests -v

On another computer, use its installed Python interpreter or the portable
python commands shown above. -B prevents creation of __pycache__ directories;
it does not change the program answers.

Problem 1: Snowfall
-------------------
Scan each possible three-day window. Its snowfall is the cumulative value at
its end minus the cumulative value just before its start (or zero for the
first window). Return YES exactly when twice that amount exceeds the final
cumulative total. Fewer than three days returns NO. Exact numeric arithmetic
also supports decimal snowfall totals without rounding a half-total boundary.
Print the original cumulative values followed by solution: YES or solution: NO.
The scan takes O(n) arithmetic operations and O(1) extra scan space; parsing
and retaining the input require O(n) storage, with numeric sizes treated as
bounded. See the problem's readme for details and the correctness argument.

Problem 2: Pandemic
-------------------
Store infection in an N by N Boolean grid. Each round, inspect four neighbors
of each healthy county and collect those with at least two infected neighbors.
Apply all collected changes together after the scan. Stop when none are found.
This preserves synchronous days. Inspect the fixed point for healthy counties.
For K initial coordinate pairs and D scans, time is O(K + D*N^2); the
conservative worst case is O(K + N^4). The grid and pending changes use O(N^2)
auxiliary space. The --show-days option displays the initial state as Day 1
and each changed board. The unchanged final board is not printed twice.
The program's final line is always the exact required healthy-county message.

Problem 3: Symbol Puzzle Game
----------------------------
Skip dots. Check every other value against the allowed symbols and against
the symbols already seen in its row, column, and square sub-board. Any failed
check returns invalid; reaching the end returns valid. The board need not be
complete, and the program does not solve it. For an n by n board, expected
time and auxiliary space are O(n^2) using hash sets and fixed-size symbols.

Supplied inputs and results
---------------------------
All eleven originals from MidTerm Input Files are retained byte-for-byte.
The assignment explicitly lists snowfall 1-4, pandemic 1-2, and puzzle 1-2.
The supplied folder additionally contains snowfall 5 and puzzle 3-4.

snowfall_input1.txt      YES
snowfall_input2.txt      NO
snowfall_input3.txt      NO
snowfall_input4.txt      YES
snowfall_input5.txt      YES
pandemic_input1.txt      There are healthy counties left
pandemic_input2.txt      There are no healthy counties left
puzzle_game_input1.txt   The board is valid
puzzle_game_input2.txt   The board is invalid
puzzle_game_input3.txt   The board is valid
puzzle_game_input4.txt   The board is invalid

The third snowfall input has maximum three-day snowfall 16 out of a total
32, so strict inequality correctly produces NO. Puzzle inputs 1-2 are 9 by 9;
inputs 3-4 are 4 by 4. Puzzle input 4 repeats @ only within the upper-left
sub-board, so checking rows and columns alone would miss its invalid state.

Verification
------------
Run all supplied inputs:

    python -B tests/run_examples.py all

Run the automated suite:

    python -B -m unittest discover -s tests -v

The 27 tests cover all original files and exact command-line messages,
filename and standard input, first and last snowfall windows, n < 3,
exactly half, zeros, decimals, and large integers. They compare 300 random
daily snowfall arrays against direct daily sums. Pandemic checks include
the assignment's exact daily boards, diagonal exclusion, empty/full grids,
N = 1, all sixteen initial 2 by 2 grids, and 250 random grids compared with
an independent event-driven final-closure algorithm. Puzzle checks isolate
row, column, and sub-board repetitions and unlisted symbols; they include
complete valid 4/9/16 boards, 200 valid partial boards, and 200 random boards
compared with pairwise checks of fully collected regions.
Random generators use fixed seeds so these checks can be reproduced.

Execution screenshots
---------------------
The screenshot folder contains thirteen original VS Code window captures:

    snowfall_1.jpg through snowfall_5.jpg
    pandemic_1.jpg and pandemic_2.jpg
    puzzle_1.jpg through puzzle_4.jpg
    pandemic_days.jpg
    tests.jpg

They show real Python 3.14.7 subprocess executions in the standard VS Code
application's integrated terminal.
An automated demonstration helper launches the programs, captures their actual
stdout/stderr, and prints the command, exit status, elapsed time, and output.
It prints the Python version by default. Add --show-interpreter to print the
exact Python executable path as well. In the displayed commands, python
denotes the interpreter used by the helper. No output is reconstructed from
answer files.
The status information precedes program output, so the required final output
line remains visible. Screenshots are saved directly from the window capture;
they are not retouched. The helper's timing is for verification, not a required
part of the assignment program's output.

To reproduce an individual demonstration:

    python -B tests/run_examples.py snowfall_1
    python -B tests/run_examples.py pandemic_2
    python -B tests/run_examples.py puzzle_4
    python -B tests/run_examples.py pandemic_days
    python -B tests/run_examples.py tests

To include the interpreter path in a demonstration:

    python -B tests/run_examples.py snowfall_1 --show-interpreter

