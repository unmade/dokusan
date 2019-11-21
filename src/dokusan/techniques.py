from dataclasses import dataclass
from typing import List, Union

from dokusan.entities import Cell, Mark, Position, Sudoku


class NotFound(Exception):
    pass


@dataclass
class Result:
    positions: List[Position]
    values: List[int]
    changed_cells: List[Union[Cell, Mark]]


class LoneSingle:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position],
                values=[cell.value],
                changed_cells=self._get_changed_cells(cell, self.sudoku),
            )
            for cell in self._find(self.sudoku)
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Lone Single found")

    def _find(self, sudoku):
        for cell in sudoku.cells():
            if isinstance(cell, Mark) and len(cell.candidates) == 1:
                yield Cell(position=cell.position, value=next(iter(cell.candidates)))

    def _get_changed_cells(self, single, sudoku) -> List[Mark]:
        return [single] + [
            Mark(
                position=mark.position,
                candidates=mark.candidates - set([single.value]),
            )
            for mark in sudoku.intersection(single)
            if isinstance(mark, Mark) and mark.candidates & set([single.value])
        ]


class HiddenSingle:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position],
                values=[cell.value],
                changed_cells=self._get_changed_cells(cell, self.sudoku),
            )
            for cell in self._find(self.sudoku)
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Hidden Single found")

    def _find(self, sudoku):
        for house in sudoku.rows() + sudoku.columns() + sudoku.squares():
            marks = [mark for mark in house if isinstance(mark, Mark)]
            for mark in marks:
                values = set.union(*[m.candidates for m in marks if m is not mark])
                if len(single := (mark.candidates - values)) == 1:
                    yield Cell(position=mark.position, value=next(iter(single)))

    def _get_changed_cells(self, single, sudoku) -> List[Mark]:
        return [single] + [
            Mark(
                position=mark.position,
                candidates=mark.candidates - set([single.value]),
            )
            for mark in sudoku.intersection(single)
            if isinstance(mark, Mark) and mark.candidates & set([single.value])
        ]


class NakedPair:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position for cell in pair],
                values=pair[0].candidates,
                changed_cells=changed_cells,
            )
            for pair in self._find(self.sudoku)
            if (changed_cells := self._get_changed_cells(pair, self.sudoku))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Naked Pair found")

    def _find(self, sudoku):
        for house in sudoku.rows() + sudoku.columns() + sudoku.squares():
            marks = [mark for mark in house if isinstance(mark, Mark)]
            counter = {}
            for mark in marks:
                if (pair := tuple(mark.candidates)) not in counter:
                    counter[pair] = 0
                counter[pair] += 1

            for pair, count in counter.items():
                if cells := [
                    mark
                    for mark in marks
                    if len(pair) == count
                    and count == 2
                    and pair == tuple(mark.candidates)
                ]:
                    yield cells

    def _get_changed_cells(self, pair, sudoku) -> List[Mark]:
        return [
            Mark(
                position=mark.position, candidates=mark.candidates - pair[0].candidates,
            )
            for mark in sudoku.intersection(*pair)
            if isinstance(mark, Mark) and mark.candidates & pair[0].candidates
        ]


