# CS526 Homework Assignment 4

Boston University Metropolitan College

## Introduction

This homework covers tree traversals, selecting the fewest array elements whose
sum is strictly greater than a target, and counting unique right triangles
among points in the plane. All programs use the Python standard library and
run with Python 3.9 or later. No package installation is required.

The screenshots label both tree questions "Problem 1." Both are answered below;
the array question is Problem 2 and the right-triangle question is Problem 3.

| File or folder | Purpose |
| --- | --- |
| `treeTraversals.py` | Optional executable verification of the Problem 1 answers |
| `smallestNumber.py` | Problem 2, with the filename shown in the assignment |
| `rightTriangles.py` | Problem 3, with the filename shown in the assignment |
| `Fewest_Resourses/` | All four original array resource files, unchanged |
| `Angles_Resourses/` | All four original geometry resource files, unchanged |
| `tests/test_homework4.py` | 28 automated tests, including 500 deterministic random cases |
| `tests/data/` | Example inputs, invalid inputs, and the large-case triangle certificate |
| `tests/run_examples.py` | Runs each demonstration with its actual command, output, and elapsed time |
| `screenshot/` | 13 VS Code integrated terminal screenshots of actual executions |

### Problem 1 answers

Children are visited from left to right in the general tree:
`A: B,C,D; B: E,F; D: G; E: H; F: I`.

| Traversal | Sequence |
| --- | --- |
| Preorder | **A B E H F I C D G** |
| Breadth-first | **A B C D E F G H I** |
| Postorder | **H E I F B C G D A** |

For the binary tree, `A: left B, right C; B: left D, right E;
D: right G; C: right F; F: left H, right I`.

| Traversal | Sequence |
| --- | --- |
| Inorder | **D G B E A C H F I** |

## Algorithm

### Problem 1: tree traversals

Preorder visits a node before its children. Postorder visits the children
before their parent. Breadth-first uses a queue to process nodes one level at a
time. Binary inorder visits the left subtree, the node, then the right subtree.
Each traversal visits every node once. The executable returns lists for easy
verification. List concatenation in the small recursive demonstrations can
copy intermediate lists; these helpers are intended for the two given trees.

### Problem 2: fewest elements

Sort a copy of the array in descending order. Add the values from largest to
smallest, stopping at the first prefix whose sum is **strictly greater** than
the target. Print the original array, the target, and the number selected.
Selections do not have to be contiguous.

**Correctness.** For any fixed size k, the k largest values have at least as
large a sum as any other k-element selection: replacing any chosen smaller
value by an unchosen larger value cannot reduce the sum. Thus, if the sorted
k-element prefix does not exceed the target, no k-element selection can do so.
The first prefix that does exceed it therefore has the minimum possible size.
This also works with repeated, zero, and negative values.

Sorting costs O(n log n) time, and the scan costs O(n). The sorted copy uses
O(n) additional space and preserves the original array for printing.

### Problem 3: right triangles

Treat each point P as a possible right-angle vertex. For every other point Q,
compute `(dx, dy) = Q - P`. Divide by `gcd(dx, dy)` and normalize the sign so
`dx > 0`, or `dx == 0` and `dy > 0`. This is an unoriented slope key, so points
on either side of P along the same line share a key.

Maintain a dictionary of how many earlier vectors have each slope. The
perpendicular to `(dx, dy)` has slope `(-dy, dx)`, normalized in the same way.
Add the frequency of that perpendicular slope to the total, then insert the
current slope. Rebuild the dictionary for each pivot.

**Correctness.** Two nonzero vectors form a right angle exactly when their
directions are perpendicular. The dictionary counts every possible endpoint
on the perpendicular line, including multiple points and opposite rays. At
each pivot, every unordered endpoint pair is counted when its second member
is processed. A nondegenerate right triangle has exactly one right-angle
vertex, so it is counted exactly once over all pivots. No final division is
needed. Collinear points contribute no triangles.

There are n(n-1) vector visits. For integer coordinates of magnitude at most C,
the algorithm takes O(n² log C) time when the gcd cost is included, and O(n)
auxiliary space. Under the usual fixed-size-coordinate model this is O(n²).
The 1,000-point supplied input finishes well below the assignment's 30-second
limit on the machine used for the saved executions.

## Interesting aspects

- Comparisons in Problem 2 use `>` rather than `>=`. A selection whose sum
  exactly equals the target needs another element.
- Array selections are nonempty. The assignment guarantees a feasible input;
  outside that guarantee the program prints `No solution` if none exists.
