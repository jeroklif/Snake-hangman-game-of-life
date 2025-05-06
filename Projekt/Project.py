import pygame
import sys
import time
import json
import math
import random
from typing import List, Optional

# Initialize Pygame
pygame.init()

# Window settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
LIGHT_BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
RED = (255, 99, 71)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 223, 0)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)


# Utility function for gradient background

def draw_animated_gradient(color1, color2, shift=0):  # Default shift to 0 if not passed
    step = 2
    for y in range(0, SCREEN_HEIGHT, step):
        ratio = (y / SCREEN_HEIGHT + shift) % 1
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


# Button icons
def load_hangman_icon():
    icon_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
    # Static parts
    pygame.draw.line(icon_surface, BLACK, (20, 70), (20, 10), 5)  # Vertical pole
    pygame.draw.line(icon_surface, BLACK, (20, 10), (60, 10), 5)  # Horizontal beam
    pygame.draw.line(icon_surface, BLACK, (60, 10), (60, 20), 5)  # Rope
    # Dynamic parts (full body)
    pygame.draw.circle(icon_surface, BLACK, (60, 30), 10, 2)  # Head
    pygame.draw.line(icon_surface, BLACK, (60, 40), (60, 60), 2)  # Body
    pygame.draw.line(icon_surface, BLACK, (60, 45), (50, 55), 2)  # Left Arm
    pygame.draw.line(icon_surface, BLACK, (60, 45), (70, 55), 2)  # Right Arm
    pygame.draw.line(icon_surface, BLACK, (60, 60), (50, 75), 2)  # Left Leg
    pygame.draw.line(icon_surface, BLACK, (60, 60), (70, 75), 2)  # Right Leg
    return icon_surface


def load_tic_tac_toe_icon():
    icon_surface = pygame.Surface((80, 80), pygame.SRCALPHA)

    # Draw grid
    for i in range(1, 3):
        pygame.draw.line(icon_surface, BLACK, (i * 26, 10), (i * 26, 70), 3)  # Vertical lines
        pygame.draw.line(icon_surface, BLACK, (10, i * 26), (70, i * 26), 3)  # Horizontal lines

    # Add X in top-left box, slightly offset to avoid overlapping the grid
    pygame.draw.line(icon_surface, RED, (14, 14), (22, 22), 3)  # X part 1
    pygame.draw.line(icon_surface, RED, (22, 14), (14, 22), 3)  # X part 2

    # Add O in bottom-right box, slightly offset to avoid overlapping the grid
    pygame.draw.circle(icon_surface, BLUE, (40, 40), 6, 3)  # O

    return icon_surface


def load_game_of_life_icon():
    icon_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
    grid_size = 5
    for row in range(grid_size):
        for col in range(grid_size):
            if (row + col) % 2 == 0:  # Simple pattern
                rect = pygame.Rect(10 + col * 12, 10 + row * 12, 10, 10)
                pygame.draw.rect(icon_surface, BLACK, rect)
    return icon_surface


icons = {
    "hangman": load_hangman_icon(),
    "tic_tac_toe": load_tic_tac_toe_icon(),
    "game_of_life": load_game_of_life_icon(),
}


particles = []


# Particle effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = color
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, -3)
        self.life = random.randint(20, 40)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# Button class with hover effects and particles
