# Solving with Q-Learning; agent starts from top left corner of the grid

import pygame
import numpy as np
import os
import time
import random
from collections import defaultdict
from game.constraints import check_win, check_triples, check_equal_counts, check_constraints, locked_cells, constraints
from game.grid_setup import create_initial_grid

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

WHITE, BLACK, RED, GREEN, GRAY, BLUE = (255,255,255), (0,0,0), (255,0,0), (0,200,0), (180,180,180), (0,0,255)

ASSET_PATH = "assets/images/"
sun_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "sun.png")), (CELL_SIZE - 20, CELL_SIZE - 20))
moon_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "moon.png")), (CELL_SIZE - 20, CELL_SIZE - 20))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tango Game")

grid = create_initial_grid()

# Q-learning Agent Class
class TangoQLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qvalues = defaultdict(float)

    def getLegalActions(self, grid, locked_cells):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) not in locked_cells and grid[i][j] == 0:
                    return [(i, j, val) for val in [1, 2]]  # Only allow the next unfilled cell
        return []  # All cells filled


    def getQValue(self, state, action):
        return self.qvalues[(self._state_key(state), action)]

    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(*state)
        if not actions: return 0.0
        return max(self.getQValue(state, a) for a in actions)

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(*state)
        if not actions: return None
        qvals = [(a, self.getQValue(state, a)) for a in actions]
        max_q = max(qvals, key=lambda x: x[1])[1]
        best = [a for a, q in qvals if q == max_q]
        return random.choice(best)

    def getAction(self, state):
        actions = self.getLegalActions(*state)
        if not actions: return None
        return random.choice(actions) if random.random() < self.epsilon else self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        sk, nk = self._state_key(state), self._state_key(nextState)
        old_q = self.qvalues[(sk, action)]
        future = self.computeValueFromQValues(nextState)
        self.qvalues[(sk, action)] = old_q + self.alpha * (reward + self.gamma * future - old_q)

    def _state_key(self, state):
        grid, locked = state
        return tuple(grid.flatten()), frozenset(locked.items())

# Agent + Support
agent = TangoQLearningAgent()
highlighted = None
history = []
start_time = None
stop_time = None
timer_stopped = False
last_move = None

def compute_reward():
    if check_win(grid): return 100
    if check_triples(grid) or check_equal_counts(grid) or check_constraints(grid): return -5
    return 1

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
            color = BLUE if (row, col) == highlighted else RED if (row, col) in errors else BLACK
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
    if last_move:
        screen.blit(FONT.render(f"Move: {last_move[0]} at {last_move[1]}", True, BLUE), (200, 60))
    if check_win(grid):
        screen.blit(FONT.render("You Win!", True, GREEN), (50, 50))

    draw_pill_button("Train", (WINDOW_WIDTH - 210, 25))
    draw_pill_button("Undo", (WINDOW_WIDTH - 130, 25))
    draw_pill_button("Clear", (WINDOW_WIDTH - 50, 25))

    pygame.display.flip()

def play_agent(max_retries=30):
    global grid, last_move, stop_time, timer_stopped
    for attempt in range(max_retries):
        grid = create_initial_grid()
        state = (grid.copy(), locked_cells)
        steps = 0
        episode = []
        while not check_win(grid) and steps < 100:
            pygame.event.pump()
            draw_grid()
            time.sleep(0.2)
            action = agent.getAction(state)
            if action is None: break
            i, j, val = action
            grid[i][j] = val
            reward = compute_reward()
            next_state = (grid.copy(), locked_cells)
            if reward < 0: grid[i][j] = 0
            else: state = next_state
            last_move = ("Sun" if val == 1 else "Moon", (i, j))
            episode.append((state, action, next_state, reward))
            steps += 1
        for s, a, ns, r in episode:
            agent.update(s, a, ns, r)
        if check_win(grid):
            print(f"Solved in {steps} steps on attempt {attempt + 1}")
            break
        else:
            print(f"Attempt {attempt + 1} failed. Retrying...")
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
                        timer_stopped = False
                        start_time = None
                    elif WINDOW_WIDTH - 95 <= x <= WINDOW_WIDTH - 5:
                        history.append(np.copy(grid))
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                if (i, j) not in locked_cells:
                                    grid[i][j] = 0
                        timer_stopped = False
                        start_time = None
                    elif WINDOW_WIDTH - 255 <= x <= WINDOW_WIDTH - 165:
                        if not start_time:
                            start_time = time.time()
                        timer_stopped = False
                        play_agent()
    pygame.quit()

if __name__ == "__main__":
    main()