class NakedTriplet:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position for cell in triplet],
                values=list(set.union(*[t.candidates for t in triplet])),
                changed_cells=changed_cells,
            )
            for triplet in self._find(self.sudoku)
            if (changed_cells := self._get_changed_cells(triplet, self.sudoku))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Naked Triplet found")

    def _find(self, sudoku):
        for house in sudoku.rows() + sudoku.columns() + sudoku.squares():
            marks = [mark for mark in house if isinstance(mark, Mark)]
            counter = {}
            for mark in marks:
                if (pair := tuple(mark.candidates)) not in counter:
                    counter[pair] = 0
                counter[pair] += 1

            for pair, count in counter.items():
                if cells := [
                    mark
                    for mark in marks
                    if 2 <= len(pair) < 4
                    and 2 <= count < 4
                    and len(set(pair) & mark.candidates) in (2, 3)
                    and len(mark.candidates) in (2, 3)
                ]:
                    if self._is_naked_triplet(cells, sudoku):
                        yield cells

        return None

    def _is_naked_triplet(self, triplet, sudoku):
        if len(triplet) != 3:
            return False
        candidates = set().union(*[t.candidates for t in triplet])
        return bool(
            len(candidates) == 3
            and (
                candidates
                & set().union(
                    *[
                        mark.candidates
                        for mark in sudoku.intersection(*triplet)
                        if isinstance(mark, Mark)
                    ]
                )
            )
        )

    def _get_changed_cells(self, triplet, sudoku) -> List[Mark]:
        candidates = set.union(*[t.candidates for t in triplet])
        return [
            Mark(position=mark.position, candidates=mark.candidates - candidates)
            for mark in sudoku.intersection(*triplet)
            if isinstance(mark, Mark) and mark.candidates & candidates
        ]


class Omission:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position for cell in omission[1:]],
                values=[omission[0]],
                changed_cells=changed_cells,
            )
            for omission in self._find(self.sudoku)
            if (changed_cells := self._get_changed_cells(omission, self.sudoku))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Omission found")

    def _find(self, sudoku):
        for block in sudoku.squares():
            marks = [mark for mark in block if isinstance(mark, Mark)]
            for mark in marks:
                for intersection in [
                    block,
                    sudoku.rows()[mark.position.row],
                    sudoku.columns()[mark.position.column],
                ]:
                    candidates = [
                        candidate
                        for m in intersection
                        if isinstance(m, Mark) and m is not mark
                        for candidate in m.candidates
                    ]
                    for candidate in mark.candidates:
                        if candidates.count(candidate) == 1:
                            for m in intersection:
                                if (
                                    isinstance(m, Mark)
                                    and m is not mark
                                    and candidate in m.candidates
                                    and self._is_omission([candidate, mark, m], sudoku)
                                    and m.position.square == mark.position.square
                                ):
                                    yield [candidate, mark, m]

    def _is_omission(self, omission, sudoku):
        return bool(
            set([omission[0]])
            & set().union(
                *[
                    mark.candidates
                    for mark in sudoku.intersection(*omission[1:])
                    if isinstance(mark, Mark)
                ]
            )
        )

    def _get_changed_cells(self, omission, sudoku):
        return [
            Mark(
                position=mark.position, candidates=mark.candidates - set([omission[0]]),
            )
            for mark in sudoku.intersection(*omission[1:])
            if isinstance(mark, Mark) and mark.candidates & set([omission[0]])
        ]


