from dataclasses import dataclass
from typing import List, Set, Tuple, Union


@dataclass
class Cell:
    position: Tuple[int, int]
    value: int


@dataclass
class Mark:
    position: Tuple[int, int]
    candidates: Set[int]


class Sudoku:
    def __init__(self, puzzle: List[List[int]]):
        self.puzzle = puzzle
        self.size_n = len(puzzle)
        self.size_m = len(puzzle[0])
        self.square_size = 3

        self.sudoku: List[List[Union[Cell, Mark]]] = []
        for i in range(self.size_n):
            row: List[Union[Cell, Mark]] = []
            for j in range(self.size_m):
                if value := self.puzzle[i][j]:
                    row.append(Cell(position=(i, j), value=value))
                else:
                    row.append(
                        Mark(position=(i, j), candidates=self._get_candidates_for(i, j))
                    )
            self.sudoku.append(row)

    def __getitem__(self, key: Tuple[int, int]):
        i, j = key
        return self.sudoku[i][j]

    def update_cells(self, cells: List[Union[Cell, Mark]]):
        for cell in cells:
            i, j = cell.position
            if isinstance(cell, Cell):
                self.puzzle[i][j] = cell.value
            self.sudoku[i][j] = cell

    def cells(self) -> List[Union[Cell, Mark]]:
        return [self[i, j] for i in range(self.size_n) for j in range(self.size_m)]

    def rows(self) -> List[List[Union[Cell, Mark]]]:
        return [[self[i, j] for j in range(self.size_m)] for i in range(self.size_n)]

    def columns(self) -> List[List[Union[Cell, Mark]]]:
        return [[self[j, i] for j in range(self.size_m)] for i in range(self.size_n)]

    def squares(self) -> List[List[Union[Cell, Mark]]]:
        result: List[List[Union[Cell, Mark]]] = [[] for i in range(self.size_n)]
        for i in range(self.size_n):
            for j in range(self.size_m):
                result[self.get_square_num_by(i, j)].append(self[i, j])
        return result

    def _rows(self) -> List[List[int]]:
        return self.puzzle[:]

    def _columns(self) -> List[List[int]]:
        return [
            [self.puzzle[j][i] for j in range(self.size_m)] for i in range(self.size_n)
        ]

    def _squares(self) -> List[List[int]]:
        result: List[List[int]] = [[] for i in range(self.size_n)]
        for i in range(self.size_n):
            for j in range(self.size_m):
                result[self.get_square_num_by(i, j)].append(self.puzzle[i][j])
        return result

    def _get_candidates_for(self, i: int, j: int) -> Set[int]:
        known_value = set(
            self._rows()[i]
            + self._columns()[j]
            + self._squares()[self.get_square_num_by(i, j)]
        )
        return set(range(1, 10)) - known_value

    def get_square_num_by(self, i: int, j: int) -> int:
        return (i // self.square_size) * 3 + (j // self.square_size)

    def is_solved(self) -> bool:
        for i, row in enumerate(self.puzzle):
            row_values = self._rows()[i]
            if len(set(row_values)) != len(row_values):
                return False

            for j, col in enumerate(row):
                col_values = self._columns()[j]
                if len(set(col_values)) != len(col_values):
                    return False

                square_values = self._squares()[self.get_square_num_by(i, j)]
                if len(set(square_values)) != len(square_values):
                    return False

        return True

    def intersection(self, *cells: Union[Cell, Mark]) -> List[Union[Cell, Mark]]:
        intersections = []
        for cell in cells:
            intersections.append(
                {c.position for c in self.cells() if self.is_intersects(c, cell)}
            )
        positions = set.intersection(*intersections)
        return [self[position] for position in positions]

    def is_intersects(
        self, cell_a: Union[Cell, Mark], cell_b: Union[Cell, Mark]
    ) -> bool:
        return cell_a.position != cell_b.position and (
            cell_a.position[0] == cell_b.position[0]
            or cell_a.position[1] == cell_b.position[1]
            or self.get_square_num_by(*cell_a.position)
            == self.get_square_num_by(*cell_b.position)
        )
