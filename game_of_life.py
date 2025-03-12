import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
SPEED = 10

# Colors
ALIVE_COLOR = (0, 255, 0)
DEAD_COLOR = (0, 0, 0)

# Patterns
PATTERNS = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
}

class GameOfLife:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Conway’s Game of Life')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.running = False
        self.speed = SPEED

    def run(self):
        while True:
            self.handle_events()
            if self.running:
                self.update_grid()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.speed)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                elif event.key == pygame.K_r:
                    self.reset_grid()
                elif event.key == pygame.K_d:
                    self.randomize_grid()
                elif event.key == pygame.K_UP:
                    self.speed = min(60, self.speed + 1)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(1, self.speed - 1)
                elif event.key == pygame.K_s:
                    self.save_grid()
                elif event.key == pygame.K_l:
                    self.load_grid()
                elif event.key == pygame.K_p:
                    self.load_pattern("glider")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                self.grid[grid_y][grid_x] = 1 - self.grid[grid_y][grid_x]
            elif event.type == pygame.VIDEORESIZE:
                self.resize_grid(event.w, event.h)

    def resize_grid(self, width, height):
        global WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT
        WIDTH, HEIGHT = width, height
        GRID_WIDTH = WIDTH // CELL_SIZE
        GRID_HEIGHT = HEIGHT // CELL_SIZE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def save_grid(self):
        with open("saved_grid.txt", "w") as f:
            for row in self.grid:
                f.write(" ".join(map(str, row)) + "\n")

    def load_grid(self):
        try:
            with open("saved_grid.txt", "r") as f:
                self.grid = [list(map(int, line.split())) for line in f]
        except FileNotFoundError:
            pass

    def load_pattern(self, pattern_name):
        if pattern_name in PATTERNS:
            self.reset_grid()
            for dx, dy in PATTERNS[pattern_name]:
                self.grid[dy][dx] = 1

    def update_grid(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.grid[y][x] == 1:
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
                else:
                    if alive_neighbors == 3:
                        new_grid[y][x] = 1
        self.grid = new_grid

    def count_alive_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                count += self.grid[ny][nx]
        return count

    def draw_grid(self):
        self.screen.fill(DEAD_COLOR)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = ALIVE_COLOR if self.grid[y][x] == 1 else DEAD_COLOR
                pygame.draw.rect(self.screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def reset_grid(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def randomize_grid(self):
        self.grid = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

if __name__ == '__main__':
    game = GameOfLife()
    game.run()
