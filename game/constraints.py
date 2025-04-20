import numpy as np

GRID_SIZE = 6

# Fixed locked values for initial state
locked_cells = {(0, 1): 1, (2, 2): 2, (4, 5): 1, (5, 0): 2}

# Constraint symbols and directions
constraints = {
    (0, 0): ('=', 'H'),
    (1, 2): ('x', 'V'),
    (3, 3): ('=', 'V'),
    (4, 1): ('x', 'H'),
    (2, 5): ('=', 'H')
}

# Optional cleanup of invalid constraints
constraints = {
    k: v for k, v in constraints.items()
    if not (v[1] == 'H' and k[1] == GRID_SIZE - 1 or v[1] == 'V' and k[0] == GRID_SIZE - 1)
}

def check_triples(grid):
    errors = set()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 2):
            row = grid[i, j:j+3]
            if row[0] == row[1] == row[2] != 0:
                errors.update({(i, j), (i, j+1), (i, j+2)})
            col = grid[j:j+3, i]
            if col[0] == col[1] == col[2] != 0:
                errors.update({(j, i), (j+1, i), (j+2, i)})
    return errors

def check_equal_counts(grid):
    errors = set()
    for i in range(GRID_SIZE):
        row = grid[i]
        col = grid[:, i]
        if list(row).count(1) > 3 or list(row).count(2) > 3:
            errors.update({(i, j) for j in range(GRID_SIZE)})
        if list(col).count(1) > 3 or list(col).count(2) > 3:
            errors.update({(j, i) for j in range(GRID_SIZE)})
    return errors

def check_constraints(grid):
    errors = set()
    for (r, c), (symbol, direction) in constraints.items():
        if direction == 'H' and c < GRID_SIZE - 1:
            val1 = grid[r][c]
            val2 = grid[r][c+1]
        elif direction == 'V' and r < GRID_SIZE - 1:
            val1 = grid[r][c]
            val2 = grid[r+1][c]
        else:
            continue
        if symbol == '=' and val1 != 0 and val2 != 0 and val1 != val2:
            errors.update({(r, c), (r, c+1) if direction == 'H' else (r+1, c)})
        elif symbol == 'x' and val1 != 0 and val2 != 0 and val1 == val2:
            errors.update({(r, c), (r, c+1) if direction == 'H' else (r+1, c)})
    return errors

def check_win(grid):
    return not np.any(grid == 0) and not (
        check_triples(grid) or check_equal_counts(grid) or check_constraints(grid)
    )