- Integer coordinates use exact arithmetic, avoiding vertical-slope division
  and floating-point equality. The input reader also supports finite decimal
  coordinates by converting all coordinates using one uniform integer scale,
  which preserves angles. Decimal array values are read as exact fractions.
- Declared counts are checked. Duplicate points are rejected because the
  assignment specifies different points; zero, one, and two distinct points
  correctly yield zero triangles.
- Inputs are read from the filename argument shown in the assignment, rather
  than from standard input. Resource names retain the supplied spelling.

### Supplied answer discrepancy for `rightangles_3.txt`

The original `Angles_Resourses/answers_angles.txt` states **5294** for its third
case. Exact counting gives **5295**. The original answer file is preserved.
The first two geometry results and all three array results match their
supplied answers.

`tests/data/rightangles3_certificate.txt` contains **5295 distinct triples** of
1-based point indices. Index 1 means the first coordinate pair after the point
count. Each triple is sorted, and no triple occurs twice. The automated test
checks that each triple is in range and independently verifies a right triangle
using exact squared side lengths and the Pythagorean theorem. Thus, these
5295 valid triples alone prove that 5294 is too small. An independent full
integer dot-product enumeration during preparation also returned 5295.

The program returns the mathematical count, 5295. The test for this case
explicitly records the supplied-file discrepancy and checks the certificate;
it does not claim to match the supplied value. The reason for the answer
file's discrepancy is unknown.

## How to run

Open this folder in VS Code and open its terminal. Use `python3` on Linux/macOS,
or `python` (or `py`) on Windows. Run commands from the homework folder.

```sh
python treeTraversals.py

python smallestNumber.py tests/data/smallest_input.txt
python smallestNumber.py Fewest_Resourses/fewest_1.txt
python smallestNumber.py Fewest_Resourses/fewest_2.txt
python smallestNumber.py Fewest_Resourses/fewest_3.txt

python rightTriangles.py Angles_Resourses/rightangles_1.txt
python rightTriangles.py Angles_Resourses/rightangles_2.txt
python rightTriangles.py Angles_Resourses/rightangles_3.txt

python -B -m unittest discover -s tests -v
```

Problem 2 input: an element count, a target, then exactly that many values.
Problem 3 input: a point count followed by that many coordinate pairs. Whitespace
separates values; both input readers tolerate a UTF-8 byte-order mark.

The automated suite compares the greedy algorithm with exhaustive subset
search on 250 small random arrays, and compares the geometry algorithm with
exhaustive triple/Pythagorean checks on 250 small random point sets. It also
checks the supplied inputs, traversal answers, strict inequality, nonadjacent
selection, a rotated triangle, squares, opposite rays, repeated slopes, huge
coordinates, decimal input, malformed input, and the command-line output.

### Example executions

Screenshots show actual program executions in the VS Code integrated terminal.
Each includes the command, real output, exit status, and elapsed time. For the
10,000-element array, the terminal view shows the tail of the full array output;
the program prints every element. Use the same command to inspect the full
output in the terminal scrollback.

| Demonstration | Screenshot |
| --- | --- |
| All tree traversals | [trees.jpg](screenshot/trees.jpg) |
| Assignment array example | [fewest_sample.jpg](screenshot/fewest_sample.jpg) |
| Array resource 1 | [fewest_1.jpg](screenshot/fewest_1.jpg) |
| Array resource 2 | [fewest_2.jpg](screenshot/fewest_2.jpg) |
| Array resource 3: 10,000 elements | [fewest_3.jpg](screenshot/fewest_3.jpg) |
| Geometry resource 1 | [angles_1.jpg](screenshot/angles_1.jpg) |
| Geometry resource 2 | [angles_2.jpg](screenshot/angles_2.jpg) |
| Geometry resource 3: 1,000 points | [angles_3.jpg](screenshot/angles_3.jpg) |
| Strictly greater boundary | [strict_greater.jpg](screenshot/strict_greater.jpg) |
| Rotated right triangle | [rotated_triangle.jpg](screenshot/rotated_triangle.jpg) |
| Square: no double counting | [square.jpg](screenshot/square.jpg) |
| Opposite rays | [opposite_rays.jpg](screenshot/opposite_rays.jpg) |
| Automated tests | [tests_unittest.jpg](screenshot/tests_unittest.jpg) |

To reproduce a timed demonstration, run, for example:

```sh
python tests/run_examples.py angles_3
python tests/run_examples.py tests_unittest
```

For the same repository layout used in earlier homework, place the complete
submission in a `Homework4/` folder in your Git repository. Include its source,
README, tests, both resource folders, and screenshots. The local preparation
does not publish the repository or submit anything to the course website.

