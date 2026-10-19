"""Instructor regressions, independent brute-force oracles, and CLI checks."""

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import random
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from smallestNumber import read_input, smallest_number
from rightTriangles import read_points, count_right_triangles
from treeTraversals import (GENERAL_TREE, BINARY_TREE, preorder, breadth_first,
                            postorder, inorder)


def brute_fewest(values, target):
    for count in range(1, len(values) + 1):
        if any(sum(group) > target for group in combinations(values, count)):
            return count
    return None


def brute_triangles(points):
    answer = 0
    for a, b, c in combinations(points, 3):
        squared = sorted((
            (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2,
            (a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2,
            (b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2,
        ))
        answer += squared[0] > 0 and squared[0] + squared[1] == squared[2]
    return answer


class TraversalTests(unittest.TestCase):
    def test_general_preorder(self):
        self.assertEqual(preorder(GENERAL_TREE, "A"), list("ABEHFICDG"))

    def test_general_breadth_first(self):
        self.assertEqual(breadth_first(GENERAL_TREE, "A"), list("ABCDEFGHI"))

    def test_general_postorder(self):
        self.assertEqual(postorder(GENERAL_TREE, "A"), list("HEIFBCGDA"))

    def test_binary_inorder(self):
        self.assertEqual(inorder(BINARY_TREE, "A"), list("DGBEACHFI"))


class FewestTests(unittest.TestCase):
    def test_instructor_files(self):
        for index, expected in enumerate((3, 9, 1058), start=1):
            with self.subTest(file=index):
                values, target = read_input(ROOT / "Fewest_Resourses" / f"fewest_{index}.txt")
                self.assertEqual(smallest_number(values, target), expected)

    def test_assignment_example(self):
        self.assertEqual(smallest_number([8, 3, 9, 2, 7, 1, 5], 18), 3)

    def test_equality_does_not_pass(self):
        self.assertEqual(smallest_number([6, 4, 1], 10), 3)

    def test_nonadjacent_selection(self):
        self.assertEqual(smallest_number([8, 1, 8], 15), 2)

    def test_one_or_all_elements(self):
        self.assertEqual(smallest_number([1, 20, 2], 10), 1)
        self.assertEqual(smallest_number([2, 2, 2], 5), 3)

    def test_signed_zero_and_impossible(self):
        self.assertEqual(smallest_number([-3, 0, 7, 2], 8), 2)
        self.assertEqual(smallest_number([-5, -2], -3), 1)
        self.assertIsNone(smallest_number([2, 3], 5))
        self.assertIsNone(smallest_number([], 0))

    def test_does_not_mutate_array(self):
        values = [1, 9, 3]
        smallest_number(values, 10)
        self.assertEqual(values, [1, 9, 3])

    def test_exact_decimal_values(self):
        self.assertEqual(smallest_number([Fraction("0.1"), Fraction("0.2"),
                                         Fraction("0.3")], Fraction("0.5")), 3)

    def test_random_against_all_subsets(self):
        rng = random.Random(526)
        for _ in range(250):
            values = [rng.randint(-5, 12) for _ in range(rng.randrange(9))]
            target = rng.randint(-8, 30)
            with self.subTest(values=values, target=target):
                self.assertEqual(smallest_number(values, target), brute_fewest(values, target))


class TriangleTests(unittest.TestCase):
    def test_instructor_files(self):
        for index, expected in enumerate((4, 7), start=1):
            with self.subTest(file=index):
                points = read_points(ROOT / "Angles_Resourses" / f"rightangles_{index}.txt")
                self.assertEqual(count_right_triangles(points), expected)

    def test_large_resource_certificate_and_supplied_discrepancy(self):
        # The supplied answer says 5294. These 5295 distinct valid triples
        # independently prove that the supplied value is too small.
        points = read_points(ROOT / "Angles_Resourses/rightangles_3.txt")
        certificate = ROOT / "tests/data/rightangles3_certificate.txt"
        triples = [tuple(map(int, line.split())) for line in certificate.read_text().splitlines()
                   if line and not line.startswith("#")]
        self.assertEqual(len(triples), 5295)
        self.assertEqual(len(set(triples)), len(triples))
        for triple in triples:
            self.assertEqual(tuple(sorted(triple)), triple)
            self.assertEqual(len(set(triple)), 3)
            self.assertTrue(all(1 <= index <= len(points) for index in triple))
            self.assertEqual(brute_triangles([points[index - 1] for index in triple]), 1)
        self.assertEqual(count_right_triangles(points), len(triples))
        supplied = (ROOT / "Angles_Resourses/answers_angles.txt").read_text()
        self.assertIn("answer 3: 5294", supplied)

    def test_rotated_triangle(self):
        self.assertEqual(count_right_triangles([(0, 0), (1, 1), (-1, 1)]), 1)

    def test_square_counts_each_triple_once(self):
        self.assertEqual(count_right_triangles([(0, 0), (1, 0), (1, 1), (0, 1)]), 4)

    def test_opposite_rays(self):
        self.assertEqual(count_right_triangles([(0, 0), (1, 0), (-1, 0),
                                                (0, 1), (0, -1)]), 8)

    def test_parallel_ray_multiplicity(self):
        points = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2)]
        self.assertEqual(count_right_triangles(points), brute_triangles(points))

    def test_empty_small_and_collinear(self):
        for points in ([], [(1, 2)], [(0, 0), (2, 2)],
                       [(-2, -2), (0, 0), (3, 3), (4, 4)]):
            self.assertEqual(count_right_triangles(points), 0)

    def test_huge_coordinates_use_exact_arithmetic(self):
        m = 10 ** 30
        self.assertEqual(count_right_triangles([(m, m), (m + 3, m), (m, m + 4)]), 1)
        self.assertEqual(count_right_triangles([(0, 0), (m, 1), (-1, m + 1)]), 0)

    def test_translation_rotation_scale_and_input_order(self):
        points = [(0, 0), (1, 0), (1, 2), (-2, 0), (0, 3)]
        expected = brute_triangles(points)
        transformed = [(17 - 7 * y, -13 + 7 * x) for x, y in reversed(points)]
        self.assertEqual(count_right_triangles(transformed), expected)

    def test_duplicate_points_rejected(self):
        with self.assertRaises(ValueError):
            count_right_triangles([(0, 0), (0, 0), (1, 0)])

    def test_random_against_all_triples(self):
        rng = random.Random(2026)
        grid = [(x, y) for x in range(-4, 5) for y in range(-4, 5)]
        for _ in range(250):
            points = rng.sample(grid, rng.randrange(13))
            with self.subTest(points=points):
                self.assertEqual(count_right_triangles(points), brute_triangles(points))


class InputAndCLITests(unittest.TestCase):
    def test_decimal_coordinates_have_uniform_scale(self):
        points = read_points(ROOT / "tests/data/decimal_triangle.txt")
        self.assertEqual(count_right_triangles(points), 1)

    def test_bad_counts_and_duplicates(self):
        for name, reader in (("bad_array_count.txt", read_input),
                             ("bad_point_count.txt", read_points),
                             ("duplicate_points.txt", read_points),
                             ("negative_count.txt", read_points)):
            with self.subTest(file=name):
                path = ROOT / "tests/data" / name
                with self.assertRaises(ValueError):
                    reader(path)

    def test_cli_output(self):
        for program, input_file, expected in (
            ("smallestNumber.py", "tests/data/smallest_input.txt",
             "Input: 8,3,9,2,7,1,5 Target: 18 Answer: 3\n"),
            ("rightTriangles.py", "Angles_Resourses/rightangles_1.txt",
             "The number of right triangles is: 4\n"),
        ):
            with self.subTest(program=program):
                completed = subprocess.run([sys.executable, "-B", program, input_file],
                                           cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stdout, expected)
                self.assertEqual(completed.stderr, "")

    def test_cli_missing_file(self):
        completed = subprocess.run([sys.executable, "-B", "rightTriangles.py", "missing.txt"],
                                   cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("error:", completed.stderr)


if __name__ == "__main__":
    unittest.main()