class Button:
    def __init__(self, x, y, width, height, color, text, icon=None, hover_color=None,):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color or color
        self.text = text
        self.icon = icon
        self.hovered = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.color

        # Hover effect (scaling)
        if is_hovered:
            pygame.draw.rect(surface, color, self.rect.inflate(10, 10), border_radius=10)
        else:
            pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Render text
        text_surface = font.render(self.text, True, WHITE)
        surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

        # Render icon if available
        if self.icon:
            surface.blit(self.icon, (self.rect.x - 90, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Buttons
buttons = [
    Button(300, 150, 300, 100, RED, "Hangman", icons["hangman"]),
    Button(300, 300, 300, 100, GREEN, "Tic Tac Toe", icons["tic_tac_toe"]),
    Button(300, 450, 300, 100, BLUE, "Game of Life", icons["game_of_life"]),
]


# Utility function for animated gradient
def draw_animated_gradients(color1, color2, shift):
    step = 2  # Adjust this value to control speed
    for y in range(0, SCREEN_HEIGHT, step):
        ratio = (y / SCREEN_HEIGHT + shift) % 1
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


# Save score function
def load_scores():
    try:
        with open("Assets/scores.json", "r") as file:
            scores = json.load(file)
            # Ensure the scores are in dictionary format
            if isinstance(scores, list):
                # Convert list to dictionary (legacy support)
                scores_dict = {}
                for score_entry in scores:
                    game_name = score_entry.get('game')
                    if game_name:
                        if game_name not in scores_dict:
                            scores_dict[game_name] = []
                        scores_dict[game_name].append(score_entry)
                return scores_dict
            elif isinstance(scores, dict):
                return scores
            return {}
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}
    except json.JSONDecodeError as e:
        print(f"Error reading scores.json: {e}. Creating a new file.")
        # Create a new empty file if there was an error
        with open("Assets/scores.json", "w") as file:
            json.dump({}, file)
        return {}


def save_score(game_name, time_taken, result):
    # Load current scores
    scores = load_scores()

    # If the game doesn't exist in the scores dictionary, initialize it
    if game_name not in scores:
        scores[game_name] = []

    # Append the new score entry to the game's list
    scores[game_name].append({
        "time": time_taken,
        "result": result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

    # Write the updated scores back to the file
    with open("Assets/scores.json", "w") as file:
        json.dump(scores, file, indent=4)


# Show saved scores (Display after each game)
def display_scores(game_name):
    scores = load_scores().get(game_name, [])
    if scores:
        score_text = f"{game_name} High Scores:"
        for score in scores:
            score_text += f"\n{score['timestamp']} - {score['result']} - Time: {score['time']}s"
        return score_text
    return f"No scores for {game_name}"


# Return to menu button
return_button = Button(650, 10, 140, 50, GRAY, "Menu")


# Hangman function
def run_hangman():
    # Function to load words from a file
    def load_words(filename="Assets/hangman_data.txt"):
        try:
            with open(filename, "r") as file:
                words = file.read().splitlines()
            return [word.strip().upper() for word in words if word.strip()]
        except FileNotFoundError:
            print(f"File {filename} not found!")
            return ["PYTHON", "HANGMAN", "COMPUTER"]  # Default words if the file does not exist

    # Load words from file
    word_list = load_words()

    while True:
        guessed_word = random.choice(word_list)  # Randomly select a new word from the list
        running = True
        screen.fill((0, 0, 0))
        display_word = "_ " * len(guessed_word)
        guessed_letters = []
        attempts = 6  # Number of attempts
        start_time = time.time()

        def draw_hangman(attempts_):
            static_parts = [
                ((200, 450), (200, 150)),  # Vertical pole
                ((200, 150), (300, 150)),  # Horizontal beam
                ((300, 150), (300, 175)),  # Rope
            ]
            dynamic_parts = [
                ((300, 175), (300, 225)),  # Head (circle center point)
                ((300, 225), (300, 350)),  # Body
                ((300, 275), (250, 250)),  # Left Arm
                ((300, 275), (350, 250)),  # Right Arm
                ((300, 350), (250, 450)),  # Left Leg
                ((300, 350), (350, 450)),  # Right Leg
            ]

            # Draw static parts
            for part in static_parts:
                pygame.draw.line(screen, BLACK, part[0], part[1], 5)

            # Draw dynamic parts
            for i in range(6 - attempts_):
                if i == 0:  # Draw head as a circle
                    pygame.draw.circle(screen, BLACK, (300, 200), 25, 3)
                else:
                    pygame.draw.line(screen, BLACK, dynamic_parts[i][0], dynamic_parts[i][1], 5)

        def end_message(won):
            screen.fill(LIGHT_GRAY)
            message = "You won!" if won else "You lost!"
            title_ = font.render(message, True, GREEN if won else RED)
            screen.blit(title_, title_.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

            correct_word = font.render(f"The word was: {guessed_word}", True, BLACK)
            screen.blit(correct_word, correct_word.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

            pygame.display.flip()
            time.sleep(3)

            # Save the score
            end_time_ = time.time()
            result = "Win" if won else "Loss"
            save_score("Hangman", end_time_ - start_time, result)

        while running:
            screen.fill(LIGHT_BLUE)

            title = font.render("Hangman", True, BLACK)
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

            return_button.draw(screen)

            # Draw the word to guess on the right side
            word_surface = font.render(display_word, True, BLACK)
            screen.blit(word_surface, word_surface.get_rect(center=(600, 200)))

            # Display attempts left
            attempts_surface = small_font.render(f"Attempts left: {attempts}", True, RED)
            screen.blit(attempts_surface, (50, 50))

            # Draw the hangman on the left
            draw_hangman(attempts)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.upper() in guessed_word and event.unicode.upper() not in guessed_letters:
                        guessed_letters.append(event.unicode.upper())
                        display_word = " ".join([
                            letter if letter in guessed_letters else "_" for letter in guessed_word
                        ])
                    elif event.unicode.upper() not in guessed_letters and event.unicode.isalpha():
                        guessed_letters.append(event.unicode.upper())
                        attempts -= 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and return_button.is_clicked(event.pos):
                        return

            if "_" not in display_word:
                end_message(True)
                break
            elif attempts <= 0:
                end_message(False)
                break

            pygame.display.flip()


# Tic Tac Toe function
def run_tic_tac_toe():
    board: List[List[Optional[str]]] = [[None for _ in range(3)] for _ in range(3)]

    assert isinstance(board, list) and all(isinstance(row, list) for row in board)
    player = "X"
    running = True
    start_time = time.time()

    def check_winner():
        for row in board:
            if row[0] == row[1] == row[2] and row[0]:
                return row[0]
        for col_ in range(3):
            if board[0][col_] == board[1][col_] == board[2][col_] and board[0][col_]:
                return board[0][col_]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
            return board[0][2]
        return None

    def display_winner(winner_):
        screen.fill(LIGHT_GRAY)
        title_ = font.render(f"{winner_} Wins!" if winner_ else "Draw!", True, BLACK)
        screen.blit(title_, title_.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()
        time.sleep(2)

        # Save the score
        end_time_ = time.time()
        result = f"{winner_} Wins" if winner_ else "Draw"
        save_score("Tic Tac Toe", end_time_ - start_time, result)

    while running:
        screen.fill((0, 0, 0))
        screen.fill(LIGHT_BLUE)

        title = font.render("Tic Tac Toe", True, BLACK)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        return_button.draw(screen)

        for row in range(3):
            for col in range(3):
                rect = pygame.Rect(200 + col * 100, 200 + row * 100, 100, 100)
                pygame.draw.rect(screen, BLACK, rect, width=3)
                if board[row][col]:
                    mark = font.render(board[row][col], True, RED if board[row][col] == "X" else BLUE)
                    screen.blit(mark, mark.get_rect(center=rect.center))

        winner = check_winner()
        if winner or all(cell is not None for row in board for cell in row):
            display_winner(winner)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_button.is_clicked(event.pos):
                        return
                    x, y = event.pos
                    col = (x - 200) // 100
                    row = (y - 200) // 100

                    # Validation and attribution
                    if isinstance(row, int) and isinstance(col, int) and 0 <= row < 3 and 0 <= col < 3:
                        if board[row][col] is None:
                            board[row][col] = player
                            player = "O" if player == "X" else "X"
                        else:
                            pass

        pygame.display.flip()


# Game of Life function
def run_game_of_life():
    grid_size = 20
    cell_size = 20
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    running = True
    simulation_running = False
    start_time = time.time()

    # Creating a Start button
    start_button = Button(300, 500, 200, 50, GREEN, "Start", hover_color=LIGHT_BLUE)

    def draw_grid():
        for row_2 in range(grid_size):
            for col_1 in range(grid_size):
                color = BLACK if grid[row_2][col_1] else WHITE
                rect = pygame.Rect(50 + col_1 * cell_size, 50 + row_2 * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRAY, rect, width=1)

    def update_grid():
        new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        for row_1 in range(grid_size):
            for col_2 in range(grid_size):
                neighbors = sum(
                    grid[(row_1 + dr) % grid_size][(col_2 + dc) % grid_size]
                    for dr in (-1, 0, 1)
                    for dc in (-1, 0, 1)
                    if not (dr == 0 and dc == 0)
                )
                if grid[row_1][col_2] == 1 and neighbors in (2, 3):
                    new_grid[row_1][col_2] = 1
                elif grid[row_1][col_2] == 0 and neighbors == 3:
                    new_grid[row_1][col_2] = 1
        return new_grid

    while running:
        screen.fill(LIGHT_BLUE)

        # Game's Title
        title = font.render("Game of Life", True, BLACK)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 20)))

        # Buttons
        return_button.draw(screen)
        start_button.draw(screen)

        # Drawing a grid
        draw_grid()

        # If the simulation is running, update the mesh state
        if simulation_running:
            grid[:] = update_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if return_button.is_clicked(event.pos):
                        end_time = time.time()
                        save_score("Game of Life", end_time - start_time, "Simulation Ended")
                        return
                    if start_button.is_clicked(event.pos):
                        simulation_running = not simulation_running
                    x, y = event.pos
                    col = (x - 50) // cell_size
                    row = (y - 50) // cell_size
                    if 0 <= row < grid_size and 0 <= col < grid_size and not simulation_running:
                        grid[row][col] = 1 - grid[row][col]

        pygame.display.flip()
        time.sleep(0.1)


# Map games
games = {
    "Hangman": run_hangman,
    "Tic Tac Toe": run_tic_tac_toe,
    "Game of Life": run_game_of_life,
}

# Themes
THEMES = {
    "Light": {"bg": WHITE, "text": BLACK, "button": GRAY},
    "Dark": {"bg": BLACK, "text": WHITE, "button": DARK_GRAY},
}
current_theme = "Light"


# Main menu
def main_menu():
    running = True
    angle = 0
    gradient_shift = 0  # Shift variable for gradient animation
    while running:
        screen.fill((0, 0, 0))
        gradient_shift += 0.002  # Adjust speed as necessary

        draw_animated_gradients(LIGHT_BLUE, BLUE, gradient_shift)
        angle += 1
        rotated_title = pygame.transform.rotate(font.render("Game Menu", True, YELLOW),
                                                math.sin(math.radians(angle)) * 5)
        screen.blit(rotated_title, rotated_title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        games[button.text]()


main_menu()
