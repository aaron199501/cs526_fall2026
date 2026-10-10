import itertools
import random
import unittest

from problem2 import SinglyLinkedList
from problem3 import ways
from problem4 import SortedDoublyLinkedList


class SinglyListTests(unittest.TestCase):
    def check_list(self, linked, expected):
        nodes = []
        seen = set()
        node = linked.head
        while node is not None:
            self.assertNotIn(id(node), seen, "The list contains a cycle")
            seen.add(id(node))
            nodes.append(node)
            node = node.next
        self.assertEqual([node.value for node in nodes], expected)
        self.assertEqual(len(linked), len(expected))
        self.assertIs(linked.head, nodes[0] if nodes else None)
        self.assertIs(linked.tail, nodes[-1] if nodes else None)
        if nodes:
            self.assertIsNone(linked.tail.next)
        for index, value in enumerate(expected):
            self.assertEqual(linked.get(index), value)

    def test_empty_and_invalid_indexes(self):
        linked = SinglyLinkedList()
        self.check_list(linked, [])
        self.assertEqual(linked.find(9), -1)
        self.assertFalse(linked.delete(9))
        for index in (-1, 0, 1):
            with self.assertRaises(IndexError):
                linked.get(index)
            with self.assertRaises(IndexError):
                linked.update(index, 9)
            with self.assertRaises(IndexError):
                linked.delete_at(index)
        for index in (-1, 1):
            with self.assertRaises(IndexError):
                linked.insert(index, 9)
        self.check_list(linked, [])

    def test_insert_head_middle_and_tail(self):
        linked = SinglyLinkedList()
        linked.append(4)
        linked.prepend(2)
        linked.insert(1, 3)
        linked.insert(0, 1)
        linked.insert(len(linked), 5)
        self.check_list(linked, [1, 2, 3, 4, 5])
        for index in (-1, 6):
            with self.assertRaises(IndexError):
                linked.insert(index, 99)
        self.check_list(linked, [1, 2, 3, 4, 5])

    def test_find_and_update_duplicate_values(self):
        linked = SinglyLinkedList()
        for value in (4, 7, 4):
            linked.append(value)
        self.assertEqual(linked.find(4), 0)
        self.assertEqual(linked.find(99), -1)
        linked.update(0, 2)
        linked.update(2, 8)
        self.check_list(linked, [2, 7, 8])
        for index in (-1, 3):
            with self.assertRaises(IndexError):
                linked.update(index, 99)
        self.check_list(linked, [2, 7, 8])

    def test_delete_removes_first_match(self):
        linked = SinglyLinkedList()
        for value in (2, 4, 4, 6):
            linked.append(value)
        self.assertTrue(linked.delete(4))
        self.check_list(linked, [2, 4, 6])
        self.assertTrue(linked.delete(2))
        self.check_list(linked, [4, 6])
        self.assertFalse(linked.delete(99))
        self.check_list(linked, [4, 6])

    def test_delete_tail_and_only_node_then_reuse(self):
        linked = SinglyLinkedList()
        linked.append(1)
        linked.append(2)
        self.assertTrue(linked.delete(2))
        self.check_list(linked, [1])
        self.assertTrue(linked.delete(1))
        self.check_list(linked, [])
        linked.prepend(3)
        linked.append(4)
        self.check_list(linked, [3, 4])

    def test_delete_at_head_middle_tail_and_single(self):
        linked = SinglyLinkedList()
        for value in (1, 2, 3, 4):
            linked.append(value)
        self.assertEqual(linked.delete_at(1), 2)
        self.check_list(linked, [1, 3, 4])
        self.assertEqual(linked.delete_at(2), 4)
        self.check_list(linked, [1, 3])
        self.assertEqual(linked.delete_at(0), 1)
        self.assertEqual(linked.delete_at(0), 3)
        self.check_list(linked, [])
        linked.append(5)
        self.check_list(linked, [5])

    def test_operation_sequence_against_python_list(self):
        generator = random.Random(526)
        linked = SinglyLinkedList()
        expected = []
        for _ in range(250):
            operation = generator.choice(("append", "prepend", "insert", "delete", "delete_at", "update"))
            value = generator.randrange(-5, 6)
            if operation == "append":
                linked.append(value)
                expected.append(value)
            elif operation == "prepend":
                linked.prepend(value)
                expected.insert(0, value)
            elif operation == "insert":
                index = generator.randrange(len(expected) + 1)
                linked.insert(index, value)
                expected.insert(index, value)
            elif operation == "delete":
                found = value in expected
                self.assertEqual(linked.delete(value), found)
                if found:
                    expected.remove(value)
            elif expected:
                index = generator.randrange(len(expected))
                if operation == "delete_at":
                    self.assertEqual(linked.delete_at(index), expected.pop(index))
                else:
                    linked.update(index, value)
                    expected[index] = value
            self.check_list(linked, expected)


