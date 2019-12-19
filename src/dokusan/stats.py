import operator

from dokusan import exceptions, solvers
from dokusan.entities import Cell, Sudoku


def rank(sudoku: Sudoku) -> int:
    total_solutions = 0
    total_branch_factor = 0

    def count(sudoku: Sudoku) -> None:
        nonlocal total_solutions
        nonlocal total_branch_factor
        _sudoku = solvers.eliminate(sudoku)

        if not _sudoku.is_valid():
            raise exceptions.InvalidSudoku

        cells = sorted(
            (cell for cell in _sudoku.cells() if not cell.value),
            key=operator.attrgetter("candidates"),
        )

        for cell in cells:
            branch_factor = len(cell.candidates)
            for candidate in cell.candidates:
                _sudoku.update([Cell(position=cell.position, value=candidate)])
                try:
                    count(_sudoku)
                except (exceptions.InvalidSudoku, exceptions.NoCandidates):
                    pass
                else:
                    total_solutions += 1
                    if total_solutions > 1:
                        raise exceptions.MultipleSolutions
                    total_branch_factor += pow(branch_factor - 1, 2)
                _sudoku.update([cell])
            else:
                raise exceptions.NoCandidates

    try:
        count(sudoku)
    except exceptions.NoCandidates:
        pass

    return (total_branch_factor * 100) + sum(1 for c in sudoku.cells() if not c.value)
