import sys
from problem2 import SinglyLinkedList


def parse_value(text):
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text


def main():
    linked_list = SinglyLinkedList()

    for line in sys.stdin:
        line = line.strip()

        # Ignore blank lines and comments
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        command = parts[0]
        args = parts[1:]

        try:
            if command == "append":
                if len(args) != 1:
                    raise ValueError

                value = parse_value(args[0])
                linked_list.append(value)

            elif command == "prepend":
                if len(args) != 1:
                    raise ValueError

                value = parse_value(args[0])
                linked_list.prepend(value)

            elif command == "insert":
                if len(args) != 2:
                    raise ValueError

                index = int(args[0])
                value = parse_value(args[1])

                linked_list.insert(index, value)

            elif command == "get":
                if len(args) != 1:
                    raise ValueError

                index = int(args[0])
                value = linked_list.get(index)

                print(f"get({index}) = {value}")

            elif command == "find":
                if len(args) != 1:
                    raise ValueError

                value = parse_value(args[0])
                position = linked_list.find(value)

                print(f"find({value}) = {position}")

            elif command == "len":
                if len(args) != 0:
                    raise ValueError

                print(len(linked_list))

            elif command == "update":
                if len(args) != 2:
                    raise ValueError

                index = int(args[0])
                value = parse_value(args[1])

                linked_list.update(index, value)

            elif command == "delete":
                if len(args) != 1:
                    raise ValueError

                value = parse_value(args[0])

                if not linked_list.delete(value):
                    print(f"Warning: value {value} not found")

            elif command == "delete_at":
                if len(args) != 1:
                    raise ValueError

                index = int(args[0])
                value = linked_list.delete_at(index)

                print(f"delete_at({index}) = {value}")

            elif command == "print_list":
                if len(args) != 0:
                    raise ValueError

                linked_list.print_list()

            else:
                print(f"Warning: unknown directive '{command}'")

        except ValueError:
            print(f"Warning: invalid arguments in line: {line}")

        except IndexError:
            print(f"Warning: index out of range in line: {line}")

    print("Final list: ", end="")
    linked_list.print_list()


if __name__ == "__main__":
    main()