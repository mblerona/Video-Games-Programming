import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600  # Extra space for palette
GRID_SIZE = 5
SQUARE_SIZE = SCREEN_WIDTH // GRID_SIZE
COLORS = {
    0: (0, 255, 0),    # Green
    1: (255, 105, 180),  # Pink
    2: (138, 43, 226),  # Violet
    3: (255, 255, 0)   # Yellow
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Board
board = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Window Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle Game by 221541")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Game Variables
last_game_times = []  # Track last game times for each level
best_time = None  # Best completion time record

# Check Adjacent Colors
def is_valid_color(x, y, color):
    neighbors = [
        (x - 1, y), (x + 1, y),
        (x, y - 1), (x, y + 1)
    ]
    for nx, ny in neighbors:
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] == color:
            return False
    return True

# Check if All Colors Used
def all_colors_used():
    used_colors = set()
    for row in board:
        for cell in row:
            if cell != -1:
                used_colors.add(cell)
    return len(used_colors) == 4

# Render Board
def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE if board[row][col] == -1 else COLORS[board[row][col]]
            pygame.draw.rect(
                screen, color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pygame.draw.rect(
                screen, BLACK,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2
            )

# Draw Color Selection Palette
def draw_color_palette(selected_color):
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    palette_label = font.render("Color Palette:", True, BLACK)
    screen.blit(palette_label, (10, SCREEN_HEIGHT - 90))
    for i, color in COLORS.items():
        x = i * 100 + 50
        y = SCREEN_HEIGHT - 60
        pygame.draw.rect(screen, color, (x, y, 50, 50))
        if i == selected_color:
            pygame.draw.rect(screen, BLACK, (x, y, 50, 50), 3)  # Highlight selected color

# Get Color Button Click
def get_color_from_click(pos):
    for i in range(4):
        x = i * 100 + 50
        y = SCREEN_HEIGHT - 60
        if x <= pos[0] <= x + 50 and y <= pos[1] <= y + 50:
            return i
    return None

# Fill Random Squares with Validity Check
def fill_random_squares_with_validity(percent_filled):
    total_squares = GRID_SIZE * GRID_SIZE
    num_filled = int(total_squares * percent_filled)

    for _ in range(num_filled):
        attempts = 0
        while attempts < 100:  # Avoid infinite loops
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if board[y][x] == -1:
                colors = [c for c in range(4) if is_valid_color(x, y, c)]
                if colors:
                    board[y][x] = random.choice(colors)
                    break
            attempts += 1

# Check if Board is Filled
def is_board_filled():
    return all(all(cell != -1 for cell in row) for row in board)

# Check if No Valid Moves are Left
def no_valid_moves_left():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == -1:  # If empty, check valid moves
                valid_colors = [c for c in range(4) if is_valid_color(col, row, c)]
                if valid_colors:
                    return False
    return True

# Display Text
def display_text(text, size, y_offset=0, background=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    if background:
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, (200, 200, 200), bg_rect)
    screen.blit(text_surface, text_rect)

# Show Game Over or Win Screen
def end_screen(message, play_time, is_win=False, level_times=[]):
    global last_game_times, best_time
    last_game_times = level_times  # Store the times for each level

    if is_win and (best_time is None or play_time < best_time):
        best_time = play_time  # Update best time if it's the fastest

    while True:
        screen.fill(WHITE)
        display_text(message, 72, background=True)
        display_text("1: Restart", 36, 50)
        if is_win:
            display_text("2: View Winning Record", 36, 100)
        else:
            display_text("2: View Last Time", 36, 100)
        display_text("3: View Rules", 36, 150)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Restart
                    return "restart"
                elif event.key == pygame.K_2:  # View Time
                    return "view_time"
                elif event.key == pygame.K_3:  # View Rules
                    return "view_rules"

# Show Time Record Screen
def time_record_screen(level_times):
    while True:
        screen.fill(WHITE)
        if level_times:
            y_offset = -50
            for idx, time_record in enumerate(level_times):
                level_text = f"Level {idx + 1}: finished in {time_record[1]}s out of {time_record[0]}s" if time_record[1] <= time_record[0] else f"Level {idx + 1}: lost game"
                display_text(level_text, 36, y_offset)
                y_offset += 50
        else:
            display_text("No Record Available", 36)
        display_text("Press R to Restart", 36, 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

# Show Rules Screen
def rules_screen():
    rules = [
        "Welcome to Color Fill Puzzle!",
        "Rules:",
        "1. Fill the board with colors.",
        "2. You must use all 4 colors to win.",
        "3. Colors cannot be adjacent.",
        "Press P to Play"
    ]
    while True:
        screen.fill(WHITE)
        y_offset = -100
        for rule in rules:
            display_text(rule, 36, y_offset)
            y_offset += 50
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

                #------------------------------------------
def no_valid_moves_left():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == -1:  # If empty, check valid moves
                valid_colors = [c for c in range(4) if is_valid_color(col, row, c)]
                if valid_colors:
                    return False
                else:
                    # If no valid moves, check if the cell is surrounded by all 4 colors
                    neighbors = [
                        (col - 1, row), (col + 1, row),
                        (col, row - 1), (col, row + 1)
                    ]
                    adjacent_colors = set()
                    for nx, ny in neighbors:
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] != -1:
                            adjacent_colors.add(board[ny][nx])
                    if len(adjacent_colors) == 4:
                        return True  # No valid moves left because surrounded by all colors
    return False  # No empty cell surrounded by all colors


# ------------------------------------------
# Main Game
#-------------
def show_next_level_screen():
    screen.fill(WHITE)
    display_text("Next Level", 72, background=True)  # Display the message with a background
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds (2000 milliseconds)
#-------------

def main():
    global board

    running = True
    level = 1
    time_limits = [40, 30, 15]  # Timer durations for each level
    percent_filled = [0.8, 0.5, 0.0]  # Pre-filled board percentages for each level
    selected_color = 0
    level_times = []  # To track time taken for each level

    rules_screen()  # Show rules screen before starting the game

    while running:
        # Reset board for the current level
        board = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        fill_random_squares_with_validity(percent_filled[level - 1])
        start_ticks = pygame.time.get_ticks()  # Track start time

        while running:
            screen.fill(WHITE)
            draw_board()
            draw_color_palette(selected_color)
            remaining_time = time_limits[level - 1] - (pygame.time.get_ticks() - start_ticks) / 1000
            timer_text = font.render(f"Time: {max(0, int(remaining_time))}", True, BLACK)
            screen.blit(timer_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[1] >= SCREEN_HEIGHT - 100:  # Click in palette area
                        selected_color = get_color_from_click(pos)
                    else:
                        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                        if board[row][col] == -1 and is_valid_color(col, row, selected_color):
                            board[row][col] = selected_color

            # Check if no valid moves are left (including surrounded white boxes)
            if no_valid_moves_left():
                level_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Time taken for the current level
                level_times.append((time_limits[level - 1], level_time))  # Store level time
                result = end_screen("No moves left", level_time, False, level_times)  # Display "No moves left" message
                if result == "restart":
                    level = 1
                    level_times.clear()
                    break
                elif result == "view_time":
                    time_record_screen(level_times)
                elif result == "view_rules":
                    rules_screen()
                    level = 1
                    level_times.clear()
                    break

            # Check if the level is completed
            if is_board_filled() and all_colors_used():
                level_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Time taken for the current level
                level_times.append((time_limits[level - 1], level_time))  # Store level time
                if level < len(time_limits):
                    show_next_level_screen()  # Show the "Next Level" screen before moving to the next level
                    level += 1  # Move to next level
                    break  # Exit the inner loop to start the next level
                else:
                    result = end_screen("You Win!", level_time, True, level_times)  # Display win screen
                    if result == "restart":
                        level = 1
                        level_times.clear()
                        break
                    elif result == "view_time":
                        time_record_screen(level_times)
                    elif result == "view_rules":
                        rules_screen()
                        level = 1
                        level_times.clear()
                        break

            elif remaining_time <= 0:
                level_times.append((time_limits[level - 1], remaining_time))  # Store level time even if lost
                result = end_screen("Game Over", remaining_time, False, level_times)  # Display lose screen
                if result == "restart":
                    level = 1
                    level_times.clear()
                    break
                elif result == "view_time":
                    time_record_screen(level_times)
                elif result == "view_rules":
                    rules_screen()
                    level = 1
                    level_times.clear()
                    break

            pygame.display.flip()

if __name__ == "__main__":
    main()
