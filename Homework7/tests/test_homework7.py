"""Independent checks using ordering and multiset preservation properties."""

from collections import Counter
from itertools import permutations
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from input_utils import read_integers
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort
from radix_sort import radix_sort
from stable_matching import gale_shapley, parse_preferences


def run_program(script, path, *options):
    return subprocess.run(
        [sys.executable, str(ROOT / script), str(path), *options],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, timeout=30,
    )


def source_preferences(text):
    """Read valid fixtures independently of the application's parser."""
    lines = [line.split() for line in text.splitlines() if line.strip()]
    n = int(lines[0][0])
    men = [row[0] for row in lines[1:n + 1]]
    women = [row[0] for row in lines[n + 1:]]
    male = {row[0]: row[1:] for row in lines[1:n + 1]}
    female = {
        row[0]: {man: rank for rank, man in enumerate(row[1:])}
        for row in lines[n + 1:]
    }
    return men, women, male, female


def is_stable(pairs, male, female):
    male_partner = dict(pairs)
    female_partner = {woman: man for man, woman in pairs}
    for man, preferences in male.items():
        for woman in preferences:
            if woman == male_partner[man]:
                break
            if female[woman][man] < female[woman][female_partner[woman]]:
                return False
    return True


class SortingTests(unittest.TestCase):
    def assert_ordered_permutation(self, result, original):
        """Verify increasing order and preservation of every input occurrence."""
        self.assertTrue(all(left <= right for left, right in zip(result, result[1:])),
                        "Result must be in non-decreasing order.")
        self.assertEqual(Counter(result), Counter(original))

    def test_comparison_sorts_order_and_permutation_without_mutation(self):
        rng = random.Random(5267)
        cases = [[], [4], [3, -2, 3, 0, -2], list(range(100)),
                 list(range(100, -1, -1)), [7] * 100]
        cases += [[rng.randint(-9999, 9999) for _ in range(n)]
                  for n in (15, 50, 500)]
        for function in (merge_sort, quick_sort, insertion_sort):
            for values in cases:
                with self.subTest(algorithm=function.__name__, size=len(values)):
                    before = values.copy()
                    result = function(values)
                    self.assert_ordered_permutation(result, before)
                    self.assertEqual(values, before)
                    self.assertIsNot(result, values)

    def test_radix_zero_duplicates_and_digit_boundaries(self):
        rng = random.Random(7526)
        cases = [[], [0], [0] * 25, [9999, 9, 100, 10, 99, 0, 1000, 1, 10],
                 [10 ** 40, 10 ** 39 - 1, 0, 10 ** 40, 42],
                 [rng.randrange(1000000) for _ in range(500)]]
        for values in cases:
            with self.subTest(values=values[:10], size=len(values)):
                before = values.copy()
                result = radix_sort(values)
                self.assert_ordered_permutation(result, before)
                self.assertEqual(values, before)
                self.assertIsNot(result, values)
        with self.assertRaises(ValueError):
            radix_sort([2, -1, 0])

    def test_custom_input_sizes_and_required_content(self):
        for prefix, non_negative in (("", False), ("radix_", True)):
            datasets = []
            for label, size in (("small", 15), ("medium", 50), ("large", 500)):
                values = read_integers(ROOT / "inputs" / f"{prefix}{label}.txt",
                                       non_negative=non_negative)
                self.assertEqual(len(values), size)
                datasets.append(values)
            self.assertTrue(any(len(set(values)) < len(values) for values in datasets))
            if non_negative:
                self.assertTrue(any(len({len(str(v)) for v in values}) > 1
                                    for values in datasets))

    def test_cli_prints_all_500_input_and_sorted_values(self):
        for name in ("merge_sort", "quick_sort", "insertion_sort", "radix_sort"):
            filename = "radix_large.txt" if name == "radix_sort" else "large.txt"
            path = ROOT / "inputs" / filename
            values = read_integers(path)
            result = run_program(name + ".py", path)
            with self.subTest(algorithm=name):
                self.assertEqual(result.returncode, 0, result.stderr)
                match = re.fullmatch(
                    r"Input \(500 values\):\n(.*?)Sorted \(500 values\):\n(.*)",
                    result.stdout, re.DOTALL,
                )
                self.assertIsNotNone(match, result.stdout[:300])
                printed_input = [int(v) for v in match.group(1).split()]
                printed_result = [int(v) for v in match.group(2).split()]
                self.assertEqual(printed_input, values)
                self.assert_ordered_permutation(printed_result, values)

    def test_input_errors_are_descriptive_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.txt"
            for script, text in (("merge_sort.py", "2\nhello\n"),
                                 ("radix_sort.py", "0\n-3\n")):
                path.write_text(text, encoding="utf-8")
                result = run_program(script, path)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Error:", result.stderr)
                self.assertIn("line 2", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
            result = run_program("quick_sort.py", Path(directory) / "absent.txt")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)


