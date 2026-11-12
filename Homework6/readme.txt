CS526 Homework Assignment 6
Boston University Metropolitan College

OVERVIEW

This folder contains implementations of all three problems: merging sorted
register logs, a linked binary min-heap, and running medians. The programs
require Python 3.9 or later and use only the Python standard library. No
third-party packages or installation steps are required.

The supplied examples and automated tests were verified with Python 3.12.14.
Screenshots show the source code, saved execution records, and actual
Python program executions in the VS Code integrated terminal.

FILES

mergeLogs.py             Problem 1: merge_logs(logs) and its command-line program
linkedHeap.py            Problem 2: Node, BinaryMinHeap, and insertion display
runningMedian.py         Problem 3: RunningMedian and running_medians(values)
input_utils.py           Safe integer-list parsing and optional file input
readme.txt               Usage, algorithms, correctness, and complexity
inputs/                  All 29 supplied input files, unchanged
tests/test_homework6.py  Automated correctness and standard-input tests
tests/run_examples.py    Reproduce examples and save their console records
tests/expected/          All 29 supplied expected-output files, unchanged
references/              The three supplied problem*_answers.txt summaries
results/                 Actual example output, checks, exit codes, and timings
screenshot/              Source, saved records, and actual VS Code terminal runs

HOW TO RUN

Extract the entire archive before running. In VS Code, open the Homework6
folder containing the .py programs and this readme.txt. Open a terminal in
that same folder. Keep linkedHeap.py beside the other two programs because
both import the heap implementation from it.

Check the interpreter:
    python --version

The required interface reads standard input. In Windows PowerShell:
    Get-Content inputs/merge_input1.txt | python mergeLogs.py
    Get-Content inputs/heap_input1.txt | python linkedHeap.py
    Get-Content inputs/median_input1.txt | python runningMedian.py

On a shell that supports input redirection, such as cmd, bash, or zsh:
    python mergeLogs.py < inputs/merge_input1.txt
    python linkedHeap.py < inputs/heap_input1.txt
    python runningMedian.py < inputs/median_input1.txt

Each program also accepts an optional input-file argument for convenience:
    python mergeLogs.py inputs/merge_input1.txt
    python linkedHeap.py inputs/heap_input1.txt
    python runningMedian.py inputs/median_input1.txt

No prompts are printed before the requested results. The first program
reads register lines until end of input. There is no leading k line; k is
the number of register lines. This end-of-input convention is an interface
choice because the assignment does not prescribe a separate terminator.
An empty register is written []; a blank register line is invalid. A stream
with no register lines represents zero registers. The other two programs
read a single bracketed integer list, including [] for an empty list.

List parsing uses ast.literal_eval, not eval. Integers, repeated values,
and negative integers are supported. Booleans, non-integer entries, and
non-list input are rejected. Problem 1 also rejects a register log that is
not in nondecreasing order. Optional files are read as UTF-8 and may have
a UTF-8 byte-order mark. Invalid input is reported on standard error with
a nonzero exit status.

On Windows, substitute py for python if needed. On macOS/Linux, substitute
python3. Quote any file path that contains spaces.

Run all automated tests:
    python -m unittest discover -s tests -v

Reproduce all supplied examples and the test suite, saving results/ records:
    python tests/run_examples.py all

Run all 29 supplied examples without running the automated test suite:
    python tests/run_examples.py resources

Run one complete group of supplied examples:
    python tests/run_examples.py merge
    python tests/run_examples.py heap
    python tests/run_examples.py median

Show the first supplied example with its full output:
    python tests/run_examples.py merge_demo
    python tests/run_examples.py heap_demo
    python tests/run_examples.py median_demo

Run and save only the automated tests:
    python tests/run_examples.py tests

The example runner supplies input through a pipe, exercising the required
standard-input interface. Its command labels, timing lines, and PASS/FAIL
summaries are added by the runner; they do not change the programs' output.

PROBLEM 1  MERGE SORTED REGISTER LOGS  30 POINTS

