CS526 Homework Assignment 5
Boston University Metropolitan College

OVERVIEW

This folder contains solutions to all three problems. The programs require
Python 3.9 or later and use only the Python standard library. No third-party
packages or installation steps are required.

The supplied example executions and automated tests were verified with
Python 3.14.7.

FILES

binarySearchTree.py       Problem 1: Node and binary search tree ADTs
vowelCombinations.py      Problem 2: count vowel-only Morse decodings
longestSequence.py        Problem 3: longest alternating increasing sequence
inputs/                  All ten supplied input files, unchanged
tests/                   Automated tests and an example execution runner
results/                 Saved commands, real output, exit codes, and timings
screenshot/              Screenshots of actual VS Code integrated terminal runs

HOW TO RUN

Extract the entire archive before running. In VS Code, open the folder
containing the three .py programs and this readme.txt file: Homework5 in
the extracted archive, or CS526_Homework5 for the Desktop copy. Select
Terminal > New Terminal and use that same folder as the working directory.

Check your interpreter:
    python --version

Run Problem 1 with a random size from 5 through 50:
    python binarySearchTree.py

Run the reproducible demonstration used for the saved results:
    python binarySearchTree.py --size 5 --seed 526

Run every supplied Problem 2 input:
    python vowelCombinations.py inputs/vowel_input1.txt
    python vowelCombinations.py inputs/vowel_input2.txt
    python vowelCombinations.py inputs/vowel_input3.txt
    python vowelCombinations.py inputs/vowel_input4.txt

Run every supplied Problem 3 input:
    python longestSequence.py inputs/longest_seq1.txt
    python longestSequence.py inputs/longest_seq2.txt
    python longestSequence.py inputs/longest_seq3.txt
    python longestSequence.py inputs/longest_seq4.txt
    python longestSequence.py inputs/longest_seq5.txt
    python longestSequence.py inputs/longest_seq6.txt

Optionally print a sequence and its original positions for Problem 3:
    python longestSequence.py inputs/longest_seq1.txt --show-sequence

Run all automated tests:
    python -m unittest discover -s tests -v

Run all demonstrations and tests, saving console records in results/:
    python tests/run_examples.py all

The example runner also accepts bst, vowels, longest, longest_small,
longest_large, tests, vowels_1 through vowels_4, and longest_1 through
longest_6. For example:
    python tests/run_examples.py vowels

On Windows, substitute py for python if needed. On macOS/Linux, substitute
python3. Paths containing spaces must be enclosed in quotation marks.
The Python files can also be run directly without the example runner.
Only that runner adds command labels, elapsed times, and exit-code lines;
the Problem 2 and Problem 3 programs retain the requested output format.

PROBLEM 1  BINARY SEARCH TREE  20 POINTS

Data types and operations

Node stores an integer value and references to its left and right children.
BST stores a root reference and a node count. Every value in a node's left
subtree is smaller than the node value; every value in its right subtree
is larger. The tree stores distinct integers.

BST.addNode(value) returns True if a new node is inserted and False if the
value is already present. Starting at the root, it follows the left child
for a smaller value and the right child for a larger value, attaching a new
leaf when the appropriate link is empty.

BST.findNode(value) follows the same comparisons and returns the matching
Node, or None when the search reaches an empty link.

BST.deleteNode(value) returns False if the value is absent. A leaf is
unlinked; a node with one child is replaced by that child. For a node with
two children, the algorithm copies its inorder successor's value, then
removes the successor. The successor is the smallest value in the right
subtree and has at most one child. The root is handled explicitly.

BST.printTree() prints a preorder drawing. Indentation indicates depth;
ROOT, L, and R identify the root and left/right child links. This makes
single-child branches unambiguous. An empty tree prints (empty tree).

Why it is correct

Search and insertion discard only subtrees whose ordering excludes the
requested value. Insertion therefore places a new value at a link that
preserves the invariant. Removing a node with at most one child preserves
all remaining order relationships. In the two-child case, the successor
is larger than all values in the left subtree and no larger than any
remaining value in the right subtree, so replacing and unlinking it also
preserves the invariant. Thus every operation maintains a valid BST.

Demonstration

The program randomly selects 5 through 50 distinct numbers from 1 through
1000 and inserts them in the displayed order. It prints the input and the
initial tree, performs two random new insertions and two deletions of
randomly selected original values, and prints the tree after each change.

It then generates random queries from 1 through 1000 with rejection
sampling until it obtains one present value and one absent value. This
guarantees both required search outcomes. --size controls the input size;
--seed makes the random choices repeatable for a saved demonstration.
The seed-526 demonstration finds 394 and does not find 417.

Complexity

With height h, add, delete, and find take O(h) time and O(1) auxiliary
space. The tree is not balanced, so h can be n and the worst-case time is
O(n). Stored nodes use O(n) space. Printing visits every node; its time
and saved drawing space also include the characters used for indentation,
which can total O(nh). The iterative operations avoid recursion limits.

PROBLEM 2  VOWEL MORSE COMBINATIONS  30 POINTS

Input and output

Each supplied input has two lines: the declared number of symbols, followed
by the dot/dash sequence. The reader checks the count and symbols, accepts
a UTF-8 BOM or CRLF endings, and rejects nonblank extra input lines.

The allowed Morse codes are A = .-, E = ., I = .., O = ---, U = ..-.
Letter boundaries are not supplied. Different vowel sequences count as
different combinations; the entire input must be consumed.

