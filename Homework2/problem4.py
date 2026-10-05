class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class SortedDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def add(self, value):
        new_node = Node(value)

        # Empty list
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._size += 1
            return

        # Insert at the beginning
        if value <= self.head.value:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self._size += 1
            return

        # Insert at the end
        if value >= self.tail.value:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self._size += 1
            return

        # Insert somewhere in the middle
        current = self.head.next

        while current is not None and current.value <= value:
            current = current.next

        previous = current.prev

        new_node.prev = previous
        new_node.next = current

        previous.next = new_node
        current.prev = new_node

        self._size += 1

    def delete(self, value):
        current = self.head

        # Because the list is sorted,
        # we can stop once values become greater than value.
        while current is not None and current.value < value:
            current = current.next

        if current is None or current.value != value:
            return False

        # Removing the head
        if current.prev is None:
            self.head = current.next
        else:
            current.prev.next = current.next

        # Removing the tail
        if current.next is None:
            self.tail = current.prev
        else:
            current.next.prev = current.prev

        self._size -= 1

        return True

    def exists(self, value):
        def helper(node):
            if node is None:
                return False

            if node.value == value:
                return True

            # Since the list is sorted,
            # no need to keep searching.
            if node.value > value:
                return False

            return helper(node.next)

        return helper(self.head)

    def print_list(self):
        if self.head is None:
            print("(empty)")
            return

        def helper(node):
            print(node.value, end="")

            if node.next is not None:
                print(" <-> ", end="")
                helper(node.next)

        helper(self.head)
        print()

    def total(self):
        def helper(node):
            if node is None:
                return 0

            return node.value + helper(node.next)

        return helper(self.head)

    def _node_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        # Search from the closer side
        if index <= self._size // 2:
            current = self.head

            for _ in range(index):
                current = current.next
        else:
            current = self.tail

            for _ in range(self._size - 1 - index):
                current = current.prev

        return current

    def sum_middle_three(self):
        if self._size < 3:
            raise ValueError("List must contain at least 3 nodes")

        mid = self._size // 2

        if self._size % 2 == 1:
            first = self._node_at(mid - 1)
            second = self._node_at(mid)
            third = self._node_at(mid + 1)

        else:
            first = self._node_at(mid - 2)
            second = self._node_at(mid - 1)
            third = self._node_at(mid)

        return first.value + second.value + third.value

    def median(self):
        if self._size == 0:
            raise ValueError("Cannot find median of an empty list")

        mid = self._size // 2

        if self._size % 2 == 1:
            return self._node_at(mid).value

        left = self._node_at(mid - 1).value
        right = self._node_at(mid).value

        return (left + right) / 2

    def count(self, value):
        def helper(node):
            if node is None:
                return 0

            # Because the list is sorted,
            # stop when node.value is greater than value.
            if node.value > value:
                return 0

            if node.value == value:
                return 1 + helper(node.next)

            return helper(node.next)

        return helper(self.head)


# Driver program
if __name__ == "__main__":
    linked_list = SortedDoublyLinkedList()

    print("Adding: 10, 4, 29, 8, 2, 15, 41")

    linked_list.add(10)
    linked_list.add(4)
    linked_list.add(29)
    linked_list.add(8)
    linked_list.add(2)
    linked_list.add(15)
    linked_list.add(41)

    print("print_list(): ", end="")
    linked_list.print_list()

    print("total():", linked_list.total())
    print("sum_middle_three():", linked_list.sum_middle_three())
    print("median():", linked_list.median())

    print("\ndelete(41):", linked_list.delete(41))

    print("print_list(): ", end="")
    linked_list.print_list()

    print("total():", linked_list.total())
    print("sum_middle_three():", linked_list.sum_middle_three())
    print("median():", linked_list.median())

    print("\nadd(8)")
    linked_list.add(8)

    print("print_list(): ", end="")
    linked_list.print_list()

    print("count(8):", linked_list.count(8))
    print("count(5):", linked_list.count(5))
    print("exists(15):", linked_list.exists(15))
    print("exists(5):", linked_list.exists(5))