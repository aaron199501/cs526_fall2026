"""Sort integers by inserting each value into a sorted prefix."""

from input_utils import run_sort_cli


def insertion_sort(values):
    """Return a new sorted list without changing the input list."""
    result = list(values)
    for i in range(1, len(result)):
        value = result[i]
        j = i - 1
        while j >= 0 and result[j] > value:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = value
    return result


if __name__ == "__main__":
    raise SystemExit(run_sort_cli(insertion_sort, "Insertion Sort"))
