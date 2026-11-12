"""Problem 2: a binary min-heap stored entirely as linked tree nodes."""

import argparse
import ast
import sys


class Node:
    """A heap value and the links needed to navigate the complete tree."""

    __slots__ = ("value", "left", "right", "parent")

    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent


class BinaryMinHeap:
    """A complete linked binary tree with the smallest value at its root.

    Only root and size are stored on the heap. Lists used for input, returned
    results, or drawing characters are not an array representation of the heap.
    Values must support consistent comparisons with one another.
    """

    def __init__(self, values=None):
        self.root = None
        self.size = 0
        if values is not None:
            self.build(values)

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _node_at(self, position):
        """Follow the bits after the leading 1 in a one-based position."""
        if position < 1 or position > self.size:
            raise IndexError("heap position out of range")
        node = self.root
        bit = 1 << (position.bit_length() - 2) if position > 1 else 0
        while bit:
            node = node.right if position & bit else node.left
            bit >>= 1
        return node

    @staticmethod
    def _sift_up(node):
        # Equality does not move an inserted value above its parent.
        while node.parent is not None and node.value < node.parent.value:
            node.value, node.parent.value = node.parent.value, node.value
            node = node.parent

    @staticmethod
    def _sift_down(node):
        while node.left is not None:
            smaller = node.left
            if node.right is not None and node.right.value < smaller.value:
                smaller = node.right
            if not smaller.value < node.value:
                break
            node.value, smaller.value = smaller.value, node.value
            node = smaller

    def insert(self, value):
        """Add value in O(log n) time, preserving order and complete shape."""
        position = self.size + 1
        if self.root is None:
            self.root = Node(value)
            self.size = 1
            return
        parent = self._node_at(position // 2)
        node = Node(value, parent)
        if position & 1:
            parent.right = node
        else:
            parent.left = node
        self.size += 1
        self._sift_up(node)

    def peek(self):
        """Return the smallest value without changing the heap."""
        if self.root is None:
            raise IndexError("peek from an empty heap")
        return self.root.value

    def _detach_last(self):
        last = self._node_at(self.size)
        if last.parent is None:
            self.root = None
        elif last.parent.right is last:
            last.parent.right = None
        else:
            last.parent.left = None
        last.parent = None
        self.size -= 1
        return last

    def extract_min(self):
        """Remove and return the smallest value in O(log n) time."""
        if self.root is None:
            raise IndexError("extract_min from an empty heap")
        minimum = self.root.value
        last = self._detach_last()
        if self.root is not None:
            self.root.value = last.value
            self._sift_down(self.root)
        return minimum

    @staticmethod
    def _find(node, value):
        if node is None:
            return None
        if node.value == value:
            return node
        found = BinaryMinHeap._find(node.left, value)
        return found if found is not None else BinaryMinHeap._find(node.right, value)

    def delete(self, value):
        """Remove one matching value, returning whether it was present.

        Finding an arbitrary value takes O(n) worst-case time. Once found,
        removal and heap-order repair take O(log n) time.
        """
        node = self._find(self.root, value)
        if node is None:
            return False
        last = self._detach_last()
        if node is not last:
            node.value = last.value
            if node.parent is not None and node.value < node.parent.value:
                self._sift_up(node)
            else:
                self._sift_down(node)
        return True

    def build(self, values):
        """Replace the heap with a complete heap of values in O(n) time.

        The input sequence supplies values, not node storage. Children are
        built first; sifting down each parent gives bottom-up heap building.
        No array or list of heap nodes is created or kept.
        """
        values = list(values)
        count = len(values)

        def create(position, parent):
            if position > count:
                return None
            node = Node(values[position - 1], parent)
            node.left = create(position * 2, node)
            node.right = create(position * 2 + 1, node)
            self._sift_down(node)
            return node

        new_root = create(1, None)
        self.root = new_root
        self.size = count

    def heap_sort(self):
        """Return increasing values while preserving this exact linked tree."""
        def clone(node, parent):
            if node is None:
                return None
            copied = Node(node.value, parent)
            copied.left = clone(node.left, copied)
            copied.right = clone(node.right, copied)
            return copied

        copied_heap = BinaryMinHeap()
        copied_heap.root = clone(self.root, None)
        copied_heap.size = self.size
        result = []
        while not copied_heap.is_empty():
            result.append(copied_heap.extract_min())
        return result

    def print_heap(self):
        """Draw the actual tree with the root above its linked children."""
        if self.root is None:
            print("(empty heap)")
            return

        def label_width(node):
            if node is None:
                return 0
            return max(len(str(node.value)), label_width(node.left), label_width(node.right))

        height = self.size.bit_length()
        cell = label_width(self.root) + 1
        width = (1 << height) * cell + 1
        # This grid stores drawing characters only; the heap remains linked.
        lines = [[" "] * width for _ in range(height * 2 - 1)]

        def column(position):
            depth = position.bit_length() - 1
            offset = position - (1 << depth)
            return (offset * 2 + 1) * (1 << (height - depth - 1)) * cell

        def draw(node, position):
            if node is None:
                return
            depth = position.bit_length() - 1
            center = column(position)
            label = str(node.value)
            start = center - len(label) // 2
            lines[depth * 2][start:start + len(label)] = label
            if node.left is not None:
                child = position * 2
                lines[depth * 2 + 1][(center + column(child)) // 2] = "/"
                draw(node.left, child)
            if node.right is not None:
                child = position * 2 + 1
                lines[depth * 2 + 1][(center + column(child)) // 2] = "\\"
                draw(node.right, child)

        draw(self.root, 1)
        for line in lines:
            print("".join(line).rstrip())


def read_values(text):
    """Read the integer-list syntax used by the supplied input files."""
    try:
        values = ast.literal_eval(text.lstrip("\ufeff").strip())
    except (SyntaxError, ValueError) as error:
        raise ValueError("input must be a list of integers, such as [8, 3, 5, 1]") from error
    if not isinstance(values, list) or any(type(value) is not int for value in values):
        raise ValueError("input must be a list of integers")
    return values


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="optional input file; otherwise read standard input")
    args = parser.parse_args(argv)
    try:
        if args.input_file:
            with open(args.input_file, encoding="utf-8-sig") as source:
                values = read_values(source.read())
        else:
            values = read_values(sys.stdin.read())
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("Input values:", values)
    heap = BinaryMinHeap()
    for value in values:
        heap.insert(value)
        print("\nAfter insert({}):".format(value))
        heap.print_heap()


if __name__ == "__main__":
    main()
