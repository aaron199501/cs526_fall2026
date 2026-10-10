# CS526 Homework 2

Boston University Metropolitan College  
CS526 Data Structures and Algorithms  
Homework Assignment 2

## Introduction

This homework focuses on linked lists and recursion in Python.

The assignment contains four problems:

- **Problem 1:** Explain the advantage of using a tail pointer in a linked list.
- **Problem 2:** Implement a singly linked list with CRUD operations and a driver program that reads commands from standard input.
- **Problem 3:** Use recursion to count the number of ways to climb a staircase when each move can be 1, 2, or 3 steps.
- **Problem 4:** Implement a sorted doubly linked list that always keeps its values in ascending order and supports searching, counting, totals, median calculation, and other list operations.

## Problem 1 - Tail Pointer

A tail pointer stores a reference to the last node in a linked list.

The main advantage of using a tail pointer is that appending a new node to the end of the list can be done in **O(1)** time. Without a tail pointer, the program would need to begin at the head and traverse the entire list to locate the last node before appending, which takes **O(n)** time.

Therefore, keeping a tail pointer makes the append operation more efficient.

## Problem 3A - Base Cases

**Question:** What are the base cases of the function, and why? What should `ways(0)` be?

The base cases are:

```text
ways(0) = 1
ways(n) = 0 when n < 0
```

`ways(0)` should be `1` because reaching exactly zero remaining steps means that one valid path has successfully reached the top.

If `n < 0`, the function returns `0` because going below zero steps means that the path is invalid and should not be counted.

## Problem 3B - Fibonacci Sequence

**Question:** If you could only climb 1 or 2 steps at a time, what well-known sequence would `ways(n)` produce?

If only 1 or 2 steps could be climbed at a time, the recurrence would become:

```text
ways(n) = ways(n - 1) + ways(n - 2)
```

This produces the **Fibonacci sequence**, with an index shift depending on the chosen base cases.

## Files

The `Homework2` folder contains the following files:

```text
Homework2/
|-- README.md
|-- problem2.py
|-- problem2_driver.py
|-- problem3.py
|-- problem4.py
|-- problem4_driver.py
|-- problem2Resources/
|   `-- *.txt                 six teacher inputs and two original inputs
|-- problem4Resources/
|   `-- *.txt                 nine teacher inputs
|-- tests/
|   |-- test_homework2.py
|   |-- test_teacher_examples.py
|   |-- teacher_cases.py
|   |-- record_runs.py
|   |-- original_resources/
|   |   |-- problem2_basic.txt
|   |   `-- problem2_errors.txt
|   `-- teacher_resources/
|       |-- problem2Executions.txt
|       |-- problem3Excutions.txt
|       `-- problem4Executions.txt
|-- example_executions/
|   `-- *.txt                 actual commands, output, and verification results
`-- screenshot/
    |-- teacher_*.jpg         19 teacher examples
    `-- *.png                 four additional executions
```

- `problem2.py` contains the `Node` and `SinglyLinkedList` classes.
- `problem2_driver.py` reads commands from standard input and applies them to a `SinglyLinkedList`.
- `problem3.py` contains the recursive `ways(n)` function, the required default demonstration, and optional commands for reproducing the teacher's staircase examples.
- `problem4.py` contains the `Node` and `SortedDoublyLinkedList` classes and a short driver demonstrating the required methods.
- `problem4_driver.py` reads the teacher's Problem 4 directives from standard input and applies them to a `SortedDoublyLinkedList`.
- The 18 original teacher resource files are retained: six Problem 2 inputs, nine Problem 4 inputs, and three execution transcripts. The original spelling `problem3Excutions.txt` is preserved.
- The original local basic and error fixtures are retained in `tests/original_resources/` because their names also occur in the teacher's resources. The original all-operations and empty/single-node inputs remain in `problem2Resources/`.

## Algorithm

### Problem 2 - Singly Linked List

Each node contains:

- `value` - the data stored in the node.
- `next` - a reference to the next node, or `None` if the node is the last node.

