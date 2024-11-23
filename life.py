import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Initialize grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]


def draw_grid():
    """Draw the grid lines."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_cells():
    """Draw the cells on the grid."""
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 1:
                pygame.draw.rect(
                    screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )


def get_neighbors(row, col):
    """Calculate the number of alive neighbors for a cell."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            count += grid[r][c]
    return count


def update_grid():
    """Update the grid based on Conway's rules."""
    global grid
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            alive_neighbors = get_neighbors(row, col)
            if grid[row][col] == 1:  # Alive cell
                if alive_neighbors in (2, 3):
                    new_grid[row][col] = 1
            else:  # Dead cell
                if alive_neighbors == 3:
                    new_grid[row][col] = 1
    grid = new_grid


# Main loop
running = True
placing = True  # True when user is placing cells
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    draw_grid()
    draw_cells()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and placing:
            # Get mouse position and toggle cell state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col, row = mouse_x // GRID_SIZE, mouse_y // GRID_SIZE
            grid[row][col] = 1 - grid[row][col]  # Toggle cell state
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                placing = not placing  # Toggle between placing and running the simulation

    if not placing:
        update_grid()

    pygame.display.flip()
    clock.tick(10)  # Adjust speed of the simulation

pygame.quit()
sys.exit()
