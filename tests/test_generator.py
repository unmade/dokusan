import pytest
from dokusan import generator
from dokusan.entities import Sudoku


@pytest.mark.slow
def test_generate():
    sudoku = generator.generate()
    assert sudoku.is_valid() is True
    assert sudoku.is_solved() is False
    assert 15 < len([c for c in sudoku.cells() if c.value]) < 35


@pytest.mark.slow
def test_generate_returns_different_sudoku_every_call():
    generator.generate().cells() != generator.generate().cells()


def test_generate_initial_cells():
    cells = generator._generate_initial_cells()
    assert len(cells) == 15

    sudoku = Sudoku(*cells)
    assert sudoku.is_valid() is True
    assert sudoku.is_solved() is False


def test_generate_initial_cells_returns_different_cells_every_call():
    generator._generate_initial_cells() != generator._generate_initial_cells()
