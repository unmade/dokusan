import operator

from dokusan import exceptions, techniques
from dokusan.entities import Cell, Sudoku


def eliminate(sudoku: Sudoku) -> Sudoku:
    _sudoku = Sudoku(*sudoku.cells(), box_size=sudoku.box_size)
    all_techniques = (
        techniques.PencilMarking,
        techniques.LoneSingle,
        techniques.HiddenSingle,
    )
    has_result = True
    while has_result:
        for technique in all_techniques:
            has_result = False
            for result in technique(_sudoku):
                _sudoku.update(result.changes)
                has_result = True
    return _sudoku


def backtrack(sudoku: Sudoku) -> Sudoku:
    _sudoku = eliminate(sudoku)

    if not _sudoku.is_valid():
        raise exceptions.InvalidSudoku

    cells = sorted(
        (cell for cell in _sudoku.cells() if not cell.value),
        key=operator.attrgetter("candidates"),
    )

    for cell in cells:
        for candidate in cell.candidates:
            _sudoku.update([Cell(position=cell.position, value=candidate)])
            try:
                return backtrack(_sudoku)
            except (exceptions.InvalidSudoku, exceptions.NoCandidates):
                pass
            _sudoku.update([cell])
        else:
            raise exceptions.NoCandidates

    return _sudoku