Output example:
    File Input: vowel_input1.txt
    The Number of Vowel combinations is:
        6

Algorithm and correctness

Let ways[i] be the number of vowel sequences encoding the first i symbols.
Set ways[0] = 1, representing the one empty decomposition. For each ending
position i and each vowel code c, if c matches the suffix ending at i, add
ways[i - len(c)] to ways[i]. The answer is ways[n].

Every valid decoding has exactly one final vowel. Removing it leaves one
valid decoding of the preceding prefix. Conversely, appending a matching
final vowel to any counted prefix gives a valid complete prefix decoding.
The cases are disjoint by final vowel, so the recurrence counts every
decoding exactly once. An impossible input has count zero. By convention,
the empty input has one decomposition, the empty vowel sequence.

There are five codes, each of length at most three. The algorithm therefore
uses O(n) arithmetic operations and O(n) integer storage. Python integers
grow as necessary and do not overflow at 32 or 64 bits. For very long
inputs, the bit cost of adding large counts also contributes to runtime.

Supplied expected results, all reproduced:
    vowel_input1.txt          6
    vowel_input2.txt          8
    vowel_input3.txt          0
    vowel_input4.txt          193050000

PROBLEM 3  ALTERNATING INCREASING SEQUENCE  50 POINTS

Interpretation and input

The selected values must strictly increase, their source must alternate
between A and B, and their original array positions must strictly increase
even across a source change. Either source may supply the first value.
Equal values and equal-position transitions are not allowed.

This follows the assignment's explicit example: for A = {1,7,2} and
B = {4,8,3,9}, B[1]=4 -> A[2]=7 -> B[4]=9 is valid. A[1]=1 -> B[1]=4
is invalid because the original position does not increase. Indices in
this explanation and the optional witness are one-based.

Each input file has exactly four lines:
    size of A
    size of B
    A values separated by spaces
    B values separated by spaces

The reader validates nonnegative sizes, integer tokens, and the number of
values. Empty arrays use blank value lines. Unequal array lengths and
negative or repeated values are supported.

The required output reports the length, matching all assignment examples:
    File Input: longest_seq1.txt
    Longest Sequence: 4

The optional --show-sequence flag additionally prints actual selected
values and source/position witnesses. It does not change the optimal length.

Dynamic programming recurrence

Let D_A[i] be the length of the longest valid sequence ending at A[i], and
define D_B[i] similarly. Then:

    D_A[i] = 1 + max({D_B[j] : j < i and B[j] < A[i]} union {0})
    D_B[i] = 1 + max({D_A[j] : j < i and A[j] < B[i]} union {0})

The answer is the maximum endpoint length, or zero when both arrays are
empty. A direct scan of all preceding endpoints would be quadratic.

Efficient implementation

Sort the distinct input values and replace them with order-preserving
integer ranks. Maintain two Fenwick trees of prefix maxima, one for each
source. Each stored maximum contains a length and an endpoint identifier.

Scan original positions in increasing order. For A[i], query the B tree
through rank(A[i])-1, and vice versa for B[i]. This returns the best earlier
endpoint with a strictly smaller value. Compute both candidates at a
position before updating either tree, so neither candidate can use the
other value from that same position. Store a predecessor identifier for
each endpoint, then follow these identifiers backward to reconstruct an
optimal sequence.

Why it is correct

Before processing position i, the trees summarize exactly the endpoints
at positions smaller than i. Querying the opposite source enforces
alternation, and querying ranks below the current rank enforces strict
value growth. These are precisely the legal predecessors in the
recurrence. By induction, the returned prefix maxima and the two new
endpoint lengths are optimal. Delaying both updates preserves the index
invariant. The largest endpoint length is globally optimal, and each
saved predecessor link belongs to an admissible optimal transition.

With N = len(A) + len(B), sorting and Fenwick operations take O(N log N)
time, and ranks, trees, and backpointers take O(N) space. This handles the
largest supplied file, which contains 10,000 values in each array.

Supplied expected results, all reproduced:
    longest_seq1.txt          4
    longest_seq2.txt          7
    longest_seq3.txt          10
    longest_seq4.txt          39
    longest_seq5.txt          192
    longest_seq6.txt          1

VALIDATION AND EXECUTION EVIDENCE

The 37 automated test methods cover the following:

* BST deletion shapes, empty trees, duplicates, missing values, a 1,200-node
  degenerate tree, and 800 random operations compared with a Python set.
* All 127 dot/dash strings of length at most six, checked against independent
  enumeration of vowel words; invalid files; exact CLI output; large counts.
* 1,600 exhaustive small array pairs and 750 seeded random pairs, checked
  against an independent quadratic endpoint algorithm. Reconstructed
  witnesses are checked for strict values, alternating sources, increasing
  original positions, and agreement with the inputs.
* All ten supplied input files, CLI validation, empty arrays, unequal
  lengths, repeated values, and 10,000-position inputs.

tests/input_sha256.json records hashes of all supplied inputs for integrity
checking. results/ contains the actual example execution records. Timings
are observations from those runs and can vary between machines.

The screenshots show complete program runs in VS Code's integrated
terminal. The two BST views show the complete random demonstration and its
search results. The vowel and sequence views cover all ten supplied inputs. The
test view shows the completed automated suite.
