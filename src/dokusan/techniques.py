from __future__ import annotations

import itertools
import operator
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from dokusan.entities import Cell, Sudoku


class NotFound(Exception):
    pass


@dataclass
class Result:
    combination: Combination
    changes: List[Cell]


@dataclass
class Combination:
    name: str
    cells: List[Cell]
    values: List[int]

    def __str__(self) -> str:
        values = (str(value) for value in self.values)
        positions = (str((c.position.row, c.position.column)) for c in self.cells)
        return f"{self.name}: `{', '.join(values)}` at {', '.join(positions)}"


class Technique:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self) -> Iterator[Result]:
        return (
            Result(combination=combination, changes=changes)
            for combination in self._find()
            if (changes := self._get_changes(combination))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("Not found")

    def _find(self) -> Iterator[Combination]:
        raise NotImplementedError

    def _get_changes(self, combination: Combination) -> List[Cell]:
        raise NotImplementedError


class LoneSingle(Technique):
    def _find(self) -> Iterator[Combination]:
        for cell in self.sudoku.cells():
            if len(cell.candidates) == 1:
                yield Combination(
                    name="Lone Single", cells=[cell], values=list(cell.candidates),
                )

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        single = Cell(
            position=combination.cells[0].position, value=combination.values[0],
        )
        return [
            Cell(position=cell.position, candidates=cell.candidates - eliminated)
            for cell in self.sudoku.intersection(single)
            if cell.candidates and cell.candidates & eliminated
        ] + [single]


class HiddenSingle(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[int, List[Cell]] = {}
            for cell in house:
                if cell.candidates:
                    for candidate in cell.candidates:
                        groups.setdefault(candidate, []).append(cell)

            for candidate, cells in groups.items():
                if len(cells) == 1:
                    yield Combination(
                        name="Hidden Single", cells=cells, values=[candidate],
                    )

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        single = Cell(
            position=combination.cells[0].position, value=combination.values[0],
        )
        return [
            Cell(position=cell.position, candidates=cell.candidates - eliminated)
            for cell in self.sudoku.intersection(single)
            if cell.candidates and cell.candidates & eliminated
        ] + [single]


class NakedPair(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[Tuple[int, ...], List[Cell]] = {}
            for cell in house:
                if cell.candidates:
                    groups.setdefault(tuple(cell.candidates), []).append(cell)

            for candidates, cells in groups.items():
                if len(candidates) == 2 and len(cells) == 2:
                    yield Combination(
                        name="Naked Pair", cells=cells, values=list(candidates),
                    )

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        return [
            Cell(position=cell.position, candidates=cell.candidates - eliminated)
            for cell in self.sudoku.intersection(*combination.cells)
            if cell.candidates and cell.candidates & eliminated
        ]


class NakedTriplet(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            cells = [cell for cell in house if cell.candidates]
            counter = Counter(tuple(cell.candidates) for cell in cells)

            for pair, count in counter.items():
                if 2 <= count < 4:
                    triplet = [c for c in cells if len(c.candidates.union(pair)) < 4]
                    if len(triplet) == 3:
                        yield Combination(
                            name="Naked Triplet",
                            cells=triplet,
                            values=list(set.union(*[c.candidates for c in triplet])),
                        )

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        return [
            Cell(position=cell.position, candidates=cell.candidates - eliminated)
            for cell in self.sudoku.intersection(*combination.cells)
            if cell.candidates and cell.candidates & eliminated
        ]


class Omission(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[int, List[Cell]] = {}
            for cell in house:
                if cell.candidates:
                    for candidate in cell.candidates:
                        groups.setdefault(candidate, []).append(cell)

            for candidate, cells in groups.items():
                if len(cells) == 2:
                    yield Combination(name="Omission", cells=cells, values=[candidate])

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        return [
            Cell(position=cell.position, candidates=cell.candidates - eliminated)
            for cell in self.sudoku.intersection(*combination.cells)
            if cell.candidates and cell.candidates & eliminated
        ]


class XYWing(Technique):
    def _find(self) -> Iterator[Combination]:
        cells = [cell for cell in self.sudoku.cells() if len(cell.candidates) == 2]
        for triplet in itertools.combinations(cells, 3):
            if self._is_xy_wing(triplet):
                wing = sorted(triplet, key=operator.attrgetter("position"))
                yield Combination(
                    name="XY Wing",
                    cells=wing,
                    values=list(set.intersection(*[c.candidates for c in wing[::2]])),
                )

    def _is_xy_wing(self, cells: Iterable[Cell]) -> bool:
        if len(set.union(*[c.candidates for c in cells])) != 3:
            return False
        combinations = tuple(itertools.combinations(cells, 2))
        if sum(self.sudoku.is_intersects(a, b) for a, b in combinations) != 2:
            return False
        if any(len(a.candidates & b.candidates) != 1 for a, b in combinations):
            return False
        return True

    def _get_changes(self, combination: Combination) -> List[Cell]:
        eliminated = set(combination.values)
        return [
            Cell(position=c.position, candidates=c.candidates - eliminated)
            for c in self.sudoku.intersection(*[x for x in combination.cells[::2]])
            if c.candidates and c.candidates & eliminated
        ]


class UniqueRectangle(Technique):
    def _find(self) -> Iterator[Combination]:
        cells = [cell for cell in self.sudoku.cells() if len(cell.candidates) == 2]
        for edges in itertools.combinations(cells, r=3):
            if self._is_edges(edges):
                rectangle = self._build_rectangle(edges)
                # waiting for https://github.com/python/mypy/issues/7316
                if rectangle is not None:
                    yield Combination(
                        name="Unique Rectangle",
                        cells=rectangle,
                        values=list(
                            set.intersection(*[c.candidates for c in rectangle])
                        ),
                    )

    def _is_edges(self, cells: Iterable[Cell]) -> bool:
        if len(set.intersection(*[c.candidates for c in cells])) != 2:
            return False
        combinations = tuple(itertools.combinations(cells, 2))
        if sum(a.position.row == b.position.row for a, b in combinations) != 1:
            return False
        if sum(a.position.column == b.position.column for a, b in combinations) != 1:
            return False
        if sum(a.position.square == b.position.square for a, b in combinations) != 1:
            return False
        return True

    def _build_rectangle(self, edges: Iterable[Cell]) -> Optional[List[Cell]]:
        rows = {edge.position.row for edge in edges}
        cols = {edge.position.column for edge in edges}
        cells = [self.sudoku[i, j] for i, j in itertools.product(rows, cols)]
        rectangle = [mark for mark in cells if mark.candidates]
        if len(rectangle) != 4:
            return None
        if len(set.intersection(*[m.candidates for m in rectangle])) != 2:
            return None
        return rectangle

    def _get_changes(self, combination: Combination) -> List[Cell]:
        return next(
            [Cell(position=edge_a.position, candidates=diff)]
            for edge_a, edge_b in itertools.combinations(combination.cells, 2)
            if (diff := edge_a.candidates - edge_b.candidates)
        )
