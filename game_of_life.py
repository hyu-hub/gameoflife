import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 1000, 600
CONTROL_PANEL_WIDTH = 200  # Fixed control panel width
CELL_SIZE = 10  # Initial cell size
MIN_CELL_SIZE = 5  # Minimum cell size
MAX_CELL_SIZE = 20  # Maximum cell size
GAME_PANEL_WIDTH = WIDTH - CONTROL_PANEL_WIDTH
GRID_WIDTH = GAME_PANEL_WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
SPEED = 10

# Colors and Themes
THEMES = {
    "classic": {
        "alive": (50, 205, 50),
        "dead": (15, 15, 15),
        "grid": (30, 30, 30),
        "text": (220, 220, 220),
        "panel": (25, 25, 25),
        "highlight": (40, 40, 40),
        "button": (35, 35, 35)
    },
    "ocean": {
        "alive": (64, 224, 208),
        "dead": (5, 15, 25),
        "grid": (20, 35, 45),
        "text": (220, 240, 255),
        "panel": (10, 20, 30),
        "highlight": (15, 30, 45),
        "button": (12, 25, 35)
    },
    "desert": {
        "alive": (255, 140, 0),
        "dead": (40, 20, 0),
        "grid": (80, 40, 0),
        "text": (255, 220, 180),
        "panel": (30, 15, 0),
        "highlight": (100, 50, 0),
        "button": (60, 30, 0)
    },
    "matrix": {
        "alive": (0, 255, 0),
        "dead": (0, 20, 0),
        "grid": (0, 40, 0),
        "text": (0, 255, 0),
        "panel": (0, 10, 0),
        "highlight": (0, 60, 0),
        "button": (0, 30, 0)
    },
    "sunset": {
        "alive": (255, 170, 50),
        "dead": (20, 10, 15),
        "grid": (40, 20, 25),
        "text": (255, 220, 200),
        "panel": (25, 12, 18),
        "highlight": (45, 22, 28),
        "button": (35, 15, 20)
    },
    "neon": {
        "alive": (255, 50, 255),
        "dead": (10, 5, 15),
        "grid": (30, 15, 35),
        "text": (200, 255, 255),
        "panel": (15, 8, 20),
        "highlight": (35, 18, 40),
        "button": (25, 12, 30)
    },
    "grayscale": {
        "alive": (255, 255, 255),
        "dead": (20, 20, 20),
        "grid": (40, 40, 40),
        "text": (200, 200, 200),
        "panel": (10, 10, 10),
        "highlight": (50, 50, 50),
        "button": (30, 30, 30)
    },
    "forest": {
        "alive": (95, 255, 95),
        "dead": (5, 15, 5),
        "grid": (15, 35, 15),
        "text": (220, 255, 220),
        "panel": (8, 20, 8),
        "highlight": (18, 40, 18),
        "button": (12, 30, 12)
    }
}

# Patterns
PATTERNS = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "block": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "beacon": [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)],
    "toad": [(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)],
    "pulsar": [(2,0), (3,0), (4,0), (8,0), (9,0), (10,0),
              (0,2), (5,2), (7,2), (12,2),
              (0,3), (5,3), (7,3), (12,3),
              (0,4), (5,4), (7,4), (12,4),
              (2,5), (3,5), (4,5), (8,5), (9,5), (10,5),
              (2,7), (3,7), (4,7), (8,7), (9,7), (10,7),
              (0,8), (5,8), (7,8), (12,8),
              (0,9), (5,9), (7,9), (12,9),
              (0,10), (5,10), (7,10), (12,10),
              (2,12), (3,12), (4,12), (8,12), (9,12), (10,12)]
}

