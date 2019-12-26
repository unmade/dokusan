import operator
from typing import Iterator

from dokusan import exceptions, techniques
from dokusan.entities import Cell, Sudoku
from dokusan.techniques import Step


def eliminate(sudoku: Sudoku) -> Sudoku:
    _sudoku = Sudoku(*sudoku.cells(), box_size=sudoku.box_size)

    all_techniques = (
        techniques.LoneSingle,
        techniques.HiddenSingle,
    )

    for step in techniques.BulkPencilMarking(_sudoku):
        _sudoku.update(step.changes)

    has_result = True
    while has_result:
        for technique in all_techniques:
            has_result = False
            for step in technique(_sudoku):
                _sudoku.update(step.changes)
                has_result = True
    return _sudoku


def backtrack(sudoku: Sudoku) -> Sudoku:
    _sudoku = eliminate(sudoku)

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


def steps(sudoku: Sudoku) -> Iterator[Step]:
    _sudoku = Sudoku(*sudoku.cells(), box_size=sudoku.box_size)

    all_techniques = (
        techniques.LoneSingle,
        techniques.HiddenSingle,
        techniques.NakedPair,
        techniques.NakedTriplet,
        techniques.LockedCandidate,
        techniques.XYWing,
        techniques.UniqueRectangle,
    )

    for step in techniques.BulkPencilMarking(_sudoku):
        _sudoku.update(step.changes)
        yield step

    while not _sudoku.is_solved():
        for technique in all_techniques:
            try:
                step = technique(_sudoku).first()
            except techniques.NotFound:
                continue
            else:
                _sudoku.update(step.changes)
                yield step
                break
        else:
            raise exceptions.Unsolvable
