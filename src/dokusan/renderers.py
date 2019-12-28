from enum import Enum
from typing import List, NamedTuple, Protocol

from dokusan.boards import BoxSize, Cell, Sudoku


class Color(Protocol):
    def __call__(self, value: int) -> str:
        ...


class TermColor(Enum):
    BOLD = "\033[;1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    ENDC = "\033[0m"

    def __call__(self, value: int) -> str:
        return f"{self.value}{value}{self.__class__.ENDC.value}"


class NoColor:
    def __call__(self, value: int) -> str:
        return str(value)


class Colors(NamedTuple):
    value: Color
    candidate: Color


class Separator(NamedTuple):
    right: str
    middle: str
    intercell: str
    interbox: str
    left: str

    def __call__(self, box_size: BoxSize) -> str:
        size = box_size.length * box_size.width
        items = [f"{self.right}"]
        for i in range(1, size + 1):
            items += [self.middle for j in range(size)]
            if i == size:
                items.append(f"{self.left}")
            elif i % box_size.length == 0:
                items.append(f"{self.interbox}")
            else:
                items.append(f"{self.intercell}")
        return "".join(items)


class Border(NamedTuple):
    top: Separator
    interbox: Separator
    interrow: Separator
    intercol: Separator
    bottom: Separator

    def template(self, box_size: BoxSize) -> str:
        size = box_size.width * box_size.length
        result = [self.top(box_size)]
        for i in range(size):
            result.append("{}")
            if i + 1 == size:
                result.append(self.bottom(box_size))
            elif (i + 1) % box_size.width == 0:
                result.append(self.interbox(box_size))
            else:
                result.append(self.interrow(box_size))

        return "\n".join(result)


class TermRenderer:
    def __init__(self, border: Border, colors: Colors):
        self.border = border
        self.colors = colors

    def __call__(self, sudoku: Sudoku) -> str:
        rows = [
            [self.render_cell(cell, sudoku.box_size) for cell in row]
            for row in sudoku.rows()
        ]

        template = self.border.template(sudoku.box_size)
        return template.format(*[self.render_row(row, sudoku.box_size) for row in rows])

    def render_cell(self, cell: Cell, box_size: BoxSize) -> List[List[str]]:
        width, length = box_size

        result = []
        for i in range(width):
            values = []
            for j in range(length):
                if cell.value and i == width // 2 and j == length // 2:
                    values.extend([" ", self.colors.value(cell.value), " "])
                elif (value := i * length + j + 1) in cell.candidates:
                    values.extend([" ", self.colors.candidate(value), " "])
                else:
                    values.extend([" ", " ", " "])
            result.append(values)

        return result

    def render_row(self, row: List[List[List[str]]], box_size: BoxSize) -> str:
        result = []
        for cell in zip(*row):
            subrow = [value for values in cell for value in values]
            result.append(self.border.intercol(box_size).format(*subrow))
        return "\n".join(result)


plain = TermRenderer(
    border=Border(
        Separator("┌", "─", "┬", "╥", "┐"),
        Separator("╞", "═", "╪", "╬", "╡"),
        Separator("├", "─", "┼", "╫", "┤"),
        Separator("│", "{}", "│", "║", "│"),
        Separator("└", "─", "┴", "╨", "┘"),
    ),
    colors=Colors(value=NoColor(), candidate=NoColor()),
)


colorful = TermRenderer(
    border=Border(
        Separator("┌", "─", "┬", "╥", "┐"),
        Separator("╞", "═", "╪", "╬", "╡"),
        Separator("├", "─", "┼", "╫", "┤"),
        Separator("│", "{}", "│", "║", "│"),
        Separator("└", "─", "┴", "╨", "┘"),
    ),
    colors=Colors(value=TermColor.BOLD, candidate=TermColor.YELLOW),
)
