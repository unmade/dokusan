SIZE = 9
SQUARE_SIZE = 3
SQUARE_MAP = {
    i: [x + i // SQUARE_SIZE * SQUARE_SIZE for x in range(3)] for i in range(SIZE)
}
ALL_VALUES = list(range(1, SIZE + 1))


def solve(puzzle, recursive=True):
    sudoku = [row[:] for row in puzzle]

    print("building variations...")
    variations = get_variations(sudoku)

    print("searching solution...")
    if recursive is True:
        solution = backtrack_recursive(variations)
    else:
        solution = backtrack(variations)

    for k, v in solution.items():
        sudoku[k[0]][k[1]] = v

    return sudoku


def get_variations(sudoku):
    variations = {}
    for i, row in enumerate(sudoku):
        for j, col in enumerate(row):
            if sudoku[i][j] > 0:
                continue

            values = get_values_in_square(sudoku, i, j)
            values += get_values_in_row(sudoku, i)
            values += get_values_in_col(sudoku, j)
            possible = list(set(ALL_VALUES) - set(values))
            variations[i, j] = sorted(possible)

    return variations


def get_values_in_square(sudoku, i, j):
    return [
        val for x in SQUARE_MAP[i] for y in SQUARE_MAP[j] if (val := sudoku[x][y]) > 0
    ]


def get_values_in_row(sudoku, i):
    return [val for val in sudoku[i] if val > 0]


def get_values_in_col(sudoku, j):
    return [val for i in range(len(sudoku)) if (val := sudoku[i][j]) > 0]


def permutate(variations):
    pools = [tuple(pool) for pool in variations.values()]
    keys = tuple(variations.keys())
    result = [[]]
    for pool in pools:
        result = [
            product
            for x in result
            for y in pool
            if is_valid_solution(product := x + [y], keys)
        ]
    for prod in result:
        yield {keys[no]: item for no, item in enumerate(prod)}


def backtrack_recursive(variations, i=0, curr=[]):
    keys = tuple(variations.keys())
    values = tuple(variations.values())
    new_val = curr[:]
    for val in values[i:]:
        for v in val:
            new_val = curr + [v]
            if is_valid_solution(new_val, tuple(variations.keys())):
                if (res := backtrack_recursive(variations, i + 1, new_val)) is not None:
                    return res
        else:
            return

    return {keys[no]: item for no, item in enumerate(new_val)}


def backtrack(variations):
    keys = tuple(variations.keys())
    values = tuple(variations.values())

    solution = []

    i = 0
    m = {i: 0 for i in range(len(values))}
    while i < len(values):
        for val in values[i:]:
            for j in range(m[i], len(val)):
                candidate = solution + [val[j]]
                if is_valid_solution(candidate, keys):
                    m[i] += 1
                    i += 1
                    solution = candidate[:]
                    break
            else:
                m[i] = 0
                i -= 1
                solution = solution[:-1]
                break

    return {keys[no]: item for no, item in enumerate(solution)}


def is_valid_solution(product, keys):
    net = []
    for i in range(SIZE):
        net.append([0 for _ in range(SIZE)])

    for no, item in enumerate(product):
        key = keys[no]
        net[key[0]][key[1]] = item

    return is_valid_sudoku(net)


def is_valid_sudoku(sudoku):
    for i, row in enumerate(sudoku):
        row_values = get_values_in_row(sudoku, i)
        if len(set(row_values)) != len(row_values):
            return False

        for j, col in enumerate(row):
            col_values = get_values_in_col(sudoku, j)
            if len(set(col_values)) != len(col_values):
                return False

            square_values = get_values_in_square(sudoku, i, j)
            if len(set(square_values)) != len(square_values):
                return False

    return True
