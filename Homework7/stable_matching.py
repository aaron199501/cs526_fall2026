"""Find the men-optimal stable matching with men proposing."""

import argparse
from collections import deque
from dataclasses import dataclass
from pathlib import Path
import re
import sys


@dataclass(frozen=True)
class PreferenceInstance:
    """Names in input order, indexed men's lists, and women's rank tables."""

    men: list[str]
    women: list[str]
    male_preferences: list[list[int]]
    female_rankings: list[list[int]]


def _preference_indices(line, owner, opposite_indices):
    """Validate one complete preference list and replace names with indexes."""
    tokens = line.split()
    count = len(opposite_indices)
    preferences = tokens[1:]
    if len(preferences) != count:
        raise ValueError(
            f"{owner!r} must rank exactly {count} people; "
            f"found {len(preferences)}."
        )

    seen = set()
    result = []
    for name in preferences:
        if name not in opposite_indices:
            raise ValueError(
                f"{owner!r} lists {name!r}, who is not in the opposite group."
            )
        if name in seen:
            raise ValueError(f"{owner!r} lists {name!r} more than once.")
        seen.add(name)
        result.append(opposite_indices[name])
    return result


def parse_preferences(text, allow_shared_names=False):
    """Parse and validate the assignment's text format; raise ValueError on error."""
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("The file is empty; the first non-blank line must be n.")
    count_text = lines[0].strip()
    if re.fullmatch(r"[+-]?\d+", count_text) is None:
        raise ValueError("The first non-blank line must be a positive integer n written without separators.")
    try:
        count = int(count_text)
    except ValueError:
        raise ValueError("The first non-blank line must be a positive integer n.") from None
    if count <= 0:
        raise ValueError("The first non-blank line must be a positive integer n.")
    if len(lines) - 1 != 2 * count:
        raise ValueError(
            f"Expected exactly {2 * count} person lines after n = {count}; "
            f"found {len(lines) - 1}."
        )

    names = []
    male_names = set()
    female_names = set()
    for index, line in enumerate(lines[1:]):
        name = line.split(maxsplit=1)[0]
        group_names = male_names if index < count else female_names
        if name in group_names:
            raise ValueError(f"Person name {name!r} appears more than once in the same group.")
        if not allow_shared_names and index >= count and name in male_names:
            raise ValueError(
                f"Person name {name!r} appears in both groups; "
                "the default format requires globally unique names."
            )
        group_names.add(name)
        names.append(name)
    men, women = names[:count], names[count:]
    male_indices = {name: index for index, name in enumerate(men)}
    female_indices = {name: index for index, name in enumerate(women)}

    male_preferences = []
    for index, name in enumerate(men):
        male_preferences.append(
            _preference_indices(lines[index + 1], name, female_indices)
        )

    female_rankings = []
    for index, name in enumerate(women):
        preference = _preference_indices(lines[count + index + 1], name, male_indices)
        ranking = [0] * count
        for rank, man in enumerate(preference):
            ranking[man] = rank
        female_rankings.append(ranking)

    return PreferenceInstance(men, women, male_preferences, female_rankings)


def gale_shapley(instance):
    """Return (man, woman) pairs in women's input order in O(n squared) time."""
    count = len(instance.men)
    free_men = deque(range(count))
    next_proposal = [0] * count
    woman_partner = [-1] * count

    while free_men:
        man = free_men.popleft()
        woman = instance.male_preferences[man][next_proposal[man]]
        next_proposal[man] += 1  # Every proposal advances, so it is never repeated.
        current = woman_partner[woman]

        if current == -1:
            woman_partner[woman] = man
        elif instance.female_rankings[woman][man] < instance.female_rankings[woman][current]:
            woman_partner[woman] = man
            free_men.append(current)
        else:
            free_men.append(man)

    return [
        (instance.men[woman_partner[index]], woman)
        for index, woman in enumerate(instance.women)
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="file containing n and complete preference lists")
    parser.add_argument(
        "--allow-shared-names", action="store_true",
        help="allow a name in both groups; names within each group must remain unique",
    )
    args = parser.parse_args(argv)
    try:
        text = Path(args.input_file).read_text(encoding="utf-8-sig")
        instance = parse_preferences(text, allow_shared_names=args.allow_shared_names)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Input:")
    print(text, end="" if text.endswith("\n") else "\n")
    print("\nMatching:")
    for man, woman in gale_shapley(instance):
        print(man, woman)
    return 0


if __name__ == "__main__":
    sys.exit(main())
