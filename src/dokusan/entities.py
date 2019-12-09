from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional, Set, Tuple


class Position(NamedTuple):
    row: int
    column: int
    box: int


class Size(NamedTuple):
    row: int = 9
    column: int = 9
    box: Tuple[int, int] = (3, 3)


@dataclass
class Cell:
    position: Position
    value: Optional[int] = None
    candidates: Set[int] = field(default_factory=set)

    def __post_init__(self):
        if self.value and self.candidates:
            raise ValueError("`value` and `candidates` attrs are mutually exclusive")


def _get_box_num(i: int, j: int, box_size: Tuple[int, int]) -> int:
    return (i // box_size[0]) * box_size[0] + (j // box_size[1])


class Sudoku:
    def __init__(self, *cells: Cell, size: Size = Size()):
        self.size = size
        self._sudoku = {
            (i, j): Cell(position=Position(i, j, _get_box_num(i, j, self.size.box)))
            for i in range(self.size.row)
            for j in range(self.size.column)
        }
        for cell in cells:
            self._sudoku[cell.position[:2]] = cell

    @classmethod
    def from_list(cls, puzzle: List[List[int]], size: Size = Size()):
        cells = []
        for i, row in enumerate(puzzle):
            for j, value in enumerate(row):
                position = Position(i, j, _get_box_num(i, j, size.box))
                cells.append(Cell(position=position, value=value if value else None,))
        return cls(*cells, size=size)

    def __getitem__(self, key: Tuple[int, int]) -> Cell:
        return self._sudoku[key]

    def update(self, cells: List[Cell]) -> None:
        for cell in cells:
            self._sudoku[cell.position.row, cell.position.column] = cell

    def cells(self) -> List[Cell]:
        return [
            self[i, j] for i in range(self.size.row) for j in range(self.size.column)
        ]

    def rows(self) -> List[List[Cell]]:
        return [
            [self[i, j] for j in range(self.size.column)] for i in range(self.size.row)
        ]

    def columns(self) -> List[List[Cell]]:
        return [
            [self[j, i] for j in range(self.size.column)] for i in range(self.size.row)
        ]

    def boxes(self) -> List[List[Cell]]:
        result: List[List[Cell]] = [[] for i in range(self.size.row)]
        for cell in self.cells():
            result[cell.position.box].append(cell)
        return result

    def groups(self) -> List[List[Cell]]:
        return self.rows() + self.columns() + self.boxes()

    def is_solved(self) -> bool:
        for group in self.groups():
            if len({cell.value for cell in group if cell.value}) != self.size.row:
                return False
        return True

    def intersection(self, *cells: Cell) -> List[Cell]:
        intersections = [
            {c.position for c in self.cells() if self.is_intersects(c, cell)}
            for cell in cells
        ]
        positions = set.intersection(*intersections)
        return [self[position.row, position.column] for position in positions]

    def is_intersects(self, cell_a: Cell, cell_b: Cell) -> bool:
        return cell_a.position != cell_b.position and (
            cell_a.position.row == cell_b.position.row
            or cell_a.position.column == cell_b.position.column
            or cell_a.position.box == cell_b.position.box
        )
