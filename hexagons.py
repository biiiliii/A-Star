import pygame
import math
from time import sleep
import heapq
import random

# Hexagon class to represent each hexagonal cell in the grid
class Hexagon:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = WHITE
        self.posx = x * size * 1.76
        self.posy = y * size * 1.5
        self.directions = []
        self.wall = False

    # Draw the hexagon on the Pygame window
    def draw(self):
        if self.wall: self.color = BLACK
        points = []
        for i in range(6):
            angle_deg = 60 * i + 90
            angle_rad = math.radians(angle_deg)
            offset = 0 if self.y % 2 == 0 else self.size * 0.9
            points.append((offset + 45 + self.posx + self.size * math.cos(angle_rad),
                           60 + self.posy + self.size * math.sin(angle_rad)))

        pygame.draw.polygon(WINDOW, self.color, points)
        pygame.draw.polygon(WINDOW, BLACK, points, 1)

    # Get the neighboring hexagons
    def get_neigbors(self):
        if self.y % 2 == 0:
            self.directions = [(self.x + 1, self.y + 0), (self.x + 0, self.y + 1), (self.x + -1,self.y +  1), (self.x + -1,self.y +  0), (self.x + -1,self.y +  -1), (self.x + 0, self.y + -1)]
        else:
            self.directions = [(self.x + 1, self.y + 0), (self.x + 1, self.y + 1), (self.x + 0, self.y + 1), (self.x + -1,self.y +  0), (self.x + 0, self.y + -1), (self.x + 1, self.y + -1)]

# Initialize Pygame
pygame.init()

SLEEP_TIME = 0.05

# Constants
WIDTH = 800
HEIGHT = 800
HEX_SIZE = 30
ROWS = 16
COLS = 14
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Grid")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Function to draw the grid and update the colors of hexagons
def draw_grid(hexagons, start, end, path, visited_cells):
    WINDOW.fill(BLACK)
    
    for cell in visited_cells:
        hexagons[cell[0]][cell[1]].color = RED
    for cell in path:
        hexagons[cell[0]][cell[1]].color = BLUE
    hexagons[start[0]][start[1]].color = YELLOW
    hexagons[end[0]][end[1]].color = ORANGE
    for row in hexagons:
        for hexagon in row:
            hexagon.draw()

# Heuristic function for A* algorithm
def calculate_heuristic(x, y, end):
    return abs(end[0] - x) + abs(end[1] - y)

# Function to renew the hexagons grid
def renew_hexagons():
    hexagons = []
    for x in range(COLS):
        tmp = []
        for y in range(ROWS):
            tmp.append(Hexagon(x, y, HEX_SIZE))
        hexagons.append(tmp)
    return hexagons

# A* pathfinding algorithm
def a_star(start, end):
    
    hexagons = renew_hexagons()

    path_found = True

    visited_cells = set()

    # Add random walls to the grid
    for i in range(75):
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) == start or (x, y) == end: continue
        hexagons[x][y].wall = True

    # Get neighbors for each hexagon
    for x in range(COLS):
        for y in range(ROWS):
            hexagons[x][y].get_neigbors()

    # Priority queue for A* algorithm
    q = [(calculate_heuristic(start[0], start[1], end), 0, start[0], start[1], [(start[0], start[1])])]
    g_scores = {start: 0}

    while q:
        sleep(SLEEP_TIME)

        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        f_score, g_score, x, y, path = heapq.heappop(q)
        current = (x, y)

        draw_grid(hexagons, start, end, path, visited_cells)
        pygame.display.update()

        if current == end: return

        for nx, ny in hexagons[x][y].directions:
            neighbor = (nx, ny)
            if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS: continue
            if neighbor in visited_cells: continue
            if hexagons[nx][ny].wall: continue
            if neighbor in path: continue

            tentative_g_score = g_score + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_heuristic(nx, ny, end)
                heapq.heappush(q, (f_score, tentative_g_score, nx, ny, path + [neighbor]))
                visited_cells.add(neighbor)
    else:
        path_found = False
    visited_cells.clear()

    if path_found: sleep(1)

# Main function to run the A* algorithm
if __name__ == "__main__":
    start = (0, 0)
    end = (COLS - 1, ROWS - 1)

    visited_cells = set()

    while True:
        a_star(start, end)