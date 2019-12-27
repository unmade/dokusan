import random
from typing import List

from dokusan import exceptions, solvers, stats
from dokusan.entities import BoxSize, Cell, Position, Sudoku

MAX_ITERATIONS = 300


def random_sudoku(avg_rank: int = 150, box_size: BoxSize = BoxSize(3, 3)) -> Sudoku:
    sudoku = Sudoku(*_random_initial_cells(box_size), box_size=box_size)
    solution = solvers.backtrack(sudoku)

    best_sudoku = Sudoku(*solution.cells(), box_size=box_size)
    best_rank = 0

    iterations = min(avg_rank, MAX_ITERATIONS)
    for i in range(iterations):
        size = random.randint(1, 2)
        rows = [random.randint(0, solution.size - 1) for _ in range(size)]
        columns = [random.randint(0, solution.size - 1) for _ in range(size)]
        cells = [solution[row, column] for (row, column) in zip(rows, columns)]
        if all(cell.value for cell in cells):
            solution.update([Cell(position=cell.position) for cell in cells])
            try:
                rank = stats.rank(solution)
            except exceptions.MultipleSolutions:
                solution.update(cells)
                continue
            if rank > best_rank:
                best_sudoku = Sudoku(*solution.cells(), box_size=box_size)
                best_rank = rank
                continue

    return best_sudoku


def _random_initial_cells(box_size: BoxSize) -> List[Cell]:
    size = box_size.width * box_size.length
    all_values = set(range(1, size + 1))

    values = random.sample(all_values, k=size)
    box_values = [
        values[i * box_size.length : i * box_size.length + box_size.length]
        for i in range(box_size.width)
    ]

    while True:
        row_values = random.sample(all_values - set(box_values[0]), k=box_size.length)
        used_values = [sorted(box_values[i]) for i in range(1, box_size.width)]
        if sorted(row_values) not in used_values:
            break

    row_values += random.sample(
        all_values.difference(box_values[0], row_values), k=box_size.length
    )

    return [
        Cell(
            position=Position(row=i, column=j, box=box_size.sequential(i, j)),
            value=box_values[i][j],
        )
        for i in range(box_size.width)
        for j in range(box_size.length)
    ] + [
        Cell(
            position=Position(row=0, column=i, box=box_size.sequential(0, i)),
            value=value,
        )
        for i, value in enumerate(row_values, start=box_size.length)
    ]
