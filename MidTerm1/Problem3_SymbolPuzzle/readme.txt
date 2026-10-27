CS526 Mid-Term - Problem 3: Symbol Puzzle Game

Requirements
------------
Python 3.9 or later. Only the Python standard library is used.
The input is assumed to be well formed, as allowed by the assignment.
The board size n has an integer square root, and the symbol list contains
n distinct symbols. A dot (.) represents an empty cell.

Heart of the algorithm
---------------------
Scan the board once, keeping one set for each row, each column, and each
square sub-board. Skip empty cells. For each non-empty symbol, first check
that it belongs to the allowed symbol list. Then check whether it has
already appeared in its row, column, or sub-board. If any check fails,
return invalid. Otherwise add the symbol to all three sets and continue.

Let k = sqrt(n). The sub-board index for a cell (row, column) is
(row // k) * k + column // k. The top-left sub-board has index 0.
This divides the n by n board into n non-overlapping k by k sub-boards.

Correctness
-----------
Before a cell is processed, each set contains exactly the non-empty
symbols already visited in its corresponding row, column, or sub-board.
Finding the current symbol in one of those sets proves a repeated symbol
in that region. A symbol outside the allowed set is also invalid.
Every repeated symbol is detected when its later occurrence is visited.
If the scan finishes, all non-empty symbols are allowed and every row,
column, and sub-board satisfies uniqueness, so the board is valid.
Dots are skipped and therefore never cause a duplicate-symbol failure.

This program checks only the current board. Empty cells are permitted;
it does not fill them, solve the puzzle, or test future solvability.

Code explanation
----------------
read_input(text) returns (symbols, board). It reads n, splits the next
line on commas, and reads the next n comma-separated rows. It removes
surrounding whitespace from values and tolerates trailing blank lines.
Commas are separators and are never treated as puzzle symbols.

is_valid_board(symbols, board) performs the set-based validation and
returns True or False. math.isqrt obtains the integer sub-board width.

main() reads the filename argument, or standard input when no filename
is provided, and prints exactly one of these messages:
The board is valid
The board is invalid

Complexity
----------
For an n by n board, the scan takes O(n^2) expected time under the usual
hash-set model. Up to three set entries are stored for each non-empty
cell, so auxiliary space is O(n^2). The parsed board also uses O(n^2)
space. These bounds treat each symbol as a fixed-size value.

How to run
----------
Open the MidTerm1 folder in VS Code and open its integrated terminal.
Change to this problem's directory:

cd Problem3_SymbolPuzzle

Run the four supplied input files:

python puzzle_game.py inputs/puzzle_game_input1.txt
python puzzle_game.py inputs/puzzle_game_input2.txt
python puzzle_game.py inputs/puzzle_game_input3.txt
python puzzle_game.py inputs/puzzle_game_input4.txt

Expected results in the same order:
The board is valid
The board is invalid
The board is valid
The board is invalid

The assignment names inputs 1 and 2. The supplied input folder also
contains inputs 3 and 4; all four original files are included unchanged.
The first two boards are 9 by 9 and the last two are 4 by 4.

On Windows, py may be substituted for python. On systems using python3,
substitute python3 for python.

The refreshed saved runs use the locally installed Python 3.14.7. This exact
PowerShell command selects that interpreter on this computer:

& 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B puzzle_game.py inputs/puzzle_game_input1.txt

Replace the input filename with inputs 2, 3, and 4 to repeat those runs.
On another computer, use the portable python commands above or substitute
the path to its installed Python interpreter. The optional -B flag prevents
bytecode cache files and does not affect the answer.

Standard input is also supported. In Command Prompt, Bash, or a similar
shell supporting input redirection:

python puzzle_game.py < inputs/puzzle_game_input1.txt

In PowerShell, use the filename commands above, or pipe the file text:

Get-Content -Raw inputs/puzzle_game_input1.txt | python puzzle_game.py