class SortedListTests(unittest.TestCase):
    def check_list(self, linked, expected):
        nodes = []
        seen = set()
        previous = None
        node = linked.head
        while node is not None:
            self.assertNotIn(id(node), seen, "The list contains a cycle")
            seen.add(id(node))
            self.assertIs(node.prev, previous)
            nodes.append(node)
            previous, node = node, node.next
        self.assertEqual([node.value for node in nodes], expected)
        self.assertEqual(linked._size, len(expected))
        self.assertIs(linked.head, nodes[0] if nodes else None)
        self.assertIs(linked.tail, nodes[-1] if nodes else None)
        backwards = []
        node = linked.tail
        for expected_node in reversed(nodes):
            self.assertIs(node, expected_node)
            backwards.append(node.value)
            node = node.prev
        self.assertIsNone(node)
        self.assertEqual(backwards, expected[::-1])

    def make_list(self, values):
        linked = SortedDoublyLinkedList()
        for value in values:
            linked.add(value)
        return linked

    def test_empty_queries_and_short_list_errors(self):
        linked = SortedDoublyLinkedList()
        self.check_list(linked, [])
        self.assertEqual(linked.total(), 0)
        self.assertEqual(linked.count(8), 0)
        self.assertFalse(linked.exists(8))
        self.assertFalse(linked.delete(8))
        with self.assertRaises(ValueError):
            linked.median()
        for value in (None, 3, 7):
            if value is not None:
                linked.add(value)
            with self.assertRaises(ValueError):
                linked.sum_middle_three()

    def test_sorted_insertion_with_duplicates_and_negatives(self):
        linked = self.make_list((8, -2, 4, 8, 0, -2, 5))
        self.check_list(linked, [-2, -2, 0, 4, 5, 8, 8])
        self.assertEqual(linked.count(-2), 2)
        self.assertEqual(linked.count(8), 2)
        self.assertEqual(linked.count(3), 0)
        self.assertTrue(linked.exists(5))
        self.assertFalse(linked.exists(-3))
        self.assertFalse(linked.exists(9))

    def test_delete_head_middle_tail_and_missing_value(self):
        linked = self.make_list((9, 3, 1, 5, 3))
        for value, expected in ((1, [3, 3, 5, 9]), (3, [3, 5, 9]), (9, [3, 5])):
            self.assertTrue(linked.delete(value))
            self.check_list(linked, expected)
        self.assertFalse(linked.delete(4))
        self.check_list(linked, [3, 5])

    def test_delete_only_node_then_reuse(self):
        linked = self.make_list((7,))
        self.assertTrue(linked.delete(7))
        self.check_list(linked, [])
        self.assertFalse(linked.delete(7))
        linked.add(2)
        linked.add(1)
        self.check_list(linked, [1, 2])

    def test_odd_middle_three_median_and_total(self):
        linked = self.make_list((10, 4, 29, 8, 2, 15, 41))
        self.assertEqual(linked.total(), 109)
        self.assertEqual(linked.sum_middle_three(), 33)
        self.assertEqual(linked.median(), 10)
        three = self.make_list((5, 1, 3))
        self.assertEqual(three.sum_middle_three(), 9)
        self.assertEqual(three.median(), 3)

    def test_even_middle_three_uses_left_middle_and_median(self):
        linked = self.make_list((10, 4, 29, 8, 2, 15))
        self.assertEqual(linked.total(), 68)
        self.assertEqual(linked.sum_middle_three(), 22)
        self.assertEqual(linked.median(), 9.0)
        four = self.make_list((10, 2, 8, 4))
        self.assertEqual(four.sum_middle_three(), 14)
        self.assertEqual(four.median(), 6.0)

    def test_operation_sequence_against_sorted_python_list(self):
        generator = random.Random(527)
        linked = SortedDoublyLinkedList()
        expected = []
        for _ in range(250):
            value = generator.randrange(-8, 9)
            if generator.random() < 0.55:
                linked.add(value)
                expected.append(value)
                expected.sort()
            else:
                found = value in expected
                self.assertEqual(linked.delete(value), found)
                if found:
                    expected.remove(value)
            self.check_list(linked, expected)
            self.assertEqual(linked.total(), sum(expected))
            for target in (-9, -3, 0, 4, 9):
                self.assertEqual(linked.exists(target), target in expected)
                self.assertEqual(linked.count(target), expected.count(target))
            if expected:
                middle = len(expected) // 2
                if len(expected) % 2:
                    median = expected[middle]
                else:
                    median = (expected[middle - 1] + expected[middle]) / 2
                self.assertEqual(linked.median(), median)


class StairsTests(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(ways(-2), 0)
        self.assertEqual(ways(-1), 0)
        self.assertEqual(ways(0), 1)

    def test_small_inputs_against_explicit_path_enumeration(self):
        for steps in range(1, 9):
            expected = sum(
                sum(path) == steps
                for length in range(1, steps + 1)
                for path in itertools.product((1, 2, 3), repeat=length)
            )
            with self.subTest(steps=steps):
                self.assertEqual(ways(steps), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
