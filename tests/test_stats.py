import pytest

from dokusan import exceptions, stats
from dokusan.boards import BoxSize, Sudoku


@pytest.mark.parametrize(
    ["puzzle", "solutions", "rank"],
    [
        (
            [
                [3, 7, 0, 0, 0, 9, 0, 0, 6],
                [8, 0, 0, 1, 0, 3, 0, 7, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 8],
                [0, 2, 0, 0, 8, 0, 0, 0, 5],
                [1, 8, 7, 0, 0, 0, 6, 4, 2],
                [5, 0, 0, 0, 2, 0, 0, 1, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 0, 6, 0, 2, 0, 0, 7],
                [2, 0, 0, 3, 0, 0, 0, 6, 1],
            ],
            1,
            451,
        ),
        (
            [
                [4, 0, 3, 9, 2, 0, 0, 0, 7],
                [0, 5, 0, 0, 0, 7, 9, 0, 0],
                [7, 6, 0, 3, 4, 5, 8, 0, 2],
                [1, 0, 4, 8, 9, 0, 0, 0, 5],
                [0, 0, 0, 0, 0, 6, 1, 4, 0],
                [0, 0, 0, 0, 0, 1, 0, 8, 9],
                [0, 0, 8, 6, 3, 4, 0, 5, 1],
                [5, 0, 0, 0, 0, 9, 0, 0, 0],
                [0, 0, 0, 0, 0, 2, 3, 0, 8],
            ],
            1,
            44,
        ),
        (
            [
                [0, 7, 0, 3, 0, 0, 0, 4, 0],
                [3, 0, 0, 0, 8, 0, 2, 0, 0],
                [2, 0, 1, 4, 0, 7, 0, 0, 0],
                [5, 0, 4, 0, 0, 0, 0, 9, 0],
                [0, 2, 0, 0, 0, 0, 0, 5, 0],
                [0, 1, 0, 0, 0, 0, 7, 0, 3],
                [0, 0, 0, 9, 0, 6, 3, 0, 2],
                [0, 0, 2, 0, 3, 0, 0, 0, 9],
                [0, 6, 0, 0, 0, 2, 0, 8, 0],
            ],
            1,
            153,
        ),
        (
            [
                [2, 4, 8, 5, 9, 3, 1, 6, 7],
                [5, 6, 1, 7, 8, 2, 3, 9, 4],
                [3, 9, 7, 6, 4, 1, 8, 2, 5],
                [6, 5, 4, 1, 3, 8, 9, 7, 2],
                [8, 1, 2, 4, 7, 9, 5, 3, 6],
                [7, 3, 9, 2, 5, 6, 4, 1, 8],
                [1, 7, 5, 3, 2, 4, 6, 8, 9],
                [9, 2, 6, 8, 1, 5, 7, 4, 3],
                [4, 8, 3, 9, 6, 7, 2, 5, 1],
            ],
            0,
            0,
        ),
    ],
)
def test_rank(puzzle, solutions, rank):
    sudoku = Sudoku.from_list(puzzle, box_size=BoxSize(3, 3))
    assert stats.rank(sudoku) == rank


def test_rank_sudoku_with_multiple_solutions():
    puzzle = [
        [8, 1, 0, 0, 0, 0, 6, 7, 9],
        [0, 0, 0, 6, 7, 9, 0, 2, 0],
        [0, 0, 0, 1, 2, 8, 3, 0, 0],
        [0, 3, 4, 0, 5, 7, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 3, 7, 0, 1, 0, 6, 2],
        [0, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 1, 0, 3, 0, 0, 8, 0],
    ]
    sudoku = Sudoku.from_list(puzzle, box_size=BoxSize(3, 3))
    with pytest.raises(exceptions.MultipleSolutions):
        stats.rank(sudoku)
