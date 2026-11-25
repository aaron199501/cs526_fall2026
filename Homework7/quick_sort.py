"""Sort integers with iterative three-way quick sort."""

from input_utils import run_sort_cli


def quick_sort(values):
    """Return a sorted copy using the middle element as each pivot."""
    result = list(values)
    if len(result) < 2:
        return result

    # An explicit stack avoids Python's recursion-depth limit.
    pending = [(0, len(result) - 1)]
    while pending:
        low, high = pending.pop()
        while low < high:
            pivot = result[(low + high) // 2]
            less = low
            current = low
            greater = high

            # Maintain regions < pivot, == pivot, unknown, and > pivot.
            while current <= greater:
                if result[current] < pivot:
                    result[less], result[current] = result[current], result[less]
                    less += 1
                    current += 1
                elif result[current] > pivot:
                    result[current], result[greater] = result[greater], result[current]
                    greater -= 1
                else:
                    current += 1

            # Process the smaller side now; save the larger side for later.
            # The equal region is already in its final position.
            if less - low < high - greater:
                if greater + 1 < high:
                    pending.append((greater + 1, high))
                high = less - 1
            else:
                if low < less - 1:
                    pending.append((low, less - 1))
                low = greater + 1
    return result


if __name__ == "__main__":
    raise SystemExit(run_sort_cli(quick_sort, "Quick Sort"))
