import operator

import pytest
from dokusan import entities, techniques


def test_lone_single():
    sudoku = entities.Sudoku(
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
    lone_single = techniques.LoneSingle(sudoku)

    assert lone_single.single == entities.Cell(position=(1, 0), value=5)

    by_position = operator.attrgetter("position")
    assert sorted(lone_single.affected_cells, key=by_position) == [
        entities.Mark(position=(0, 0), candidates={2, 3}),
        entities.Mark(position=(0, 1), candidates={2, 3, 4, 6, 8}),
        entities.Mark(position=(0, 2), candidates={2, 6, 8}),
        entities.Cell(position=(1, 0), value=5),
        entities.Mark(position=(1, 1), candidates={4, 6, 8, 9}),
        entities.Mark(position=(1, 2), candidates={1, 6, 8}),
        entities.Mark(position=(1, 3), candidates={4, 6, 7, 8}),
        entities.Mark(position=(1, 4), candidates={4, 7, 8}),
        entities.Mark(position=(5, 0), candidates={2, 3, 7}),
    ]


def test_lone_single_not_found():
    sudoku = entities.Sudoku(
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
        techniques.LoneSingle(sudoku)


def test_hidden_single():
    sudoku = entities.Sudoku(
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

    hidden_single = techniques.HiddenSingle(sudoku)

    assert hidden_single.single == entities.Cell(position=(1, 6), value=7)

    by_position = operator.attrgetter("position")
    assert sorted(hidden_single.affected_cells, key=by_position) == [
        entities.Cell(position=(1, 6), value=7),
        entities.Mark(position=(4, 6), candidates={2, 8, 9}),
        entities.Mark(position=(6, 6), candidates={2, 4, 5, 9}),
        entities.Mark(position=(7, 6), candidates={2, 4, 5, 8}),
    ]


def test_hidden_single_not_found():
    sudoku = entities.Sudoku(
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
        techniques.HiddenSingle(sudoku)


def test_naked_pair():
    sudoku = entities.Sudoku(
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

    naked_pair = techniques.NakedPair(sudoku)

    assert naked_pair.pair == [
        entities.Mark(position=(6, 3), candidates={2, 5}),
        entities.Mark(position=(6, 6), candidates={2, 5}),
    ]

    by_position = operator.attrgetter("position")
    assert sorted(naked_pair.affected_cells, key=by_position) == [
        entities.Mark(position=(6, 0), candidates={1, 3, 4, 6}),
        entities.Mark(position=(6, 1), candidates={3, 7, 9}),
        entities.Mark(position=(6, 2), candidates={1, 3, 7}),
        entities.Mark(position=(6, 5), candidates={6, 7}),
    ]


def test_naked_pair_not_found():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(6, 0), candidates={1, 3, 4, 6}),
            entities.Mark(position=(6, 1), candidates={3, 7, 9}),
            entities.Mark(position=(6, 2), candidates={1, 3, 7}),
            entities.Mark(position=(6, 5), candidates={6, 7}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedPair(sudoku)


def test_naked_triplet():
    sudoku = entities.Sudoku(
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

    naked_triplet = techniques.NakedTriplet(sudoku)

    assert naked_triplet.triplet == [
        entities.Mark(position=(6, 7), candidates={7, 9}),
        entities.Mark(position=(8, 7), candidates={7, 8, 9}),
        entities.Mark(position=(8, 8), candidates={7, 8, 9}),
    ]

    by_position = operator.attrgetter("position")
    assert sorted(naked_triplet.affected_cells, key=by_position) == [
        entities.Mark(position=(6, 8), candidates={3, 4}),
        entities.Mark(position=(7, 8), candidates={3, 4}),
    ]


def test_naked_triplet_not_found():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(6, 8), candidates={3, 4}),
            entities.Mark(position=(7, 8), candidates={3, 4}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedTriplet(sudoku)


def test_omission():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(1, 1), candidates={4, 6}),
            entities.Mark(position=(1, 7), candidates={6, 9}),
            entities.Mark(position=(1, 8), candidates={4, 9}),
        ]
    )

    omission = techniques.Omission(sudoku)

    assert omission.omission == [
        7,
        entities.Mark(position=(3, 7), candidates={1, 5, 7}),
        entities.Mark(position=(3, 8), candidates={2, 7}),
    ]

    assert omission.affected_cells == [
        entities.Mark(position=(3, 3), candidates={1, 2})
    ]


def test_omission_not_found():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(1, 1), candidates={4, 6}),
            entities.Mark(position=(1, 7), candidates={6, 9}),
            entities.Mark(position=(1, 8), candidates={4, 9}),
            entities.Mark(position=(3, 3), candidates={1, 2}),
            entities.Mark(position=(8, 1), candidates={2, 5, 8}),
            entities.Mark(position=(8, 3), candidates={7, 9}),
            entities.Mark(position=(8, 5), candidates={7, 9}),
            entities.Mark(position=(8, 6), candidates={2, 5}),
            entities.Mark(position=(8, 7), candidates={5, 8}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        print(techniques.Omission(sudoku))


def test_xy_wing():
    sudoku = entities.Sudoku(
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

    sudoku.update_cells([entities.Mark(position=(3, 3), candidates={1, 2})])

    xy_wing = techniques.XYWing(sudoku)

    assert xy_wing.xy_wing == [
        entities.Mark(position=(5, 4), candidates={2, 5}),
        entities.Mark(position=(5, 7), candidates={1, 5}),
        entities.Mark(position=(3, 3), candidates={1, 2}),
    ]

    assert xy_wing.affected_cells == [
        entities.Mark(position=(3, 7), candidates={5, 7}),
        entities.Mark(position=(5, 3), candidates={2, 4}),
    ]


def test_xy_wing_not_found():
    sudoku = entities.Sudoku(
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
        techniques.XYWing(sudoku)


def test_unique_rectangle_in_a_row():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(8, 3), candidates={7, 9}),
            entities.Mark(position=(8, 5), candidates={7, 9}),
        ]
    )

    unique_rectangle = techniques.UniqueRectangle(sudoku)

    assert unique_rectangle.unique_rectangle == [
        entities.Mark(position=(4, 3), candidates={2, 4, 7, 9}),
        entities.Mark(position=(4, 5), candidates={7, 9}),
        entities.Mark(position=(8, 3), candidates={7, 9}),
        entities.Mark(position=(8, 5), candidates={7, 9}),
    ]

    assert unique_rectangle.affected_cells == [
        entities.Mark(position=(4, 3), candidates={2, 4})
    ]


def test_unique_rectangle_in_a_column():
    sudoku = entities.Sudoku(
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
            entities.Mark(position=(6, 0), candidates={1, 3, 4, 6}),
            entities.Mark(position=(6, 8), candidates={3, 4}),
            entities.Mark(position=(7, 0), candidates={3, 4}),
            entities.Mark(position=(7, 8), candidates={3, 4}),
        ]
    )

    unique_rectangle = techniques.UniqueRectangle(sudoku)

    assert unique_rectangle.unique_rectangle == [
        entities.Mark(position=(6, 0), candidates={1, 3, 4, 6}),
        entities.Mark(position=(6, 8), candidates={3, 4}),
        entities.Mark(position=(7, 0), candidates={3, 4}),
        entities.Mark(position=(7, 8), candidates={3, 4}),
    ]


def test_unique_rectangle_not_found():
    sudoku = entities.Sudoku(
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
        techniques.UniqueRectangle(sudoku)
