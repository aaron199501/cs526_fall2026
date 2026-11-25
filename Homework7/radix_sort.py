"""Sort non-negative integers with base-10 LSD radix sort."""

from input_utils import run_sort_cli


def _counting_pass(values, place):
    """Stably sort one decimal digit using a hand-written counting sort."""
    counts = [0] * 10
    for value in values:
        digit = (value // place) % 10
        counts[digit] += 1

    # Each accumulated count is the end position of its digit's bucket.
    for digit in range(1, 10):
        counts[digit] += counts[digit - 1]

    output = [0] * len(values)
    # Right-to-left placement preserves the order of equal digit keys.
    for i in range(len(values) - 1, -1, -1):
        digit = (values[i] // place) % 10
        counts[digit] -= 1
        output[counts[digit]] = values[i]
    return output


def radix_sort(values):
    """Return a new list sorted from least to most significant digit."""
    result = list(values)
    maximum = 0
    for value in result:
        if value < 0:
            raise ValueError("Radix Sort requires non-negative integers.")
        if value > maximum:
            maximum = value

    place = 1
    while place <= maximum:
        result = _counting_pass(result, place)
        place *= 10
    return result


if __name__ == "__main__":
    raise SystemExit(run_sort_cli(radix_sort, "LSD Radix Sort (base 10)", non_negative=True))
