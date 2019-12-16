import itertools
import operator

from dokusan import techniques
from dokusan.entities import Cell, Sudoku


class CandidatesMismatch(Exception):
    pass


def backtrack(sudoku: Sudoku) -> Sudoku:
    _sudoku = Sudoku(*sudoku.cells())

    for result in itertools.chain(
        techniques.PencilMarking(_sudoku),
        techniques.LoneSingle(_sudoku),
        techniques.HiddenSingle(_sudoku),
    ):
        _sudoku.update(result.changes)

    if not _sudoku.is_valid():
        raise CandidatesMismatch

    cells = sorted(
        (cell for cell in _sudoku.cells() if not cell.value),
        key=operator.attrgetter("candidates"),
    )

    for cell in cells:
        for candidate in cell.candidates:
            _sudoku.update([Cell(position=cell.position, value=candidate)])
            try:
                return backtrack(_sudoku)
            except CandidatesMismatch:
                pass
            _sudoku.update([cell])
        else:
            raise CandidatesMismatch

    return _sudoku
