import pygame
import sys
from rushHourPuzzle import RushHourPuzzle
from search import Search

# Constants for the GUI
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
CELL_SIZE = 100

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
Goldenrod = (218, 165, 32)
Lavender = (230, 230, 250)
BORDER_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rush Hour Puzzle Solver")
font = pygame.font.Font(None, 36)

# Function for heuristic selection menu
def heuristic_selection_menu():
    selected_heuristic = 1  # Default heuristic selection
    menu_font = pygame.font.Font(None, 36)
    menu_text = ["Select Heuristic:", "1. Heuristic 1", "2. Heuristic 2", "3. Heuristic 3", "Press 1, 2, or 3 to select"]
    text_objects = [menu_font.render(text, True, BLACK) for text in menu_text]
    text_positions = [(SCREEN_WIDTH // 2 - text.get_width() // 2, 100 + i * 40) for i, text in enumerate(text_objects)]

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode == '1':
                    return 1
                elif event.unicode == '2':
                    return 2
                elif event.unicode == '3':
                    return 3

        for i, text_surface in enumerate(text_objects):
            screen.blit(text_surface, text_positions[i])

        pygame.display.flip()

# Load the initial puzzle state
initial_state = RushHourPuzzle('1.csv')

# Call the heuristic_selection_menu to get the selected heuristic
selected_heuristic = heuristic_selection_menu()

# Use the selected heuristic in the A* search
solution, steps = Search.AStar(initial_state, selected_heuristic)

# Store the solution steps
solution_states = solution.getPath()
current_step = 0

# Define a color mapping for vehicle IDs
vehicle_colors = {
    'A': Lavender,
    'B': Lavender,
    'X': RED,
    'C': Lavender,
    'D': Goldenrod,
    'E': Lavender,
    'F': Goldenrod,
    'G': Goldenrod,
    'H': Lavender,
    'I': Lavender,
    'J': Goldenrod,
    'K': Goldenrod,
    'L': Lavender,
}

# Main loop for the GUI
running = True
clock = pygame.time.Clock()
success = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not success:
        screen.fill(WHITE)

        for y in range(initial_state.board_height):
            for x in range(initial_state.board_width):
                cell = initial_state.board[y][x]
                color = BLACK if cell == '#' else WHITE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for vehicle in solution_states[current_step].vehicles:
            x = vehicle["x"]
            y = vehicle["y"]
            length = vehicle["length"]
            color = vehicle_colors[vehicle["id"]]
            if vehicle["orientation"] == 'H':
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, length * CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BORDER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, length * CELL_SIZE, CELL_SIZE), 2)
                # Display the vehicle letter inside the rectangle
                text = font.render(vehicle["id"], True, BLACK)
                text_rect = text.get_rect(center=(x * CELL_SIZE + length * CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
            else:
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, length * CELL_SIZE))
                pygame.draw.rect(screen, BORDER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, length * CELL_SIZE), 2)
                # Display the vehicle letter inside the rectangle
                text = font.render(vehicle["id"], True, BLACK)
                text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + length * CELL_SIZE // 2))
            screen.blit(text, text_rect)

        text = font.render(f"Step: {current_step}/{len(solution_states) - 1}", True, BLACK)
        screen.blit(text, (10, SCREEN_HEIGHT - 90))

        text = font.render(f"Steps taken: {steps}", True, BLACK)
        screen.blit(text, (10, SCREEN_HEIGHT - 50))

        if solution_states[current_step].isGoal():
            success = True
            text = font.render("Success", True, RED)
            screen.blit(text, (10, SCREEN_HEIGHT - 130))

        pygame.display.flip()

        current_step += 1
        if current_step >= len(solution_states):
            current_step = 0

        clock.tick(3)

# Close Pygame
pygame.quit()
sys.exit()