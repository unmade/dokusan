import operator

import pytest
from dokusan import techniques
from dokusan.entities import Cell, Mark, Position, Sudoku


def test_lone_single():
    sudoku = Sudoku(
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
    lone_single = techniques.LoneSingle(sudoku).first()

    assert lone_single.positions == [Position(1, 0, 0)]
    assert lone_single.values == [5]

    by_position = operator.attrgetter("position")
    assert sorted(lone_single.changed_cells, key=by_position) == [
        Mark(position=Position(0, 0, 0), candidates={2, 3}),
        Mark(position=Position(0, 1, 0), candidates={2, 3, 4, 6, 8}),
        Mark(position=Position(0, 2, 0), candidates={2, 6, 8}),
        Cell(position=Position(1, 0, 0), value=5),
        Mark(position=Position(1, 1, 0), candidates={4, 6, 8, 9}),
        Mark(position=Position(1, 2, 0), candidates={1, 6, 8}),
        Mark(position=Position(1, 3, 1), candidates={4, 6, 7, 8}),
        Mark(position=Position(1, 4, 1), candidates={4, 7, 8}),
        Mark(position=Position(5, 0, 3), candidates={2, 3, 7}),
    ]


def test_lone_single_not_found():
    sudoku = Sudoku(
        [
            [9, 0, 6, 7, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 2, 5],
            [7, 4, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 6, 4, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 6, 9, 1, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.LoneSingle(sudoku).first()


def test_hidden_single():
    sudoku = Sudoku(
        [
            [9, 0, 6, 7, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 2, 5],
            [7, 4, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 6, 4, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 6, 9, 1, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    hidden_single = techniques.HiddenSingle(sudoku).first()

    assert hidden_single.positions == [Position(1, 6, 2)]
    assert hidden_single.values == [7]

    by_position = operator.attrgetter("position")
    assert sorted(hidden_single.changed_cells, key=by_position) == [
        Cell(position=Position(1, 6, 2), value=7),
        Mark(position=Position(4, 6, 5), candidates={2, 8, 9}),
        Mark(position=Position(6, 6, 8), candidates={2, 4, 5, 9}),
        Mark(position=Position(7, 6, 8), candidates={2, 4, 5, 8}),
    ]


def test_hidden_single_not_found():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )
    with pytest.raises(techniques.NotFound):
        techniques.HiddenSingle(sudoku).first()


def test_naked_pair():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    naked_pair = techniques.NakedPair(sudoku).first()

    assert naked_pair.positions == [Position(6, 3, 7), Position(6, 6, 8)]
    assert naked_pair.values == {2, 5}

    by_position = operator.attrgetter("position")
    assert sorted(naked_pair.changed_cells, key=by_position) == [
        Mark(position=Position(6, 0, 6), candidates={1, 3, 4, 6}),
        Mark(position=Position(6, 1, 6), candidates={3, 7, 9}),
        Mark(position=Position(6, 2, 6), candidates={1, 3, 7}),
        Mark(position=Position(6, 5, 7), candidates={6, 7}),
    ]


def test_naked_pair_not_found():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )
    sudoku.update_cells(
        [
            Mark(position=Position(6, 0, 6), candidates={1, 3, 4, 6}),
            Mark(position=Position(6, 1, 6), candidates={3, 7, 9}),
            Mark(position=Position(6, 2, 6), candidates={1, 3, 7}),
            Mark(position=Position(6, 5, 7), candidates={6, 7}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedPair(sudoku).first()


def test_naked_triplet():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    naked_triplet = techniques.NakedTriplet(sudoku).first()

    assert naked_triplet.positions == [
        Position(6, 7, 8),
        Position(8, 7, 8),
        Position(8, 8, 8),
    ]
    assert naked_triplet.values == [7, 8, 9]

    by_position = operator.attrgetter("position")
    assert sorted(naked_triplet.changed_cells, key=by_position) == [
        Mark(position=Position(6, 8, 8), candidates={3, 4}),
        Mark(position=Position(7, 8, 8), candidates={3, 4}),
    ]


def test_naked_triplet_not_found():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    sudoku.update_cells(
        [
            Mark(position=Position(6, 8, 8), candidates={3, 4}),
            Mark(position=Position(7, 8, 8), candidates={3, 4}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedTriplet(sudoku).first()


def test_omission():
    sudoku = Sudoku(
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

    sudoku.update_cells(
        [
            Mark(position=Position(1, 1, 0), candidates={4, 6}),
            Mark(position=Position(1, 7, 2), candidates={6, 9}),
            Mark(position=Position(1, 8, 2), candidates={4, 9}),
            Mark(position=Position(8, 3, 7), candidates={7, 9}),
            Mark(position=Position(8, 7, 8), candidates={5, 8}),
        ]
    )

    omission = techniques.Omission(sudoku).first()

    assert omission.values == [7]
    assert omission.positions == [Position(3, 7, 5), Position(3, 8, 5)]

    assert omission.changed_cells == [
        Mark(position=Position(3, 3, 4), candidates={1, 2})
    ]


def test_omission_not_found():
    sudoku = Sudoku(
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

    sudoku.update_cells(
        [
            Mark(position=Position(1, 1, 0), candidates={4, 6}),
            Mark(position=Position(1, 7, 2), candidates={6, 9}),
            Mark(position=Position(1, 8, 2), candidates={4, 9}),
            Mark(position=Position(3, 3, 4), candidates={1, 2}),
            Mark(position=Position(8, 1, 6), candidates={2, 5, 8}),
            Mark(position=Position(8, 3, 7), candidates={7, 9}),
            Mark(position=Position(8, 5, 7), candidates={7, 9}),
            Mark(position=Position(8, 6, 8), candidates={2, 5}),
            Mark(position=Position(8, 7, 8), candidates={5, 8}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.Omission(sudoku).first()


def test_xy_wing():
    sudoku = Sudoku(
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

    sudoku.update_cells([Mark(position=Position(3, 3, 4), candidates={1, 2})])

    xy_wing = techniques.XYWing(sudoku).first()

    assert xy_wing.positions == [
        Position(5, 4, 4),
        Position(5, 7, 5),
        Position(3, 3, 4),
    ]
    assert xy_wing.values == [1]

    assert xy_wing.changed_cells == [
        Mark(position=Position(3, 7, 5), candidates={5, 7}),
        Mark(position=Position(5, 3, 4), candidates={2, 4}),
    ]


def test_xy_wing_not_found():
    sudoku = Sudoku(
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

    with pytest.raises(techniques.NotFound):
        techniques.XYWing(sudoku).first()


def test_unique_rectangle_in_a_row():
    sudoku = Sudoku(
        [
            [2, 0, 0, 5, 9, 3, 1, 0, 0],
            [5, 0, 1, 0, 0, 2, 3, 0, 0],
            [3, 9, 7, 6, 4, 1, 8, 2, 5],
            [6, 0, 4, 1, 3, 8, 9, 0, 0],
            [8, 1, 0, 0, 0, 0, 0, 3, 6],
            [7, 3, 9, 0, 0, 6, 0, 1, 8],
            [1, 7, 0, 3, 0, 4, 6, 0, 0],
            [9, 0, 0, 0, 1, 5, 7, 4, 3],
            [4, 0, 3, 0, 6, 0, 0, 0, 1],
        ]
    )

    sudoku.update_cells(
        [
            Mark(position=Position(8, 3, 7), candidates={7, 9}),
            Mark(position=Position(8, 5, 7), candidates={7, 9}),
        ]
    )

    unique_rectangle = techniques.UniqueRectangle(sudoku).first()

    assert unique_rectangle.positions == [
        Position(4, 3, 4),
        Position(4, 5, 4),
        Position(8, 3, 7),
        Position(8, 5, 7),
    ]
    assert unique_rectangle.values == [7, 9]

    assert unique_rectangle.changed_cells == [
        Mark(position=Position(4, 3, 4), candidates={2, 4})
    ]


def test_unique_rectangle_in_a_column():
    sudoku = Sudoku(
        [
            [9, 2, 6, 7, 3, 5, 4, 0, 0],
            [0, 0, 0, 6, 4, 9, 7, 2, 5],
            [7, 4, 5, 8, 2, 1, 9, 3, 6],
            [0, 1, 0, 0, 0, 8, 6, 4, 0],
            [5, 0, 4, 0, 0, 0, 8, 0, 0],
            [8, 6, 9, 1, 7, 4, 3, 5, 2],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 9, 1, 0, 0, 6, 0],
            [0, 0, 0, 4, 0, 3, 1, 0, 0],
        ]
    )

    sudoku.update_cells(
        [
            Mark(position=Position(6, 0, 6), candidates={1, 3, 4, 6}),
            Mark(position=Position(6, 8, 8), candidates={3, 4}),
            Mark(position=Position(7, 0, 6), candidates={3, 4}),
            Mark(position=Position(7, 8, 8), candidates={3, 4}),
        ]
    )

    unique_rectangle = techniques.UniqueRectangle(sudoku).first()

    assert unique_rectangle.positions == [
        Position(6, 0, 6),
        Position(6, 8, 8),
        Position(7, 0, 6),
        Position(7, 8, 8),
    ]
    assert unique_rectangle.values == [3, 4]
    assert unique_rectangle.changed_cells == [
        Mark(position=Position(6, 0, 6), candidates={1, 6}),
    ]


def test_unique_rectangle_not_found():
    sudoku = Sudoku(
        [
            [2, 0, 0, 5, 9, 3, 1, 0, 0],
            [5, 0, 1, 0, 0, 2, 3, 0, 0],
            [3, 9, 7, 6, 4, 1, 8, 2, 5],
            [6, 0, 4, 1, 3, 8, 9, 0, 0],
            [8, 1, 0, 0, 0, 0, 0, 3, 6],
            [7, 3, 9, 0, 0, 6, 0, 1, 8],
            [1, 7, 0, 3, 0, 4, 6, 0, 0],
            [9, 0, 0, 0, 1, 5, 7, 4, 3],
            [4, 0, 3, 0, 6, 0, 0, 0, 1],
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.UniqueRectangle(sudoku).first()
