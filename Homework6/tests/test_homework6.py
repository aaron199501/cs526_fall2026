"""Independent correctness tests for CS526 Homework 6.

The standard-library sorting used here is a test oracle only. The three
assignment programs must perform their own heap and ordering operations.

Run from Homework6 with: python -m unittest discover -s tests -v
"""

import ast
from collections import deque
from contextlib import redirect_stdout
import io
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from linkedHeap import BinaryMinHeap
import mergeLogs as merge_module
from mergeLogs import merge_logs
from runningMedian import RunningMedian, running_medians


def level_values(heap):
    """Read linked nodes breadth first; this does not call heap helpers."""
    if heap.root is None:
        return []
    pending = deque([heap.root])
    values = []
    while pending:
        node = pending.popleft()
        values.append(node.value)
        if node.left is not None:
            pending.append(node.left)
        if node.right is not None:
            pending.append(node.right)
    return values


def tree_snapshot(heap):
    """Include object identities and links when checking non-mutation."""
    pending = deque([heap.root] if heap.root is not None else [])
    result = []
    while pending:
        node = pending.popleft()
        result.append((id(node), node.value, id(node.left),
                       id(node.right), id(node.parent)))
        if node.left is not None:
            pending.append(node.left)
        if node.right is not None:
            pending.append(node.right)
    return len(heap), id(heap.root), tuple(result)


def median_oracle(values):
    result = []
    for end in range(1, len(values) + 1):
        ordered = sorted(values[:end])
        middle = end // 2
        if end % 2:
            result.append(float(ordered[middle]))
        else:
            result.append((ordered[middle - 1] + ordered[middle]) / 2.0)
    return result


def merge_oracle(logs):
    return sorted((value, register)
                  for register, log in enumerate(logs, 1) for value in log)


def drawing_signature(text):
    """Parse top-down tree rows, permitting different horizontal spacing.

    A signature retains each level's left-to-right node values and the
    ordered left/right connectors above the next level. It therefore catches
    missing, misplaced, or repeated nodes without demanding exact whitespace.
    """
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.fullmatch(r"-?\d+(?:\s+-?\d+)*", stripped):
            rows.append(("values", tuple(map(int, stripped.split()))))
        elif re.fullmatch(r"[/\\\s]+", stripped):
            rows.append(("branches", tuple(re.findall(r"[/\\]", stripped))))
        else:
            raise AssertionError("Unexpected content in tree drawing: " + line)
    return tuple(rows)


def heap_output_signature(text):
    """Keep the input header and every insertion drawing, ignoring spacing."""
    lines = text.splitlines()
    if not lines or not lines[0].startswith("Input values: "):
        raise AssertionError("Missing 'Input values: ' header")
    values = ast.literal_eval(lines[0].split(":", 1)[1].strip())
    blocks = []
    value = None
    drawing = []
    for line in lines[1:]:
        match = re.fullmatch(r"\s*After insert\((-?\d+)\):\s*", line)
        if match:
            if value is not None:
                blocks.append((value, drawing_signature("\n".join(drawing))))
            value = int(match.group(1))
            drawing = []
        elif value is not None:
            drawing.append(line)
        elif line.strip():
            raise AssertionError("Unexpected text before insertion output: " + line)
    if value is not None:
        blocks.append((value, drawing_signature("\n".join(drawing))))
    return values, tuple(blocks)


def run_program(filename, input_text):
    completed = subprocess.run(
        [sys.executable, str(ROOT / filename)], input=input_text, text=True,
        capture_output=True, cwd=ROOT, encoding="utf-8", timeout=20,
    )
    if completed.returncode:
        raise AssertionError(
            f"{filename} exited {completed.returncode}: {completed.stderr}"
        )
    if completed.stderr.strip():
        raise AssertionError(f"Unexpected stderr from {filename}: {completed.stderr}")
    return completed.stdout


def merged_output_value(text):
    for line in text.splitlines():
        if line.startswith("Merged log:"):
            return ast.literal_eval(line.split(":", 1)[1].strip())
    return ast.literal_eval(text.strip())


