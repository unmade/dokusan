import itertools
import string
from dataclasses import dataclass, field
from typing import Iterator, List, NamedTuple, Optional, Set, Tuple, Type, TypeVar

T = TypeVar("T", bound="Sudoku")

DIGIT_TO_STR_MAP = dict(
    zip(
        range(len(string.digits) + len(string.ascii_uppercase)),
        string.digits + string.ascii_uppercase,
    )
)
STR_TO_DIGIT_MAP = dict(zip(DIGIT_TO_STR_MAP.values(), DIGIT_TO_STR_MAP.keys()))


class Position(NamedTuple):
    row: int
    column: int
    box: int


class BoxSize(NamedTuple):
    width: int
    length: int

    def sequential(self, row: int, column: int) -> int:
        return (row // self.width) * self.width + (column // self.length)

    def indexes(self, row: int, column: int) -> Iterator[Tuple[int, int]]:
        return itertools.product(
            (i + row // self.width * self.width for i in range(self.length)),
            (j + column // self.width * self.width for j in range(self.length)),
        )


@dataclass
class Cell:
    position: Position
    value: Optional[int] = None
    candidates: Set[int] = field(default_factory=set)

    def __post_init__(self):
        if self.value and self.candidates:
            raise ValueError("`value` and `candidates` attrs are mutually exclusive")


class Sudoku:
    def __init__(self, *cells: Cell, box_size: BoxSize):
        self.box_size = box_size
        self.size = box_size.width * box_size.length
        self._sudoku = {
            (i, j): Cell(position=Position(i, j, box_size.sequential(i, j)))
            for i in range(self.size)
            for j in range(self.size)
        }
        for cell in cells:
            self._sudoku[cell.position[:2]] = cell

    @classmethod
    def from_list(cls: Type[T], puzzle: List[List[int]], box_size: BoxSize) -> T:
        cells = []
        for i, row in enumerate(puzzle):
            for j, value in enumerate(row):
                position = Position(i, j, box_size.sequential(i, j))
                cells.append(Cell(position=position, value=value if value else None,))
        return cls(*cells, box_size=box_size)

    @classmethod
    def from_string(cls: Type[T], puzzle: str, box_size: BoxSize) -> T:
        size = box_size.width * box_size.length
        return cls.from_list(
            [
                [
                    STR_TO_DIGIT_MAP.get(value, 0)
                    for value in puzzle[i * size : i * size + size]
                ]
                for i in range(size)
            ],
            box_size=box_size,
        )

    def __str__(self) -> str:
        return "".join(
            "".join(
                # see https://github.com/python/typing/issues/448
                DIGIT_TO_STR_MAP.get(cell.value, "0")  # type: ignore
                for cell in row
            )
            for row in self.rows()
        )

    def __getitem__(self, key: Tuple[int, int]) -> Cell:
        return self._sudoku[key]

    def update(self, cells: List[Cell]) -> None:
        self._sudoku.update((cell.position[:2], cell) for cell in cells)

    def cells(self) -> Iterator[Cell]:
        return iter(self._sudoku.values())

    def rows(self) -> Iterator[List[Cell]]:
        return ([self[i, j] for j in range(self.size)] for i in range(self.size))

    def columns(self) -> Iterator[List[Cell]]:
        return ([self[j, i] for j in range(self.size)] for i in range(self.size))

    def boxes(self) -> Iterator[List[Cell]]:
        return (
            [self[x, y] for x, y in self.box_size.indexes(i, j)]
            for i in range(0, self.size, self.box_size.length)
            for j in range(0, self.size, self.box_size.width)
        )

    def groups(self) -> Iterator[List[Cell]]:
        return itertools.chain(self.rows(), self.columns(), self.boxes())

    def is_solved(self) -> bool:
        for group in self.groups():
            if len({cell.value for cell in group if cell.value}) != self.size:
                return False
        return True

    def is_valid(self) -> bool:
        for group in self.groups():
            values = [cell.value for cell in group if cell.value]
            if len(set(values)) != len(values):
                return False
        return True

    def intersection(self, *cells: Cell) -> List[Cell]:
        intersections: Set[Tuple[int, int]] = set()
        for i, cell in enumerate(cells):
            row, column = cell.position.row, cell.position.column
            cross = set.union(
                {(row, i) for i in range(self.size)},
                {(i, column) for i in range(self.size)},
                {(i, j) for i, j in self.box_size.indexes(row, column)},
            )
            if i == 0:
                intersections |= cross
            else:
                intersections &= cross
        intersections -= {(cell.position.row, cell.position.column) for cell in cells}
        return [self[position] for position in intersections]

    def is_intersects(self, cell_a: Cell, cell_b: Cell) -> bool:
        return cell_a.position != cell_b.position and (
            cell_a.position.row == cell_b.position.row
            or cell_a.position.column == cell_b.position.column
            or cell_a.position.box == cell_b.position.box
        )
