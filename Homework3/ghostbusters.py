"""Decide whether all paired, infinite proton streams avoid intersection."""

from math import gcd
import sys


def _normalized_line(bx, by, gx, gy):
    """Return a unique integer representation of A*x + B*y = C."""
    a = gy - by
    b = bx - gx
    divisor = gcd(a, b)
    if divisor == 0:
        raise ValueError("A Ghostbuster and its ghost must have distinct positions.")
    a //= divisor
    b //= divisor
    if a < 0 or (a == 0 and b < 0):
        a = -a
        b = -b
    return a, b, a * bx + b * by


def all_ghosts_eliminated(pairs):
    """Return True exactly when every stream is parallel and distinct.

    Each pair is (buster_x, buster_y, ghost_x, ghost_y). The assignment
    guarantees at least one pair and distinct positions within each pair.
    Integer arithmetic handles vertical streams and arbitrarily large
    coordinates without rounding. Each pair is processed once; a set stores
    the offsets of the parallel lines already seen.
    """
    direction = None
    offsets = set()
    for bx, by, gx, gy in pairs:
        a, b, c = _normalized_line(bx, by, gx, gy)
        if direction is None:
            direction = (a, b)
        elif direction != (a, b):
            # Any two nonparallel infinite lines meet somewhere.
            return False
        if c in offsets:
            # Equal normalized direction and offset mean coincident lines.
            return False
        offsets.add(c)
    return True


def read_pairs(stream):
    """Read the teacher's B x y G x y format from a text stream."""
    n = int(stream.readline())
    if n < 1:
        raise ValueError("There must be at least one Ghostbuster.")
    pairs = []
    for _ in range(n):
        fields = stream.readline().split()
        if len(fields) != 6 or fields[0] != "B" or fields[3] != "G":
            raise ValueError("Each pair must use the format B x y G x y.")
        pairs.append(tuple(map(int, (fields[1], fields[2], fields[4], fields[5]))))
    return pairs


def main():
    pairs = read_pairs(sys.stdin)
    if all_ghosts_eliminated(pairs):
        print("All Ghosts: were eliminated")
    else:
        print("All Ghosts: were not eliminated")


if __name__ == "__main__":
    main()