class HeapTests(unittest.TestCase):
    def assert_heap(self, heap, expected):
        self.assertEqual(len(heap), len(expected))
        self.assertEqual(heap.is_empty(), not expected)
        if not expected:
            self.assertIsNone(heap.root)
            return
        self.assertIsNotNone(heap.root)
        self.assertIsNone(heap.root.parent)
        pending = deque([heap.root])
        nodes = set()
        encountered_gap = False
        actual = []
        while pending:
            node = pending.popleft()
            if node is None:
                encountered_gap = True
                continue
            self.assertFalse(encountered_gap, "Tree is not complete and left-filled")
            self.assertNotIn(id(node), nodes, "Cycle or node with two parents")
            nodes.add(id(node))
            actual.append(node.value)
            for child in (node.left, node.right):
                if child is not None:
                    self.assertIs(child.parent, node)
                    self.assertLessEqual(node.value, child.value)
                pending.append(child)
        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(heap.peek(), min(expected))

    def make_heap(self, values):
        heap = BinaryMinHeap()
        for value in values:
            heap.insert(value)
        return heap

    def test_empty_heap_contract(self):
        heap = BinaryMinHeap()
        self.assert_heap(heap, [])
        with self.assertRaises(IndexError):
            heap.peek()
        with self.assertRaises(IndexError):
            heap.extract_min()
        self.assertIs(heap.delete(100), False)
        self.assertEqual(heap.heap_sort(), [])
        self.assert_heap(heap, [])

    def test_assignment_insert_example_and_peek_does_not_mutate(self):
        heap = BinaryMinHeap()
        expected_levels = ([8], [3, 8], [3, 8, 5], [1, 3, 5, 8])
        inserted = []
        for value, levels in zip([8, 3, 5, 1], expected_levels):
            inserted.append(value)
            heap.insert(value)
            self.assert_heap(heap, inserted)
            self.assertEqual(level_values(heap), levels)
            before = tree_snapshot(heap)
            heap.peek()
            self.assertEqual(tree_snapshot(heap), before)

    def test_equal_insert_keeps_values_at_original_positions(self):
        class TaggedInt(int):
            pass

        first, second, third = (TaggedInt(7) for _ in range(3))
        heap = BinaryMinHeap()
        heap.insert(first)
        heap.insert(second)
        heap.insert(third)
        self.assertIs(heap.root.value, first)
        self.assertIs(heap.root.left.value, second)
        self.assertIs(heap.root.right.value, third)
        self.assert_heap(heap, [7, 7, 7])

    def test_insert_across_complete_tree_level_boundaries(self):
        values = list(range(96, -1, -1))
        heap = BinaryMinHeap()
        for end, value in enumerate(values, 1):
            heap.insert(value)
            self.assert_heap(heap, values[:end])

    def test_extract_min_preserves_invariants_until_empty(self):
        values = [8, -3, 5, 1, 1, 12, -3, 0, 900, 4, 2]
        heap = self.make_heap(values)
        ordered = sorted(values)
        for index, expected in enumerate(ordered):
            self.assertEqual(heap.extract_min(), expected)
            self.assert_heap(heap, ordered[index + 1:])
        with self.assertRaises(IndexError):
            heap.extract_min()

    def test_delete_removes_only_one_duplicate(self):
        values = [4, 2, 2, 2, 9, 0]
        heap = self.make_heap(values)
        self.assertIs(heap.delete(2), True)
        values.remove(2)
        self.assert_heap(heap, values)
        self.assertEqual(heap.heap_sort().count(2), 2)
        before = tree_snapshot(heap)
        self.assertIs(heap.delete(12345), False)
        self.assertEqual(tree_snapshot(heap), before)

    def test_delete_root_and_last_and_single_node(self):
        heap = self.make_heap([1, 2, 3, 4, 5, 6, 7])
        self.assertIs(heap.delete(7), True)
        self.assert_heap(heap, [1, 2, 3, 4, 5, 6])
        self.assertIs(heap.delete(1), True)
        self.assert_heap(heap, [2, 3, 4, 5, 6])
        singleton = self.make_heap([42])
        self.assertIs(singleton.delete(42), True)
        self.assert_heap(singleton, [])
        self.assertIs(singleton.delete(42), False)

    def test_delete_replacement_must_sift_up(self):
        heap = self.make_heap([1, 10, 2, 11, 12, 3, 4])
        self.assertEqual(level_values(heap), [1, 10, 2, 11, 12, 3, 4])
        self.assertIs(heap.delete(11), True)
        self.assert_heap(heap, [1, 10, 2, 12, 3, 4])

    def test_delete_replacement_must_sift_down(self):
        heap = self.make_heap([1, 2, 3, 4, 5, 6, 7])
        self.assertIs(heap.delete(2), True)
        self.assert_heap(heap, [1, 3, 4, 5, 6, 7])

    def test_build_handles_empty_singleton_duplicates_and_negatives(self):
        for values in ([], [42], [3, 1, 1, -8, 0, 99, -8],
                       list(range(64, -1, -1))):
            with self.subTest(values=values):
                heap = BinaryMinHeap()
                original = values[:]
                heap.build(values)
                self.assertEqual(values, original)
                self.assert_heap(heap, values)
                self.assertEqual(heap.heap_sort(), sorted(values))

    def test_heap_sort_preserves_entire_linked_tree(self):
        values = [9, 4, 17, 3, 8, 8, -5, 10, 100, 0]
        heap = self.make_heap(values)
        before = tree_snapshot(heap)
        self.assertEqual(heap.heap_sort(), sorted(values))
        self.assertEqual(tree_snapshot(heap), before)
        self.assertEqual(heap.heap_sort(), sorted(values))
        self.assert_heap(heap, values)
        heap.insert(-100)
        self.assertEqual(heap.extract_min(), -100)
        self.assert_heap(heap, values)

    def test_print_heap_draws_assignment_tree_without_mutation(self):
        heap = self.make_heap([8, 3, 5, 1])
        before = tree_snapshot(heap)
        stream = io.StringIO()
        with redirect_stdout(stream):
            heap.print_heap()
        expected = "1\n/ \\\n3 5\n/\n8\n"
        self.assertEqual(drawing_signature(stream.getvalue()),
                         drawing_signature(expected))
        self.assertEqual(tree_snapshot(heap), before)

    def test_random_mixed_operations_against_multiset(self):
        for seed in (526, 617, 2026):
            with self.subTest(seed=seed):
                rng = random.Random(seed)
                heap = BinaryMinHeap()
                reference = []
                for _ in range(500):
                    operation = rng.randrange(5)
                    if operation < 2 or not reference:
                        value = rng.randint(-40, 40)
                        heap.insert(value)
                        reference.append(value)
                    elif operation == 2:
                        expected = min(reference)
                        self.assertEqual(heap.extract_min(), expected)
                        reference.remove(expected)
                    elif operation == 3:
                        value = rng.randint(-40, 40)
                        found = value in reference
                        self.assertIs(heap.delete(value), found)
                        if found:
                            reference.remove(value)
                    else:
                        before = tree_snapshot(heap)
                        self.assertEqual(heap.heap_sort(), sorted(reference))
                        self.assertEqual(tree_snapshot(heap), before)
                    self.assert_heap(heap, reference)


