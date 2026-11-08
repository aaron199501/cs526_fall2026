"""Independent invariant and operation checks for Problem 1."""

import contextlib
import io
import random
import unittest

from binarySearchTree import BST, Node, demo


class BSTTests(unittest.TestCase):
    def make_tree(self, values):
        tree = BST()
        for value in values:
            tree.addNode(value)
        return tree

    def assert_invariant(self, tree, expected):
        self.assertEqual(tree.inorder(), sorted(expected))
        self.assertEqual(len(tree), len(expected))
        pending = [(tree.root, None, None)]
        while pending:
            node, lower, upper = pending.pop()
            if node is None:
                continue
            if lower is not None:
                self.assertGreater(node.value, lower)
            if upper is not None:
                self.assertLess(node.value, upper)
            pending.append((node.left, lower, node.value))
            pending.append((node.right, node.value, upper))

    def test_node_defaults(self):
        node = Node(12)
        self.assertEqual(node.value, 12)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_empty_tree(self):
        tree = BST()
        self.assertIsNone(tree.findNode(1))
        self.assertFalse(tree.deleteNode(1))
        self.assertEqual(tree.treeLines(), ["(empty tree)"])
        self.assert_invariant(tree, set())

    def test_duplicates_do_not_create_nodes(self):
        tree = self.make_tree([4, 2, 6])
        self.assertFalse(tree.addNode(4))
        self.assertFalse(tree.addNode(2))
        self.assert_invariant(tree, {2, 4, 6})

    def test_find_returns_node_or_none(self):
        tree = self.make_tree([4, 2, 6])
        self.assertIs(tree.findNode(2), tree.root.left)
        self.assertIsNone(tree.findNode(5))

    def test_delete_only_root(self):
        tree = self.make_tree([9])
        self.assertTrue(tree.deleteNode(9))
        self.assertIsNone(tree.root)
        self.assert_invariant(tree, set())

    def test_delete_leaf(self):
        tree = self.make_tree([8, 3, 10, 1, 6])
        self.assertTrue(tree.deleteNode(1))
        self.assert_invariant(tree, {3, 6, 8, 10})

    def test_delete_one_child_and_root_with_one_child(self):
        tree = self.make_tree([8, 3, 6])
        self.assertTrue(tree.deleteNode(3))
        self.assertEqual(tree.root.left.value, 6)
        self.assertTrue(tree.deleteNode(8))
        self.assertEqual(tree.root.value, 6)
        self.assert_invariant(tree, {6})

    def test_delete_two_children_successor_has_right_child(self):
        values = {20, 10, 40, 30, 35, 50}
        tree = self.make_tree([20, 10, 40, 30, 35, 50])
        self.assertTrue(tree.deleteNode(20))
        self.assertEqual(tree.root.value, 30)
        self.assertEqual(tree.root.right.left.value, 35)
        self.assert_invariant(tree, values - {20})

    def test_delete_two_children_immediate_successor(self):
        tree = self.make_tree([8, 3, 10, 12])
        self.assertTrue(tree.deleteNode(8))
        self.assertEqual(tree.root.value, 10)
        self.assert_invariant(tree, {3, 10, 12})

    def test_missing_delete_preserves_tree(self):
        tree = self.make_tree([5, 2, 9])
        before = tree.treeLines()
        self.assertFalse(tree.deleteNode(7))
        self.assertEqual(tree.treeLines(), before)
        self.assert_invariant(tree, {2, 5, 9})

    def test_random_operations_against_set(self):
        rng = random.Random(526)
        tree = BST()
        expected = set()
        for _ in range(800):
            value = rng.randint(-100, 100)
            operation = rng.randrange(3)
            if operation == 0:
                self.assertEqual(tree.addNode(value), value not in expected)
                expected.add(value)
            elif operation == 1:
                self.assertEqual(tree.deleteNode(value), value in expected)
                expected.discard(value)
            else:
                self.assertEqual(tree.findNode(value) is not None, value in expected)
            self.assert_invariant(tree, expected)

    def test_degenerate_tree_avoids_recursion_limit(self):
        tree = self.make_tree(range(1200))
        self.assertEqual(tree.findNode(1199).value, 1199)
        self.assertEqual(len(tree.treeLines()), 1200)
        self.assertTrue(tree.deleteNode(1199))
        self.assert_invariant(tree, set(range(1199)))

    def test_demo_includes_success_and_failure(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            demo(5, 526)
        text = output.getvalue()
        self.assertEqual(text.count("Add Node("), 2)
        self.assertEqual(text.count("Delete Node("), 2)
        queries = [line for line in text.splitlines() if line.startswith("FindNode(")]
        self.assertEqual(len(queries), 2)
        self.assertTrue(queries[0].endswith(": found"))
        self.assertTrue(queries[1].endswith(": not found"))

    def test_demo_size_bounds(self):
        for size in (4, 51):
            with self.assertRaises(ValueError):
                demo(size, 526)


if __name__ == "__main__":
    unittest.main()
