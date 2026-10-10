"""Read singly linked-list directives and report recoverable input errors."""
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


SYNTAX = {
    "append": "append <value>",
    "prepend": "prepend <value>",
    "insert": "insert <index> <value>",
    "get": "get <index>",
    "find": "find <value>",
    "len": "len",
    "update": "update <index> <value>",
    "delete": "delete <value>",
    "delete_at": "delete_at <index>",
    "print_list": "print_list",
}
ARG_COUNTS = {
    "append": 1, "prepend": 1, "insert": 2, "get": 1,
    "find": 1, "len": 0, "update": 2, "delete": 1,
    "delete_at": 1, "print_list": 0,
}


def main():
    linked_list = SinglyLinkedList()
    for line_number, raw_line in enumerate(sys.stdin, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        command, *args = line.split()
        prefix = f"line {line_number}: "
        if command not in SYNTAX:
            print(f"{prefix}unknown directive '{command}'")
            continue
        if len(args) != ARG_COUNTS[command]:
            print(f"{prefix}expected '{SYNTAX[command]}', got '{line}'")
            continue
        if command in ("insert", "get", "update", "delete_at"):
            try:
                index = int(args[0])
            except ValueError:
                print(f"{prefix}index must be a whole number, got '{line}'")
                continue
        try:
            if command == "append":
                linked_list.append(parse_value(args[0]))
            elif command == "prepend":
                linked_list.prepend(parse_value(args[0]))
            elif command == "insert":
                linked_list.insert(index, parse_value(args[1]))
            elif command == "get":
                print(f"get({index}) = {linked_list.get(index)}")
            elif command == "find":
                value = parse_value(args[0])
                print(f"find({value}) = {linked_list.find(value)}")
            elif command == "len":
                print(f"len = {len(linked_list)}")
            elif command == "update":
                linked_list.update(index, parse_value(args[1]))
            elif command == "delete":
                value = parse_value(args[0])
                if not linked_list.delete(value):
                    print(f"{prefix}{value} not found, nothing deleted")
            elif command == "delete_at":
                print(f"delete_at({index}) = {linked_list.delete_at(index)}")
            elif command == "print_list":
                linked_list.print_list()
        except IndexError:
            print(f"{prefix}index {index} out of range")
    print("Final list: ", end="")
    linked_list.print_list()


if __name__ == "__main__":
    main()