class MergeTests(unittest.TestCase):
    def test_assignment_example(self):
        logs = [[3, 9, 14], [1, 9, 20, 25], [], [5]]
        self.assertEqual(merge_logs(logs),
                         [(1, 2), (3, 1), (5, 4), (9, 1), (9, 2),
                          (14, 1), (20, 2), (25, 2)])

    def test_zero_registers_and_all_empty_logs(self):
        self.assertEqual(merge_logs([]), [])
        self.assertEqual(merge_logs([[], [], []]), [])

    def test_ties_use_register_number_and_keep_all_duplicates(self):
        logs = [[9, 9, 9], [9, 9], [], [9]]
        self.assertEqual(merge_logs(logs),
                         [(9, 1), (9, 1), (9, 1), (9, 2), (9, 2), (9, 4)])

    def test_empty_logs_preserve_original_register_numbers(self):
        self.assertEqual(merge_logs([[], [1, 2], [], [1], []]),
                         [(1, 2), (1, 4), (2, 2)])

    def test_single_register_and_uneven_lengths(self):
        for logs in ([[0, 0, 3, 99]], [[1], list(range(20)), [], [2, 2, 2]]):
            with self.subTest(logs=logs):
                self.assertEqual(merge_logs(logs), merge_oracle(logs))

    def test_input_logs_are_not_mutated(self):
        logs = [[1, 2, 2], [], [0, 1], [7]]
        before = [log[:] for log in logs]
        merge_logs(logs)
        self.assertEqual(logs, before)

    def test_random_sorted_logs(self):
        rng = random.Random(5261)
        for _ in range(100):
            logs = [sorted(rng.randint(0, 50) for _ in range(rng.randrange(35)))
                    for _ in range(rng.randrange(25))]
            self.assertEqual(merge_logs(logs), merge_oracle(logs))

    def test_live_queue_has_at_most_one_entry_per_register(self):
        logs = [[0, 2, 2, 8], [], [0, 0, 1, 2, 20], [2],
                list(range(25)), [], [0, 2, 100]]
        owner = self
        instances = []
        operations = []

        class TrackingHeap(BinaryMinHeap):
            def __init__(self):
                super().__init__()
                instances.append(self)

            def check_live_entries(self):
                entries = level_values(self)
                registers = [entry[1] for entry in entries]
                owner.assertEqual(len(entries), len(self))
                owner.assertLessEqual(len(entries), len(logs))
                owner.assertEqual(len(registers), len(set(registers)),
                                  "Multiple queued sales from one register")

            def insert(self, value):
                self.check_live_entries()
                result = super().insert(value)
                self.check_live_entries()
                operations.append("insert")
                return result

            def extract_min(self):
                self.check_live_entries()
                result = super().extract_min()
                self.check_live_entries()
                operations.append("extract")
                return result

        with patch.object(merge_module, "BinaryMinHeap", TrackingHeap):
            self.assertEqual(merge_module.merge_logs(logs), merge_oracle(logs))
        self.assertTrue(instances, "Merge must use the linked priority queue")
        self.assertEqual(operations.count("insert"), sum(map(len, logs)))
        self.assertEqual(operations.count("extract"), sum(map(len, logs)))
        self.assertTrue(all(heap.is_empty() for heap in instances))


