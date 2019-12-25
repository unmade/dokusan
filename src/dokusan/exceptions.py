class DokusanError(Exception):
    pass


class InvalidSudoku(DokusanError):
    pass


class NoCandidates(DokusanError):
    pass


class MultipleSolutions(DokusanError):
    pass


class Unsolvable(DokusanError):
    pass
