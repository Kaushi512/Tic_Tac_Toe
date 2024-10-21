import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors (classic theme)
BG_COLOR = (0, 0, 0)  # Black background
LINE_COLOR = (128, 128, 128)  # Gray lines
CIRCLE_COLOR = (255, 0, 0)  # Red for circles (Player 1)
CROSS_COLOR = (0, 0, 255)  # Blue for crosses (Player 2)

# Initialize board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(BG_COLOR)

# Font for text
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)


# Draw lines
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


draw_lines()


# Mark square on the board
def mark_square(row, col, player):
    board[row][col] = player


# Check if square is available
def available_square(row, col):
    return board[row][col] == 0


# Check for a win
def check_win(player):
    # Check vertical, horizontal, and diagonal wins
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    return False


# Check for a draw
def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


# Draw figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (
                int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


# Display message (win, draw, restart)
def display_message(text):
    text_surface = font.render(text, True, (255, 255, 255))  # White text for result
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BG_COLOR)
    screen.blit(text_surface, text_rect)

    # Show restart instruction
    restart_text = small_font.render('Press Ctrl + R to restart', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

    pygame.display.update()


# Restart the game
def restart_game():
    global board, game_over, player
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player = 1
    screen.fill(BG_COLOR)
    draw_lines()


# Main game loop
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # X coordinate
            mouseY = event.pos[1]  # Y coordinate

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()

                if check_win(player):
                    game_over = True
                    display_message(f'Player {player} wins!')
                elif check_draw():
                    game_over = True
                    display_message('It\'s a Draw!')

                player = 2 if player == 1 else 1

        # Restart the game if Ctrl + R is pressed
        if event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL:
            if event.key == pygame.K_r and game_over:
                restart_game()

    pygame.display.update()