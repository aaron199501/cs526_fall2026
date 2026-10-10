"""Correctness, structure, recursion, and exact-output tests.

Run from the Homework3 directory:
    python -m unittest discover -s tests -v
"""

import ast
import inspect
import itertools
from pathlib import Path
import random
import subprocess
import sys
import unittest

import ghostbusters
import palindrome
import stacks
import substrings


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"
STACK_TYPES = (stacks.ArrayStack, stacks.SinglyLinkedStack, stacks.DoublyLinkedStack)


def run_program(filename, input_text=""):
    """Capture a real command-line run using the same Python interpreter."""
    result = subprocess.run(
        [sys.executable, str(ROOT / filename)],
        # Bytes avoid Windows translating an existing CRLF into CRCRLF.
        input=input_text.encode("utf-8"),
        capture_output=True,
        cwd=ROOT,
        timeout=30,
        check=True,
    )
    if result.stderr:
        raise AssertionError("Unexpected standard-error output: " + result.stderr.decode("utf-8"))
    return result.stdout.decode("utf-8").replace("\r\n", "\n")


def reference_substrings(text):
    return {text[start:end] for start in range(len(text))
            for end in range(start + 1, len(text) + 1)}


def reference_elimination(pairs):
    """Independent pairwise determinant check for infinite lines."""
    for first, second in itertools.combinations(pairs, 2):
        x1, y1, x2, y2 = first
        x3, y3, x4, y4 = second
        dx1, dy1 = x2 - x1, y2 - y1
        dx2, dy2 = x4 - x3, y4 - y3
        if dx1 * dy2 - dy1 * dx2 != 0:
            return False
        if dx1 * (y3 - y1) - dy1 * (x3 - x1) == 0:
            return False
    return True


def linked_nodes(stack):
    """Read top to bottom, detecting cycles and broken backward links."""
    nodes = []
    seen = set()
    node = stack.head
    previous = None
    while node is not None:
        if id(node) in seen:
            raise AssertionError("Cycle in linked stack")
        seen.add(id(node))
        if isinstance(stack, stacks.DoublyLinkedStack):
            if node.prev is not previous:
                raise AssertionError("Incorrect doubly linked prev pointer")
        nodes.append(node)
        previous, node = node, node.next
    if isinstance(stack, stacks.DoublyLinkedStack):
        if stack.tail is not previous:
            raise AssertionError("Incorrect doubly linked tail")
        backward = []
        node = stack.tail
        while node is not None:
            backward.append(node)
            if len(backward) > len(nodes):
                raise AssertionError("Cycle in backward links")
            node = node.prev
        if backward != list(reversed(nodes)):
            raise AssertionError("Forward and backward traversals disagree")
    return nodes


class PalindromeTests(unittest.TestCase):
    def test_teacher_examples(self):
        for text, expected in (("geek", False), ("asleelsa", True),
                               ("thisisatesttsetasisiht", True)):
            with self.subTest(text=text):
                self.assertEqual(palindrome.is_palindrome(text), expected)

    def test_space_separated_characters(self):
        self.assertTrue(palindrome.is_palindrome("r a c e c a r"))
        self.assertFalse(palindrome.is_palindrome("g e e k"))

    def test_case_is_significant(self):
        self.assertFalse(palindrome.is_palindrome("Aa"))
        self.assertTrue(palindrome.is_palindrome("AaA"))

    def test_single_character_and_symbols(self):
        self.assertTrue(palindrome.is_palindrome("x"))
        self.assertTrue(palindrome.is_palindrome("!? !"))
        self.assertFalse(palindrome.is_palindrome("!?"))

    def test_exhaustive_short_strings(self):
        for length in range(1, 7):
            for characters in itertools.product("aAb", repeat=length):
                text = "".join(characters)
                expected = text == text[::-1]
                self.assertEqual(palindrome.is_palindrome(text), expected)
                self.assertEqual(palindrome.is_palindrome(" ".join(text)), expected)

    def test_crlf_and_final_line_without_newline(self):
        self.assertEqual(run_program("palindrome.py", "Aa\r\na b a"), "False\nTrue\n1\n")

    def test_no_input(self):
        self.assertEqual(run_program("palindrome.py"), "0\n")


