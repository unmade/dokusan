from __future__ import annotations

import itertools
import operator
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Tuple, Union

from dokusan.entities import Cell, Mark, Sudoku


class NotFound(Exception):
    pass


@dataclass
class Result:
    combination: Combination
    changed_cells: List[Union[Cell, Mark]]


@dataclass
class Combination:
    marks: List[Mark]
    values: List[int]


class Technique:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def __iter__(self) -> Iterator[Result]:
        return (
            Result(combination=combination, changed_cells=changed_cells)
            for combination in self._find()
            if (changed_cells := self._get_changed_cells(combination))
        )

    def first(self) -> Result:
        try:
            return next(iter(self))
        except StopIteration:
            raise NotFound("Not found")

    def _find(self) -> Iterator[Combination]:
        raise NotImplementedError

    def _get_changed_cells(self, combination: Combination) -> List[Union[Cell, Mark]]:
        raise NotImplementedError


class LoneSingle(Technique):
    def _find(self) -> Iterator[Combination]:
        for mark in self.sudoku.marks():
            if len(mark.candidates) == 1:
                yield Combination(marks=[mark], values=list(mark.candidates))

    def _get_changed_cells(self, combination: Combination) -> List[Union[Cell, Mark]]:
        cell = Cell(position=combination.marks[0].position, value=combination.values[0])
        eliminated = set(combination.values)
        return [
            Mark(position=mark.position, candidates=mark.candidates - eliminated)
            for mark in self.sudoku.intersection(cell)
            if isinstance(mark, Mark) and mark.candidates & eliminated
        ] + [cell]


class HiddenSingle(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[int, List[Mark]] = {}
            for mark in house:
                if isinstance(mark, Mark):
                    for candidate in mark.candidates:
                        groups.setdefault(candidate, []).append(mark)

            for candidate, marks in groups.items():
                if len(marks) == 1:
                    yield Combination(
                        marks=marks, values=[candidate],
                    )

    def _get_changed_cells(self, combination: Combination) -> List[Union[Cell, Mark]]:
        cell = Cell(position=combination.marks[0].position, value=combination.values[0])
        eliminated = set(combination.values)
        return [
            Mark(position=mark.position, candidates=mark.candidates - eliminated)
            for mark in self.sudoku.intersection(cell)
            if isinstance(mark, Mark) and mark.candidates & eliminated
        ] + [cell]


class NakedPair(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[Tuple[int, ...], List[Mark]] = {}
            for mark in house:
                if isinstance(mark, Mark):
                    groups.setdefault(tuple(mark.candidates), []).append(mark)

            for candidates, marks in groups.items():
                if len(candidates) == 2 and len(marks) == 2:
                    yield Combination(
                        marks=marks, values=list(candidates),
                    )

    def _get_changed_cells(self, combination: Combination) -> List[Mark]:
        eliminated = set(combination.values)
        return [
            Mark(position=mark.position, candidates=mark.candidates - eliminated)
            for mark in self.sudoku.intersection(*combination.marks)
            if isinstance(mark, Mark) and mark.candidates & eliminated
        ]


class NakedTriplet(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            marks = [mark for mark in house if isinstance(mark, Mark)]
            counter = Counter(tuple(mark.candidates) for mark in marks)

            for pair, count in counter.items():
                if 2 <= count < 4:
                    triplet = [m for m in marks if len(m.candidates.union(pair)) < 4]
                    if len(triplet) == 3:
                        yield Combination(
                            marks=triplet,
                            values=list(set.union(*[m.candidates for m in triplet])),
                        )

    def _get_changed_cells(self, combination: Combination) -> List[Mark]:
        eliminated = set(combination.values)
        return [
            Mark(position=mark.position, candidates=mark.candidates - eliminated)
            for mark in self.sudoku.intersection(*combination.marks)
            if isinstance(mark, Mark) and mark.candidates & eliminated
        ]


class Omission(Technique):
    def _find(self) -> Iterator[Combination]:
        for house in self.sudoku.rows() + self.sudoku.columns() + self.sudoku.squares():
            groups: Dict[int, List[Mark]] = {}
            for mark in house:
                if isinstance(mark, Mark):
                    for candidate in mark.candidates:
                        groups.setdefault(candidate, []).append(mark)

            for candidate, marks in groups.items():
                if len(marks) == 2:
                    yield Combination(marks=marks, values=[candidate])

    def _get_changed_cells(self, combination: Combination) -> List[Mark]:
        eliminated = set(combination.values)
        return [
            Mark(position=mark.position, candidates=mark.candidates - eliminated)
            for mark in self.sudoku.intersection(*combination.marks)
            if isinstance(mark, Mark) and mark.candidates & eliminated
        ]


class XYWing(Technique):
    def _find(self) -> Iterator[Combination]:
        marks = [mark for mark in self.sudoku.marks() if len(mark.candidates) == 2]
        for item in itertools.combinations(marks, 3):
            if self._is_xy_wing(item):
                wing = sorted(item, key=operator.attrgetter("position"))
                yield Combination(
                    marks=wing,
                    values=list(set.intersection(*[m.candidates for m in wing[::2]])),
                )

    def _is_xy_wing(self, marks: Iterable[Mark]) -> bool:
        if len(set.union(*[m.candidates for m in marks])) != 3:
            return False
        combinations = tuple(itertools.combinations(marks, 2))
        if sum(self.sudoku.is_intersects(a, b) for a, b in combinations) != 2:
            return False
        if any(len(a.candidates & b.candidates) != 1 for a, b in combinations):
            return False
        return True

    def _get_changed_cells(self, combination: Combination) -> List[Mark]:
        eliminated = set(combination.values)
        return [
            Mark(position=m.position, candidates=m.candidates - eliminated)
            for m in self.sudoku.intersection(*[x for x in combination.marks[::2]])
            if isinstance(m, Mark) and m.candidates & eliminated
        ]


class UniqueRectangle(Technique):
    def _find(self) -> Iterator[Combination]:
        marks = [mark for mark in self.sudoku.marks() if len(mark.candidates) == 2]
        for edges in itertools.combinations(marks, r=3):
            if self._is_edges(edges):
                rows = {edge.position.row for edge in edges}
                cols = {edge.position.column for edge in edges}
                rectangle = [self.sudoku[pos] for pos in itertools.product(rows, cols)]
                if self._is_rect(rectangle):
                    yield Combination(
                        marks=rectangle,
                        values=list(
                            set.intersection(*[m.candidates for m in rectangle])
                        ),
                    )

    def _is_edges(self, marks: Iterable[Mark]) -> bool:
        if len(set.intersection(*[m.candidates for m in marks])) != 2:
            return False
        combinations = itertools.combinations(marks, 2)
        if sum(a.position.square == b.position.square for a, b in combinations) != 1:
            return False
        return True

    def _is_rect(self, marks: Iterable[Mark]) -> bool:
        if any(isinstance(cell, Cell) for cell in marks):
            return False
        if len(set.intersection(*[m.candidates for m in marks])) != 2:
            return False
        return True

    def _get_changed_cells(self, combination: Combination) -> List[Mark]:
        return next(
            [Mark(position=edge_a.position, candidates=diff)]
            for edge_a, edge_b in itertools.combinations(combination.marks, 2)
            if (diff := edge_a.candidates - edge_b.candidates)
        )
