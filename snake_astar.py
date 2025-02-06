"""
# MIT License
# 
# Copyright (c) 2025 Biel Martinez Olivé
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import heapq
import random
import sys

# --------- Global Constants ---------
GRID_WIDTH = 30
GRID_HEIGHT = 30
CELL_SIZE = 20
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
BLACK       = (0, 0, 0)
DARK_GREY   = (50, 50, 50)   # grid lines
GREY        = (128, 128, 128) # explored cells in A*
WHITE       = (255, 255, 255) # current cell & reconstructed path in A*
GREEN       = (0, 255, 0)     # snake head
DARK_GREEN  = (0, 180, 0)     # snake body
RED         = (255, 0, 0)     # apple

# --------- A* Helper Functions ---------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node):
    x, y = node
    results = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid = []
    for nx, ny in results:
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            valid.append((nx, ny))
    return valid

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar_search(start, goal, obstacles, visualize=True):
    """
    A* search implemented as a generator for visualization.
    Parameters:
      start: starting cell (tuple)
      goal: target cell (tuple)
      obstacles: set of cells that cannot be passed (e.g. snake's body, excluding the head)
      visualize: whether to yield intermediate states for visualization (default: True)
    Yields dictionaries with the current A* state:
      - "current": cell being expanded
      - "closed": set of already expanded cells
      - "open": list of cells in the frontier (for information)
      - "came_from": dictionary of parent pointers
      - "done": whether the search is finished
      - "final": whether this is the final state (path found or failure)
    When a path is found, the final yield includes key "path" with the full path.
    """
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    gscore = {start: 0}
    closed_set = set()
    counter = 0

    while open_set:
        current_f, _, current = heapq.heappop(open_set)
        if visualize:
            # Yield the state for visualization.
            yield {
                "current": current,
                "closed": closed_set.copy(),
                "open": [item[2] for item in open_set],
                "came_from": came_from.copy(),
                "done": False,
                "final": False,
            }
        if current == goal:
            path = reconstruct_path(came_from, current)
            yield {"path": path, "done": True, "final": True}
            return

        closed_set.add(current)

        for neighbor in neighbors(current):
            if neighbor in obstacles:
                continue
            if neighbor in closed_set:
                continue
            tentative_g = gscore[current] + 1
            if neighbor not in gscore or tentative_g < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g
                fscore = tentative_g + heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (fscore, counter, neighbor))
    # No path found:
    yield {"path": None, "done": True, "final": True}
    return

# --------- The Snake Game Class ---------
class SnakeGame:
    visualize = True

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake with A* Radar & Growing Body")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        # Initialize the snake with a few segments.
        midx = GRID_WIDTH // 2
        midy = GRID_HEIGHT // 2
        self.snake = [(midx, midy), (midx - 1, midy), (midx - 2, midy)]
        self.apple = self.random_apple()
        # Modes:
        # "compute" = A* is computing the path to the apple
        # "move"    = snake is following the computed path
        self.mode = "compute"
        self.astar_generator = self.create_astar_generator()
        self.astar_state = None
        self.path = None  # Final computed path (list of cells, excluding current head)

    def random_apple(self):
        # Choose a random apple location not on the snake.
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def create_astar_generator(self):
        # For planning, treat the snake's body (except the head) as obstacles.
        obstacles = set(self.snake[1:])
        return astar_search(self.snake[0], self.apple, obstacles, self.visualize)

    def update(self):
        # Process quit events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.mode == "compute":
            # Step one iteration of A* for visualization.
            try:
                self.astar_state = next(self.astar_generator)
                if self.astar_state.get("done"):
                    # A* finished—if a path was found, use it.
                    if self.astar_state.get("path") is None:
                        print("No path found!")
                        self.mode = "move"
                        self.path = []
                    else:
                        full_path = self.astar_state["path"]
                        # Remove the first cell (current head) from the planned path.
                        self.path = full_path[1:] if len(full_path) > 1 else []
                        self.mode = "move"
            except StopIteration:
                self.mode = "move"

        elif self.mode == "move":
            # Follow the computed path one step at a time.
            if self.path and len(self.path) > 0:
                next_cell = self.path.pop(0)
                # Check if the next move leads to the apple.
                if next_cell == self.apple:
                    # Grow: add new head, but do not remove tail.
                    self.snake.insert(0, next_cell)
                    # Place new apple and recompute path.
                    self.apple = self.random_apple()
                    self.mode = "compute"
                    self.astar_generator = self.create_astar_generator()
                    self.astar_state = None
                    self.path = None
                else:
                    # Normal move: add new head and remove tail.
                    self.snake.insert(0, next_cell)
                    self.snake.pop()
            else:
                # If there is no valid path (or the computed path is empty), replan.
                self.mode = "compute"
                self.astar_generator = self.create_astar_generator()
                self.astar_state = None
                self.path = None

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw the apple.
        ax, ay = self.apple
        apple_rect = pygame.Rect(ax * CELL_SIZE, ay * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, apple_rect)

        # Draw the snake.
        for idx, segment in enumerate(self.snake):
            sx, sy = segment
            rect = pygame.Rect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if idx == 0 else DARK_GREEN
            pygame.draw.rect(self.screen, color, rect)

        # Visualize A* search when computing:
        if self.mode == "compute" and self.astar_state:
            # Draw explored (closed) cells in grey.
            for cell in self.astar_state.get("closed", set()):
                cx, cy = cell
                rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GREY, rect)
            # Draw the current cell being expanded in bright white.
            current = self.astar_state.get("current", None)
            if current:
                cx, cy = current
                rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect)

            came_from = self.astar_state.get("came_from", {})
            if current:
                path_so_far = reconstruct_path(came_from, current)
                for cell in path_so_far:
                    cx, cy = cell
                    rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, WHITE, rect)


        if self.mode == "move" and self.path:
            for cell in self.path:
                cx, cy = cell
                rect = pygame.Rect(cx * CELL_SIZE + CELL_SIZE // 4,
                                   cy * CELL_SIZE + CELL_SIZE // 4,
                                   CELL_SIZE // 2, CELL_SIZE // 2)
                pygame.draw.rect(self.screen, WHITE, rect)

        pygame.display.flip()

    def run(self):
        ticks = 20
        self.visualize = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        ticks += 5
                    elif event.key == pygame.K_DOWN:
                        ticks -= 5
                    elif event.key == pygame.K_SPACE:
                        self.visualize = not self.visualize
            self.update()
            self.draw()
            self.clock.tick(ticks)

if __name__ == "__main__":
    print("=========================================")
    print("Snake with A* Radar & Growing Body")
    print("Controls:")
    print("  Arrow keys: Increase/decrease speed")
    print("  Space: Toggle visualization")
    print("=========================================")
    game = SnakeGame()
    game.run()
