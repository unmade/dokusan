import pytest
from dokusan import generators
from dokusan.entities import Sudoku


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
    cells = generators._random_initial_cells()
    assert len(cells) == 15

    sudoku = Sudoku(*cells)
    assert sudoku.is_valid() is True
    assert sudoku.is_solved() is False


def test_random_initial_cells_returns_different_cells_every_call():
    generators._random_initial_cells() != generators._random_initial_cells()
