import pytest
from dokusan import exceptions, solvers
from dokusan.entities import BoxSize, Sudoku


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
        ],
        box_size=BoxSize(3, 3),
    )

    solution = solvers.eliminate(given)
    assert str(solution) == (
        "200593100"
        "501002300"
        "397641825"
        "604038900"
        "810000036"
        "739006008"
        "170304600"
        "900015743"
        "403060001"
    )


def test_backtrack():
    given = Sudoku.from_list(
        [
            [0, 0, 0, 8, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 3],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 2, 0, 0, 3, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 7, 5],
            [0, 0, 3, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 6, 0, 0],
        ],
        box_size=BoxSize(3, 3),
    )
    solution = solvers.backtrack(given)
    assert solution.is_solved() is True
    assert solution.is_valid() is True
    assert str(solution) == (
        "237841569"
        "186795243"
        "594326718"
        "315674892"
        "469582137"
        "728139456"
        "642918375"
        "853467921"
        "971253684"
    )


def test_steps():
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
        ],
        box_size=BoxSize(3, 3),
    )

    assert [step.combination.name for step in solvers.steps(given)] == [
        "Bulk Pencil Marking",
        *["Lone Single"] * 8,
        *["Hidden Single"] * 7,
        "Lone Single",
        "Hidden Single",
        *["Naked Pair"] * 3,
        "Locked Candidate",
        "XY Wing",
        *["Hidden Single"] * 2,
        "Unique Rectangle",
        "Hidden Single",
        *["Lone Single"] * 2,
        "Hidden Single",
        *["Lone Single"] * 28,
    ]


def test_steps_raises_unsolvable():
    given = Sudoku.from_list(
        [
            [7, 0, 0, 0, 8, 2, 5, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 7, 0, 2, 6],
            [0, 0, 8, 0, 9, 0, 0, 7, 5],
            [3, 0, 0, 6, 7, 5, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 9, 0],
            [9, 0, 1, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 0, 3],
            [6, 0, 2, 0, 0, 0, 0, 0, 0],
        ],
        box_size=BoxSize(3, 3),
    )

    with pytest.raises(exceptions.Unsolvable):
        list(solvers.steps(given))
