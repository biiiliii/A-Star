import pygame
import math
from time import sleep

class Hexagon:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = WHITE
        self.posx = x * size * 1.76
        self.posy = y * size * 1.5

    def draw(self):
        points = []
        for i in range(6):
            angle_deg = 60 * i + 90
            angle_rad = math.radians(angle_deg)
            offset = 0 if self.y % 2 == 0 else self.size * 0.9
            points.append((offset + 45 + self.posx + self.size * math.cos(angle_rad),
                           60 + self.posy + self.size * math.sin(angle_rad)))

        pygame.draw.polygon(WINDOW, self.color, points)
        pygame.draw.polygon(WINDOW, BLACK, points, 1)

    

# Initialize Pygame
pygame.init()

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

def draw_grid():
    WINDOW.fill(BLACK)
    for row in hexagons:
        for hexagon in row:
            hexagon.draw()



def a_star(start, end):
    pass

    
if __name__ == "__main__":

    hexagons = []
    for x in range(COLS):
        tmp = []
        for y in range(ROWS):
            tmp.append(Hexagon(x, y, HEX_SIZE))
        hexagons.append(tmp)

    

    start = (0, 0)
    end = (COLS - 1, ROWS - 1)

    hexagons[start[0]][start[1]].color = YELLOW
    hexagons[end[0]][end[1]].color = ORANGE

    draw_grid()
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()