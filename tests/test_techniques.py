import operator
from typing import List

import pytest

from dokusan import techniques
from dokusan.boards import BoxSize, Cell, Position, Sudoku


def make_sudoku_with_marks(puzzle: List[List[int]], box_size: BoxSize) -> Sudoku:
    sudoku = Sudoku.from_list(puzzle, box_size=box_size)
    sudoku.update(techniques.BulkPencilMarking(sudoku).first().changes)
    return sudoku


def test_combination_as_str():
    combination = techniques.Combination(
        name="Naked Pair",
        cells=[
            Cell(position=Position(6, 3, 7), candidates={2, 5}),
            Cell(position=Position(6, 6, 8), candidates={2, 5}),
        ],
        values=[2, 5],
    )

    assert str(combination) == "Naked Pair: `2, 5` at (6, 3), (6, 6)"


def test_pencil_marking():
    sudoku = Sudoku.from_list(
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
        ],
        box_size=BoxSize(3, 3),
    )

    pencil_marks = techniques.PencilMarking(sudoku).first()
    assert pencil_marks.changes == [
        Cell(position=Position(0, 0, 0), candidates={2, 3, 5})
    ]


def test_pencil_marking_all_board():
    sudoku = Sudoku.from_list(
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
        ],
        box_size=BoxSize(3, 3),
    )

    for step in techniques.PencilMarking(sudoku):
        sudoku.update(step.changes)

    assert sudoku.is_valid()


def test_pencil_marking_corrects_invalid_mark():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update([Cell(position=Position(1, 0, 0), candidates={3, 5})])
    pencil_marks = techniques.PencilMarking(sudoku).first()
    assert pencil_marks.changes == [Cell(position=Position(1, 0, 0), candidates={5})]


def test_bulk_pencil_marking():
    sudoku = Sudoku.from_list(
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
        ],
        box_size=BoxSize(3, 3),
    )

    pencil_marks = techniques.BulkPencilMarking(sudoku).first()
    assert len(pencil_marks.changes) == 51
    assert len(list(techniques.BulkPencilMarking(sudoku))) == 1


def test_lone_single():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )
    lone_single = techniques.LoneSingle(sudoku).first()

    assert lone_single.combination.cells == [
        Cell(position=Position(1, 0, 0), candidates={5})
    ]
    assert lone_single.combination.values == [5]

    by_position = operator.attrgetter("position")
    assert sorted(lone_single.changes, key=by_position) == [
        Cell(position=Position(0, 0, 0), candidates={2, 3}),
        Cell(position=Position(0, 1, 0), candidates={2, 3, 4, 6, 8}),
        Cell(position=Position(0, 2, 0), candidates={2, 6, 8}),
        Cell(position=Position(1, 0, 0), value=5),
        Cell(position=Position(1, 1, 0), candidates={4, 6, 8, 9}),
        Cell(position=Position(1, 2, 0), candidates={1, 6, 8}),
        Cell(position=Position(1, 3, 1), candidates={4, 6, 7, 8}),
        Cell(position=Position(1, 4, 1), candidates={4, 7, 8}),
        Cell(position=Position(5, 0, 3), candidates={2, 3, 7}),
    ]


def test_lone_single_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    with pytest.raises(techniques.NotFound):
        techniques.LoneSingle(sudoku).first()


def test_hidden_single():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    hidden_single = techniques.HiddenSingle(sudoku).first()

    assert hidden_single.combination.cells == [
        Cell(position=Position(1, 6, 2), candidates={4, 7, 8})
    ]
    assert hidden_single.combination.values == [7]

    by_position = operator.attrgetter("position")
    assert sorted(hidden_single.changes, key=by_position) == [
        Cell(position=Position(1, 6, 2), value=7),
        Cell(position=Position(4, 6, 5), candidates={2, 8, 9}),
        Cell(position=Position(6, 6, 8), candidates={2, 4, 5, 9}),
        Cell(position=Position(7, 6, 8), candidates={2, 4, 5, 8}),
    ]


def test_hidden_single_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )
    with pytest.raises(techniques.NotFound):
        techniques.HiddenSingle(sudoku).first()


