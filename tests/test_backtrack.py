import unittest

from dokusan import backtrack


class TestBacktrack(unittest.TestCase):
    def setUp(self) -> None:
        self.unsolved_sudoku = [
            [0, 0, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 0, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [0, 7, 0, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 0, 8, 9, 5, 7, 1, 3, 6],
            [7, 6, 0, 4, 1, 8, 2, 5, 9],
        ]
        self.sudoku = [
            [4, 3, 5, 2, 6, 9, 7, 8, 1],
            [6, 8, 2, 5, 7, 1, 4, 9, 3],
            [1, 9, 7, 8, 3, 4, 5, 6, 2],
            [8, 2, 6, 1, 9, 5, 3, 4, 7],
            [3, 7, 4, 6, 8, 2, 9, 1, 5],
            [9, 5, 1, 7, 4, 3, 6, 2, 8],
            [5, 1, 9, 3, 2, 6, 8, 7, 4],
            [2, 4, 8, 9, 5, 7, 1, 3, 6],
            [7, 6, 3, 4, 1, 8, 2, 5, 9],
        ]
        self.variations = {
            (0, 0): [3, 4],
            (0, 1): [3, 4],
            (1, 6): [4],
            (4, 0): [3, 4],
            (4, 2): [3, 4],
            (7, 1): [4],
            (8, 2): [3],
        }
        self.solution = {
            (0, 0): 4,
            (0, 1): 3,
            (1, 6): 4,
            (4, 0): 3,
            (4, 2): 4,
            (7, 1): 4,
            (8, 2): 3,
        }

    def test_solve(self):
        self.assertEqual(backtrack.solve(self.unsolved_sudoku), self.sudoku)

    def test_variations(self):
        self.assertEqual(
            backtrack.get_variations(self.unsolved_sudoku), self.variations
        )

    def test_backtrack(self):
        self.assertEqual(backtrack.backtrack(self.variations), self.solution)

    def test_backtrack_recursive(self):
        self.assertEqual(backtrack.backtrack_recursive(self.variations), self.solution)

    def test_is_valid_sudoku(self):
        self.assertTrue(backtrack.is_valid_sudoku(self.sudoku))