The `SinglyLinkedList` keeps:

- `head` - the first node.
- `tail` - the last node.
- `_size` - the current number of nodes.

The required operations work as follows:

- `append(value)` creates a new node and attaches it after the current tail. If the list is empty, both `head` and `tail` are set to the new node.
- `prepend(value)` creates a new node before the current head. If the list is empty, both `head` and `tail` are set to the new node.
- `insert(index, value)` checks that the insertion index is valid. Index `0` uses `prepend()`, inserting at the end uses `append()`, and other positions are reached by traversing to the node immediately before the requested index.
- `get(index)` traverses from the head to the requested position and returns that node's value.
- `find(value)` traverses the list and returns the index of the first matching value, or `-1` if the value is not found.
- `__len__()` returns `_size`.
- `update(index, value)` traverses to the requested position and replaces the value stored there.
- `delete(value)` removes the first node containing the requested value and returns `True`; if the value is not found, it returns `False`.
- `delete_at(index)` removes the node at the requested index and returns its value.
- `print_list()` traverses from head to tail and prints values in the form `12 -> 3 -> 5 -> 2`. An empty list prints `(empty)`.

Methods that take an index raise `IndexError` when the index is outside the valid range. When the only node is removed, both `head` and `tail` are updated to `None`.

### Problem 2 - Driver Program

`problem2_driver.py` reads one directive at a time from standard input.

Supported directives are:

```text
append <value>
prepend <value>
insert <index> <value>
get <index>
find <value>
len
update <index> <value>
delete <value>
delete_at <index>
print_list
```

Blank lines and lines beginning with `#` are ignored. Physical input line numbers still include those lines, so diagnostics agree with the teacher's execution transcripts. Values are parsed as integers, floating-point numbers, or text.

The driver prints a warning and continues when it encounters:

- an unknown directive,
- the wrong number of arguments,
- an index that is not a whole number,
- an index that is out of range, or
- a request to delete a value that is not in the list.

Warnings identify the input line and the reason, such as `line 8: index 10 out of range`. A `len` directive prints `len = N`. After all input lines are processed, the driver prints `Final list: ` followed by the list.

### Problem 3 - Climbing Stairs

The recursive function `ways(n)` counts the number of ways to reach the top when each move can climb 1, 2, or 3 steps.

The recurrence is:

```text
ways(n) = ways(n - 1) + ways(n - 2) + ways(n - 3)
```

The base cases are:

```text
ways(0) = 1
ways(n) = 0 when n < 0
```

Running the program without arguments calls `ways()` for 3, 5, and 10 steps, as required by the assignment. The output is `4`, `13`, and `274`, respectively.

The optional `--steps` command reproduces the teacher's sequence listings. A recursive helper explores a first move of 1, then 2, then 3 steps and prints each completed path in the same order as the supplied transcript. `--count-only` prints only the count. `--teacher-examples` reproduces the complete supplied transcript for 3, 4, 7, and 10 steps. These optional examples leave the required default demonstration available.

The explanations for the base cases and the 1-or-2-step version are provided above in **Problem 3A** and **Problem 3B**.

### Problem 4 - Sorted Doubly Linked List

Each node contains:

- `value` - the data stored in the node.
- `prev` - a reference to the previous node, or `None` for the first node.
- `next` - a reference to the next node, or `None` for the last node.

The `SortedDoublyLinkedList` keeps references to both `head` and `tail`, tracks its size, always stores values in ascending order, and allows duplicate values.

The required operations work as follows:

