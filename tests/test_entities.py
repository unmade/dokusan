import operator

import pytest
from dokusan.entities import BoxSize, Cell, Position, Sudoku


@pytest.fixture
def sudoku():
    return Sudoku.from_list(
        [
            [0, 0, 7, 0, 3, 0, 8, 0, 0],
            [0, 0, 0, 2, 0, 5, 0, 0, 0],
            [4, 0, 0, 9, 0, 6, 0, 0, 1],
            [0, 4, 3, 0, 0, 0, 2, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 5, 8, 0, 0, 0, 6, 7, 0],
            [5, 0, 0, 1, 0, 8, 0, 0, 9],
            [0, 0, 0, 5, 0, 3, 0, 0, 0],
            [0, 0, 2, 0, 9, 0, 5, 0, 0],
        ]
    )


@pytest.fixture
def sudoku_12x12():
    return Sudoku.from_list(
        [
            [3, 0, 0, 9, 7, 4, 11, 1, 0, 6, 8, 12],
            [8, 0, 0, 6, 9, 2, 12, 0, 11, 4, 3, 0],
            [0, 0, 0, 4, 0, 3, 6, 5, 0, 2, 0, 10],
            [12, 5, 6, 1, 11, 10, 0, 0, 0, 9, 2, 3],
            [2, 8, 4, 10, 6, 0, 7, 3, 12, 0, 11, 5],
            [7, 11, 9, 3, 12, 0, 5, 0, 4, 0, 0, 6],
            [10, 4, 0, 7, 2, 11, 3, 0, 9, 0, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 12, 10, 0, 6, 0],
            [0, 3, 1, 12, 0, 8, 10, 9, 2, 7, 0, 11],
            [4, 0, 0, 0, 10, 0, 2, 7, 6, 0, 1, 9],
            [9, 2, 10, 0, 3, 0, 1, 0, 0, 0, 7, 0],
            [0, 6, 0, 11, 0, 12, 0, 0, 0, 0, 5, 2],
        ],
        box_size=BoxSize(3, 4),
    )


def test_cell():
    with pytest.raises(ValueError):
        Cell(position=Position(0, 0, 0), value=2, candidates={2, 6, 9})


def test_str(sudoku_12x12):
    assert str(sudoku_12x12) == (
        "300974B1068C"
        "800692C0B430"
        "00040365020A"
        "C561BA000923"
        "284A6073C0B5"
        "7B93C0504006"
        "A4072B309000"
        "0900000CA060"
        "031C08A9270B"
        "4000A0276019"
        "92A030100070"
        "060B0C000052"
    )


def test_from_string(sudoku_12x12):
    sudoku = Sudoku.from_string(
        "300974B1068C"
        "800692C0B430"
        "00040365020A"
        "C561BA000923"
        "284A6073C0B5"
        "7B93C0504006"
        "A4072B309000"
        "0900000CA060"
        "031C08A9270B"
        "4000A0276019"
        "92A030100070"
        "060B0C000052",
        box_size=BoxSize(3, 4),
    )
    assert sudoku.cells() == sudoku_12x12.cells()


def test_getitem(sudoku):
    assert sudoku[0, 0] == Cell(position=Position(0, 0, 0), candidates=set())
    assert sudoku[2, 3] == Cell(position=Position(2, 3, 1), value=9)


def test_sudoku():
    sudoku = Sudoku(
        Cell(position=Position(0, 0, 0), value=2),
        Cell(position=Position(0, 1, 0), candidates=set()),
    )
    assert sudoku[0, 0].value == 2
    assert sudoku[0, 1].candidates == set()
    assert sudoku[0, 2].value is None
    assert len(sudoku[0, 2].candidates) == 0


def test_update(sudoku):
    cell_a = Cell(position=Position(0, 0, 0), value=2)
    cell_b = Cell(position=Position(0, 1, 0), candidates=set())
    sudoku.update([cell_a, cell_b])
    assert sudoku[0, 0] is cell_a
    assert sudoku[0, 1] is cell_b


def test_cells(sudoku):
    assert sudoku.cells()[0].candidates == set()
    assert sudoku.cells()[2].value == 7


def test_rows(sudoku):
    for i in range(sudoku.size):
        for j in range(sudoku.size):
            assert sudoku.rows()[i][j] == sudoku[i, j]


def test_columns(sudoku):
    for i in range(sudoku.size):
        for j in range(sudoku.size):
            assert sudoku.columns()[i][j] == sudoku[j, i]


