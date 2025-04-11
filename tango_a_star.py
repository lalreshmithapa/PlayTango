# Tango Puzzle Game with A* Solver Integration

import numpy as np
import pygame
import os
import time
import heapq

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 6
CELL_SIZE = 75
PADDING = 10
TOP_BAR_HEIGHT = 100
GRID_AREA = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = GRID_AREA + 2 * PADDING
WINDOW_HEIGHT = GRID_AREA + TOP_BAR_HEIGHT + 2 * PADDING
FONT = pygame.font.SysFont(None, 35)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)

# Load images
ASSET_PATH = "E:/AI/Game/tango_chat/images/"
sun_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "sun.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
moon_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "moon.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
undo_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "undo.png")), (40, 40))
clear_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "clear.jpg")), (40, 40))

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tango Game with A* Solver")

# Game setup
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
locked_cells = {(0, 1): 1, (2, 2): 2, (4, 5): 1, (5, 0): 2}
for (r, c), val in locked_cells.items():
    grid[r][c] = val

constraints = {
    (0, 0): ('=', 'H'),
    (1, 2): ('x', 'V'),
    (3, 3): ('=', 'V'),
    (4, 1): ('x', 'H'),
    (2, 5): ('=', 'H')
}

# Remove constraints that would end on the last column or row
to_remove = []
for (r, c), (symbol, direction) in constraints.items():
    if (direction == 'H' and c == GRID_SIZE - 1) or (direction == 'V' and r == GRID_SIZE - 1):
        to_remove.append((r, c))
for key in to_remove:
    del constraints[key]

history = []

# --- Constraint Check Functions ---
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
    return not np.any(grid == 0) and not (check_triples(grid) or check_equal_counts(grid) or check_constraints(grid))

# --- A* Solver ---
class TangoState:
    def __init__(self, grid, locked, parent=None):
        self.grid = np.copy(grid)
        self.locked = locked
        self.parent = parent

    def __lt__(self, other):
        return False  # Required for heapq to avoid comparison error

    def __hash__(self):
        return hash(self.grid.tobytes())

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)

    def get_next_states(self):
        states = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0 and (i, j) not in self.locked:
                    for val in [1, 2]:
                        new_grid = np.copy(self.grid)
                        new_grid[i][j] = val
                        temp = TangoState(new_grid, self.locked, self)
                        if not check_triples(temp.grid) and not check_equal_counts(temp.grid) and not check_constraints(temp.grid):
                            states.append(temp)
                    return states
        return []

def heuristic(grid):
    return len(check_triples(grid)) + len(check_equal_counts(grid)) + len(check_constraints(grid))

def a_star_solver(start_grid, locked):
    start = TangoState(start_grid, locked)
    frontier = [(heuristic(start.grid), 0, start)]
    seen = {hash(start): 0}
    while frontier:
        _, g, current = heapq.heappop(frontier)
        if check_win(current.grid):
            return reconstruct_path(current)
        for next_state in current.get_next_states():
            key = hash(next_state)
            new_cost = g + 1
            if key not in seen or new_cost < seen[key]:
                seen[key] = new_cost
                heapq.heappush(frontier, (new_cost + heuristic(next_state.grid), new_cost, next_state))
    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append(state.grid)
        state = state.parent
    return path[::-1]

# --- Drawing ---
def draw_grid(start_time, timer_stopped):
    screen.fill(WHITE)
    errors = check_triples(grid).union(check_equal_counts(grid)).union(check_constraints(grid))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = PADDING + col * CELL_SIZE
            y = TOP_BAR_HEIGHT + PADDING + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = RED if (row, col) in errors else BLACK
            pygame.draw.rect(screen, color, rect, 3 if (row, col) in errors else 1)
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

    elapsed = stop_time - start_time if timer_stopped else time.time() - start_time
    mins, secs = divmod(int(elapsed), 60)
    screen.blit(FONT.render(f"Time: {mins:02}:{secs:02}", True, BLACK), (10, 5))
    if check_win(grid):
        screen.blit(FONT.render("You Win!", True, GREEN), (200, 5))
    screen.blit(undo_img, (WINDOW_WIDTH - 100, 5))
    screen.blit(clear_img, (WINDOW_WIDTH - 50, 5))
    pygame.draw.rect(screen, GRAY, (WINDOW_WIDTH - 170, 5, 60, 40))
    screen.blit(FONT.render("Solve", True, BLACK), (WINDOW_WIDTH - 165, 10))
    pygame.display.flip()

# --- Main Loop ---
def main():
    global stop_time
    running = True
    last_click = 0
    click_delay = 300
    start_time = time.time()
    timer_stopped = False

    while running:
        if not timer_stopped and check_win(grid):
            stop_time = time.time()
            timer_stopped = True

        draw_grid(start_time, timer_stopped)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    path = a_star_solver(grid, locked_cells)
                    if path:
                        for g in path:
                            grid[:, :] = g
                            draw_grid(start_time, timer_stopped)
                            pygame.time.delay(300)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 5 <= y <= 45:
                    if WINDOW_WIDTH - 100 <= x <= WINDOW_WIDTH - 60 and history:
                        grid[:, :] = history.pop()
                    elif WINDOW_WIDTH - 50 <= x <= WINDOW_WIDTH - 10:
                        history.append(np.copy(grid))
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                if (i, j) not in locked_cells:
                                    grid[i][j] = 0
                        timer_stopped = False
                    elif WINDOW_WIDTH - 170 <= x <= WINDOW_WIDTH - 110:
                        path = a_star_solver(grid, locked_cells)
                        if path:
                            for g in path:
                                grid[:, :] = g
                                draw_grid(start_time, timer_stopped)
                                pygame.time.delay(300)
                elif TOP_BAR_HEIGHT + PADDING <= y < TOP_BAR_HEIGHT + PADDING + GRID_AREA:
                    col = (x - PADDING) // CELL_SIZE
                    row = (y - TOP_BAR_HEIGHT - PADDING) // CELL_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and (row, col) not in locked_cells:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_click < click_delay:
                            history.append(np.copy(grid))
                            grid[row][col] = (grid[row][col] % 2) + 1 if grid[row][col] else 1
                        else:
                            if grid[row][col] == 0:
                                history.append(np.copy(grid))
                                grid[row][col] = 1
                        last_click = current_time

    pygame.quit()

if __name__ == "__main__":
    main()
