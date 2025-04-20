import numpy as np

GRID_SIZE = 6

locked_cells = {
    (0, 1): 1,
    (2, 2): 2,
    (4, 5): 1,
    (5, 0): 2,
    (3, 4): 1

}

def create_initial_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for (r, c), val in locked_cells.items():
        grid[r][c] = val
    return grid