def test_boxes(sudoku):
    index_map = [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
        [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
        [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
        [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
        [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
        [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
        [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)],
    ]
    expected = [[sudoku[pos] for pos in row] for row in index_map]
    assert sudoku.boxes() == expected


@pytest.mark.parametrize(
    ["puzzle", "solved"],
    [
        (
            [
                [0, 0, 7, 0, 3, 0, 8, 0, 0],
                [0, 0, 0, 2, 0, 5, 0, 0, 0],
                [4, 0, 0, 9, 0, 6, 0, 0, 1],
                [0, 4, 3, 0, 0, 0, 2, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 5],
                [0, 5, 8, 0, 0, 0, 6, 7, 0],
                [5, 0, 0, 1, 0, 8, 0, 0, 9],
                [0, 0, 0, 5, 0, 3, 0, 0, 0],
                [0, 0, 2, 0, 9, 0, 5, 0, 0],
            ],
            False,
        ),
        # duplicate `2` in the bottom row
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 8],
                [6, 1, 2, 7, 9, 4, 5, 2, 3],
            ],
            False,
        ),
        # duplicate `2` in the first column
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 2],
                [2, 1, 6, 7, 9, 4, 5, 8, 3],
            ],
            False,
        ),
        # duplicates in boxes
        (
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 8],
            ],
            False,
        ),
        # correct puzzle
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 2],
                [6, 1, 2, 7, 9, 4, 5, 8, 3],
            ],
            True,
        ),
    ],
)
def test_is_solved_false(puzzle, solved):
    sudoku = Sudoku.from_list(puzzle)
    assert sudoku.is_solved() is solved


@pytest.mark.parametrize(
    ["puzzle", "is_valid"],
    [
        (
            [
                [0, 0, 7, 0, 3, 0, 8, 0, 0],
                [0, 0, 0, 2, 0, 5, 0, 0, 0],
                [4, 0, 0, 9, 0, 6, 0, 0, 1],
                [0, 4, 3, 0, 0, 0, 2, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 5],
                [0, 5, 8, 0, 0, 0, 6, 7, 0],
                [5, 0, 0, 1, 0, 8, 0, 0, 9],
                [0, 0, 0, 5, 0, 3, 0, 0, 0],
                [0, 0, 2, 0, 9, 0, 5, 0, 0],
            ],
            True,
        ),
        # duplicate `2` in the bottom row
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 8],
                [6, 1, 2, 7, 9, 4, 5, 2, 3],
            ],
            False,
        ),
        # duplicate `2` in the first column
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 2],
                [2, 1, 6, 7, 9, 4, 5, 8, 3],
            ],
            False,
        ),
        # duplicates in boxes
        (
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 8],
            ],
            False,
        ),
        # correct puzzle
        (
            [
                [2, 9, 7, 4, 3, 1, 8, 5, 6],
                [3, 6, 1, 2, 8, 5, 4, 9, 7],
                [4, 8, 5, 9, 7, 6, 3, 2, 1],
                [7, 4, 3, 6, 5, 9, 2, 1, 8],
                [1, 2, 6, 8, 4, 7, 9, 3, 5],
                [9, 5, 8, 3, 1, 2, 6, 7, 4],
                [5, 3, 4, 1, 2, 8, 7, 6, 9],
                [8, 7, 9, 5, 6, 3, 1, 4, 2],
                [6, 1, 2, 7, 9, 4, 5, 8, 3],
            ],
            True,
        ),
    ],
)
def test_is_valid(puzzle, is_valid):
    sudoku = Sudoku.from_list(puzzle)
    assert sudoku.is_valid() is is_valid


def test_intersection_for_single_cell(sudoku):
    by_position = operator.attrgetter("position")
    expected = (
        sudoku.rows()[0][1:]
        + sudoku.columns()[0][1:]
        + [sudoku[1, 1], sudoku[1, 2], sudoku[2, 1], sudoku[2, 2]]
    )
    assert sorted(sudoku.intersection(sudoku[0, 0]), key=by_position) == sorted(
        expected, key=by_position
    )


def test_intersection_between_two_cells(sudoku):
    by_position = operator.attrgetter("position")
    expected = sudoku.rows()[0][1:8]
    assert sorted(
        sudoku.intersection(sudoku[0, 0], sudoku[0, 8]), key=by_position
    ) == sorted(expected, key=by_position)


def test_intersection_between_three_cells(sudoku):
    by_position = operator.attrgetter("position")
    expected = sudoku.rows()[0][1:3]
    assert sorted(
        sudoku.intersection(sudoku[0, 0], sudoku[0, 8], sudoku[2, 2]), key=by_position
    ) == sorted(expected, key=by_position)


def test_intersection_between_cells_with_no_intersection(sudoku):
    assert sudoku.intersection(sudoku[0, 0], sudoku[3, 3], sudoku[8, 8]) == []