class MedianTests(unittest.TestCase):
    def test_assignment_example(self):
        self.assertEqual(running_medians([5, 15, 2, 4, 8]),
                         [5.0, 10.0, 5.0, 4.5, 5.0])

    def test_empty_and_singleton(self):
        self.assertEqual(running_medians([]), [])
        self.assertEqual(running_medians([42]), [42.0])

    def test_duplicates(self):
        self.assertEqual(running_medians([7] * 30), [7.0] * 30)
        self.assertEqual(running_medians([2, 2, 5, 5, 2, 5]),
                         median_oracle([2, 2, 5, 5, 2, 5]))

    def test_increasing_and_decreasing_streams(self):
        for values in (list(range(81)), list(range(80, -1, -1))):
            self.assertEqual(running_medians(values), median_oracle(values))

    def test_negative_values_and_half_integer_medians(self):
        values = [-9, -2, -7, 0, -1, -1, -100, 50]
        self.assertEqual(running_medians(values), median_oracle(values))

    def test_alternating_extremes(self):
        values = [10**9, -10**9, 999, -999, 1, -1, 0, 4, -4]
        self.assertEqual(running_medians(values), median_oracle(values))

    def test_input_values_are_not_mutated(self):
        values = [5, 15, 2, 4, 8]
        before = values[:]
        running_medians(values)
        self.assertEqual(values, before)

    def test_random_streams(self):
        rng = random.Random(5263)
        for _ in range(80):
            values = [rng.randint(-300, 300) for _ in range(rng.randrange(150))]
            self.assertEqual(running_medians(values), median_oracle(values))

    def test_stream_preserves_balance_partition_and_linked_heap_invariants(self):
        rng = random.Random(52630)
        values = [5, 15, 2, 4, 8, 8, -10, 100, -10, 0]
        values.extend(rng.randint(-500, 500) for _ in range(180))
        expected_medians = median_oracle(values)
        stream = RunningMedian()
        for end, (value, expected) in enumerate(zip(values, expected_medians), 1):
            self.assertEqual(stream.add(value), expected)
            self.assertEqual(stream.median(), expected)
            self.assertIn(len(stream.lower) - len(stream.upper), (0, 1))
            lower_stored = level_values(stream.lower)
            upper_values = level_values(stream.upper)
            HeapTests.assert_heap(self, stream.lower, lower_stored)
            HeapTests.assert_heap(self, stream.upper, upper_values)
            lower_values = [-value for value in lower_stored]
            self.assertEqual(sorted(lower_values + upper_values),
                             sorted(values[:end]))
            if lower_values and upper_values:
                self.assertLessEqual(max(lower_values), min(upper_values))


class InstructorResourceTests(unittest.TestCase):
    """One test per supplied input/output pair, generated below.

    The original resource set has no merge_input4.txt or heap_input11.txt.
    Their absent inputs are not fabricated or counted as instructor cases.
    """

    def check_resource(self, input_path):
        expected_path = ROOT / "tests" / "expected" / input_path.name.replace(
            "_input", "_output")
        self.assertTrue(expected_path.is_file(), str(expected_path))
        input_text = input_path.read_text(encoding="utf-8-sig")
        expected_text = expected_path.read_text(encoding="utf-8-sig")
        kind = input_path.name.split("_", 1)[0]
        if kind == "merge":
            logs = [ast.literal_eval(line) for line in input_text.splitlines()
                    if line.strip()]
            expected = merged_output_value(expected_text)
            self.assertEqual(merge_logs(logs), expected)
            actual = run_program("mergeLogs.py", input_text)
            self.assertEqual(merged_output_value(actual), expected)
        elif kind == "median":
            values = ast.literal_eval(input_text.strip())
            expected = ast.literal_eval(expected_text.strip())
            self.assertEqual(running_medians(values), expected)
            actual = run_program("runningMedian.py", input_text)
            self.assertEqual(ast.literal_eval(actual.strip()), expected)
        elif kind == "heap":
            values = ast.literal_eval(input_text.strip())
            expected = heap_output_signature(expected_text)
            actual = heap_output_signature(run_program("linkedHeap.py", input_text))
            self.assertEqual(actual, expected)
            self.assertEqual(actual[0], values)
            self.assertEqual(len(actual[1]), len(values))
        else:
            self.fail("Unknown resource kind: " + kind)


def _resource_test(input_path):
    def test(self):
        self.check_resource(input_path)
    test.__doc__ = "Instructor case " + input_path.name
    return test


for _input_path in sorted((ROOT / "inputs").glob("*_input*.txt")):
    _name = "test_instructor_" + _input_path.stem
    setattr(InstructorResourceTests, _name, _resource_test(_input_path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