class XYWing:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        import itertools

        return (
            Result(
                positions=[cell.position for cell in xy_wing],
                values=[
                    next(iter(cell_a.candidates & cell_b.candidates))
                    for cell_a, cell_b in itertools.combinations(xy_wing, r=2)
                    if not self.sudoku.is_intersects(cell_a, cell_b)
                ],
                changed_cells=changed_cells,
            )
            for xy_wing in self._find(self.sudoku)
            if (changed_cells := self._get_changed_cells(xy_wing, self.sudoku))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No XYWing found")

    def _find(self, sudoku: Sudoku):
        houses = sudoku.rows() + sudoku.columns() + sudoku.squares()
        for house in houses:
            pairs = []
            marks = [
                mark
                for mark in house
                if isinstance(mark, Mark) and len(mark.candidates) == 2
            ]
            for mark_a in marks:
                for mark_b in marks:
                    if len(mark_a.candidates & mark_b.candidates) == 1:
                        pairs.append([mark_a, mark_b])

            if not pairs:
                continue

            for pair in pairs:
                for mark in [
                    mark
                    for mark in sudoku.cells()
                    if isinstance(mark, Mark) and len(mark.candidates) == 2
                ]:
                    if mark in pair:
                        continue
                    if (
                        (
                            sudoku.is_intersects(mark, pair[0])
                            or sudoku.is_intersects(mark, pair[1])
                        )
                        and len(
                            mark.candidates | pair[0].candidates | pair[1].candidates
                        )
                        == 3
                        and len(mark.candidates & pair[0].candidates) == 1
                        and len(mark.candidates & pair[1].candidates) == 1
                        and self._is_xy_wing(pair + [mark], sudoku)
                    ):
                        yield pair + [mark]

    def _is_xy_wing(self, xy_wing, sudoku):
        for cell_a in xy_wing:
            for cell_b in xy_wing:
                if cell_a is not cell_b and not sudoku.is_intersects(cell_a, cell_b):
                    value = cell_a.candidates & cell_b.candidates
                    return bool(
                        value
                        & set().union(
                            *[
                                m.candidates
                                for m in sudoku.intersection(cell_a, cell_b)
                                if isinstance(m, Mark)
                            ]
                        )
                    )
        return False

    def _get_changed_cells(self, xy_wing, sudoku):
        for cell_a in xy_wing:
            for cell_b in xy_wing:
                if cell_a is not cell_b and not sudoku.is_intersects(cell_a, cell_b):
                    value = cell_a.candidates & cell_b.candidates
                    return [
                        Mark(position=m.position, candidates=m.candidates - value)
                        for m in sudoku.intersection(cell_a, cell_b)
                        if isinstance(m, Mark) and m.candidates & value
                    ]
        return []


class UniqueRectangle:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self):
        return (
            Result(
                positions=[cell.position for cell in rectangle],
                values=sorted(rectangle[0].candidates & rectangle[1].candidates),
                changed_cells=changed_cells,
            )
            for rectangle in self._find(self.sudoku)
            if (changed_cells := self._get_changed_cells(rectangle, self.sudoku))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("No Unique Rectangle found")

    def _find(self, sudoku):
        for row in sudoku.rows():
            marks = [
                mark
                for mark in row
                if isinstance(mark, Mark) and len(mark.candidates) == 2
            ]
            counter = {}
            for mark in marks:
                if (pair := tuple(mark.candidates)) not in counter:
                    counter[pair] = 0
                counter[pair] += 1

            pairs = [set(key) for key in counter if counter[key] == 2]
            for pair in pairs:
                cells = [mark for mark in marks if mark.candidates == pair]
                assert len(cells) == 2, f"Expected 2, got: {len(cells)}:{cells}:{pairs}"
                x, y = cells[0].position.column, cells[1].position.column

                for row_b in sudoku.rows():
                    if row == row_b:
                        continue
                    for cell in row_b:
                        if not isinstance(cell, Mark):
                            continue
                        if cell.position.column in (x, y) and cell.candidates == pair:
                            pos = cell.position.row, x
                            if (
                                isinstance(row_b[pos[1]], Mark)
                                and len(row_b[pos[1]].candidates & cell.candidates) == 2
                            ):
                                if self._is_unique_rectangle(
                                    [sudoku[pos], cell, *cells], sudoku
                                ):
                                    yield [sudoku[pos], cell, *cells]

    def _is_unique_rectangle(self, rectangle, sudoku):
        intersection_map = {}
        for edge_a in rectangle:
            for edge_b in rectangle:
                if edge_a is edge_b:
                    continue
                if edge_a.position.square == edge_b.position.square:
                    intersection_map[edge_a.position] = (
                        intersection_map.get(edge_a.position, 0) + 1
                    )

        for key in intersection_map:
            if intersection_map[key] != 1:
                return False

        return True

    def _get_changed_cells(self, rectangle, sudoku):
        for edge_a in rectangle:
            for edge_b in rectangle:
                if diff := (edge_a.candidates - edge_b.candidates):
                    return [Mark(position=edge_a.position, candidates=diff)]
