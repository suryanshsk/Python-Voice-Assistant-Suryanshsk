import pygame
import random
import time
from colorama import Fore, Style, init

init(autoreset=True)  

WINDOW_SIZE = 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)

pygame.init()

# Create a window for the game
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Generator")
font = pygame.font.SysFont(None, 40)

def print_grid(grid):
    """Print Sudoku grid with colored output using colorama."""
    print(Fore.CYAN + "Sudoku Grid:")
    for row in grid:
        print(" ".join(Fore.GREEN + str(num) if num != 0 else Fore.RED + '.' for num in row))
    print(Style.RESET_ALL)

def draw_grid(grid):
    """Draw the Sudoku grid."""
    window.fill(WHITE)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE
            if num != 0:
                text = font.render(str(num), True, BLACK)
                window.blit(text, (x + 20, y + 10))

    for i in range(GRID_SIZE + 1):
        thickness = 5 if i % 3 == 0 else 1
        pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), thickness)
        pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), thickness)

    pygame.display.update()

def is_valid(grid, row, col, num):
    """Check if placing a number is valid."""
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def solve(grid, start_time=None, time_limit=5):
    """Solve the Sudoku grid using backtracking with a time limit."""
    if start_time is None:
        start_time = time.time()

    if time.time() - start_time > time_limit:
        return False

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid, start_time, time_limit):
                            return True
                        grid[row][col] = 0
                return False
    return True

def fill_grid(grid):
    """Fill the Sudoku grid with a valid solution."""
    for _ in range(20):
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if is_valid(grid, row, col, num):
            grid[row][col] = num
    solve(grid)

def remove_numbers(grid, difficulty):
    """Remove numbers from the grid based on difficulty."""
    cells_to_remove = 0
    if difficulty == 'easy':
        cells_to_remove = 40
    elif difficulty == 'medium':
        cells_to_remove = 50
    elif difficulty == 'hard':
        cells_to_remove = 60

    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_to_remove -= 1

def generate_sudoku(difficulty='medium'):
    """Generate a Sudoku puzzle."""
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    fill_grid(grid)
    remove_numbers(grid, difficulty)
    return grid

def main():
    difficulty = input(Fore.YELLOW + "Choose difficulty (easy, medium, hard): ").lower()

    if difficulty not in ['easy', 'medium', 'hard']:
        print(Fore.RED + "Invalid difficulty! Defaulting to 'medium'.")
        difficulty = 'medium'

    sudoku_grid = generate_sudoku(difficulty)
    print_grid(sudoku_grid)
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(sudoku_grid)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