class MatchingTests(unittest.TestCase):
    fixtures = (
        ("marraige_ten.txt", None, False),
        ("marriage_hundred.txt", "hundred_ans.txt", True),
        ("marraige_thousand.txt", "marriage_thousand_ans.txt", True),
    )

    def expected_pairs(self, answer):
        if answer is None:
            lines = (ROOT / "references" / "Marriage_answers.txt").read_text(
                encoding="utf-8-sig").splitlines()
            nonblank = [line.strip() for line in lines if line.strip()]
            return [tuple(line.split()) for line in nonblank[1:11]]
        text = (ROOT / "references" / answer).read_text(encoding="utf-8-sig")
        return [tuple(line.split()) for line in text.splitlines() if line.strip()]

    def test_supplied_answers_female_order_and_no_blocking_pair(self):
        for filename, answer, compat in self.fixtures:
            with self.subTest(filename=filename):
                text = (ROOT / "inputs" / filename).read_text(encoding="utf-8-sig")
                instance = parse_preferences(text, allow_shared_names=compat)
                actual = gale_shapley(instance)
                self.assertEqual(actual, self.expected_pairs(answer))
                men, women, male, female = source_preferences(text)
                self.assertEqual([woman for _, woman in actual], women)
                self.assertEqual({man for man, _ in actual}, set(men))
                self.assertEqual(len(actual), len(women))
                self.assertTrue(is_stable(actual, male, female))

    def test_cli_echoes_input_and_every_supplied_pair(self):
        for filename, answer, compat in self.fixtures:
            with self.subTest(filename=filename):
                path = ROOT / "inputs" / filename
                options = ("--allow-shared-names",) if compat else ()
                result = run_program("stable_matching.py", path, *options)
                self.assertEqual(result.returncode, 0, result.stderr)
                echoed, matching = result.stdout.split("\nMatching:\n", 1)
                self.assertEqual(echoed.removeprefix("Input:\n").strip(),
                                 path.read_text(encoding="utf-8-sig").strip())
                self.assertEqual([tuple(line.split()) for line in matching.splitlines()],
                                 self.expected_pairs(answer))

    def test_legacy_shared_names_require_explicit_option(self):
        for filename, _, compat in self.fixtures:
            if compat:
                text = (ROOT / "inputs" / filename).read_text(encoding="utf-8-sig")
                with self.assertRaisesRegex(ValueError, "both groups"):
                    parse_preferences(text)
                parse_preferences(text, allow_shared_names=True)

    def test_invalid_inputs_and_blank_lines(self):
        valid = "\n2\n\nAdam Beth Cara\nDave Beth Cara\nBeth Dave Adam\nCara Adam Dave\n"
        self.assertEqual(gale_shapley(parse_preferences(valid)),
                         [("Dave", "Beth"), ("Adam", "Cara")])
        self.assertEqual(gale_shapley(parse_preferences("1\nA B\nB A\n")), [("A", "B")])
        invalid = ["", "zero\n", "0\n", "-2\n", "1.5\n", "2 extra\n",
                   "1\nA B\n", "1\nA B\nB A\nC A\n",
                   valid.replace("Adam Beth Cara", "Adam Beth Beth"),
                   valid.replace("Adam Beth Cara", "Adam Beth"),
                   valid.replace("Adam Beth Cara", "Adam Beth Zed"),
                   valid.replace("Cara Adam Dave", "Cara Adam Adam"),
                   valid.replace("Dave Beth Cara", "Adam Beth Cara"),
                   valid.replace("Cara Adam Dave", "Beth Adam Dave")]
        for text in invalid:
            for compat in (False, True):
                with self.subTest(text=text, compatibility=compat):
                    with self.assertRaises(ValueError):
                        parse_preferences(text, allow_shared_names=compat)
        with self.assertRaisesRegex(ValueError, "both groups"):
            parse_preferences("1\nAlex Alex\nAlex Alex\n")
        self.assertEqual(gale_shapley(parse_preferences(
            "1\nAlex Alex\nAlex Alex\n", allow_shared_names=True)), [("Alex", "Alex")])
        # Case-sensitive names remain distinct.
        self.assertEqual(gale_shapley(parse_preferences("1\nAlex alex\nalex Alex\n")),
                         [("Alex", "alex")])

    def test_supplied_badinput_reports_23_person_lines(self):
        path = ROOT / "inputs" / "badInput.txt"
        text = path.read_text(encoding="utf-8-sig")
        with self.assertRaisesRegex(ValueError, r"20 person lines.*23"):
            parse_preferences(text)
        result = run_program("stable_matching.py", path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("20 person lines", result.stderr)
        self.assertIn("23", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_men_optimal_against_all_small_matchings(self):
        rng = random.Random(526)
        for n, repetitions in ((2, 12), (3, 30), (4, 12)):
            men = [f"M{i}" for i in range(n)]
            women = [f"W{i}" for i in range(n)]
            for case in range(repetitions):
                rows = [str(n)]
                for man in men:
                    rows.append(" ".join([man] + rng.sample(women, n)))
                for woman in women:
                    rows.append(" ".join([woman] + rng.sample(men, n)))
                text = "\n".join(rows)
                _, _, male, female = source_preferences(text)
                actual = gale_shapley(parse_preferences(text))
                self.assertTrue(is_stable(actual, male, female))
                actual_by_man = dict(actual)
                stable_count = 0
                for candidate in permutations(women):
                    pairs = list(zip(men, candidate))
                    if is_stable(pairs, male, female):
                        stable_count += 1
                        for man, woman in pairs:
                            with self.subTest(n=n, case=case, man=man):
                                self.assertLessEqual(male[man].index(actual_by_man[man]),
                                                     male[man].index(woman))
                self.assertGreater(stable_count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
