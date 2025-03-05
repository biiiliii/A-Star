import heapq
from collections import deque
import pygame
from time import sleep
import random

# Constants
WIDTH = 800               # Amplada de la finestra
SQUARE_SIZE = 20          # Mida de cada quadrat
ROWS = 40                 # Nombre de files
COLS = 40                 # Nombre de columnes
SLEEP_TIME = 0.0001        # Retard per la visualització

MIN_BLOCKS = 400          # Mínim de cel·les bloquejades
MAX_BLOCKS = 500          # Màxim de cel·les bloquejades

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

WIN = None  # La finestra global

class Cell:
    def __init__(self, x, y, wall=False):
        self.x = x
        self.y = y
        self.wall = wall
        self.visited = False
        self.start = False
        self.end = False
        self.in_path = False

    def draw(self, path):
        # Selecciona el color en funció de la propietat de la cel·la
        if self.wall:
            color = BLACK
        elif self.start:
            color = YELLOW
        elif self.end:
            color = ORANGE
        elif (self.x, self.y) in path:
            color = RED
        elif self.in_path:
            color = BLUE
        else:
            color = WHITE
        pygame.draw.rect(WIN, color, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def neighbors_that_are_not_wall(self, maze):
        # Retorna els veïns que no són parets
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = self.x + dx, self.y + dy
            if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
                continue
            if not maze[nx][ny].wall:
                neighbors.append(maze[nx][ny])
        return neighbors
    
def gen_empty_maze():
    # Genera una graella plena de cel·les sense parets
    return [[Cell(x, y, False) for y in range(ROWS)] for x in range(COLS)]

def draw_grid():
    WIN.fill(WHITE)
    # Dibuixa les línies de la graella
    for i in range(ROWS + 1):
        pygame.draw.line(WIN, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
    for j in range(COLS + 1):
        pygame.draw.line(WIN, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, WIDTH))

def draw_maze(maze, path):
    draw_grid()
    for row in maze:
        for cell in row:
            cell.draw(path)
    pygame.display.update()

def add_random_walls(maze, start, end):
    # Afegeix aleatòriament parets, assegurant que el punt d'inici i final no quedin bloquejats
    num_walls = random.randint(MIN_BLOCKS, MAX_BLOCKS)
    placed = 0
    while placed < num_walls:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) == start or (x, y) == end:
            continue
        if not maze[x][y].wall:
            maze[x][y].wall = True
            placed += 1

def grid_maze():
    maze = gen_empty_maze()
    for x in range(COLS):
        for y in range(ROWS):
            if x % 2 == 1 or y % 2 == 1:
                maze[x][y].wall = True
    return maze


def gen_procedural_maze(start):
    maze = grid_maze()
    heap = []
    heapq.heappush(heap, (0, start))
    visited = set()
    visited.add(start)
    while heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        _, pos = heapq.heappop(heap)
        x, y = pos
        maze[x][y].visited = True
        visited.add((x, y))
        draw_maze(maze, [])
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
                continue
            if maze[nx][ny].visited:
                continue
            if (nx, ny) in visited:
                continue
            maze[(x + nx) // 2][(y + ny) // 2].wall = False
            heapq.heappush(heap, (random.random(), (nx, ny)))
            visited.add((nx, ny))
    return maze

def calculate_heuristic(x, y, end):
    # Distància Manhattan
    return abs(end[0] - x) + abs(end[1] - y)

def a_star(maze, start, end):
    # Reinicia les propietats de totes les cel·les
    for row in maze:
        for cell in row:
            cell.visited = False
            cell.in_path = False
            cell.start = False
            cell.end = False

    # Marca el punt d'inici i final
    maze[start[0]][start[1]].start = True
    maze[end[0]][end[1]].end = True

    open_set = []
    heapq.heappush(open_set, (calculate_heuristic(start[0], start[1], end), 0, start[0], start[1], [start]))
    g_scores = {start: 0}
    path_found = False

    while open_set:
        sleep(SLEEP_TIME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        f_score, current_g, x, y, path = heapq.heappop(open_set)
        current = (x, y)
        maze[x][y].visited = True
        # Marca el camí actual: actualitza la propietat in_path de les cel·les corresponents

        for pos in path:
            maze[pos[0]][pos[1]].in_path = True

        draw_maze(maze, path)
        
        if current == end:
            path_found = True
            break

        # Explora els veïns (amunt, avall, esquerra, dreta)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
                continue
            neighbor = maze[nx][ny]
            if neighbor.wall or neighbor.visited:
                continue
            tentative_g = current_g + 1
            if (nx, ny) not in g_scores or tentative_g < g_scores[(nx, ny)]:
                g_scores[(nx, ny)] = tentative_g
                new_f = tentative_g + calculate_heuristic(nx, ny, end)
                heapq.heappush(open_set, (new_f, tentative_g, nx, ny, path + [(nx, ny)]))
    if path_found:
        draw_maze(maze, path)
        sleep(1)
    
    start = (0, 0)
    end = (COLS - 2, ROWS - 2)
    maze = gen_procedural_maze(start)
    a_star(maze, start, end)

def main():
    global WIN
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* amb la classe Cell")
    
    
    start = (0, 0)
    maze = gen_procedural_maze(start)
    end = (COLS - 2, ROWS - 2)
    # add_random_walls(maze, start, end)
    a_star(maze, start, end)

    # Espera que l'usuari tanqui la finestra
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    main()