- `add(value)` finds the correct sorted position and inserts the new node while updating both `prev` and `next` references.
- `delete(value)` removes one node containing the requested value and returns `True`; it returns `False` if the value is not present.
- `exists(value)` recursively searches for a value. Because the list is sorted, the search can stop when the current value becomes greater than the target.
- `print_list()` recursively prints the list from head to tail in the form `2 <-> 4 <-> 8 <-> 10`. An empty list prints `(empty)`.
- `total()` recursively returns the sum of all values. The total of an empty list is `0`.
- `count(value)` recursively counts how many times the requested value appears and can stop early because the list is sorted.
- `sum_middle_three()` returns the sum of the three middle nodes. For an odd-sized list it uses positions `mid - 1`, `mid`, and `mid + 1`; for an even-sized list it uses `mid - 2`, `mid - 1`, and `mid`. It raises `ValueError` when the list has fewer than three nodes.
- `median()` returns the middle value for an odd-sized list and the average of the two middle values for an even-sized list. It raises `ValueError` for an empty list.

A short driver in `problem4.py` builds a list and demonstrates every required method.

### Problem 4 - Input Driver

`problem4_driver.py` accepts `add <value>`, `delete <value>`, `exists <value>`, `count <value>`, `print_list`, `total`, `sum_middle_three`, and `median`. It parses numeric values, ignores comments and blank lines, prints each requested result, and finishes with the final list. Invalid directives, arguments, values, and queries on lists that are too short produce diagnostics with the input line number; processing then continues.

## Interesting aspects

Several design and edge-case decisions are important in this homework.

For Problem 2, keeping both a head and a tail pointer makes appending efficient because the list does not need to be traversed to locate its final node. Special handling is also required when deleting the only node in the list so that both `head` and `tail` become `None`.

Index validation is performed before accessing or modifying nodes. Invalid indexes raise `IndexError`, allowing the driver to catch the error, print a warning, and continue processing the remaining input.

For Problem 4, maintaining sorted order during every insertion makes later operations more efficient. In particular, `exists()` and `count()` can stop searching as soon as the current value becomes greater than the requested value. Because the list is doubly linked, both `prev` and `next` references must be updated carefully when nodes are inserted or deleted.

Recursion is required for Problem 3 and is also used where it naturally fits in Problem 4, including `total()`, `count()`, `exists()`, and `print_list()`.

The staircase recurrence keeps the solution close to the assignment's recursive definition. The number of paths grows rapidly, so the optional count-only mode avoids printing every combination when only the total is needed.

The teacher's inputs and output transcripts are retained separately from actual execution logs. The automated comparison uses the supplied output for all 19 examples, including diagnostic wording, numeric formatting, and the staircase sequence order. The original local tests are also retained and continue to check pointer consistency and boundary cases.

## How to run

Open a terminal in the `Homework2` directory.

### Problem 2

Run the teacher's basic input. Replace the input filename to run any other Problem 2 case listed below.

macOS / Linux:

```bash
python3 -B problem2_driver.py < problem2Resources/problem2_basic.txt
```

Windows PowerShell:

```powershell
Get-Content .\problem2Resources\problem2_basic.txt | py -B .\problem2_driver.py
```

### Problem 3

Run the assignment's required demonstration:

macOS / Linux:

```bash
python3 -B problem3.py
```

Windows PowerShell:

```powershell
py -B .\problem3.py
```

Run each staircase example supplied by the teacher:

macOS / Linux:

```bash
python3 -B problem3.py --steps 3
python3 -B problem3.py --steps 4
python3 -B problem3.py --steps 7
python3 -B problem3.py --steps 10 --count-only
```

Windows PowerShell:

```powershell
py -B .\problem3.py --steps 3
py -B .\problem3.py --steps 4
py -B .\problem3.py --steps 7
py -B .\problem3.py --steps 10 --count-only
```

To reproduce the combined teacher transcript in one execution:

```bash
python3 -B problem3.py --teacher-examples
```

```powershell
py -B .\problem3.py --teacher-examples
```

The complete combined execution is also saved as [command and output](example_executions/problem3_teacher_examples.txt).

### Problem 4

Run the original demonstration of every required method:

macOS / Linux:

```bash
python3 -B problem4.py
```

Windows PowerShell:

```powershell
py -B .\problem4.py
```

Run the teacher's example input through the new input driver. Replace the input filename to run any of the nine Problem 4 cases listed below.

macOS / Linux:

```bash
python3 -B problem4_driver.py < problem4Resources/problem4_example.txt
```