class SubstringTests(unittest.TestCase):
    def test_teacher_example(self):
        self.assertEqual(substrings.unique_substrings("abcab"), {
            "a", "ab", "abc", "abca", "abcab", "b", "bc", "bca", "bcab", "c", "ca", "cab"
        })

    def test_repetitions_are_unique(self):
        self.assertEqual(substrings.unique_substrings("aaaa"), {"a", "aa", "aaa", "aaaa"})

    def test_empty_and_single_character(self):
        self.assertEqual(substrings.unique_substrings(""), set())
        self.assertEqual(substrings.unique_substrings("Z"), {"Z"})

    def test_nonconsecutive_characters_are_excluded(self):
        self.assertNotIn("ac", substrings.unique_substrings("abc"))

    def test_spaces_and_case_are_preserved(self):
        self.assertEqual(substrings.unique_substrings("A a"), reference_substrings("A a"))
        self.assertEqual(run_program("substrings.py", "Aa\n"), "A\nAa\na\n3\n")

    def test_exhaustive_short_strings(self):
        for length in range(8):
            for characters in itertools.product("ab", repeat=length):
                text = "".join(characters)
                self.assertEqual(substrings.unique_substrings(text), reference_substrings(text))

    def test_recursion_depth_on_long_repeated_input(self):
        text = "a" * 1100
        self.assertEqual(substrings.unique_substrings(text), {"a" * k for k in range(1, 1101)})

    def test_no_input(self):
        self.assertEqual(run_program("substrings.py"), "0\n")


class StackTests(unittest.TestCase):
    def test_empty_stack_and_underflow(self):
        for stack_type in STACK_TYPES:
            with self.subTest(stack_type=stack_type.__name__):
                stack = stack_type()
                self.assertTrue(stack.is_empty())
                self.assertEqual(stack.to_list(), [])
                with self.assertRaises(IndexError):
                    stack.pop()
                with self.assertRaises(IndexError):
                    stack.peek()
                self.assertIsNone(stack.reverse())
                self.assertTrue(stack.is_empty())
                if hasattr(stack, "head"):
                    self.assertEqual(linked_nodes(stack), [])

    def test_push_peek_pop_lifo(self):
        for stack_type in STACK_TYPES:
            with self.subTest(stack_type=stack_type.__name__):
                stack = stack_type()
                for value in (1, 2, 3):
                    stack.push(value)
                    self.assertEqual(stack.peek(), value)
                    self.assertFalse(stack.is_empty())
                self.assertEqual(stack.to_list(), [1, 2, 3])
                self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [3, 2, 1])
                self.assertTrue(stack.is_empty())
                if hasattr(stack, "head"):
                    linked_nodes(stack)

    def test_reverse_same_stack_and_storage(self):
        for stack_type in STACK_TYPES:
            for count in (0, 1, 2, 10, 200):
                with self.subTest(stack_type=stack_type.__name__, count=count):
                    stack = stack_type()
                    values = list(range(count))
                    for value in values:
                        stack.push(value)
                    alias = stack
                    if hasattr(stack, "head"):
                        before_nodes = linked_nodes(stack)
                    else:
                        backing = stack.items
                    self.assertIsNone(stack.reverse())
                    self.assertIs(stack, alias)
                    self.assertEqual(stack.to_list(), list(reversed(values)))
                    if hasattr(stack, "head"):
                        self.assertEqual(linked_nodes(stack), list(reversed(before_nodes)))
                    else:
                        self.assertIs(stack.items, backing)
                    self.assertEqual(len(stack), count)
                    if values:
                        self.assertEqual(stack.peek(), 0)

    def test_reverse_twice_restores_order(self):
        for stack_type in STACK_TYPES:
            stack = stack_type()
            for value in (4, 4, -2, 0, 7):
                stack.push(value)
            stack.reverse()
            stack.reverse()
            self.assertEqual(stack.to_list(), [4, 4, -2, 0, 7])
            if hasattr(stack, "head"):
                linked_nodes(stack)

    def test_operations_after_reverse(self):
        for stack_type in STACK_TYPES:
            stack = stack_type()
            for value in (1, 2, 3):
                stack.push(value)
            stack.reverse()
            stack.push(9)
            self.assertEqual(stack.pop(), 9)
            self.assertEqual(stack.pop(), 1)
            self.assertEqual(stack.peek(), 2)
            self.assertEqual(stack.to_list(), [3, 2])
            if hasattr(stack, "head"):
                linked_nodes(stack)

    def test_reversal_functions_use_recursion_without_loops(self):
        tree = ast.parse(inspect.getsource(stacks))
        functions = {node.name: node for node in ast.walk(tree)
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        loops = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp,
                 ast.DictComp, ast.GeneratorExp)
        for entry in ("reverse_array_stack", "reverse_singly_linked_stack", "reverse_doubly_linked_stack"):
            reachable = set()
            pending = [entry]
            recursive = False
            while pending:
                name = pending.pop()
                if name in reachable:
                    continue
                reachable.add(name)
                function = functions[name]
                self.assertFalse(any(isinstance(node, loops) for node in ast.walk(function)), name)
                for node in ast.walk(function):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id == name:
                            recursive = True
                        if node.func.id in functions and node.func.id not in reachable:
                            pending.append(node.func.id)
            self.assertTrue(recursive, entry + " must invoke a recursive helper")


