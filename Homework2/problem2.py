class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1
    
    def prepend(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node

        else:
            new_node.next = self.head
            self.head = new_node

        self._size +=1

    def insert(self, index, value):
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(value)
            return

        if index == self._size:
            self.append(value)
            return

        new_node = Node(value)
        previous = self.head

        for _ in range(index - 1):
            previous = previous.next

        new_node.next = previous.next
        previous.next = new_node

        self._size += 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        return current.value

    def find(self, value):
        current = self.head
        index = 0

        while current is not None:
            if current.value == value:
                return index

            current = current.next
            index +=1

        return -1

    def update(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        current.value = value

    def delete(self, value):
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1

            if self._size == 0:
                self.tail = None

            return True

        previous = self.head
        current = self.head.next

        while current is not None:
            if current.value == value:
                previous.next = current.next

                if current is self.tail:
                    self.tail = previous

                self._size -= 1
                return True

            previous = current
            current = current.next

        return False

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        if index == 0:
            value = self.head.value
            self.head = self.head.next
            self._size -= 1

            if self._size == 0:
                self.tail = None

            return value

        previous = self.head

        for _ in range(index - 1):
            previous = previous.next

        current = previous.next
        value = current.value

        previous.next = current.next

        if current is self.tail:
            self.tail = previous

        self._size -= 1

        return value

    def print_list(self):
        if self.head is None:
            print("(empty)")
            return

        current = self.head
        values = []

        while current is not None:
            values.append(str(current.value))
            current = current.next

        print(" -> ".join(values))