def test_naked_pair():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )
    naked_pair = techniques.NakedPair(sudoku).first()

    assert naked_pair.combination.cells == [
        Cell(position=Position(6, 3, 7), candidates={2, 5}),
        Cell(position=Position(6, 6, 8), candidates={2, 5}),
    ]
    assert naked_pair.combination.values == [2, 5]

    by_position = operator.attrgetter("position")
    assert sorted(naked_pair.changes, key=by_position) == [
        Cell(position=Position(6, 0, 6), candidates={1, 3, 4, 6}),
        Cell(position=Position(6, 1, 6), candidates={3, 7, 9}),
        Cell(position=Position(6, 2, 6), candidates={1, 3, 7}),
        Cell(position=Position(6, 5, 7), candidates={6, 7}),
    ]


def test_naked_pair_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )
    sudoku.update(
        [
            Cell(position=Position(6, 0, 6), candidates={1, 3, 4, 6}),
            Cell(position=Position(6, 1, 6), candidates={3, 7, 9}),
            Cell(position=Position(6, 2, 6), candidates={1, 3, 7}),
            Cell(position=Position(6, 5, 7), candidates={6, 7}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedPair(sudoku).first()


def test_naked_triplet():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    naked_triplet = techniques.NakedTriplet(sudoku).first()

    assert naked_triplet.combination.cells == [
        Cell(position=Position(6, 7, 8), candidates={7, 9}),
        Cell(position=Position(8, 7, 8), candidates={7, 8, 9}),
        Cell(position=Position(8, 8, 8), candidates={7, 8, 9}),
    ]
    assert naked_triplet.combination.values == [7, 8, 9]

    by_position = operator.attrgetter("position")
    assert sorted(naked_triplet.changes, key=by_position) == [
        Cell(position=Position(6, 8, 8), candidates={3, 4}),
        Cell(position=Position(7, 8, 8), candidates={3, 4}),
    ]


def test_naked_triplet_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update(
        [
            Cell(position=Position(6, 8, 8), candidates={3, 4}),
            Cell(position=Position(7, 8, 8), candidates={3, 4}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.NakedTriplet(sudoku).first()


def test_locked_candidate_in_a_box():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update(
        [
            Cell(position=Position(1, 1, 0), candidates={4, 6}),
            Cell(position=Position(1, 7, 2), candidates={6, 9}),
            Cell(position=Position(1, 8, 2), candidates={4, 9}),
            Cell(position=Position(8, 3, 7), candidates={7, 9}),
            Cell(position=Position(8, 7, 8), candidates={5, 8}),
        ]
    )

    locked_candidate = techniques.LockedCandidate(sudoku).first()

    assert locked_candidate.combination.cells == [
        Cell(position=Position(3, 7, 5), candidates={1, 5, 7}),
        Cell(position=Position(3, 8, 5), candidates={2, 7}),
    ]
    assert locked_candidate.combination.values == [7]

    assert locked_candidate.changes == [
        Cell(position=Position(3, 3, 4), candidates={1, 2})
    ]


def test_locked_candidate_in_a_row():
    sudoku = make_sudoku_with_marks(
        [
            [9, 0, 0, 5, 3, 1, 2, 8, 0],
            [0, 2, 5, 7, 0, 4, 9, 3, 0],
            [0, 3, 0, 0, 0, 2, 0, 4, 0],
            [4, 8, 1, 2, 5, 7, 6, 9, 3],
            [3, 5, 9, 0, 0, 8, 0, 0, 2],
            [7, 6, 2, 3, 1, 9, 8, 5, 4],
            [0, 1, 0, 0, 0, 0, 0, 6, 8],
            [6, 0, 8, 1, 0, 5, 3, 0, 0],
            [0, 0, 3, 8, 7, 6, 0, 0, 0],
        ],
        box_size=BoxSize(3, 3),
    )

    locked_candidate = techniques.LockedCandidate(sudoku).first()

    assert locked_candidate.combination.cells == [
        Cell(position=Position(6, 3, 7), candidates={4, 9}),
        Cell(position=Position(6, 4, 7), candidates={2, 4, 9}),
    ]
    assert locked_candidate.combination.values == [9]

    assert locked_candidate.changes == [
        Cell(position=Position(7, 4, 7), candidates={2, 4})
    ]


def test_locked_candidate_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update(
        [
            Cell(position=Position(1, 1, 0), candidates={4, 6}),
            Cell(position=Position(1, 7, 2), candidates={6, 9}),
            Cell(position=Position(1, 8, 2), candidates={4, 9}),
            Cell(position=Position(3, 3, 4), candidates={1, 2}),
            Cell(position=Position(8, 1, 6), candidates={2, 5, 8}),
            Cell(position=Position(8, 3, 7), candidates={7, 9}),
            Cell(position=Position(8, 5, 7), candidates={7, 9}),
            Cell(position=Position(8, 6, 8), candidates={2, 5}),
            Cell(position=Position(8, 7, 8), candidates={5, 8}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.LockedCandidate(sudoku).first()


def test_xy_wing():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update([Cell(position=Position(3, 3, 4), candidates={1, 2})])

    xy_wing = techniques.XYWing(sudoku).first()

    assert xy_wing.combination.cells == [
        Cell(position=Position(3, 3, 4), candidates={1, 2}),
        Cell(position=Position(5, 4, 4), candidates={2, 5}),
        Cell(position=Position(5, 7, 5), candidates={1, 5}),
    ]
    assert xy_wing.combination.values == [1]
    assert xy_wing.changes == [
        Cell(position=Position(3, 7, 5), candidates={5, 7}),
        Cell(position=Position(5, 3, 4), candidates={2, 4}),
    ]


def test_xy_wing_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    with pytest.raises(techniques.NotFound):
        techniques.XYWing(sudoku).first()


def test_unique_rectangle():
    sudoku = make_sudoku_with_marks(
        [
            [0, 6, 0, 8, 0, 2, 3, 7, 1],
            [3, 0, 7, 1, 6, 5, 8, 0, 4],
            [0, 8, 1, 3, 7, 0, 5, 6, 0],
            [8, 7, 4, 9, 2, 3, 1, 5, 6],
            [9, 1, 3, 6, 5, 8, 2, 4, 7],
            [6, 0, 0, 4, 1, 7, 9, 3, 8],
            [0, 3, 8, 0, 0, 0, 6, 1, 5],
            [0, 0, 6, 0, 8, 1, 4, 0, 3],
            [1, 4, 0, 5, 3, 6, 7, 8, 0],
        ],
        box_size=BoxSize(3, 3),
    )

    assert len(list(techniques.UniqueRectangle(sudoku))) == 1

    unique_rectangle = techniques.UniqueRectangle(sudoku).first()
    assert unique_rectangle.combination.cells == [
        Cell(position=Position(6, 0, 6), candidates={2, 7}),
        Cell(position=Position(6, 3, 7), candidates={2, 7}),
        Cell(position=Position(7, 0, 6), candidates={2, 5, 7}),
        Cell(position=Position(7, 3, 7), candidates={2, 7}),
    ]
    assert unique_rectangle.combination.values == [2, 7]
    assert unique_rectangle.changes == [
        Cell(position=Position(7, 0, 6), candidates={5}),
    ]


def test_unique_rectangle_block_apart():
    sudoku = make_sudoku_with_marks(
        [
            [9, 0, 1, 0, 3, 0, 5, 0, 0],
            [0, 0, 7, 8, 1, 9, 0, 0, 0],
            [0, 2, 0, 4, 5, 6, 1, 9, 7],
            [1, 0, 2, 9, 0, 0, 6, 0, 5],
            [0, 0, 0, 6, 7, 1, 0, 2, 4],
            [6, 0, 0, 3, 2, 5, 8, 0, 0],
            [0, 1, 5, 0, 9, 0, 4, 6, 3],
            [0, 0, 6, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 6, 3, 0, 5, 0],
        ],
        box_size=BoxSize(3, 3),
    )

    unique_rectangle = techniques.UniqueRectangle(sudoku).first()
    assert unique_rectangle.combination.cells == [
        Cell(position=Position(0, 3, 1), candidates={2, 7}),
        Cell(position=Position(0, 5, 1), candidates={2, 7}),
        Cell(position=Position(6, 3, 7), candidates={2, 7}),
        Cell(position=Position(6, 5, 7), candidates={2, 7, 8}),
    ]

    assert unique_rectangle.changes == [
        Cell(position=Position(6, 5, 7), candidates={8})
    ]


def test_unique_rectangle_not_found():
    sudoku = make_sudoku_with_marks(
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
        ],
        box_size=BoxSize(3, 3),
    )

    sudoku.update(
        [
            Cell(position=Position(6, 0, 6), candidates={1, 6}),
            Cell(position=Position(6, 8, 8), candidates={3, 4}),
            Cell(position=Position(7, 0, 6), candidates={3, 4}),
            Cell(position=Position(7, 8, 8), candidates={3, 4}),
        ]
    )

    with pytest.raises(techniques.NotFound):
        techniques.UniqueRectangle(sudoku).first()
