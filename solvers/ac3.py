# AC-3 + Backtracking Visualization

import numpy as np
import pygame
import os
import time
from collections import deque
from game.constraints import check_win, check_triples, check_equal_counts, check_constraints, locked_cells, constraints
from game.grid_setup import create_initial_grid, locked_cells

pygame.init()

GRID_SIZE = 6
CELL_SIZE = 75
PADDING = 10
TOP_BAR_HEIGHT = 100
GRID_AREA = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = GRID_AREA + 2 * PADDING
WINDOW_HEIGHT = GRID_AREA + TOP_BAR_HEIGHT + 2 * PADDING
FONT = pygame.font.SysFont(None, 35)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
ORANGE = (255, 165, 0)

ASSET_PATH = "/Users/mgrsuraz/Downloads/PlayTango/assets/images/"
sun_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "sun.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
moon_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "moon.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
undo_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "undo.png")), (40, 40))
clear_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "clear.jpg")), (40, 40))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tango Game")

# grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
# locked_cells = {(0, 1): 1, (2, 2): 2, (4, 5): 1, (5, 0): 2}
# for (r, c), val in locked_cells.items():
#     grid[r][c] = val
grid = create_initial_grid()

# constraints = {
#     (0, 0): ('=', 'H'),
#     (1, 2): ('x', 'V'),
#     (3, 3): ('=', 'V'),
#     (4, 1): ('x', 'H'),
#     (2, 5): ('=', 'H')
# }
# constraints = {k: v for k, v in constraints.items() if not (v[1] == 'H' and k[1] == GRID_SIZE - 1 or v[1] == 'V' and k[0] == GRID_SIZE - 1)}
highlighted_cells = set()
history = []
start_time = None
timer_stopped = False


# def check_win(grid):
#     return not np.any(grid == 0) and not (check_triples(grid) or check_equal_counts(grid) or check_constraints(grid))

def draw_grid():
    screen.fill(WHITE)
    errors = check_triples(grid).union(check_equal_counts(grid)).union(check_constraints(grid))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = PADDING + col * CELL_SIZE
            y = TOP_BAR_HEIGHT + PADDING + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = ORANGE if (row, col) in highlighted_cells else RED if (row, col) in errors else BLACK
            pygame.draw.rect(screen, color, rect, 3 if color != BLACK else 1)
            val = grid[row][col]
            if val == 1:
                screen.blit(sun_img, (x + 5, y + 5))
            elif val == 2:
                screen.blit(moon_img, (x + 5, y + 5))

    for (r, c), (symbol, direction) in constraints.items():
        if direction == 'H':
            x_center = PADDING + (c + 1) * CELL_SIZE
            y_center = TOP_BAR_HEIGHT + PADDING + (r + 0.5) * CELL_SIZE
        else:
            x_center = PADDING + (c + 0.5) * CELL_SIZE
            y_center = TOP_BAR_HEIGHT + PADDING + (r + 1) * CELL_SIZE
        c_text = FONT.render(symbol, True, RED)
        screen.blit(c_text, c_text.get_rect(center=(x_center, y_center)))

    elapsed = time.time() - start_time if start_time and not timer_stopped else (stop_time - start_time if start_time else 0)
    mins, secs = divmod(int(elapsed), 60)
    screen.blit(FONT.render(f"Time: {mins:02}:{secs:02}", True, BLACK), (10, 5))
    if check_win(grid):
        screen.blit(FONT.render("You Win!", True, GREEN), (200, 5))

    pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH - 210, 5, 60, 40))
    screen.blit(FONT.render("Solve", True, BLACK), (WINDOW_WIDTH - 200, 10))
    pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH - 140, 5, 40, 40))
    screen.blit(undo_img, (WINDOW_WIDTH - 137, 7))
    pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH - 90, 5, 40, 40))
    screen.blit(clear_img, (WINDOW_WIDTH - 87, 7))
    pygame.display.flip()

# def check_triples(grid):
#     errors = set()
#     for i in range(GRID_SIZE):
#         for j in range(GRID_SIZE - 2):
#             row = grid[i, j:j+3]
#             if row[0] == row[1] == row[2] != 0:
#                 errors.update({(i, j), (i, j+1), (i, j+2)})
#             col = grid[j:j+3, i]
#             if col[0] == col[1] == col[2] != 0:
#                 errors.update({(j, i), (j+1, i), (j+2, i)})
#     return errors

