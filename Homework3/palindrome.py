"""Read strings from standard input and report case-sensitive palindromes."""

import sys


def is_palindrome(text: str) -> bool:
    """Ignore literal separator spaces and compare the remaining characters."""
    characters = text.replace(" ", "")
    return characters == characters[::-1]


def main() -> None:
    """Print one Boolean per input line, followed by the palindrome count."""
    count = 0
    for line in sys.stdin:
        result = is_palindrome(line.rstrip("\r\n"))
        print(result)
        if result:
            count += 1
    print(count)


if __name__ == "__main__":
    main()
