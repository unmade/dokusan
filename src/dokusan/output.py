from typing import List, Union

from dokusan.entities import Cell, Mark, Sudoku


class Colors:
    BOLD = "\033[;1m"
    ORANGE = "\033[93m"
    ENDC = "\033[0m"


def plain(sudoku: List[List[int]]) -> str:
    result = "┌───┬───┬───╥───┬───┬───╥───┬───┬───┐\n"
    for i, row in enumerate(sudoku):
        for j, val in enumerate(row):
            if j == 0:
                result += "│ "
            if j == len(sudoku) - 1:
                border = " │"
            else:
                border = " ║ " if (j + 1) % 3 == 0 else " │ "
            result += f"{val}{border}" if val else f" {border}"
        result += "\n"
        if i == len(sudoku) - 1:
            result += "└───┴───┴───╨───┴───┴───╨───┴───┴───┘\n"
        elif (i + 1) % 3 == 0:
            result += "╞═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╡\n"
        else:
            result += "├───┼───┼───╫───┼───┼───╫───┼───┼───┤\n"
    return result


def colorful(sudoku: Sudoku) -> str:
    result = [_build_horizontal_border(sudoku, "┌", "─", "┬", "╥", "┐")]
    for i, row in enumerate(sudoku.rows()):
        result.append(_build_row(row))

        if i == len(sudoku.rows()) - 1:
            result.append(_build_horizontal_border(sudoku, "└", "─", "┴", "╨", "┘"))
        elif (i + 1) % 3 == 0:
            result.append(_build_horizontal_border(sudoku, "╞", "═", "╪", "╬", "╡"))
        else:
            result.append(_build_horizontal_border(sudoku, "├", "─", "┼", "╫", "┤"))

    return "".join(result)


def _build_horizontal_border(
    sudoku: Sudoku, right: str, middle: str, cell_sep: str, square_sep: str, left: str
) -> str:
    items = [f"{right}"]
    for i in range(sudoku.size_n):
        for j in range(sudoku.square_size * 3):
            items.append(f"{middle}")
        if (i + 1) == sudoku.size_n:
            items.append(f"{left}\n")
        elif (i + 1) % sudoku.square_size == 0:
            items.append(f"{square_sep}")
        else:
            items.append(f"{cell_sep}")
    return "".join(items)


def _build_row(row: List[Union[Cell, Mark]], size: int = 3) -> str:
    result = []
    for k in range(size):
        result.append("│")
        for j, cell in enumerate(row):
            start, end = k * 3, k * 3 + size
            for i in range(start, end):
                if (
                    isinstance(cell, Cell)
                    and k == size // 2
                    and i == (start + end) // 2
                ):
                    result.append(f" {Colors.BOLD}{cell.value}{Colors.ENDC} ")
                elif (
                    isinstance(cell, Mark)
                    and k == i // 3
                    and (i + 1) in cell.candidates
                ):
                    result.append(f" {Colors.ORANGE}{i + 1}{Colors.ENDC} ")
                else:
                    result.append("   ")
            result.append("║" if (j + 1) % size == 0 and j != len(row) - 1 else "│")
        result.append("\n")
    return "".join(result)
