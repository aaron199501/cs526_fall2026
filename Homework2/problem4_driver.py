"""Read numeric directives for the sorted doubly linked list."""
import math
import sys

from problem4 import SortedDoublyLinkedList


SYNTAX = {
    "add": "add <value>",
    "delete": "delete <value>",
    "exists": "exists <value>",
    "count": "count <value>",
    "print_list": "print_list",
    "total": "total",
    "sum_middle_three": "sum_middle_three",
    "median": "median",
}
VALUE_COMMANDS = {"add", "delete", "exists", "count"}


def parse_value(text):
    try:
        return int(text)
    except ValueError:
        value = float(text)
        if not math.isfinite(value):
            raise ValueError("value must be finite")
        return value


def main():
    linked_list = SortedDoublyLinkedList()
    for line_number, raw_line in enumerate(sys.stdin, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        directive, *args = line.split()
        command = directive.lower()
        prefix = f"line {line_number}: "
        if command not in SYNTAX:
            print(f"{prefix}unknown directive '{directive}'")
            continue
        expected_count = 1 if command in VALUE_COMMANDS else 0
        if len(args) != expected_count:
            print(f"{prefix}expected '{SYNTAX[command]}', got '{line}'")
            continue
        if command in VALUE_COMMANDS:
            try:
                value = parse_value(args[0])
            except ValueError:
                print(f"{prefix}value must be a number, got '{line}'")
                continue
        if command == "add":
            linked_list.add(value)
            print(f"add({value})")
        elif command == "delete":
            if linked_list.delete(value):
                print(f"delete({value})")
            else:
                print(f"{prefix}{value} not found, nothing deleted")
        elif command == "exists":
            print(f"exists({value}) = {linked_list.exists(value)}")
        elif command == "count":
            print(f"count({value}) = {linked_list.count(value)}")
        elif command == "print_list":
            linked_list.print_list()
        elif command == "total":
            print(f"total = {linked_list.total()}")
        elif command == "median":
            try:
                print(f"median = {linked_list.median()}")
            except ValueError:
                print(f"{prefix}median of an empty list")
        elif command == "sum_middle_three":
            try:
                print(f"sum_middle_three = {linked_list.sum_middle_three()}")
            except ValueError:
                print(f"{prefix}sum_middle_three needs at least 3 nodes")
    print("Final list: ", end="")
    linked_list.print_list()


if __name__ == "__main__":
    main()
