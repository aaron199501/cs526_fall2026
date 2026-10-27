CS526 Mid-Term - Problem 2: Pandemic

Requirements
------------
Python 3.9 or later. Only the Python standard library is used.

Input
-----
The first line is N, the side length of the square grid. Every subsequent
nonempty line gives the row and column of one initially infected county.
Rows and columns start at 0. There is no separate infected-county count.
The input format is assumed to be correct, as allowed by the assignment.
The files in inputs/ are unchanged copies of the supplied sample inputs.

Heart of the algorithm
----------------------
Represent the state with an N by N Boolean grid: True means infected.
Initially, mark exactly the counties listed in the input. For each day,
scan every healthy county and count its infected neighbors above, below,
left, and right. Do not count diagonal neighbors or positions outside the
grid. Save every county with at least two infected neighbors in a separate
newly_infected list. Only after finishing the whole scan, mark all counties
in that list infected. Repeat until the list is empty.

The separate list is essential: all neighbor counts use the same day's
grid, so an infection discovered during a scan cannot spread again during
that scan. Previously infected counties remain infected.

Correctness
-----------
The initial grid exactly represents Day 1. Suppose the grid represents the
current day correctly. Each healthy county is added to newly_infected if
and only if at least two of its four in-bounds neighbors are currently
infected. Because the grid is unchanged during this scan, the list contains
exactly the counties that should become infected on the next day. Applying
the whole list therefore produces the correct next-day state. By induction,
all simulated states are correct. Every nonterminal round infects at least
one previously healthy county, and there are only N squared counties, so
the simulation terminates. An empty list means no county can become infected
under the rule, so the state is final. Checking this final grid for any
False cell gives exactly the required healthy-county answer.

Code explanation
----------------
read_input(text) returns N and the list of initial coordinate pairs.
simulate(n, initial, show_days=False) returns the final Boolean grid.
print_board(board, day) displays X for infected counties and . for healthy
counties. main() reads a filename argument or standard input, runs the
simulation, and prints the required final message.

Complexity
----------
Let K be the number of input coordinate pairs and D the number of full-grid
scans, including the final scan that finds no new infections. Each scan
checks at most four neighbors per cell. Time is O(K + D*N^2). Since there
can be at most N^2 nonempty infection rounds, D <= N^2 + 1, giving the
conservative worst-case bound O(K + N^4). The board and pending list use
O(N^2) auxiliary space. Including the parsed coordinate list, stored data
uses O(K + N^2) space.

How to run
----------
Open the MidTerm1 folder in VS Code and open its integrated terminal.
Change into this problem's directory:

    cd Problem2_Pandemic

Run these exact commands from Problem2_Pandemic:

    python pandemic.py inputs/pandemic_input1.txt
    python pandemic.py inputs/pandemic_input2.txt

Expected outputs, respectively:

    There are healthy counties left
    There are no healthy counties left

Optional daily-board demonstration:

    python pandemic.py inputs/pandemic_input1.txt --show-days

Day 1 is the initial state. Only the initial board and changed boards are
printed; the unchanged terminating board is not printed a second time.
The final output line is still exactly one of the two required messages.

Standard-input alternative in Windows PowerShell:

    Get-Content inputs/pandemic_input1.txt | python pandemic.py

Standard-input alternative in Command Prompt or Bash:

    python pandemic.py < inputs/pandemic_input1.txt

On Windows, py may be substituted for python. On systems using python3,
substitute python3 for python.

Interpreter used for verification on this computer
-------------------------------------------------
The refreshed saved runs use the locally installed Python 3.14.7.
These exact Windows PowerShell commands work from Problem2_Pandemic:

    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B pandemic.py inputs/pandemic_input1.txt
    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B pandemic.py inputs/pandemic_input2.txt
    & 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B pandemic.py inputs/pandemic_input1.txt --show-days

The -B option prevents Python from writing bytecode cache files; it does
not change the program's result. On another computer, use the portable
python commands above or substitute its installed Python interpreter.