Input and output

Each input line contains one register's already sorted list. Register IDs
are one-based and follow input order, including registers whose logs are
empty. The result contains every sale as a (time, register) pair. Earlier
times come first; equal times are ordered by the smaller register ID.

For the supplied first example, the program prints:
    Registers: 4
    Total sales: 8
    Merged log: [(1, 2), (3, 1), (5, 4), (9, 1), (9, 2), (14, 1), (20, 2), (25, 2)]

The count labels match the supplied expected-output resources. The
merge_logs(logs) function itself returns only the list of pairs.

Algorithm and queue invariant

The priority queue is an instance of the linked BinaryMinHeap implemented
for Problem 2. An entry is (time, register, index), where index identifies
the sale's position in that register's input list. Python's comparisons of
these tuples apply the requested time and register priorities; no sorting
function is used.

Initially, insert the first sale from each nonempty register. Repeatedly
extract the smallest entry, append its (time, register) pair to the result,
and insert the next sale from that same register if one remains. Extraction
happens before replacement, so a register never has two entries in the
queue. At every step, the queue contains exactly the earliest unprocessed
sale from each register that still has sales. It therefore has at most k
entries, including when some or all logs are empty.

Why it is correct

Every remaining sale in a register is at least as late as that register's
queued sale. Thus the smallest queued entry is the smallest remaining
sale under the required (time, register) order. Appending that entry keeps
the result ordered. Replacing it with its register's next sale restores
the queue invariant. Each input position is inserted and extracted exactly
once, so every sale appears once, including repeated times within the same
register. Empty logs contribute no entries but retain their register IDs.

Complexity

Let k be the number of registers and N the total number of sales. Input
validation and initialization scan the registers and values. Each sale
requires a constant number of heap operations on at most k entries. Total
time is O(k + N log(k + 1)); the queue occupies O(k) space. The returned
merged list uses O(N) space, and the input logs already occupy O(N + k).
These are properties of this implementation, rather than additional time
limits imposed by the assignment.

PROBLEM 2  LINKED BINARY MIN-HEAP  40 POINTS

Representation and invariants

Node stores value, left, right, and parent. BinaryMinHeap stores only root
and size. The heap's persistent representation is the linked node tree;
there is no list or array holding its heap positions or node references.

Two properties hold after every operation:
    Heap order: a node's value is at most either child's value.
    Complete shape: all levels are full except possibly the last, which
    is filled from left to right.

Logical positions are numbered from 1 in level order. _node_at(position)
follows the binary digits after the leading 1: 0 goes left and 1 goes
right. Position 6, binary 110, is reached by going right and then left.
This locates a position in O(log n) time without storing an index array.

Required methods

insert(value)
    Attach a new node at position size + 1 using its parent's bit path.
    Swap its value upward only while it is strictly smaller than its
    parent's value. Equality does not move a newly inserted value upward.
    Time: O(log(n + 1)).

peek()
    Return root.value without changing any node or link. Raise IndexError
    when the heap is empty. Time: O(1).

extract_min()
    Save the root's value. Detach the last node, move its value to the
    root if another node remains, then sift downward through the smaller
    child until heap order holds. Return the saved minimum. Raise
    IndexError when empty. Time: O(log(n + 1)).

delete(value)
    Search the linked tree for one matching value. Return False without
    changing the heap if absent. Otherwise detach the last node and, if
    necessary, use its value to replace the found value. Sift up if that
    value is smaller than its parent; otherwise sift down. Return True.
    Only one copy is removed. Searching takes O(n) worst-case time; repair
    takes O(log(n + 1)), so total worst-case time is O(n).

build(values)
    Replace the current heap with a heap containing the supplied values.
    Make a temporary copy of the input values, recursively create linked
    nodes at valid complete-tree positions, and heapify each parent after
    its child subtrees. This is bottom-up heap construction in O(n) time.
    The temporary input copy uses O(n) space and is discarded afterward;
    it is not the heap's storage. No array of heap nodes is created.
    The input collection is not modified. build([]) clears the heap.

