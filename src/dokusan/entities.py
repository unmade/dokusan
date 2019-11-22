from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Set, Tuple, Union


class Position(NamedTuple):
    row: int
    column: int
    square: int


@dataclass
class Cell:
    position: Position
    value: int


@dataclass
class Mark:
    position: Position
    candidates: Set[int]


class Sudoku:
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.size_n = len(puzzle)
        self.size_m = len(puzzle[0])
        self.square_size = 3
        self._sudoku = self._build_sudoku(puzzle)

    def __getitem__(self, key: Tuple[int, int]) -> Union[Cell, Mark]:
        return self._sudoku[key]

    def _build_sudoku(
        self, puzzle: List[List[int]]
    ) -> Dict[Tuple[int, int], Union[Cell, Mark]]:
        sudoku: Dict[Tuple[int, int], Union[Cell, Mark]] = {}
        for i, row in enumerate(puzzle):
            for j, value in enumerate(row):
                position = Position(row=i, column=j, square=self._get_square_num(i, j))
                if value:
                    sudoku[i, j] = Cell(position=position, value=value)
                else:
                    sudoku[i, j] = Mark(
                        position=position,
                        candidates=self._get_candidates_for(position),
                    )
        return sudoku

    def update_cells(self, cells: List[Union[Cell, Mark]]):
        for cell in cells:
            self._sudoku[cell.position.row, cell.position.column] = cell

    def cells(self) -> List[Union[Cell, Mark]]:
        return [self[i, j] for i in range(self.size_n) for j in range(self.size_m)]

    def marks(self) -> List[Mark]:
        return [mark for mark in self.cells() if isinstance(mark, Mark)]

    def rows(self) -> List[List[Union[Cell, Mark]]]:
        return [[self[i, j] for j in range(self.size_m)] for i in range(self.size_n)]

    def columns(self) -> List[List[Union[Cell, Mark]]]:
        return [[self[j, i] for j in range(self.size_m)] for i in range(self.size_n)]

    def squares(self) -> List[List[Union[Cell, Mark]]]:
        result: List[List[Union[Cell, Mark]]] = [[] for i in range(self.size_n)]
        for cell in self.cells():
            result[cell.position.square].append(cell)
        return result

    def _get_candidates_for(self, position: Position) -> Set[int]:
        known_values = set(
            self.puzzle[position.row]
            + [self.puzzle[i][position.column] for i in range(self.size_n)]
            + [
                self.puzzle[i][j]
                for i in range(self.size_n)
                for j in range(self.size_m)
                if self._get_square_num(i, j) == position.square
            ]
        )
        return set(range(1, 10)) - known_values

    def _get_square_num(self, i: int, j: int) -> int:
        return (i // self.square_size) * 3 + (j // self.square_size)

    def is_solved(self) -> bool:
        for house in self.rows() + self.columns() + self.squares():
            if len({c.value for c in house if isinstance(c, Cell)}) != self.size_n:
                return False
        return True

    def intersection(self, *cells: Union[Cell, Mark]) -> List[Union[Cell, Mark]]:
        intersections = []
        for cell in cells:
            intersections.append(
                {c.position for c in self.cells() if self.is_intersects(c, cell)}
            )
        positions = set.intersection(*intersections)
        return [self[position.row, position.column] for position in positions]

    def is_intersects(
        self, cell_a: Union[Cell, Mark], cell_b: Union[Cell, Mark]
    ) -> bool:
        return cell_a.position != cell_b.position and (
            cell_a.position.row == cell_b.position.row
            or cell_a.position.column == cell_b.position.column
            or cell_a.position.square == cell_b.position.square
        )
