import heapq
import pygame
from time import sleep
import random

# Constants
WIDTH = 800  # Width of the window
SQUARE_SIZE = 20  # Size of each square in the grid
ROWS = 40  # Number of rows in the grid
COLS = 40  # Number of columns in the grid
SLEEP_TIME = 0.001  # Sleep time for visualization

MIN_BLOCKS = 400  # Minimum number of blocked cells
MAX_BLOCKS = 500  # Maximum number of blocked cells

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

# Function to draw the grid
def draw_grid():
    WIN.fill(WHITE)
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
        pygame.draw.line(WIN, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH))

# Function to draw the walls (blocked cells)
def draw_walls(blocked_cells):
    for cell in blocked_cells:
        pygame.draw.rect(WIN, BLACK, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the start and end points
def draw_start_end(start, end):
    pygame.draw.rect(WIN, YELLOW, (start[0] * SQUARE_SIZE, start[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(WIN, ORANGE, (end[0] * SQUARE_SIZE, end[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the current path
def draw_current_path(path):
    for cell in path:
        pygame.draw.rect(WIN, BLUE, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the visited cells
def draw_visited_cells(visited_cells):
    for cell in visited_cells:
        pygame.draw.rect(WIN, RED, (cell[0] * SQUARE_SIZE, cell[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to calculate the heuristic (Manhattan distance)
def calculate_heuristic(x, y, end):
    return abs(end[0] - x) + abs(end[1] - y)

# A* algorithm implementation
def a_star(start, end):
    path_found = True

    # Generate random blocked cells
    blocked_cells = set()
    for i in range(random.randint(MIN_BLOCKS, MAX_BLOCKS)):
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) == start or (x, y) == end: continue
        if (x, y) in blocked_cells: continue
        blocked_cells.add((x, y))

    # Priority queue for the A* algorithm
    q = [(calculate_heuristic(start[0], start[1], end), 0, start[0], start[1], [(start[0], start[1])])]
    g_scores = {start: 0}  # Dictionary to store the g-scores

    while q:
        sleep(SLEEP_TIME)
        
        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Get the current node with the lowest f-score
        f_score, g_score, x, y, path = heapq.heappop(q)
        current = (x, y)

        # Draw the current state of the grid
        draw_grid()
        draw_visited_cells(visited_cells)
        draw_current_path(path)
        draw_walls(blocked_cells)
        draw_start_end(start, end)
        pygame.display.update()

        # Check if we have reached the end
        if current == end:
            break

        # Explore the neighbors
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            neighbor = (nx, ny)
            if neighbor in visited_cells: continue
            if nx < 0 or nx > COLS - 1: continue
            if ny < 0 or ny > ROWS - 1: continue
            if neighbor in blocked_cells: continue
            if neighbor in path: continue

            tentative_g_score = g_score + 1

            # If this path to the neighbor is better, update the path
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_heuristic(nx, ny, end)
                visited_cells.add(neighbor)
                heapq.heappush(q, (f_score, tentative_g_score, nx, ny, path + [neighbor]))
    else:
        path_found = False
    visited_cells.clear()
    
    # If path is found, sleep for a while before restarting
    if path_found: sleep(SLEEP_TIME * 100)
    a_star(start, end)

if __name__ == '__main__':
    start = (0, 0)  # Starting point
    end = ((WIDTH // SQUARE_SIZE) - 1, (WIDTH // SQUARE_SIZE) - 1)  # Ending point
    visited_cells = set()  # Set to store visited cells
    a_star(start, end)  # Run the A* algorithm