class GameOfLife:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.running = False
        self.speed = SPEED
        self.current_theme = "classic"
        self.show_grid = True
        self.cell_size = CELL_SIZE
        self.zoom_speed = 1  # New: Control zoom sensitivity
        self.min_zoom_speed = 1
        self.max_zoom_speed = 3
        
        # Mouse position tracking for centered zooming
        self.last_mouse_pos = (0, 0)
        
        # Calculate initial grid dimensions
        self.game_panel_width = WIDTH - CONTROL_PANEL_WIDTH
        self.grid_width = self.game_panel_width // self.cell_size
        self.grid_height = HEIGHT // self.cell_size
        
        # Initialize empty grid
        self.reset_grid()
        
        # Better fonts
        try:
            self.title_font = pygame.font.SysFont('segoe ui', 28, bold=True)
            self.font = pygame.font.SysFont('segoe ui', 20)
            self.small_font = pygame.font.SysFont('segoe ui', 16)
        except:
            self.title_font = pygame.font.Font(None, 32)
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 20)
        
        # Modern symbols
        self.symbols = {
            'play': '>',  # Changed to simple ASCII character
            'pause': '||',  # Changed to simple ASCII characters
            'up': '▲',
            'down': '▼',
            'current': '●',
            'zoom_in': '🔍+',
            'zoom_out': '🔍-',
            'speed': '⚡'
        }
        
        # Store theme button positions for click detection
        self.theme_buttons = []

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):  # Mouse wheel up (4) or down (5)
                    # Store mouse position for centered zooming
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x < self.game_panel_width:  # Only zoom when mouse is over game panel
                        self.last_mouse_pos = (mouse_x, mouse_y)
                        zoom_amount = self.zoom_speed
                        if event.button == 4:  # Wheel up - zoom in
                            self.change_cell_size(self.cell_size + zoom_amount)
                        else:  # Wheel down - zoom out
                            self.change_cell_size(self.cell_size - zoom_amount)
                else:
                    x, y = pygame.mouse.get_pos()
                    if x < self.game_panel_width:  # Game panel clicks
                        grid_x, grid_y = x // self.cell_size, y // self.cell_size
                        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
                            self.grid[grid_y][grid_x] = 1 - self.grid[grid_y][grid_x]
                    else:  # Control panel clicks
                        self.handle_control_panel_click(x - self.game_panel_width, y)
            elif event.type == pygame.VIDEORESIZE:
                self.resize_grid(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                elif event.key == pygame.K_r:
                    self.reset_grid()
                elif event.key == pygame.K_d:
                    self.randomize_grid()
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_t:
                    themes = list(THEMES.keys())
                    current_idx = themes.index(self.current_theme)
                    self.current_theme = themes[(current_idx + 1) % len(themes)]
                elif event.key == pygame.K_UP:
                    self.speed = min(60, self.speed + 1)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(1, self.speed - 1)
                elif event.key == pygame.K_s:
                    self.save_grid()
                elif event.key == pygame.K_l:
                    self.load_grid()
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.zoom_speed = min(self.max_zoom_speed, self.zoom_speed + 1)
                elif event.key == pygame.K_MINUS:
                    self.zoom_speed = max(self.min_zoom_speed, self.zoom_speed - 1)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    patterns = list(PATTERNS.keys())
                    idx = event.key - pygame.K_1
                    if idx < len(patterns):
                        self.load_pattern(patterns[idx])

    def handle_control_panel_click(self, rel_x, rel_y):
        # Check if click is within any theme button
        for theme_name, (button_x, button_y, button_width, button_height) in self.theme_buttons:
            # Convert relative x,y to actual coordinates
            if (0 <= rel_x <= button_width and 
                button_y <= rel_y <= button_y + button_height):
                self.current_theme = theme_name
                break

    def resize_grid(self, width, height):
        # Store current grid state
        old_grid = [row[:] for row in self.grid]
        old_width = self.grid_width
        old_height = self.grid_height
        
        # Ensure minimum window size
        width = max(width, CONTROL_PANEL_WIDTH + 200)
        height = max(height, 300)
        
        # Update window dimensions
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
        # Calculate new game panel width and height
        self.game_panel_width = width - CONTROL_PANEL_WIDTH
        
        # Calculate new grid dimensions
        self.grid_width = self.game_panel_width // self.cell_size
        self.grid_height = height // self.cell_size
        
        # Create new empty grid
        self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]
        
        # Calculate centering offsets
        x_offset = max(0, (self.grid_width - old_width) // 2)
        y_offset = max(0, (self.grid_height - old_height) // 2)
        
        # Copy old pattern to center of new grid
        for y in range(min(old_height, self.grid_height)):
            for x in range(min(old_width, self.grid_width)):
                try:
                    new_x = x + x_offset
                    new_y = y + y_offset
                    if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                        self.grid[new_y][new_x] = old_grid[y][x]
                except IndexError:
                    continue

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
            # Calculate center position
            center_x = self.grid_width // 2
            center_y = self.grid_height // 2
            
            # Find pattern dimensions
            pattern = PATTERNS[pattern_name]
            min_x = min(x for x, _ in pattern)
            max_x = max(x for x, _ in pattern)
            min_y = min(y for _, y in pattern)
            max_y = max(y for _, y in pattern)
            pattern_width = max_x - min_x + 1
            pattern_height = max_y - min_y + 1
            
            # Calculate offset to center pattern
            offset_x = center_x - pattern_width // 2
            offset_y = center_y - pattern_height // 2
            
            self.reset_grid()
            for dx, dy in pattern:
                new_x = dx - min_x + offset_x
                new_y = dy - min_y + offset_y
                if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                    self.grid[new_y][new_x] = 1

    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        for y in range(self.grid_height):
            for x in range(self.grid_width):
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
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                count += self.grid[ny][nx]
        return count

    def draw_grid(self):
        theme = THEMES[self.current_theme]
        # Draw game panel background
        pygame.draw.rect(self.screen, theme["dead"], (0, 0, self.game_panel_width, self.screen.get_height()))
        
        # Draw cells - Fixed to use actual grid dimensions instead of visible area
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] == 1:
                    rect = (x * self.cell_size, y * self.cell_size, 
                           self.cell_size - 1, self.cell_size - 1)
                    # Only draw if cell is in visible area
                    if (0 <= rect[0] <= self.game_panel_width and 
                        0 <= rect[1] <= self.screen.get_height()):
                        pygame.draw.rect(self.screen, theme["alive"], rect)
                        if self.cell_size > 4:  # Only add glow effect for larger cells
                            pygame.draw.rect(self.screen, theme["alive"], rect, 1)

        # Draw grid lines
        if self.show_grid and self.cell_size > 3:
            for x in range(0, self.game_panel_width + self.cell_size, self.cell_size):
                pygame.draw.line(self.screen, theme["grid"], 
                               (x, 0), (x, self.screen.get_height()))
            for y in range(0, self.screen.get_height() + self.cell_size, self.cell_size):
                pygame.draw.line(self.screen, theme["grid"], 
                               (0, y), (self.game_panel_width, y))

        # Draw control panel
        self.draw_control_panel()

    def draw_control_panel(self):
        theme = THEMES[self.current_theme]
        # Draw control panel background
        panel_rect = pygame.Rect(self.game_panel_width, 0, CONTROL_PANEL_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, theme["panel"], panel_rect)
        
        # Draw separator line
        pygame.draw.line(self.screen, theme["grid"],
                        (self.game_panel_width, 0),
                        (self.game_panel_width, self.screen.get_height()), 2)

        padding = 10
        window_height = self.screen.get_height()
        
        # Calculate available space and spacing
        content_height = window_height - 2 * padding
        section_spacing = min(40, max(25, content_height * 0.04))  # Reduced section spacing
        item_spacing = min(22, max(18, content_height * 0.025))  # Reduced item spacing
        
        y_offset = padding * 1.5  # Reduced top padding
        
        # Title with adjusted space
        title = self.title_font.render("Game of Life", True, theme["text"])
        x_pos = self.game_panel_width + (CONTROL_PANEL_WIDTH - title.get_width()) // 2
        self.screen.blit(title, (x_pos, y_offset))
        y_offset += section_spacing  # Reduced space after title

        # Game Status with adjusted space
        status_text = f"{self.symbols['play'] if not self.running else self.symbols['pause']}  "
        status_text += "RUNNING" if self.running else "PAUSED"
        status = self.font.render(status_text, True, theme["text"])
        self.screen.blit(status, (self.game_panel_width + padding + 5, y_offset))
        y_offset += section_spacing * 0.8  # Reduced space after status

        # Controls Sections
        sections = [
            ("Game Controls", [
                ("SPACE", "Play/Pause"),
                ("R", "Reset"),
                ("D", "Random"),
                ("S", "Save"),
                ("L", "Load")
            ]),
            ("View Options", [
                (f"Zoom ({self.cell_size})", "Mouse Wheel"),
                (f"Speed ({self.speed})", "↑/↓ Keys"),
                ("Grid", "G Toggle"),
                ("Theme", "T Cycle")
            ]),
            ("Patterns", [
                ("1", "Glider"),
                ("2", "Blinker"),
                ("3", "Block"),
                ("4", "Beacon"),
                ("5", "Toad"),
                ("6", "Pulsar")
            ])
        ]

        # Calculate total content height
        total_sections_height = 0
        for section_name, items in sections:
            total_sections_height += item_spacing  # Section header
            total_sections_height += len(items) * item_spacing  # Items
            total_sections_height += section_spacing  # Spacing after section

        # Add themes section height
        themes_height = item_spacing + (len(THEMES) * (item_spacing + 2))
        total_content_height = total_sections_height + themes_height

        # Adjust spacing if content is too tall
        if total_content_height > content_height * 0.7:
            item_spacing = max(15, (content_height * 0.7 - section_spacing * len(sections)) / 
                             (sum(len(items) for _, items in sections) + len(THEMES)))

        for section_name, items in sections:
            # Section header without background
            header = self.font.render(section_name, True, theme["alive"])
            self.screen.blit(header, (self.game_panel_width + padding + 5, y_offset))
            y_offset += item_spacing

            # Section items with adjusted spacing
            for key, action in items:
                text = self.small_font.render(f"{key}: {action}", True, theme["text"])
                self.screen.blit(text, (self.game_panel_width + padding + 12, y_offset))  # Slightly reduced indentation
                y_offset += item_spacing  # Reduced spacing between items
            y_offset += section_spacing * 0.6  # Reduced space between sections

        # Theme Selection
        theme_header = self.font.render("Themes", True, theme["alive"])
        self.screen.blit(theme_header, (self.game_panel_width + padding + 5, y_offset))
        y_offset += item_spacing

        # Reset theme buttons list
        self.theme_buttons = []
        button_height = max(20, min(25, item_spacing))
        button_width = CONTROL_PANEL_WIDTH - (padding * 2)

        for theme_name in THEMES.keys():
            # Store button position
            self.theme_buttons.append((
                theme_name,
                (padding, y_offset, button_width, button_height)
            ))

            # Draw button (no background or border)
            button_rect = pygame.Rect(self.game_panel_width + padding, y_offset,
                                    button_width, button_height)
            
            # Theme name (removed border drawing)
            text = f"{'● ' if theme_name == self.current_theme else '  '}{theme_name.title()}"
            surface = self.small_font.render(text, True, theme["text"])
            self.screen.blit(surface, (self.game_panel_width + padding + 5, y_offset + 2))
            
            y_offset += button_height + 2

        # Stats and credit with adjusted spacing
        bottom_section_height = 60  # Reduced height
        stats_y = window_height - bottom_section_height
        
        # Stats without background
        cells = sum(sum(row) for row in self.grid)
        stats = self.font.render(f"Active Cells: {cells}", True, theme["alive"])  # Changed to theme["alive"] for better visibility
        stats_x = self.game_panel_width + padding + 5
        self.screen.blit(stats, (stats_x, stats_y))

        # Credit with adjusted space
        credit = self.small_font.render("Made by hyu", True, theme["text"])
        credit_x = self.game_panel_width + (CONTROL_PANEL_WIDTH - credit.get_width()) // 2
        self.screen.blit(credit, (credit_x, window_height - padding - 20))  # Reduced space from bottom

    def reset_grid(self):
        # Initialize completely empty grid
        self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]

    def randomize_grid(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def change_cell_size(self, new_size):
        # Constrain cell size
        new_size = max(MIN_CELL_SIZE, min(MAX_CELL_SIZE, new_size))
        if new_size != self.cell_size:
            # Store current grid and dimensions
            old_grid = [row[:] for row in self.grid]
            old_width = self.grid_width
            old_height = self.grid_height
            old_cell_size = self.cell_size
            
            # Get mouse position for zoom center
            mouse_x, mouse_y = self.last_mouse_pos
            
            # Calculate relative position of mouse in grid
            rel_x = mouse_x / (old_width * old_cell_size)
            rel_y = mouse_y / (old_height * old_cell_size)
            
            # Update cell size and recalculate grid dimensions
            self.cell_size = new_size
            self.grid_width = self.game_panel_width // self.cell_size
            self.grid_height = self.screen.get_height() // self.cell_size
            
            # Create new grid
            self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]
            
            # Calculate scaling factors
            scale_x = self.grid_width / old_width
            scale_y = self.grid_height / old_height
            
            # Calculate offsets to maintain zoom center
            offset_x = int((rel_x * self.grid_width) - (rel_x * old_width))
            offset_y = int((rel_y * self.grid_height) - (rel_y * old_height))
            
            # Copy all cells with proper scaling and centering
            for old_y in range(old_height):
                for old_x in range(old_width):
                    if old_grid[old_y][old_x] == 1:
                        # Calculate new position with scaling and offset
                        new_x = int(old_x * scale_x) - offset_x
                        new_y = int(old_y * scale_y) - offset_y
                        
                        # Ensure new position is within bounds
                        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                            self.grid[new_y][new_x] = 1
                            
                            # For smoother scaling, fill adjacent cells when zooming in
                            if scale_x > 1 and scale_y > 1:
                                for dy in range(2):
                                    for dx in range(2):
                                        nx, ny = new_x + dx, new_y + dy
                                        if (nx < self.grid_width and 
                                            ny < self.grid_height):
                                            self.grid[ny][nx] = 1

if __name__ == '__main__':
    game = GameOfLife()
    game.run()
