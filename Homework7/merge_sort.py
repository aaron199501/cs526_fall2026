"""Sort integers by recursively splitting and merging sorted halves."""

from input_utils import run_sort_cli


def merge_sort(values):
    """Return a new list in increasing order; leave values unchanged."""
    if len(values) <= 1:
        return list(values)

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        # Taking the left value on ties also preserves stability.
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


if __name__ == "__main__":
    raise SystemExit(run_sort_cli(merge_sort, "Merge Sort"))
