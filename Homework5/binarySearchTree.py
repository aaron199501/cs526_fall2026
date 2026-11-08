"""Problem 1: an unbalanced binary search tree and a random demonstration.

The tree stores distinct integers. Adding an existing value or deleting a
missing value returns False and leaves the tree unchanged.
"""

import argparse
from dataclasses import dataclass
import random
from typing import List, Optional


@dataclass
class Node:
    """A node holds one value and references to its two child nodes."""

    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


class BST:
    """A binary search tree with smaller values left and larger values right."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def addNode(self, value: int) -> bool:
        """Insert a new value; return whether a node was added."""
        if self.root is None:
            self.root = Node(value)
            self._size += 1
            return True
        current = self.root
        while True:
            if value == current.value:
                return False
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    break
                current = current.right
        self._size += 1
        return True

    def findNode(self, value: int) -> Optional[Node]:
        """Return the matching node, or None if the value is absent."""
        current = self.root
        while current is not None:
            if value == current.value:
                return current
            current = current.left if value < current.value else current.right
        return None

    def deleteNode(self, value: int) -> bool:
        """Remove a value, preserving the BST ordering invariant."""
        parent = None
        current = self.root
        while current is not None and current.value != value:
            parent = current
            current = current.left if value < current.value else current.right
        if current is None:
            return False

        if current.left is not None and current.right is not None:
            # Replace the value by its inorder successor, then remove that node.
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.value = successor.value
            parent, current = successor_parent, successor

        child = current.left if current.left is not None else current.right
        if parent is None:
            self.root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
        return True

    def inorder(self) -> List[int]:
        """Return values in sorted order without changing the tree."""
        values = []
        stack = []
        current = self.root
        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            values.append(current.value)
            current = current.right
        return values

    def treeLines(self) -> List[str]:
        """Return a preorder drawing with explicit ROOT, L and R labels."""
        if self.root is None:
            return ["(empty tree)"]
        lines = []
        pending = [(self.root, 0, "ROOT")]
        while pending:
            node, depth, label = pending.pop()
            lines.append("  " * depth + "{}: {}".format(label, node.value))
            if node.right is not None:
                pending.append((node.right, depth + 1, "R"))
            if node.left is not None:
                pending.append((node.left, depth + 1, "L"))
        return lines

    def printTree(self) -> None:
        """Print the tree; indentation represents depth, L/R identify edges."""
        for line in self.treeLines():
            print(line)


def demo(size: int, seed: Optional[int] = None) -> None:
    """Run reproducible random operations when a seed is supplied."""
    if not 5 <= size <= 50:
        raise ValueError("input size must be between 5 and 50")
    rng = random.Random(seed)
    values = rng.sample(range(1, 1001), size)
    tree = BST()
    for value in values:
        tree.addNode(value)

    print("Problem 1: Binary Search Tree")
    if seed is not None:
        print("Random seed:", seed)
    print("Input set (in insertion order):", values)
    print("Initial tree (indentation = depth; L/R = left/right child):")
    tree.printTree()

    for _ in range(2):
        value = rng.randint(1, 1000)
        while tree.findNode(value) is not None:
            value = rng.randint(1, 1000)
        added = tree.addNode(value)
        print("\nAdd Node({}): {}".format(value, "added" if added else "already present"))
        tree.printTree()

    for value in rng.sample(values, 2):
        deleted = tree.deleteNode(value)
        print("\nDelete Node({}): {}".format(value, "deleted" if deleted else "not found"))
        tree.printTree()

    # Rejection sampling keeps every query random and in 1..1000, while ensuring
    # that the demonstration includes one successful and one failed search.
    for should_find in (True, False):
        value = rng.randint(1, 1000)
        node = tree.findNode(value)
        while (node is not None) != should_find:
            value = rng.randint(1, 1000)
            node = tree.findNode(value)
        print("\nFindNode({}): {}".format(value, "found" if node is not None else "not found"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, help="random input size, from 5 to 50")
    parser.add_argument("--seed", type=int, help="optional seed for repeatable output")
    args = parser.parse_args()
    if args.size is not None and not 5 <= args.size <= 50:
        parser.error("--size must be between 5 and 50")
    size = args.size if args.size is not None else random.Random(args.seed).randint(5, 50)
    demo(size, args.seed)


if __name__ == "__main__":
    main()