Windows PowerShell:

```powershell
Get-Content .\problem4Resources\problem4_example.txt | py -B .\problem4_driver.py
```

### Run All Examples and Tests

Run the complete expanded unit-test suite:

```bash
python3 -B -m unittest discover -s tests -v
```

```powershell
py -B -m unittest discover -s tests -v
```

Run and verify all 19 teacher examples, the original demonstrations, retained input fixtures, and unit tests:

```bash
python3 -B tests/record_runs.py --verify-only
```

```powershell
py -B .\tests\record_runs.py --verify-only
```

To refresh the saved text executions after running the checks:

```bash
python3 -B tests/record_runs.py --export --verify-only
```

```powershell
py -B .\tests\record_runs.py --export --verify-only
```

## Test Files and Teacher Examples

The six Problem 2 inputs and nine Problem 4 inputs use the filenames and folder names shown in the teacher's commands. The expected results come from the three unmodified execution transcripts in `tests/teacher_resources/`. Problem 3 has no external input file: its four supplied examples are selected with command-line arguments.

`tests/teacher_cases.py` maps each example to its input or arguments and the corresponding supplied expected output. `tests/test_teacher_examples.py` checks the actual executions against those results. Comparison normalizes Windows line endings and permits an optional final newline; the output values, messages, sequence order, and other whitespace are preserved.

### Problem 2 - Six Teacher Inputs

| Input | Teacher's expected output | Actual execution | VS Code screenshot |
|---|---|---|---|
| [Basic](problem2Resources/problem2_basic.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_basic.txt) | [Screenshot](screenshot/teacher_problem2_basic.jpg) |
| [Create](problem2Resources/problem2_create.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_create.txt) | [Screenshot](screenshot/teacher_problem2_create.jpg) |
| [Delete](problem2Resources/problem2_delete.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_delete.txt) | [Screenshot](screenshot/teacher_problem2_delete.jpg) |
| [Errors](problem2Resources/problem2_errors.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_errors.txt) | [Screenshot](screenshot/teacher_problem2_errors.jpg) |
| [Read](problem2Resources/problem2_read.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_read.txt) | [Screenshot](screenshot/teacher_problem2_read.jpg) |
| [Update](problem2Resources/problem2_update.txt) | [problem2Executions.txt](tests/teacher_resources/problem2Executions.txt) | [Command and output](example_executions/teacher_problem2_update.txt) | [Screenshot](screenshot/teacher_problem2_update.jpg) |

The teacher's basic input ends with:

```text
Final list: 12 -> 5 -> 2 -> 7
```

The original local basic fixture is retained as [tests/original_resources/problem2_basic.txt](tests/original_resources/problem2_basic.txt). It reproduces the different example in the assignment PDF, whose final list is `8 -> 12 -> 5 -> 7`.

### Problem 3 - Four Teacher Examples

The original transcript supplies output without invocation commands; the following arguments reproduce each section. They produce 4, 7, 44, and 274 combinations respectively. The 10-step section prints only the total, as in the supplied transcript.

| Arguments for problem3.py | Teacher's expected output | Actual execution | VS Code screenshot |
|---|---|---|---|
| `--steps 3` | [problem3Excutions.txt](tests/teacher_resources/problem3Excutions.txt) | [Command and output](example_executions/teacher_problem3_steps_3.txt) | [Screenshot](screenshot/teacher_problem3_steps_3.jpg) |
| `--steps 4` | [problem3Excutions.txt](tests/teacher_resources/problem3Excutions.txt) | [Command and output](example_executions/teacher_problem3_steps_4.txt) | [Screenshot](screenshot/teacher_problem3_steps_4.jpg) |
| `--steps 7` | [problem3Excutions.txt](tests/teacher_resources/problem3Excutions.txt) | [Command and output](example_executions/teacher_problem3_steps_7.txt) | [Screenshot](screenshot/teacher_problem3_steps_7.jpg) |
| `--steps 10 --count-only` | [problem3Excutions.txt](tests/teacher_resources/problem3Excutions.txt) | [Command and output](example_executions/teacher_problem3_steps_10.txt) | [Screenshot](screenshot/teacher_problem3_steps_10.jpg) |

