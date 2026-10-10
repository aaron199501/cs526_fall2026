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
|
|-- README.md
|-- problem2.py
|-- problem2_driver.py
|-- problem3.py
|-- problem4.py
|-- problem2Resources/
|   |-- problem2_basic.txt
|   |-- problem2_all_operations.txt
|   |-- problem2_errors.txt
|   `-- problem2_empty_single.txt
|-- tests/
|   `-- test_homework2.py
`-- screenshot/
    `-- *.png
```

- `problem2.py` contains the `Node` and `SinglyLinkedList` classes.
- `problem2_driver.py` reads commands from standard input and applies them to a `SinglyLinkedList`.
- `problem3.py` contains the recursive `ways(n)` function.
- `problem4.py` contains the `Node` and `SortedDoublyLinkedList` classes and a short driver demonstrating the required methods.
- `problem2Resources/problem2_basic.txt` contains the basic test input for Problem 2.

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

Blank lines and lines beginning with `#` are ignored.

The driver prints a warning and continues when it encounters:

- an unknown directive,
- the wrong number of arguments,
- an index that is not a whole number,
- an index that is out of range, or
- a request to delete a value that is not in the list.

After all input lines are processed, the driver prints the final list.

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

The demonstration calls `ways()` for 3, 5, and 10 steps. Its execution is recorded in the screenshot section below.

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

## Interesting aspects

Several design and edge-case decisions are important in this homework.

For Problem 2, keeping both a head and a tail pointer makes appending efficient because the list does not need to be traversed to locate its final node. Special handling is also required when deleting the only node in the list so that both `head` and `tail` become `None`.

Index validation is performed before accessing or modifying nodes. Invalid indexes raise `IndexError`, allowing the driver to catch the error, print a warning, and continue processing the remaining input.

For Problem 4, maintaining sorted order during every insertion makes later operations more efficient. In particular, `exists()` and `count()` can stop searching as soon as the current value becomes greater than the requested value. Because the list is doubly linked, both `prev` and `next` references must be updated carefully when nodes are inserted or deleted.

Recursion is required for Problem 3 and is also used where it naturally fits in Problem 4, including `total()`, `count()`, `exists()`, and `print_list()`.

## How to run

Open a terminal in the `Homework2` directory.

### Problem 2

macOS / Linux / Git Bash:

```bash
python3 problem2_driver.py < problem2Resources/problem2_basic.txt
```

Windows PowerShell:

```powershell
Get-Content .\problem2Resources\problem2_basic.txt | py -B .\problem2_driver.py
```

### Problem 3

macOS / Linux / Git Bash:

```bash
python3 problem3.py
```

Windows:

```powershell
py -B .\problem3.py
```

### Problem 4

macOS / Linux / Git Bash:

```bash
python3 problem4.py
```

Windows:

```powershell
py -B .\problem4.py
```

## Test Files

### problem2Resources/problem2_basic.txt

This file is used to test the basic Problem 2 driver behavior.

```text
append 12
append 3
append 5
prepend 1
get 2
delete 3
update 0 8
append 7
```

This test checks:

- `append`
- `prepend`
- `get`
- `delete`
- `update`
- final list output

The Problem 2 driver also supports testing `insert`, `find`, `len`, `delete_at`, `print_list`, invalid indexes, invalid directives, incorrect argument counts, and attempts to delete values that are not present.

Problems 3 and 4 use the example calls and driver code included directly in their source files, so no additional external test files are required for those examples.

## Execution Screenshots

Four representative execution screenshots are provided in `screenshot/`: Problems 2-4 and the automated checks. They show actual executions captured from the VS Code integrated terminal. All test scripts and input files are retained, including cases without individual screenshots.

| Execution | Screenshot |
|---|---|
| Problem 2: all directives | [List operations](screenshot/problem2_all_operations.png) |
| Problem 3: recursive staircase demonstration | [Staircase](screenshot/problem3.png) |
| Problem 4: sorted doubly linked list demonstration | [Sorted list](screenshot/problem4.png) |
| Automated checks | [Test execution](screenshot/tests_unittest.png) |

`problem2.py` provides the linked-list classes used by `problem2_driver.py`; its behavior is demonstrated through the driver and automated checks. Problem 1 is the written answer above.

## Automated Checks

From the submission directory, run:

```powershell
py -B -m unittest discover -s tests -v
```

On macOS or Linux, use `python3` in place of `py`.
The checks cover linked-list links and sizes, staircase base cases, duplicate values, and odd/even median and middle-three calculations. The saved driver inputs exercise all directives, invalid input, continued processing, and empty-list boundaries.

## Submission

Place the entire `Homework2/` folder in your Git repository, commit it, and push it. Keeping the folder name satisfies the assignment's folder option.

Include `README.md`, all four source Python files, every file in `problem2Resources/` and `tests/`, and the four screenshots in `screenshot/`. The screenshots provide the example executions.

Confirm that these files are visible in the repository, then submit the repository link on Brightspace.

