from dokusan import solvers
from dokusan.entities import Sudoku


def test_eliminate():
    given = Sudoku.from_list(
        [
            [0, 0, 0, 0, 9, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 2, 3, 0, 0],
            [0, 0, 7, 0, 0, 1, 8, 2, 5],
            [6, 0, 4, 0, 3, 8, 9, 0, 0],
            [8, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 8],
            [1, 7, 0, 0, 0, 0, 6, 0, 0],
            [9, 0, 0, 0, 1, 0, 7, 4, 3],
            [4, 0, 3, 0, 6, 0, 0, 0, 1],
        ]
    )
    expected = Sudoku.from_list(
        [
            [2, 0, 0, 5, 9, 3, 1, 0, 0],
            [5, 0, 1, 0, 0, 2, 3, 0, 0],
            [3, 9, 7, 6, 4, 1, 8, 2, 5],
            [6, 0, 4, 0, 3, 8, 9, 0, 0],
            [8, 1, 0, 0, 0, 0, 0, 3, 6],
            [7, 3, 9, 0, 0, 6, 0, 0, 8],
            [1, 7, 0, 3, 0, 4, 6, 0, 0],
            [9, 0, 0, 0, 1, 5, 7, 4, 3],
            [4, 0, 3, 0, 6, 0, 0, 0, 1],
        ]
    )

    solution = solvers.eliminate(given)
    solution_cells = [c for c in solution.cells() if c.value]
    expected_cells = [c for c in expected.cells() if c.value]
    assert solution_cells == expected_cells


def test_backtrack():
    given = Sudoku.from_list(
        [
            [5, 3, 4, 0, 0, 8, 0, 1, 0],
            [0, 0, 0, 0, 0, 2, 0, 9, 0],
            [0, 0, 0, 0, 0, 7, 6, 0, 4],
            [0, 0, 0, 5, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 9, 0, 0, 1, 0, 0, 0],
            [3, 0, 5, 4, 0, 0, 0, 0, 0],
            [0, 8, 0, 2, 0, 0, 0, 0, 0],
            [0, 6, 0, 7, 0, 0, 3, 8, 2],
        ],
    )
    solution = solvers.backtrack(given)
    assert solution.is_solved() is True
    assert solution.is_valid() is True