### Problem 4 - Nine Teacher Inputs

| Input | Teacher's expected output | Actual execution | VS Code screenshot |
|---|---|---|---|
| [Basic](problem4Resources/problem4_basic.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_basic.txt) | [Screenshot](screenshot/teacher_problem4_basic.jpg) |
| [Duplicates](problem4Resources/problem4_duplicates.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_duplicates.txt) | [Screenshot](screenshot/teacher_problem4_duplicates.jpg) |
| [Errors](problem4Resources/problem4_errors.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_errors.txt) | [Screenshot](screenshot/teacher_problem4_errors.jpg) |
| [Assignment example](problem4Resources/problem4_example.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_example.txt) | [Screenshot](screenshot/teacher_problem4_example.jpg) |
| [Mixed operations](problem4Resources/problem4_mixed.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_mixed.txt) | [Screenshot](screenshot/teacher_problem4_mixed.jpg) |
| [Numbers](problem4Resources/problem4_numbers.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_numbers.txt) | [Screenshot](screenshot/teacher_problem4_numbers.jpg) |
| [Node positions](problem4Resources/problem4_positions.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_positions.txt) | [Screenshot](screenshot/teacher_problem4_positions.jpg) |
| [Simple](problem4Resources/problem4_simple.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_simple.txt) | [Screenshot](screenshot/teacher_problem4_simple.jpg) |
| [Statistics](problem4Resources/problem4_statistics.txt) | [problem4Executions.txt](tests/teacher_resources/problem4Executions.txt) | [Command and output](example_executions/teacher_problem4_statistics.txt) | [Screenshot](screenshot/teacher_problem4_statistics.jpg) |

### Retained Original Tests

All original test inputs are retained:

- [All Problem 2 directives](problem2Resources/problem2_all_operations.txt).
- [Empty and single-node boundaries](problem2Resources/problem2_empty_single.txt).
- [Original basic example](tests/original_resources/problem2_basic.txt).
- [Original error cases](tests/original_resources/problem2_errors.txt).
- [Original unit tests](tests/test_homework2.py), covering head/tail references, forward and backward links, cycles, sizes, duplicate values, staircase base cases, odd/even statistics, and seeded operation sequences.

## Execution Screenshots

`screenshot/` contains 23 actual execution screenshots captured from the VS Code integrated terminal: all 19 teacher examples above and the four additional executions below. The original four PNG filenames are retained with fresh executions of the updated programs and complete expanded test suite. Each screenshot shows the command, input or arguments, actual output, and successful verification. The matching text logs preserve the command and complete output for easier review.

| Additional execution | Actual execution | VS Code screenshot |
|---|---|---|
| Problem 2: all directives | [Command and output](example_executions/problem2_all_operations.txt) | [List operations](screenshot/problem2_all_operations.png) |
| Problem 3: required default demonstration | [Command and output](example_executions/problem3.txt) | [Staircase](screenshot/problem3.png) |
| Problem 4: original demonstration | [Command and output](example_executions/problem4.txt) | [Sorted list](screenshot/problem4.png) |
| Complete expanded unit-test suite | [Command and output](example_executions/tests_unittest.txt) | [Test execution](screenshot/tests_unittest.png) |

`problem2.py` supplies classes used by `problem2_driver.py`; its behavior is demonstrated through that driver and the unit tests. Problem 1 is the written answer above.

## Submission

Place the entire `Homework2/` folder in your Git repository, commit it, and push it. Keeping the folder name satisfies the assignment's folder option.

Include `README.md`, all five source Python files, every file in `problem2Resources/`, `problem4Resources/`, and `tests/`, all saved text logs in `example_executions/`, and all 23 screenshots in `screenshot/`.

Confirm that these files are visible in the repository, then submit the repository link on Brightspace.

