import heapq
import pygame
from time import sleep
import random

# Constants
WIDTH = 800
SQUARE_SIZE = 20
ROWS = 40
COLS = 40
SLEEP_TIME = 0.001 

MIN_BLOCKS = 400    
MAX_BLOCKS = 500


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Initialize the game
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Pathfinding Algorithm')

def draw_grid():
    WIN.fill(WHITE)
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
        pygame.draw.line(WIN, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH))

def draw_walls(blocked_cells):
    for cell in blocked_cells:
        pygame.draw.rect(WIN, BLACK, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_start_end(start, end):
    pygame.draw.rect(WIN, YELLOW, (start[0] * SQUARE_SIZE, start[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(WIN, ORANGE, (end[0] * SQUARE_SIZE, end[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_current_path(path):
    for cell in path:
        pygame.draw.rect(WIN, BLUE, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_visited_cells(visited_cells):
    for cell in visited_cells:
        pygame.draw.rect(WIN, RED, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def calculate_heuristic(x, y, end):
    return abs(end[0] - x) + abs(end[1] - y)

def a_star(start, end):
    path_found = True

    blocked_cells = set()
    for i in range(random.randint(MIN_BLOCKS, MAX_BLOCKS)):
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) == start or (x, y) == end: continue
        if (x, y) in blocked_cells: continue
        blocked_cells.add((x, y))


    q = [(calculate_heuristic(start[0], start[1], end), 0, start[0], start[1], [(start[0], start[1])])]
    g_scores = {start: 0}  

    while q:
        sleep(SLEEP_TIME)
        
        # Pygame handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        f_score, g_score, x, y, path = heapq.heappop(q)
        current = (x, y)

        draw_grid()
        draw_visited_cells(visited_cells)
        draw_current_path(path)
        draw_walls(blocked_cells)
        draw_start_end(start, end)
        pygame.display.update()

        if current == end:
            break

        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            neighbor = (nx, ny)
            if neighbor in visited_cells: continue
            if nx < 0 or nx > COLS - 1: continue
            if ny < 0 or ny > ROWS - 1: continue
            if neighbor in blocked_cells: continue
            if neighbor in path: continue

            tentative_g_score = g_score + 1

            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_heuristic(nx, ny, end)
                visited_cells.add(neighbor)
                heapq.heappush(q, (f_score, tentative_g_score, nx, ny, path + [neighbor]))
    else:
        path_found = False
    visited_cells.clear()
    
    if path_found: sleep(SLEEP_TIME * 100)
    a_star(start, end)

if __name__ == '__main__':
    start = (0, 0)
    end = ((WIDTH // SQUARE_SIZE) - 1, (WIDTH // SQUARE_SIZE) - 1)
    visited_cells = set()
    a_star(start, end)
