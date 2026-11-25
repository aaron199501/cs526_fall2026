CS526 Homework Assignment 7

Requirements and execution
--------------------------
Use Python 3.10 or newer. No third-party packages are required.
Run the commands below from the Homework7 directory. On a system where the
Python 3 command is python3, replace python with python3.
The submission uses a Homework7 directory on the main branch.

The five programs read the input filename from the command line and never
prompt for input. The solution algorithms do not use sort(), sorted(),
heapq, or a library sorting or priority-queue implementation.

Files and directories:
  merge_sort.py, quick_sort.py, insertion_sort.py: Problem 1 programs.
  radix_sort.py: Problem 2 program.
  stable_matching.py: Problem 3 program.
  input_utils.py: Shared integer-file reader and complete output formatting.
  inputs/: Six custom sorting files and four supplied matching files.
  references/: Supplied answer files, retained without modification.
  results/: Saved complete program output and execution records.
  screenshots/: Screenshots of the 16 required program/input combinations.
  tests/: Independent automated correctness and input-validation checks.

All custom integer files contain exactly one integer per line. Every sorting
run prints the original values in file order, followed by all sorted values.
The output wraps after 20 integers for readability; no values are omitted.
For long output, a screenshot can show the beginning and end while the
complete output is retained in results/.

To run the automated checks:
  python -m unittest discover -s tests -v

The tests may use Python's sorted() as an independent expected-result
oracle. The five solution programs and their shared input helper do not.

To repeat all 16 required executions and save their complete outputs:
  python tests/run_examples.py all --preview
