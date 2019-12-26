# flake8: noqa

import pytest
from dokusan import entities, output


@pytest.fixture
def puzzle():
    return [
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


def test_plain(puzzle):
    expected = (
        "┌───┬───┬───╥───┬───┬───╥───┬───┬───┐\n"
        "│ 9 │   │ 6 ║ 7 │   │ 5 ║   │   │   │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│   │   │   ║   │   │ 9 ║   │ 2 │ 5 │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│ 7 │ 4 │   ║   │   │ 1 ║   │   │   │\n"
        "╞═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╡\n"
        "│   │ 1 │   ║   │   │   ║ 6 │ 4 │   │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│ 5 │   │   ║   │   │   ║   │   │   │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│ 8 │ 6 │ 9 ║ 1 │   │   ║ 3 │   │   │\n"
        "╞═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╡\n"
        "│   │   │   ║   │ 8 │   ║   │   │   │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│   │   │   ║ 9 │   │   ║   │ 6 │   │\n"
        "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
        "│   │   │   ║ 4 │   │ 3 ║ 1 │   │   │\n"
        "└───┴───┴───╨───┴───┴───╨───┴───┴───┘\n"
    )
    assert output.plain(puzzle) == expected


def test_colorful(puzzle):
    expected = (
        "┌─────────┬─────────┬─────────╥─────────┬─────────┬─────────╥─────────┬─────────┬─────────┐\n"
        "│         │    \033[93m2\033[0m  \033[93m3\033[0m │         ║         │    \033[93m2\033[0m  \033[93m3\033[0m │         ║         │ \033[93m1\033[0m     \033[93m3\033[0m │ \033[93m1\033[0m     \033[93m3\033[0m │\n"
        "│    \033[;1m9\033[0m    │         │    \033[;1m6\033[0m    ║    \033[;1m7\033[0m    │ \033[93m4\033[0m       │    \033[;1m5\033[0m    ║ \033[93m4\033[0m       │         │ \033[93m4\033[0m       │\n"
        "│         │    \033[93m8\033[0m    │         ║         │         │         ║    \033[93m8\033[0m    │    \033[93m8\033[0m    │    \033[93m8\033[0m    │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│ \033[93m1\033[0m     \033[93m3\033[0m │       \033[93m3\033[0m │ \033[93m1\033[0m     \033[93m3\033[0m ║       \033[93m3\033[0m │       \033[93m3\033[0m │         ║         │         │         │\n"
        "│         │         │         ║       \033[93m6\033[0m │ \033[93m4\033[0m     \033[93m6\033[0m │    \033[;1m9\033[0m    ║ \033[93m4\033[0m       │    \033[;1m2\033[0m    │    \033[;1m5\033[0m    │\n"
        "│         │    \033[93m8\033[0m    │    \033[93m8\033[0m    ║    \033[93m8\033[0m    │         │         ║ \033[93m7\033[0m  \033[93m8\033[0m    │         │         │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│         │         │    \033[93m2\033[0m  \033[93m3\033[0m ║    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │         ║         │       \033[93m3\033[0m │       \033[93m3\033[0m │\n"
        "│    \033[;1m7\033[0m    │    \033[;1m4\033[0m    │    \033[93m5\033[0m    ║       \033[93m6\033[0m │       \033[93m6\033[0m │    \033[;1m1\033[0m    ║         │         │       \033[93m6\033[0m │\n"
        "│         │         │    \033[93m8\033[0m    ║    \033[93m8\033[0m    │         │         ║    \033[93m8\033[0m  \033[93m9\033[0m │    \033[93m8\033[0m  \033[93m9\033[0m │    \033[93m8\033[0m  \033[93m9\033[0m │\n"
        "╞═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╡\n"
        "│    \033[93m2\033[0m  \033[93m3\033[0m │         │    \033[93m2\033[0m  \033[93m3\033[0m ║    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m    ║         │         │    \033[93m2\033[0m    │\n"
        "│         │    \033[;1m1\033[0m    │         ║    \033[93m5\033[0m    │    \033[93m5\033[0m    │         ║    \033[;1m6\033[0m    │    \033[;1m4\033[0m    │         │\n"
        "│         │         │ \033[93m7\033[0m       ║    \033[93m8\033[0m    │ \033[93m7\033[0m     \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m    ║         │         │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│         │    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m ║    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m    ║    \033[93m2\033[0m    │ \033[93m1\033[0m       │ \033[93m1\033[0m  \033[93m2\033[0m    │\n"
        "│    \033[;1m5\033[0m    │         │ \033[93m4\033[0m       ║       \033[93m6\033[0m │ \033[93m4\033[0m     \033[93m6\033[0m │ \033[93m4\033[0m     \033[93m6\033[0m ║         │         │         │\n"
        "│         │ \033[93m7\033[0m       │ \033[93m7\033[0m       ║    \033[93m8\033[0m    │ \033[93m7\033[0m     \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m    ║ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│         │         │         ║         │    \033[93m2\033[0m    │    \033[93m2\033[0m    ║         │         │    \033[93m2\033[0m    │\n"
        "│    \033[;1m8\033[0m    │    \033[;1m6\033[0m    │    \033[;1m9\033[0m    ║    \033[;1m1\033[0m    │ \033[93m4\033[0m  \033[93m5\033[0m    │ \033[93m4\033[0m       ║    \033[;1m3\033[0m    │    \033[93m5\033[0m    │         │\n"
        "│         │         │         ║         │ \033[93m7\033[0m       │ \033[93m7\033[0m       ║         │ \033[93m7\033[0m       │ \033[93m7\033[0m       │\n"
        "╞═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╡\n"
        "│ \033[93m1\033[0m  \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │ \033[93m1\033[0m  \033[93m2\033[0m  \033[93m3\033[0m ║    \033[93m2\033[0m    │         │    \033[93m2\033[0m    ║    \033[93m2\033[0m    │       \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │\n"
        "│ \033[93m4\033[0m     \033[93m6\033[0m │    \033[93m5\033[0m    │ \033[93m4\033[0m  \033[93m5\033[0m    ║    \033[93m5\033[0m  \033[93m6\033[0m │    \033[;1m8\033[0m    │       \033[93m6\033[0m ║ \033[93m4\033[0m  \033[93m5\033[0m    │    \033[93m5\033[0m    │ \033[93m4\033[0m       │\n"
        "│         │ \033[93m7\033[0m     \033[93m9\033[0m │ \033[93m7\033[0m       ║         │         │ \033[93m7\033[0m       ║ \033[93m7\033[0m     \033[93m9\033[0m │ \033[93m7\033[0m     \033[93m9\033[0m │ \033[93m7\033[0m     \033[93m9\033[0m │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│ \033[93m1\033[0m  \033[93m2\033[0m  \033[93m3\033[0m │    \033[93m2\033[0m  \033[93m3\033[0m │ \033[93m1\033[0m  \033[93m2\033[0m  \033[93m3\033[0m ║         │ \033[93m1\033[0m  \033[93m2\033[0m    │    \033[93m2\033[0m    ║    \033[93m2\033[0m    │         │    \033[93m2\033[0m  \033[93m3\033[0m │\n"
        "│ \033[93m4\033[0m       │    \033[93m5\033[0m    │ \033[93m4\033[0m  \033[93m5\033[0m    ║    \033[;1m9\033[0m    │    \033[93m5\033[0m    │         ║ \033[93m4\033[0m  \033[93m5\033[0m    │    \033[;1m6\033[0m    │ \033[93m4\033[0m       │\n"
        "│         │ \033[93m7\033[0m  \033[93m8\033[0m    │ \033[93m7\033[0m  \033[93m8\033[0m    ║         │ \033[93m7\033[0m       │ \033[93m7\033[0m       ║ \033[93m7\033[0m  \033[93m8\033[0m    │         │ \033[93m7\033[0m  \033[93m8\033[0m    │\n"
        "├─────────┼─────────┼─────────╫─────────┼─────────┼─────────╫─────────┼─────────┼─────────┤\n"
        "│    \033[93m2\033[0m    │    \033[93m2\033[0m    │    \033[93m2\033[0m    ║         │    \033[93m2\033[0m    │         ║         │         │    \033[93m2\033[0m    │\n"
        "│       \033[93m6\033[0m │    \033[93m5\033[0m    │    \033[93m5\033[0m    ║    \033[;1m4\033[0m    │    \033[93m5\033[0m  \033[93m6\033[0m │    \033[;1m3\033[0m    ║    \033[;1m1\033[0m    │    \033[93m5\033[0m    │         │\n"
        "│         │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m    ║         │ \033[93m7\033[0m       │         ║         │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │ \033[93m7\033[0m  \033[93m8\033[0m  \033[93m9\033[0m │\n"
        "└─────────┴─────────┴─────────╨─────────┴─────────┴─────────╨─────────┴─────────┴─────────┘\n"
    )

    sudoku = entities.Sudoku.from_list(puzzle, box_size=entities.BoxSize(3, 3))
    sudoku.update(
        [
            entities.Cell(position=entities.Position(0, 1, 0), candidates={8, 2, 3}),
            entities.Cell(position=entities.Position(0, 4, 1), candidates={2, 3, 4}),
            entities.Cell(position=entities.Position(0, 6, 2), candidates={8, 4}),
            entities.Cell(position=entities.Position(0, 7, 2), candidates={8, 1, 3}),
            entities.Cell(position=entities.Position(0, 8, 2), candidates={8, 1, 3, 4}),
            entities.Cell(position=entities.Position(1, 0, 0), candidates={1, 3}),
            entities.Cell(position=entities.Position(1, 1, 0), candidates={8, 3}),
            entities.Cell(position=entities.Position(1, 2, 0), candidates={8, 1, 3}),
            entities.Cell(position=entities.Position(1, 3, 1), candidates={8, 3, 6}),
            entities.Cell(position=entities.Position(1, 4, 1), candidates={3, 4, 6}),
            entities.Cell(position=entities.Position(1, 6, 2), candidates={8, 4, 7}),
            entities.Cell(position=entities.Position(2, 2, 0), candidates={8, 2, 3, 5}),
            entities.Cell(position=entities.Position(2, 3, 1), candidates={8, 2, 3, 6}),
            entities.Cell(position=entities.Position(2, 4, 1), candidates={2, 3, 6}),
            entities.Cell(position=entities.Position(2, 6, 2), candidates={8, 9}),
            entities.Cell(position=entities.Position(2, 7, 2), candidates={8, 9, 3}),
            entities.Cell(position=entities.Position(2, 8, 2), candidates={8, 9, 3, 6}),
            entities.Cell(position=entities.Position(3, 0, 3), candidates={2, 3}),
            entities.Cell(position=entities.Position(3, 2, 3), candidates={2, 3, 7}),
            entities.Cell(position=entities.Position(3, 3, 4), candidates={8, 2, 3, 5}),
            entities.Cell(
                position=entities.Position(3, 4, 4), candidates={2, 3, 5, 7, 9}
            ),
            entities.Cell(position=entities.Position(3, 5, 4), candidates={8, 2, 7}),
            entities.Cell(position=entities.Position(3, 8, 5), candidates={8, 9, 2, 7}),
            entities.Cell(position=entities.Position(4, 1, 3), candidates={2, 3, 7}),
            entities.Cell(position=entities.Position(4, 2, 3), candidates={2, 3, 4, 7}),
            entities.Cell(position=entities.Position(4, 3, 4), candidates={8, 2, 3, 6}),
            entities.Cell(
                position=entities.Position(4, 4, 4), candidates={2, 3, 4, 6, 7, 9}
            ),
            entities.Cell(
                position=entities.Position(4, 5, 4), candidates={2, 4, 6, 7, 8}
            ),
            entities.Cell(position=entities.Position(4, 6, 5), candidates={8, 9, 2, 7}),
            entities.Cell(position=entities.Position(4, 7, 5), candidates={8, 1, 9, 7}),
            entities.Cell(
                position=entities.Position(4, 8, 5), candidates={1, 2, 7, 8, 9}
            ),
            entities.Cell(position=entities.Position(5, 4, 4), candidates={2, 4, 5, 7}),
            entities.Cell(position=entities.Position(5, 5, 4), candidates={2, 4, 7}),
            entities.Cell(position=entities.Position(5, 7, 5), candidates={5, 7}),
            entities.Cell(position=entities.Position(5, 8, 5), candidates={2, 7}),
            entities.Cell(
                position=entities.Position(6, 0, 6), candidates={1, 2, 3, 4, 6}
            ),
            entities.Cell(
                position=entities.Position(6, 1, 6), candidates={2, 3, 5, 7, 9}
            ),
            entities.Cell(
                position=entities.Position(6, 2, 6), candidates={1, 2, 3, 4, 5, 7}
            ),
            entities.Cell(position=entities.Position(6, 3, 7), candidates={2, 5, 6}),
            entities.Cell(position=entities.Position(6, 5, 7), candidates={2, 6, 7}),
            entities.Cell(
                position=entities.Position(6, 6, 8), candidates={2, 4, 5, 7, 9}
            ),
            entities.Cell(position=entities.Position(6, 7, 8), candidates={9, 3, 5, 7}),
            entities.Cell(
                position=entities.Position(6, 8, 8), candidates={2, 3, 4, 7, 9}
            ),
            entities.Cell(position=entities.Position(7, 0, 6), candidates={1, 2, 3, 4}),
            entities.Cell(
                position=entities.Position(7, 1, 6), candidates={2, 3, 5, 7, 8}
            ),
            entities.Cell(
                position=entities.Position(7, 2, 6), candidates={1, 2, 3, 4, 5, 7, 8}
            ),
            entities.Cell(position=entities.Position(7, 4, 7), candidates={1, 2, 5, 7}),
            entities.Cell(position=entities.Position(7, 5, 7), candidates={2, 7}),
            entities.Cell(
                position=entities.Position(7, 6, 8), candidates={2, 4, 5, 7, 8}
            ),
            entities.Cell(
                position=entities.Position(7, 8, 8), candidates={2, 3, 4, 7, 8}
            ),
            entities.Cell(position=entities.Position(8, 0, 6), candidates={2, 6}),
            entities.Cell(
                position=entities.Position(8, 1, 6), candidates={2, 5, 7, 8, 9}
            ),
            entities.Cell(position=entities.Position(8, 2, 6), candidates={8, 2, 5, 7}),
            entities.Cell(position=entities.Position(8, 4, 7), candidates={2, 5, 6, 7}),
            entities.Cell(position=entities.Position(8, 7, 8), candidates={8, 9, 5, 7}),
            entities.Cell(position=entities.Position(8, 8, 8), candidates={8, 9, 2, 7}),
        ]
    )

    assert output.colorful(sudoku) == expected