# def check_equal_counts(grid):
#     errors = set()
#     for i in range(GRID_SIZE):
#         row = grid[i]
#         col = grid[:, i]
#         if list(row).count(1) > 3 or list(row).count(2) > 3:
#             errors.update({(i, j) for j in range(GRID_SIZE)})
#         if list(col).count(1) > 3 or list(col).count(2) > 3:
#             errors.update({(j, i) for j in range(GRID_SIZE)})
#     return errors

# def check_constraints(grid):
#     errors = set()
#     for (r, c), (symbol, direction) in constraints.items():
#         if direction == 'H' and c < GRID_SIZE - 1:
#             val1 = grid[r][c]
#             val2 = grid[r][c+1]
#         elif direction == 'V' and r < GRID_SIZE - 1:
#             val1 = grid[r][c]
#             val2 = grid[r+1][c]
#         else:
#             continue
#         if symbol == '=' and val1 != 0 and val2 != 0 and val1 != val2:
#             errors.update({(r, c), (r, c+1) if direction == 'H' else (r+1, c)})
#         elif symbol == 'x' and val1 != 0 and val2 != 0 and val1 == val2:
#             errors.update({(r, c), (r, c+1) if direction == 'H' else (r+1, c)})
#     return errors

def is_valid():
    return not check_triples(grid) and not check_equal_counts(grid) and not check_constraints(grid)

def neighbors(cell):
    i, j = cell
    return [(i+di, j+dj) for di, dj in [(-1,0),(1,0),(0,-1),(0,1)] if 0<=i+di<GRID_SIZE and 0<=j+dj<GRID_SIZE]

def get_domains():
    domains = {}
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) not in locked_cells and grid[i][j] == 0:
                domains[(i, j)] = [1, 2]
    return domains

def revise(x, y, domains):
    if x not in domains or y not in domains:
        return False
    revised = False
    new_domain = []
    for vx in domains[x]:
        grid[x] = vx
        consistent = False
        for vy in domains[y]:
            grid[y] = vy
            if is_valid():
                consistent = True
                break
        grid[y] = 0
        if consistent:
            new_domain.append(vx)
    grid[x] = 0
    if new_domain != domains[x]:
        domains[x] = new_domain
        revised = True
    return revised

def ac3(domains):
    queue = deque([(x, y) for x in domains for y in neighbors(x) if y in domains])
    while queue:
        x, y = queue.popleft()
        if revise(x, y, domains):
            draw_grid()
            pygame.time.delay(100)
            if not domains[x]:
                return False
            for z in neighbors(x):
                if z != y:
                    queue.append((z, x))
    return True

def backtrack():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0 and (i, j) not in locked_cells:
                for val in [1, 2]:
                    grid[i][j] = val
                    highlighted_cells.clear()
                    highlighted_cells.add((i, j))
                    draw_grid()
                    pygame.time.delay(100)
                    if is_valid():
                        if backtrack():
                            return True
                    grid[i][j] = 0
                    draw_grid()
                    pygame.time.delay(100)
                return False
    return True

def solve():
    global stop_time, timer_stopped
    domains = get_domains()
    if ac3(domains):
        if not backtrack():
            print("Backtracking failed after AC-3")
    else:
        print("AC-3 detected inconsistency")
    stop_time = time.time()
    timer_stopped = True

# Main

def main():
    global start_time, timer_stopped
    running = True
    while running:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 5 <= y <= 45:
                    if WINDOW_WIDTH - 140 <= x <= WINDOW_WIDTH - 100 and history:
                        grid[:, :] = history.pop()
                        start_time = None
                        timer_stopped = False
                    elif WINDOW_WIDTH - 90 <= x <= WINDOW_WIDTH - 50:
                        history.append(np.copy(grid))
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                if (i, j) not in locked_cells:
                                    grid[i][j] = 0
                        start_time = None
                        timer_stopped = False
                    elif WINDOW_WIDTH - 210 <= x <= WINDOW_WIDTH - 150:
                        if not start_time:
                            start_time = time.time()
                        timer_stopped = False
                        solve()
    pygame.quit()

if __name__ == "__main__":
    main()
