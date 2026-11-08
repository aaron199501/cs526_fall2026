"""Count the vowel-only decodings of an unseparated Morse-code sequence.

Usage: python vowelCombinations.py inputs/vowel_input1.txt
The input contains its declared length followed by the dot/dash sequence.
"""

import argparse
from pathlib import Path
from typing import Union


VOWEL_CODES = (".-", ".", "..", "---", "..-")  # A, E, I, O, U


def count_vowel_combinations(sequence: str) -> int:
    """Return the number of vowel sequences encoding exactly ``sequence``.

    ways[i] counts the decodings of the first i symbols. The empty prefix has
    one decoding (the empty sequence), so the empty input also returns one.
    """
    if any(symbol not in ".-" for symbol in sequence):
        raise ValueError("the Morse sequence may contain only '.' and '-'")

    ways = [0] * (len(sequence) + 1)
    ways[0] = 1
    for end in range(1, len(sequence) + 1):
        for code in VOWEL_CODES:
            start = end - len(code)
            if start >= 0 and sequence.startswith(code, start, end):
                ways[end] += ways[start]
    return ways[-1]


def read_input(filename: Union[str, Path]) -> str:
    """Read a declared nonnegative length and one dot/dash line.

    A UTF-8 BOM, surrounding line whitespace, and blank trailing lines are
    accepted. A zero-length input may omit the empty second line.
    """
    lines = Path(filename).read_text(encoding="utf-8-sig").splitlines()
    if not lines:
        raise ValueError("the input file is empty")
    try:
        declared_length = int(lines[0].strip())
    except ValueError as error:
        raise ValueError("the first line must be a nonnegative integer length") from error
    if declared_length < 0:
        raise ValueError("the declared length cannot be negative")
    if len(lines) < 2 and declared_length != 0:
        raise ValueError("the second line must contain the Morse sequence")
    if any(line.strip() for line in lines[2:]):
        raise ValueError("expected one Morse sequence line after the length")

    sequence = lines[1].strip() if len(lines) >= 2 else ""
    if any(symbol not in ".-" for symbol in sequence):
        raise ValueError("the Morse sequence may contain only '.' and '-'")
    if len(sequence) != declared_length:
        raise ValueError(
            "declared length {} does not match {} Morse symbols".format(
                declared_length, len(sequence)
            )
        )
    return sequence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=Path, help="file with length and Morse sequence")
    args = parser.parse_args()
    try:
        sequence = read_input(args.input_file)
        count = count_vowel_combinations(sequence)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))

    print("File Input: {}".format(args.input_file.name))
    print("The Number of Vowel combinations is:")
    print("    {}".format(count))


if __name__ == "__main__":
    main()
