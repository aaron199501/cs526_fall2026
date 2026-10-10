"""Recursive staircase counts and the teacher's ordered example paths."""
import argparse


def ways(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return ways(n - 1) + ways(n - 2) + ways(n - 3)


def combinations(n, prefix=()):
    """Yield valid paths recursively, trying 1, 2, and 3 in that order."""
    if n < 0:
        return
    if n == 0:
        yield prefix
        return
    yield from combinations(n - 1, prefix + (1,))
    yield from combinations(n - 2, prefix + (2,))
    yield from combinations(n - 3, prefix + (3,))


def print_example(steps, count_only=False):
    if count_only:
        print(f"Step Combinations for an input of {steps} steps:  {ways(steps)} ")
        return
    print(f"Step Combinations for an input of {steps} steps: ")
    for path in combinations(steps):
        print("+".join(map(str, path)))
    print(f"Total Step Combinations:  {ways(steps)} ")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--steps", type=int, help="show the paths for this many steps")
    selection.add_argument("--teacher-examples", action="store_true", help="show all four teacher examples")
    parser.add_argument("--count-only", action="store_true", help="show only the count with --steps")
    args = parser.parse_args(argv)
    if args.count_only and args.steps is None:
        parser.error("--count-only requires --steps")
    if args.steps is not None and args.steps < 0:
        parser.error("--steps must be non-negative")
    if args.teacher_examples:
        for steps in (3, 4, 7):
            print_example(steps)
            print()
        print_example(10, count_only=True)
        print()
    elif args.steps is not None:
        print_example(args.steps, args.count_only)
    else:
        # Retain the demonstration specifically requested in Homework2.pdf.
        print("ways(3) =", ways(3))
        print("ways(5) =", ways(5))
        print("ways(10) =", ways(10))


if __name__ == "__main__":
    main()