class GhostbusterTests(unittest.TestCase):
    def test_single_stream(self):
        self.assertTrue(ghostbusters.all_ghosts_eliminated([(1, 2, 3, 4)]))

    def test_nonparallel_infinite_lines_cross_outside_segments(self):
        pairs = [(0, 0, 1, 0), (2, 1, 2, 2)]
        self.assertFalse(ghostbusters.all_ghosts_eliminated(pairs))

    def test_parallel_distinct_lines(self):
        self.assertTrue(ghostbusters.all_ghosts_eliminated([
            (0, 0, 2, 2), (3, 0, 5, 2), (0, 4, 1, 5)
        ]))

    def test_collinear_separate_pairs(self):
        self.assertFalse(ghostbusters.all_ghosts_eliminated([(0, 0, 2, 2), (5, 5, 7, 7)]))

    def test_vertical_and_horizontal_lines(self):
        self.assertTrue(ghostbusters.all_ghosts_eliminated([(1, 0, 1, 6), (4, 2, 4, -3)]))
        self.assertTrue(ghostbusters.all_ghosts_eliminated([(0, 1, 3, 1), (8, 4, 1, 4)]))
        self.assertFalse(ghostbusters.all_ghosts_eliminated([(1, 0, 1, 6), (1, 9, 1, -3)]))
        self.assertFalse(ghostbusters.all_ghosts_eliminated([(0, 1, 3, 1), (8, 1, 1, 1)]))

    def test_opposite_directions_and_scaled_vectors(self):
        self.assertTrue(ghostbusters.all_ghosts_eliminated([(0, 0, 2, 4), (4, 1, 1, -5)]))
        self.assertFalse(ghostbusters.all_ghosts_eliminated([(0, 0, 2, 4), (4, 8, 1, 2)]))

    def test_large_integer_coordinates_without_rounding(self):
        large = 10 ** 100
        self.assertTrue(ghostbusters.all_ghosts_eliminated([
            (0, 0, large, large - 1), (1, 0, large + 1, large - 1)
        ]))
        self.assertFalse(ghostbusters.all_ghosts_eliminated([
            (0, 0, large, large - 1), (0, 1, large - 1, large - 1)
        ]))

    def test_randomized_against_independent_pairwise_geometry(self):
        generator = random.Random(526)
        for trial in range(1000):
            pairs = []
            for _ in range(generator.randint(1, 8)):
                while True:
                    pair = tuple(generator.randint(-9, 9) for _ in range(4))
                    if pair[:2] != pair[2:]:
                        break
                pairs.append(pair)
            with self.subTest(trial=trial):
                self.assertEqual(ghostbusters.all_ghosts_eliminated(pairs), reference_elimination(pairs))

    def test_many_parallel_streams(self):
        pairs = [(0, offset, 1, offset + 1) for offset in range(5000)]
        self.assertTrue(ghostbusters.all_ghosts_eliminated(pairs))
        pairs[-1] = pairs[0]
        self.assertFalse(ghostbusters.all_ghosts_eliminated(pairs))


class ExactOutputTests(unittest.TestCase):
    def test_all_input_and_expected_output_files(self):
        scripts = {"p1": "palindrome.py", "p2": "substrings.py", "p4": "ghostbusters.py"}
        inputs = sorted(DATA.glob("*_input.txt"))
        self.assertTrue(inputs, "No test input fixtures found")
        for input_path in inputs:
            expected_path = input_path.with_name(input_path.name.replace("_input.txt", "_expected.txt"))
            with self.subTest(fixture=input_path.name):
                self.assertTrue(expected_path.is_file(), str(expected_path))
                script = scripts[input_path.name[:2]]
                self.assertEqual(run_program(script, input_path.read_text(encoding="utf-8")),
                                 expected_path.read_text(encoding="utf-8"))

    def test_stack_demonstration_output(self):
        self.assertEqual(run_program("stacks.py"), (DATA / "p3_expected.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
