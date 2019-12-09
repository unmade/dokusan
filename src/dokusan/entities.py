from dataclasses import dataclass, field
from typing import Dict, List, NamedTuple, Optional, Set, Tuple


class Position(NamedTuple):
    row: int
    column: int
    box: int


@dataclass
class Cell:
    position: Position
    value: Optional[int] = None
    candidates: Set[int] = field(default_factory=set)

    def __post_init__(self):
        if self.value and self.candidates:
            raise ValueError("`value` and `candidates` attrs are mutually exclusive")


class Sudoku:
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.size_n = len(puzzle)
        self.size_m = len(puzzle[0])
        self.box_size = 3
        self._sudoku = self._build_sudoku(puzzle)

    def __getitem__(self, key: Tuple[int, int]) -> Cell:
        return self._sudoku[key]

    def _build_sudoku(self, puzzle: List[List[int]]) -> Dict[Tuple[int, int], Cell]:
        sudoku = {}
        for i, row in enumerate(puzzle):
            for j, value in enumerate(row):
                position = Position(i, j, self._get_box_num(i, j))
                sudoku[i, j] = Cell(
                    position=position,
                    value=value if value else None,
                    candidates=set() if value else self._get_candidates_for(position),
                )
        return sudoku

    def update(self, cells: List[Cell]) -> None:
        for cell in cells:
            self._sudoku[cell.position.row, cell.position.column] = cell

    def cells(self) -> List[Cell]:
        return [self[i, j] for i in range(self.size_n) for j in range(self.size_m)]

    def rows(self) -> List[List[Cell]]:
        return [[self[i, j] for j in range(self.size_m)] for i in range(self.size_n)]

    def columns(self) -> List[List[Cell]]:
        return [[self[j, i] for j in range(self.size_m)] for i in range(self.size_n)]

    def boxes(self) -> List[List[Cell]]:
        result: List[List[Cell]] = [[] for i in range(self.size_n)]
        for cell in self.cells():
            result[cell.position.box].append(cell)
        return result

    def groups(self) -> List[List[Cell]]:
        return self.rows() + self.columns() + self.boxes()

    def _get_candidates_for(self, position: Position) -> Set[int]:
        known_values = set(
            self.puzzle[position.row]
            + [self.puzzle[i][position.column] for i in range(self.size_n)]
            + [
                self.puzzle[i][j]
                for i in range(self.size_n)
                for j in range(self.size_m)
                if self._get_box_num(i, j) == position.box
            ]
        )
        return set(range(1, 10)) - known_values

    def _get_box_num(self, i: int, j: int) -> int:
        return (i // self.box_size) * 3 + (j // self.box_size)

    def is_solved(self) -> bool:
        for group in self.groups():
            if len({cell.value for cell in group if cell.value}) != self.size_n:
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
