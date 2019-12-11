========
Overview
========

Sudoku solver with step-by-step guidance

This lib is currently in pre-alpha phase,
but already can solve some simple and medium level sudoku.

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
