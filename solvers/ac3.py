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
FONT = pygame.font.SysFont("arial", 25)
BUTTONFONT = pygame.font.SysFont("arial", 17, bold=False)
GRAY_TRANSPARENT = (150, 150, 150, 180) 
BORDER_COLOR = (100, 100, 100)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)
ORANGE = (255, 165, 0)

ASSET_PATH = "/Users/mgrsuraz/Downloads/PlayTango/assets/images/"
sun_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "sun.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
moon_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "moon.png")), (CELL_SIZE - 20, CELL_SIZE - 20))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tango Game")

grid = create_initial_grid()

highlighted_cells = set()
history = []
start_time = None
timer_stopped = False


def draw_pill_button(text, pos, padding=20):
    text_surf = BUTTONFONT.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    
    btn_width = text_rect.width + 2 * padding
    btn_height = text_rect.height + padding
    btn_rect = pygame.Rect(pos[0], pos[1], btn_width, btn_height)
    btn_rect.center = pos

    button_surf = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surf, GRAY_TRANSPARENT, button_surf.get_rect(), border_radius=btn_height // 2)
    pygame.draw.rect(button_surf, BORDER_COLOR, button_surf.get_rect(), width=2, border_radius=btn_height // 2)

    screen.blit(button_surf, btn_rect.topleft)
    text_pos = text_surf.get_rect(center=btn_rect.center)
    screen.blit(text_surf, text_pos)

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
        screen.blit(FONT.render("You Win!", True, GREEN), (200, 60))

    draw_pill_button("Solve", (WINDOW_WIDTH - 210, 25))
    draw_pill_button("Undo", (WINDOW_WIDTH - 130, 25))
    draw_pill_button("Clear", (WINDOW_WIDTH - 50, 25))


    pygame.display.flip()

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
                    if WINDOW_WIDTH - 170 <= x <= WINDOW_WIDTH - 90 and history:
                        grid[:, :] = history.pop()
                        start_time = None
                        timer_stopped = False
                    elif WINDOW_WIDTH - 95 <= x <= WINDOW_WIDTH - 5:
                        history.append(np.copy(grid))
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                if (i, j) not in locked_cells:
                                    grid[i][j] = 0
                        start_time = None
                        timer_stopped = False
                    elif WINDOW_WIDTH - 255 <= x <= WINDOW_WIDTH - 165:
                        if not start_time:
                            start_time = time.time()
                        timer_stopped = False
                        solve()
    pygame.quit()

if __name__ == "__main__":
    main()
