import sys
import pygame

pygame.init()

# Set screen dimensions, grid size and colors
WIN_CONDITION = 5
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
GRID_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BROWN = (150, 75, 0)

# Create the screen and set the title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gonoku")

# Set the font
font = pygame.font.SysFont("Malgun Gothic", 26)

# Generate the grid

global grid


def generate_grid():
    global grid
    grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]


generate_grid()


def draw_grid():
    cell_size = SCREEN_WIDTH // GRID_SIZE
    for x in range(0, SCREEN_WIDTH, cell_size):
        for y in range(0, SCREEN_HEIGHT, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)


def draw_status(message):
    # Set the background rectangle properties
    bg_height = 50
    bg_y = SCREEN_HEIGHT - bg_height
    bg_padding = 10
    bg_color = (128, 128, 128, 180)  # RGBA color with lower opacity

    # Render the text and get its size
    text = font.render(message, True, BLACK)
    text_width, text_height = text.get_size()

    # Calculate the position to center the text
    text_x = (SCREEN_WIDTH - text_width) // 2
    text_y = bg_y + (bg_height - text_height) // 2

    # Draw the background rectangle with reduced opacity
    rect = pygame.Rect(bg_padding, bg_y + bg_padding, SCREEN_WIDTH - bg_padding * 2, bg_height - bg_padding * 2)
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    surface.fill(bg_color)
    screen.blit(surface, (bg_padding, bg_y + bg_padding))

    # Render the centered text
    screen.blit(text, (text_x, text_y))


def main():
    global running, current_player, game_over, status_message
    running = True
    current_player = "X"
    game_over = False
    # status_message = "Player X's turn"
    status_message = "플레이어 X 차례"

    while running:
        screen.fill(BROWN)
        draw_grid()
        draw_mark()
        draw_status(status_message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cell_x, cell_y = mouse_x // (SCREEN_WIDTH // GRID_SIZE), mouse_y // (SCREEN_HEIGHT // GRID_SIZE)

                if grid[cell_y][cell_x] == 0:
                    grid[cell_y][cell_x] = current_player

                    if check_win(cell_x, cell_y, current_player):
                        # status_message = f"Player {current_player} wins! Click to restart"  in korean
                        status_message = f"플레이어 {current_player} 승리! 클릭하여 재시작"
                        game_over = True
                    else:
                        current_player = "O" if current_player == "X" else "X"
                        # status_message = f"Player {current_player}'s turn"
                        status_message = f"플레이어 {current_player} 차례"
            elif not game_over and event.type == pygame.KEYUP and event.key == pygame.K_r:
                restart(current_player)
            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                restart(current_player)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


def restart(current_player):
    generate_grid()
    global game_over, status_message
    game_over = False
    # status_message = f"Player {current_player}'s turn"
    status_message = f"플레이어 {current_player} 차례"


def draw_mark():
    cell_size = SCREEN_WIDTH // GRID_SIZE
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in ["X", "O"]:
                text = font.render(cell, True, BLACK)
                text_width, text_height = text.get_size()
                screen.blit(text, (x * cell_size + (cell_size - text_width) // 2,
                                   y * cell_size + (cell_size - text_height) // 2))


def check_win(x, y, player):
    grid_size = len(grid)
    win_condition = 5

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        streak = 0
        for i in range(-win_condition + 1, win_condition):
            px, py = x + i * dx, y + i * dy
            if 0 <= px < grid_size and 0 <= py < grid_size:
                if grid[py][px] == player:
                    streak += 1
                    if streak >= win_condition:
                        return True
                else:
                    streak = 0
            else:
                streak = 0

    return False


if __name__ == "__main__":
    main()