heap_sort()
    Clone the linked tree into a separate heap and repeatedly extract its
    minimum into the returned list. The original root, node identities,
    node values, parent/child links, shape, and size remain unchanged.
    Time: O(n log(n + 1)); additional space: O(n) for the clone and result.

is_empty()
    Return whether size is zero. Time: O(1).

__len__()
    Return size, allowing len(heap). Time: O(1).

print_heap()
    Draw the actual linked tree with its root on top and / or \ above
    each child. Equal-width logical cells keep negative and multi-digit
    labels aligned. An empty tree prints (empty heap). The character grid
    is only a drawing buffer and never stores or operates as the heap.
    If L is the maximum label width, drawing time and buffer space are
    O(n(L + 1) log(n + 1)), including the blank cells in the grid.

The stored nodes use O(n) space. Bit-path navigation and sifting are
iterative. Tree search, building, cloning, and drawing use recursive calls
whose depth is O(log(n + 1)) because the tree remains complete. Building
also uses its temporary O(n) input copy, as described above.

Why the operations are correct

Appending at the next position and removing the last position preserve
complete shape. Insertion can violate heap order only along the path from
the new leaf to the root, which sifting upward repairs. After extracting
the root, all existing subtrees are heaps; only the replacement value can
violate order, and sifting it downward repairs that path.

For deletion, replacing a found value with the last value can require
upward or downward repair. Comparing with the parent identifies the
upward case; otherwise only a child relationship can require repair.
Bottom-up building creates heap-ordered subtrees before their parents;
sifting down the parent therefore makes the entire subtree a heap. The
sum of node heights in a complete binary tree is O(n), giving linear
bottom-up construction time.

heap_sort() extracts from its clone only. Every extracted value is the
smallest remaining value, so the returned list is increasing while the
original tree remains untouched.

Command-line demonstration

The program reads one integer list and prints Input values: followed by
that list. It begins with an empty heap, inserts each value in the given
order, and prints After insert(value): and the current tree after every
insertion. It does not use build() for this demonstration because the
assignment requires each intermediate insertion state. Horizontal spacing
may differ from the supplied examples; node positions and branches match.
Input [] prints only the Input values: [] header because no insert occurs.

PROBLEM 3  RUNNING MEDIAN  30 POINTS

Input and output

The program reads one integer list in arrival order and prints the list
of prefix medians. For [5, 15, 2, 4, 8], the result is:
    [5.0, 10.0, 5.0, 4.5, 5.0]
For an empty list, the result is []. Integer-valued medians are displayed
as floating-point values, matching the supplied expected outputs.

Use of the Problem 2 heap

RunningMedian creates two BinaryMinHeap instances from linkedHeap.py. The
lower heap stores negated values, making its minimum the negative of the
largest value in the lower half. The upper heap stores ordinary values,
so its minimum is the smallest value in the upper half. Both heaps retain
the linked-node implementation from Problem 2.

Algorithm and invariants

After every sale, maintain these conditions:
    1. Every value in the lower half is at most every value in the upper
       half, interpreting lower's stored values with their signs restored.
    2. The lower half and upper half have equal sizes, or lower has one
       extra value.

Insert a value into lower if lower is empty or the value is at most its
current maximum; otherwise insert it into upper. If lower then has more
than one extra value, transfer its maximum to upper. If upper is larger,
transfer its minimum to lower. One transfer is sufficient because a single
arrival changes the size difference by only one.

When lower has one extra value, the median is -lower.peek(). When sizes
are equal, it is (-lower.peek() + upper.peek()) / 2.0. The methods peek()
and len() take O(1), so reading the median after an update takes O(1).
RunningMedian.add(value) performs the update and returns this median;
running_medians(values) returns one result for each successive addition.
Calling RunningMedian.median() before any addition raises IndexError;
running_medians([]) makes no such call and correctly returns [].

