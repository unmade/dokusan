========
Overview
========

.. start-badges

.. image:: https://github.com/unmade/dokusan/workflows/Lint%20and%20tests/badge.svg
    :alt: Build Status
    :target: https://github.com/unmade/dokusan/blob/master/.github/workflows/lint-and-tests.yml

.. image:: https://codecov.io/gh/unmade/dokusan/branch/master/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/unmade/dokusan

.. image:: https://img.shields.io/pypi/v/dokusan.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/dokusan

.. image:: https://img.shields.io/pypi/wheel/dokusan.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/dokusan

.. image:: https://img.shields.io/pypi/pyversions/dokusan.svg
    :alt: Supported versions
    :target: https://pypi.org/project/dokusan

.. image:: https://img.shields.io/badge/License-GPLv3-purple.svg
    :alt: GPLv3 License
    :target: https://github.com/unmade/dokusan/blob/master/LICENSE

.. end-badges

Sudoku generator and solver with a step-by-step guidance

Installation
============

.. code-block:: bash

    pip install dokusan

Quickstart
==========

Sudoku Solvers
--------------

Step-by-step solver
*******************

This solver tries to solve sudoku using human-like strategies.
Currently following techniques are supported:

- Naked/Hidden singles
- Naked Pairs/Triplets
- Locked Candidate
- XY-Wing
- Unique Rectangle

For example to see all techniques that sudoku has:

.. code-block:: python

    from dokusan import solvers
    from dokusan.entities import BoxSize, Sudoku


    sudoku = Sudoku.from_list(
        [
            [0, 0, 0, 0, 9, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 2, 3, 0, 0],
            [0, 0, 7, 0, 0, 1, 8, 2, 5],
            [6, 0, 4, 0, 3, 8, 9, 0, 0],
            [8, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 8],
            [1, 7, 0, 0, 0, 0, 6, 0, 0],
            [9, 0, 0, 0, 1, 0, 7, 4, 3],
            [4, 0, 3, 0, 6, 0, 0, 0, 1],
        ],
        box_size=BoxSize(3, 3),
    )

    {step.combination.name for step in solvers.steps(sudoku)}

Backtracking-based solver
*************************

This solver is based on backtracking algorithm,
however slightly modified to work fast

.. code-block:: python

    from dokusan import solvers
    from dokusan.entities import BoxSize, Sudoku


    sudoku = Sudoku.from_list(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 8, 5],
            [0, 0, 1, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 7, 3],
            [0, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 9],
        ],
        box_size=BoxSize(3, 3),
    )

    solvers.backtrack(sudoku)

Sudoku Generator
----------------

Generator algorithm is mainly based on
`article <https://dlbeer.co.nz/articles/sudoku.html>`_ by Daniel Beer.
The average time to generate Sudoku with rank of 150 is 700ms.

To generate a new sudoku:

.. code-block:: python

    from dokusan import generators


    generators.random_sudoku(avg_rank=150)

Ranking and Sudoku difficulty
*****************************

``avg_rank`` option roughly defines the difficulty of the sudoku.
Sudoku with rank lower than 100 contains only naked/hidden singles.
Sudoku with rank greater than 150 contains
Naked Subsets/Locked Candidate/XY Wing/etc...,
however this is not always guaranteed.

For higher ranks it is also not guaranteed that generated Sudoku rank
will be higher than provided ``avg_rank``,
so to ensure sudoku has desired rank one can do the following:

.. code-block:: python

    from dokusan import generators, stats


    avg_rank = 450
    while stats.rank(sudoku := generators.random_sudoku(avg_rank)) < avg_rank:
        continue
