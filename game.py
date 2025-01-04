import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Set the dimensions of the grid
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Define the number of cells in the grid
cols, rows = 50, 50
cell_size = width // cols

# Create a 2D array to represent the grid
grid = np.zeros((cols, rows))

# Colors
BG_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
ALIVE_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Font for button text
font = pygame.font.Font(None, 36)

# Function to draw the grid
def draw_grid(surface, grid):
    for x in range(cols):
        for y in range(rows):
            color = ALIVE_COLOR if grid[x, y] == 1 else BG_COLOR
            pygame.draw.rect(surface, color, (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))
            pygame.draw.rect(surface, GRID_COLOR, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

# Function to update the grid
def update_grid(grid):
    new_grid = grid.copy()
    for x in range(cols):
        for y in range(rows):
            # Count the number of alive neighbors
            alive_neighbors = (
                grid[(x - 1) % cols, (y - 1) % rows] + grid[x % cols, (y - 1) % rows] + grid[(x + 1) % cols, (y - 1) % rows] +
                grid[(x - 1) % cols, y % rows] + grid[(x + 1) % cols, y % rows] +
                grid[(x - 1) % cols, (y + 1) % rows] + grid[x % cols, (y + 1) % rows] + grid[(x + 1) % cols, (y + 1) % rows]
            )
            
            # Apply the rules of the Game of Life
            if grid[x, y] == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[x, y] = 0
            else:
                if alive_neighbors == 3:
                    new_grid[x, y] = 1
    return new_grid

# Function to draw buttons
def draw_button(surface, text, x, y, width, height):
    pygame.draw.rect(surface, BUTTON_COLOR, (x, y, width, height))
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

# Main game loop
running = True
paused = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 50 <= mouse_x <= 150 and 10 <= mouse_y <= 50:
                paused = not paused
            else:
                grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size
                if grid_x < cols and grid_y < rows:
                    grid[grid_x, grid_y] = 1 - grid[grid_x, grid_y]

    if not paused:
        grid = update_grid(grid)

    screen.fill(BG_COLOR)
    draw_grid(screen, grid)
    draw_button(screen, "Start" if paused else "Pause", 50, 10, 100, 40)
    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
