CS526 Mid-Term - Problem 1: Snowfall

Purpose
-------
Determine whether any three consecutive days contain strictly more than half
of the total snowfall. The input contains the number of days on line 1 and
that many cumulative snowfall totals on line 2. The supplied files contain
integer totals; exact decimal totals are supported as well. Python 3.9 or
later is required, using only the standard library. The input is assumed
to be well formed, as the assignment allows.

Core algorithm
--------------
The last cumulative value is the total snowfall. Visit every three-day
window, including the first three days. If a window ends at zero-based index
end, its snowfall is cumulative[end] minus cumulative[end - 3]. For the first
window, subtract 0 instead because no snow fell before day 1.

Compare 2 * window_total > total. This is a strict comparison. The standard
library's Fraction type reads each numeric token exactly, including decimal
tokens, so rounding cannot make an exactly-half window qualify.
Return YES as soon as a qualifying window is found. If all windows fail, or
there are fewer than three days, return NO.

Why it is correct
-----------------
Subtracting the cumulative total before a window removes precisely the snow
from all earlier days, leaving exactly the snowfall on its three days. The
loop considers every possible ending index from 2 through n - 1, so every
three-day window is checked once. A YES is returned only for a window that
satisfies the strict inequality. If none satisfies it, NO is correct. When
n < 3 there is no three-day window, so NO is also correct.

Code organization
-----------------
has_heavy_three_days(cumulative): checks the windows and returns a Boolean.
read_input(text): reads n and returns the n cumulative values as exact
Fraction objects. A leading UTF-8 byte-order mark is ignored.
main(): reads the optional command-line file or standard input, calls the
functions above, and prints the original cumulative numeric tokens followed
by the answer. For example, the numeric spelling 1.50 stays 1.50 in output.
The usual __main__ guard runs main() when the file is executed directly.

Complexity
----------
The window scan performs O(n) arithmetic operations in the worst case and
uses O(1) auxiliary numeric values beyond the input list. Reading and
storing the input takes O(n) numeric entries, so the complete program uses
O(n) time and O(n) space under the usual fixed-size-number assumption.
Fraction uses arbitrary-precision integers: for unbounded-length numeric
tokens, actual arithmetic time and storage also depend on their bit lengths.

Files
-----
snowfall.py: Python 3 program using only the standard library.
inputs/snowfall_input1.txt through inputs/snowfall_input5.txt: unchanged
copies of the supplied input files. The first four are listed in the
assignment; the fifth was also included in the supplied input folder.

How to run
----------
Open a terminal in the Problem1_Snowfall directory. Python 3 must be installed
and available as python. No extra packages are required. Run each command:

python snowfall.py inputs/snowfall_input1.txt
python snowfall.py inputs/snowfall_input2.txt
python snowfall.py inputs/snowfall_input3.txt
python snowfall.py inputs/snowfall_input4.txt
python snowfall.py inputs/snowfall_input5.txt

On Windows, py may be substituted for python. On systems using python3,
substitute python3 for python.

The refreshed saved runs use the locally installed Python 3.14.7. This exact
PowerShell command selects that interpreter on this computer:

& 'C:\Users\Aaron\AppData\Local\Python\pythoncore-3.14-64\python.exe' -B snowfall.py inputs/snowfall_input1.txt

Replace the input filename with inputs 2, 3, 4, and 5 to repeat those runs.
On another computer, use the portable python commands above or substitute
the path to its installed Python interpreter. The optional -B flag prevents
bytecode cache files and does not affect the answer.

Standard input is also supported. In Windows Command Prompt or a POSIX shell:

python snowfall.py < inputs/snowfall_input1.txt

In PowerShell:

Get-Content inputs/snowfall_input1.txt | python snowfall.py

Expected output, in the same order as the five filename commands:

1 4 10 14 15 17 17 23 solution: YES
44 127 166 231 238 320 363 429 500 511 577 642 689 764 812 886 solution: NO
3 8 14 19 21 24 25 25 32 solution: NO
1 2 3 4 5 solution: YES
1 2 3 solution: YES