The runner launches the same Python interpreter for each command. Its
terminal preview may show only the start and end; results/*.txt retains
the complete program output. Exit code 1 is expected only for badInput.txt.


Problem 1 - Merge Sort, Quick Sort and Insertion Sort (25 points)
----------------------------------------------------------------
The custom input files are:
  inputs/small.txt     15 integers
  inputs/medium.txt    50 integers
  inputs/large.txt    500 integers

These files include negative numbers, zero, and repeated values. Each of the
three programs is run on all three files, giving nine required executions.

Exact commands:
  python merge_sort.py inputs/small.txt
  python merge_sort.py inputs/medium.txt
  python merge_sort.py inputs/large.txt
  python quick_sort.py inputs/small.txt
  python quick_sort.py inputs/medium.txt
  python quick_sort.py inputs/large.txt
  python insertion_sort.py inputs/small.txt
  python insertion_sort.py inputs/medium.txt
  python insertion_sort.py inputs/large.txt

Merge Sort:
The list is divided into two halves until each sublist has at most one
element. The recursively sorted halves are merged by comparing their next
unused values and copying the smaller one. Any values left in either half
are then copied. Taking the left value on ties preserves stability. The
function returns a new list and does not change its argument.

Quick Sort:
The pivot is the value at the middle index of the current subarray. A
three-way partition divides it into values less than, equal to, and greater
than the pivot. Only the less-than and greater-than regions need further
sorting. An explicit stack replaces recursion. The smaller region is
processed immediately and the larger region is saved on the stack. This
avoids Python's recursion-depth limit and handles repeated values directly.
The function partitions a copy, leaving the original input unchanged.

Insertion Sort:
Before each iteration, the prefix before the current element is sorted.
The current value is saved, larger prefix elements are shifted right, and
the saved value is inserted into the resulting gap. Elements with equal
values are not moved past each other. The algorithm works on a copy.

Screenshots:
  01_merge_small.jpg       02_merge_medium.jpg       03_merge_large.jpg
  04_quick_small.jpg       05_quick_medium.jpg       06_quick_large.jpg
  07_insertion_small.jpg   08_insertion_medium.jpg   09_insertion_large.jpg


Problem 2 - LSD Radix Sort (25 points)
--------------------------------------
The custom input files are:
  inputs/radix_small.txt     15 non-negative integers
  inputs/radix_medium.txt    50 non-negative integers
  inputs/radix_large.txt    500 non-negative integers

The files include zero, repeated values, and values with different numbers
of digits. Negative input is rejected with an error message.

Exact commands:
  python radix_sort.py inputs/radix_small.txt
  python radix_sort.py inputs/radix_medium.txt
  python radix_sort.py inputs/radix_large.txt

The radix is 10. Starting with the units digit, the algorithm sorts one
decimal position at a time, then advances to tens, hundreds, and so on.
It stops after processing the most significant digit of the largest value.
Shorter values implicitly have zero in their missing leading positions.
Empty input and lists containing only zero are already sorted.

Each digit pass uses a hand-written stable Counting Sort. First it counts
the occurrences of digits 0 through 9, then accumulates those counts to
find bucket boundaries. It scans the current list from right to left and
places each value at the last free position in its digit's bucket.

Stability is essential: values with the same current digit must retain the
order established by the lower-digit passes. Therefore, after each pass,
the list is sorted by all digits processed so far. After the final pass,
the entire list is in increasing numeric order.

Screenshots:
  10_radix_small.jpg   11_radix_medium.jpg   12_radix_large.jpg


Problem 3 - Men-Proposing Gale-Shapley Stable Matching (50 points)
------------------------------------------------------------------
Input format and validation:
The first non-blank line is a positive integer n. The next n non-blank
person lines describe the men; the next n describe the women. Each line
contains the person's single-word name followed by all n opposite-group
names in preference order, most preferred first. Names are case sensitive.
Blank lines are ignored.

By default, the program enforces the assignment's globally unique names.
It also checks that there are exactly 2n person lines, that each list has
exactly n entries, and that those entries name every opposite-group person
exactly once. Invalid input produces an explanatory error and exit code 1,
without a Python traceback. Missing or unreadable files are also reported.

Important discrepancy in the supplied files:
The assignment says every person's name is different across the entire
file. However, marriage_hundred.txt uses Leslie in both groups, and
marraige_thousand.txt has 80 names shared across the two groups. These
supplied input files are retained unchanged. The default strict mode
rejects them because they violate the written uniqueness requirement.

To execute those two supplied cases, the explicit --allow-shared-names
option treats a person's identity as their group and name. It permits
cross-group shared names only; it still rejects duplicate person names
within either group and still validates every complete preference list.
This option is a compatibility exception to the document's global-name
rule, rather than a change to the default validation or to the input files.

Exact commands for all four supplied files:
  python stable_matching.py inputs/marraige_ten.txt
  python stable_matching.py inputs/marriage_hundred.txt --allow-shared-names
  python stable_matching.py inputs/marraige_thousand.txt --allow-shared-names
  python stable_matching.py inputs/badInput.txt

The last command is expected to fail with exit code 1: badInput.txt declares
n = 10 but contains 23 person lines instead of the required 20.
The differing spellings marraige and marriage above match the supplied files.

The program first prints the full input, then the heading Matching:, then
one <man> <woman> pair per line. Couples are listed in the same order that
the women appear in the input, not in men's order or alphabetical order.
The large cases still produce every input line and every couple.

For the 100- and 1000-person cases, output may be redirected to files:
  python stable_matching.py inputs/marriage_hundred.txt --allow-shared-names > results/matching_hundred.txt
  python stable_matching.py inputs/marraige_thousand.txt --allow-shared-names > results/matching_thousand.txt

Data structures:
1. male_preferences[m] is a list of women's integer indexes in man m's
   preference order. next_proposal[m] records the next list position to
   consider, so he never proposes to the same woman twice.
2. female_rankings[w][m] is woman w's rank for man m, where a smaller rank
   means greater preference. This inverse table makes comparisons constant
   time without searching her preference list during each proposal.
3. woman_partner[w] stores the index of woman w's current partner, or -1
   if she is unmatched. The final pairs are built from this array.
4. free_men is a deque of unmatched men's indexes. A rejected man or a man
   displaced by a preferred proposer is returned to the deque.

Algorithm and termination:
Initially, all men are in free_men and all women are unmatched. A free man
proposes to his next woman. She accepts if unmatched, replaces her current
partner if she prefers him, or rejects him otherwise. Each proposal moves
the man's next_proposal index forward. There are at most n squared distinct
proposals. With equally sized groups and complete lists, a free man cannot
exhaust all women: if all had rejected him, every woman would be holding
another man, leaving no man free. Thus the algorithm ends with n couples.

Why the result is stable:
Suppose man M prefers woman W to his final partner. He must have proposed
to W earlier and been rejected, either immediately or after a later
replacement. At that rejection W preferred her held partner to M. Her
partner can only improve afterward, so her final partner is preferred to
M. Therefore M and W cannot be a blocking pair, and the matching is stable.

Why the result is men-optimal:
Consider the first rejection of a pair that occurs in some stable matching.
At that moment W holds a man M' whom she prefers to rejected man M. If M'
preferred his partner in that stable matching to W, she would already have
rejected him, contradicting the choice of the first such rejection. Thus
M' prefers W to that partner, and W prefers M' to M, creating a blocking
pair in the supposed stable matching. No rejected pair can therefore occur
in a stable matching. Each man's final partner is his highest-ranked woman
who has not rejected him, so he receives his best possible stable partner.

Screenshots:
  13_matching_ten.jpg        14_matching_hundred.jpg
  15_matching_thousand.jpg   16_matching_invalid.jpg