Why it is correct

The insertion comparison places the new value on a side consistent with
the partition order. Transferring lower's maximum or upper's minimum
preserves that order while restoring the size condition. The two halves
contain all values received so far, with their multiplicities unchanged.
For an odd count, lower's maximum is the middle value. For an even count,
lower's maximum and upper's minimum are the two middle values, so their
average is the required median.

Complexity

Each arrival uses a constant number of heap insertions and extractions,
taking O(log(n + 1)) time after n values have arrived. Reading the current
median takes O(1). Processing N sales takes O(N log(N + 1)) total time.
The linked heaps store O(N) values, and the returned median list uses
O(N) additional space. Sales are never maintained in a sorted list and
are never re-sorted after an arrival.

SUPPLIED RESOURCES AND VERIFICATION

All supplied input and expected-output files are included unchanged.
The 29 input files are:

Problem 1, 8 files:
    merge_input1.txt
    merge_input2.txt
    merge_input3.txt
    merge_input5.txt
    merge_input6.txt
    merge_input7.txt
    merge_input8.txt
    merge_input9.txt

Problem 2, 10 files:
    heap_input1.txt
    heap_input2.txt
    heap_input3.txt
    heap_input4.txt
    heap_input5.txt
    heap_input6.txt
    heap_input7.txt
    heap_input8.txt
    heap_input9.txt
    heap_input10.txt

Problem 3, 11 files:
    median_input1.txt
    median_input2.txt
    median_input3.txt
    median_input4.txt
    median_input5.txt
    median_input6.txt
    median_input7.txt
    median_input8.txt
    median_input9.txt
    median_input10.txt
    median_input11.txt

The original resources do not contain merge_input4.txt or heap_input11.txt,
although their summary files mention those case numbers. No replacement
input or expected-output files have been invented for those missing cases.
Zero-register behavior is additionally covered by an automated test.

All 29 supplied cases passed. Merge and median output is compared with
the supplied expected output while allowing whitespace differences. Heap
output is checked against the supplied insertion drawings while allowing
the spacing differences permitted by the assignment.

The complete unittest suite passed all 59 tests, including the 29 supplied
cases. Additional tests cover heap order, complete shape, parent links,
empty-heap exceptions, equal insertion behavior, deletion in both repair
directions, duplicate removal, bottom-up building, non-mutating heap_sort(),
randomized operations, merge ordering and queue capacity, and median edge
cases. The large supplied cases include 20,737 sales across 50 registers
and a running-median stream of 20,000 sales.

The solution modules do not use heapq, sort(), sorted(), statistics, or
other library sorting, priority-queue, heap, or median implementations.
The tests use standard-library sorting solely as an independent expected-
result oracle. The example runner also sorts input filenames numerically
to present cases in order; this is not part of any assignment algorithm.

SCREENSHOTS AND SAVED RESULTS

The screenshot folder contains ten screenshots, all recaptured directly
from VS Code with the mouse pointer outside the captured window. The first
five views show source code beside real saved execution records:
    01_merge.jpg              First supplied merge example
    02_heap.jpg               First supplied heap insertion example
    03_median.jpg             First supplied running-median example
    04_resources.jpg          Supplied-resource verification summary
    05_tests.jpg              Automated test result

The last five views show actual Python executions in the VS Code
integrated terminal:
    06_terminal_merge.jpg     First supplied merge example
    07_terminal_heap.jpg      First supplied heap insertion example
    08_terminal_median.jpg    First supplied running-median example
    09_terminal_resources.jpg All 29 supplied examples
    10_terminal_tests.jpg     All 59 automated tests

Full terminal transcripts are retained as results/terminal_*.txt.

The example runner saves each supplied run as results/<input_stem>.txt.
Each record includes the program, input filename, actual program output,
exit code, expected-result check, and elapsed time. results/tests.txt
contains the verbose test output and exit code. Rerunning the runner
refreshes these records; timings can vary by machine and interpreter.
