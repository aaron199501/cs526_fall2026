"""Problem 3: reverse three stack implementations in place with recursion.

Each stack's ``to_list`` returns the values from bottom to top.  Linked
stacks keep their top node in ``head``; ``next`` points toward the bottom.
The reversal functions preserve both the stack object and its storage.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar


T = TypeVar("T")


class ArrayStack(Generic[T]):
    """An array stack whose last element is the top."""

    def __init__(self) -> None:
        self.items: List[T] = []

    @property
    def size(self) -> int:
        return len(self.items)

    def __len__(self) -> int:
        return self.size

    def push(self, value: T) -> None:
        self.items.append(value)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self.items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self.items[-1]

    def is_empty(self) -> bool:
        return not self.items

    def to_list(self) -> List[T]:
        return self.items.copy()

    def reverse(self) -> None:
        reverse_array_stack(self)


@dataclass(eq=False)
class SinglyNode(Generic[T]):
    value: T
    next: Optional[SinglyNode[T]] = None


class SinglyLinkedStack(Generic[T]):
    """A singly linked stack with its head node at the top."""

    def __init__(self) -> None:
        self.head: Optional[SinglyNode[T]] = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self.size

    def push(self, value: T) -> None:
        self.head = SinglyNode(value, self.head)
        self._size += 1

    def pop(self) -> T:
        if self.head is None:
            raise IndexError("pop from an empty stack")
        node = self.head
        self.head = node.next
        node.next = None
        self._size -= 1
        return node.value

    def peek(self) -> T:
        if self.head is None:
            raise IndexError("peek at an empty stack")
        return self.head.value

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[T]:
        values: List[T] = []
        node = self.head
        while node is not None:
            values.append(node.value)
            node = node.next
        values.reverse()
        return values

    def reverse(self) -> None:
        reverse_singly_linked_stack(self)


@dataclass(eq=False)
class DoublyNode(Generic[T]):
    value: T
    next: Optional[DoublyNode[T]] = None
    prev: Optional[DoublyNode[T]] = None


class DoublyLinkedStack(Generic[T]):
    """A doubly linked stack: head is top, tail is bottom.

    ``next`` points down the stack and ``prev`` points up the stack.
    """

    def __init__(self) -> None:
        self.head: Optional[DoublyNode[T]] = None
        self.tail: Optional[DoublyNode[T]] = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self.size

    def push(self, value: T) -> None:
        node = DoublyNode(value, next=self.head)
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self._size += 1

    def pop(self) -> T:
        if self.head is None:
            raise IndexError("pop from an empty stack")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        node.next = None
        node.prev = None
        self._size -= 1
        return node.value

    def peek(self) -> T:
        if self.head is None:
            raise IndexError("peek at an empty stack")
        return self.head.value

    def is_empty(self) -> bool:
        return self.head is None

    def to_list(self) -> List[T]:
        values: List[T] = []
        node = self.tail
        while node is not None:
            values.append(node.value)
            node = node.prev
        return values

    def reverse(self) -> None:
        reverse_doubly_linked_stack(self)


def _reverse_array(items: List[T], left: int, right: int) -> None:
    """Swap one outside pair, then recursively reverse the inside."""
    if left >= right:
        return
    items[left], items[right] = items[right], items[left]
    _reverse_array(items, left + 1, right - 1)


def reverse_array_stack(stack: ArrayStack[T]) -> None:
    _reverse_array(stack.items, 0, stack.size - 1)


def _reverse_singly_nodes(
    node: Optional[SinglyNode[T]],
) -> Optional[SinglyNode[T]]:
    """Reverse the suffix, then make the old next node point back."""
    if node is None or node.next is None:
        return node
    next_node = node.next
    new_head = _reverse_singly_nodes(next_node)
    next_node.next = node
    node.next = None
    return new_head


def reverse_singly_linked_stack(stack: SinglyLinkedStack[T]) -> None:
    stack.head = _reverse_singly_nodes(stack.head)


def _reverse_doubly_nodes(node: Optional[DoublyNode[T]]) -> None:
    """Swap each node's links, recursing along the original next link."""
    if node is None:
        return
    original_next = node.next
    node.next, node.prev = node.prev, node.next
    _reverse_doubly_nodes(original_next)


def reverse_doubly_linked_stack(stack: DoublyLinkedStack[T]) -> None:
    _reverse_doubly_nodes(stack.head)
    stack.head, stack.tail = stack.tail, stack.head


def main() -> None:
    implementations = (
        ("Array stack:", ArrayStack),
        ("Singly linked stack:", SinglyLinkedStack),
        ("Doubly linked stack:", DoublyLinkedStack),
    )
    for heading, stack_type in implementations:
        stack = stack_type()
        for value in range(1, 11):
            stack.push(value)
        print(heading)
        print("Before:  " + ", ".join(map(str, stack.to_list())))
        stack.reverse()
        print("After:   " + ", ".join(map(str, stack.to_list())))


if __name__ == "__main__":
    main()
