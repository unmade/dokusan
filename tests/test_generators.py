import pytest
from dokusan import generators
from dokusan.boards import BoxSize, Sudoku


@pytest.mark.slow
def test_random_sudoku():
    sudoku = generators.random_sudoku()
    assert sudoku.is_valid() is True
    assert sudoku.is_solved() is False
    assert 15 < len([c for c in sudoku.cells() if c.value]) < 35


@pytest.mark.slow
def test_random_sudoku_returns_different_sudoku_every_call():
    generators.random_sudoku().cells() != generators.random_sudoku().cells()


def test_random_initial_cells():
    box_size = BoxSize(3, 3)
    cells = generators._random_initial_cells(box_size)
    assert len(cells) == 15

    sudoku = Sudoku(*cells, box_size=box_size)
    assert sudoku.is_valid() is True
    assert sudoku.is_solved() is False


def test_random_initial_cells_returns_different_cells_every_call():
    size = BoxSize(3, 3)
    generators._random_initial_cells(size) != generators._random_initial_cells(size)
