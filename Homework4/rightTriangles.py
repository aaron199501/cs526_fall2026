"""Problem 3: count distinct right triangles using exact perpendicular slopes."""

import argparse
from fractions import Fraction
from math import gcd
from pathlib import Path


def read_points(path):
    tokens = Path(path).read_text(encoding="utf-8-sig").split()
    if not tokens:
        raise ValueError("expected a point count")
    n = int(tokens[0])
    if n < 0 or len(tokens) != 1 + 2 * n:
        raise ValueError("point count does not match the coordinate pairs")
    # One uniform scale preserves angles and avoids floating-point rounding.
    # Integer resource files take the direct, fast path.
    try:
        coordinates = [int(value) for value in tokens[1:]]
    except ValueError:
        exact = [Fraction(value) for value in tokens[1:]]
        scale = 1
        for value in exact:
            scale = scale // gcd(scale, value.denominator) * value.denominator
        coordinates = [value.numerator * (scale // value.denominator) for value in exact]
    points = list(zip(coordinates[::2], coordinates[1::2]))
    if len(set(points)) != n:
        raise ValueError("points must be distinct")
    return points


def count_right_triangles(points):
    """Count unordered triples of distinct integer-coordinate points.

    At each pivot, reduce vectors to unoriented slope keys. While visiting a
    new vector, count previously seen vectors perpendicular to it. Each pair
    is counted once, and each right triangle has exactly one right-angle pivot.
    """
    if len(set(points)) != len(points):
        raise ValueError("points must be distinct")
    answer = 0
    for px, py in points:
        seen = {}
        for qx, qy in points:
            dx, dy = qx - px, qy - py
            if dx == 0 and dy == 0:
                continue
            divisor = gcd(dx, dy)
            dx, dy = dx // divisor, dy // divisor
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            # Normalize the perpendicular to the same unoriented convention.
            rx, ry = -dy, dx
            if rx < 0 or (rx == 0 and ry < 0):
                rx, ry = -rx, -ry
            answer += seen.get((rx, ry), 0)
            key = (dx, dy)
            seen[key] = seen.get(key, 0) + 1
    return answer


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="file containing n and n coordinate pairs")
    args = parser.parse_args(argv)
    try:
        points = read_points(args.input_file)
        answer = count_right_triangles(points)
    except (OSError, ValueError, ZeroDivisionError) as error:
        parser.error(str(error))
    print(f"The number of right triangles is: {answer}")


if __name__ == "__main__":
    main()
