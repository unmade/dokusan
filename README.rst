========
Overview
========

Sudoku solver with step-by-step guidance

Installation
============

.. code-block:: bash

    pip install dokusan

Quickstart
==========

Sudoku Solver
-------------

The following code displays all steps leading to solution:

.. code-block:: python

    from dokusan import entities, techniques


    class Unsolvable(Exception):
        pass


    def list_steps(sudoku: entities.Sudoku):
        all_techniques = (
            techniques.PencilMarking,
            techniques.LoneSingle,
            techniques.HiddenSingle,
            techniques.NakedPair,
            techniques.NakedTriplet,
            techniques.LockedCandidate,
            techniques.XYWing,
            techniques.UniqueRectangle,
        )
        while not sudoku.is_solved():
            for technique in all_techniques:
                try:
                    result = technique(sudoku).first()
                except techniques.NotFound as exc:
                    continue
                else:
                    sudoku.update(result.changes)
                    yield result
                    break
            else:
                raise Unsolvable

    _ = 0

    sudoku = entities.Sudoku.from_list([
        [_, _, _, _, 9, _, 1, _, _],
        [_, _, _, _, _, 2, 3, _, _],
        [_, _, 7, _, _, 1, 8, 2, 5],
        [6, _, 4, _, 3, 8, 9, _, _],
        [8, 1, _, _, _, _, _, _, _],
        [_, _, 9, _, _, _, _, _, 8],
        [1, 7, _, _, _, _, 6, _, _],
        [9, _, _, _, 1, _, 7, 4, 3],
        [4, _, 3, _, 6, _, _, _, 1],
    ])

    for step in list_steps(sudoku):
        print(step.combination)

Sudoku Generator
----------------

Generator algorithm is mainly based on
`article <https://dlbeer.co.nz/articles/sudoku.html>`_ by Daniel Beer.
The average time to generate Sudoku with rank of 150 is 700ms.

To generate a new sudoku:

.. code-block:: python

    from dokusan.generator import generate


    generate(min_rank=150)

Ranking and Sudoku difficulty
*****************************

``min_rank`` option is used to roughly estimate the difficulty of the sudoku.
Sudoku with rank lower than 100 contains only naked/hidden singles.
Sudoku with rank greater than 150 might contains
Naked Subsets/Locked Candidate/XY Wing/etc...,
however this is not always guaranteed.

For higher ranks it is also not guaranteed that generated Sudoku rank
will be higher than provided ``min_rank``,
so to ensure sudoku has desired rank one can do the following:

.. code-block:: python

    from dokusan import stats
    from dokusan.generator import generate

    min_rank = 450
    while stats.rank(sudoku := generate(min_rank=min_rank)) < min_rank:
        continue
