import pytest
from dokusan import algorithms, techniques
from dokusan.entities import Sudoku


@pytest.fixture
def sudoku():
    return Sudoku.from_list(
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


def test_backtrack(sudoku):
    for result in techniques.PencilMarking(sudoku):
        sudoku.update(result.changes)
    solution = algorithms.backtrack(sudoku)
    assert solution.is_solved() is True
    assert solution.is_valid() is True
