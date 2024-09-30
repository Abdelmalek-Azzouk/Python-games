import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Define snake_color, ensuring it's valid
snake_color = (0, 255, 0)  # Example: green


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake.io")

clock = pygame.time.Clock()
FPS = 15

menu_options = {
    0: {"text": "Start", "highlighted": True},
    1: {"text": "Options", "highlighted": False},
    2: {"text": "Quit", "highlighted": False},
}

SNAKE_SIZE = 25
FOOD_SIZE = SNAKE_SIZE

# Initial snake color
snake_color = (0, 255, 0)  # Default snake color


def show_options():
    global snake_color  # Declare snake_color as global to modify it
    color_square_size = 256  # Size of the color picker square
    color_square_pos = (SCREEN_WIDTH // 2 - color_square_size // 2, 150)  # Center the color square

    font = pygame.font.Font(None, 50)
    selected_color_text = font.render("Selected Color", True, WHITE)

    while True:
        screen.fill(BLACK)

        # Draw the color square
        for x in range(color_square_size):
            for y in range(color_square_size):
                # Create a gradient of RGB colors
                color = (x, y, 128)  # Modify this to get different gradient effects
                screen.set_at((color_square_pos[0] + x, color_square_pos[1] + y), color)

        # Draw the selected color indicator
        pygame.draw.rect(screen, snake_color, (SCREEN_WIDTH // 2 - 50, 450, 100, 50))

        # Display the "Selected Color" text
        screen.blit(selected_color_text, (SCREEN_WIDTH // 2 - selected_color_text.get_width() // 2, 500))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm color selection
                    return  # Exit the options menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (color_square_pos[0] <= mouse_pos[0] <= color_square_pos[0] + color_square_size) and \
                   (color_square_pos[1] <= mouse_pos[1] <= color_square_pos[1] + color_square_size):
                    # Get the color from the gradient square
                    relative_x = mouse_pos[0] - color_square_pos[0]
                    relative_y = mouse_pos[1] - color_square_pos[1]
                    snake_color = (relative_x, relative_y, 128)  # Update snake color


def main_menu():
    selected_option = 0
    font = pygame.font.Font(None, 50)

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)

        title_text = font.render("Snake.io", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        for index, option in menu_options.items():
            color = GREEN if option["highlighted"] else WHITE
            text_surface = font.render(option["text"], True, color)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 300 + index * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_option > 0:
                        menu_options[selected_option]["highlighted"] = False
                        selected_option -= 1
                        menu_options[selected_option]["highlighted"] = True
                elif event.key == pygame.K_DOWN:
                    if selected_option < len(menu_options) - 1:
                        menu_options[selected_option]["highlighted"] = False
                        selected_option += 1
                        menu_options[selected_option]["highlighted"] = True
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return True  # Start the game
                    elif selected_option == 1:
                        print("Options selected")
                        show_options()  # Call options menu
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()


def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, snake_color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))


def draw_food(food_pos):
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))


def main():
    snake_pos = [100, 50]
    snake_body = [[100, 50], [80, 50], [60, 50]]

    direction = "RIGHT"
    change_to = direction

    food_pos = [random.randrange(0, SCREEN_WIDTH // FOOD_SIZE) * FOOD_SIZE, 
                random.randrange(0, SCREEN_HEIGHT // FOOD_SIZE) * FOOD_SIZE]
    food_spawn = True

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"

        if change_to == "UP":
            direction = "UP"
        if change_to == "DOWN":
            direction = "DOWN"
        if change_to == "LEFT":
            direction = "LEFT"
        if change_to == "RIGHT":
            direction = "RIGHT"

        if direction == "UP":
            snake_pos[1] -= SNAKE_SIZE
        if direction == "DOWN":
            snake_pos[1] += SNAKE_SIZE
        if direction == "LEFT":
            snake_pos[0] -= SNAKE_SIZE
        if direction == "RIGHT":
            snake_pos[0] += SNAKE_SIZE

        snake_body.insert(0, list(snake_pos))

        snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], SNAKE_SIZE, SNAKE_SIZE)
        food_rect = pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE)

        if snake_rect.colliderect(food_rect):
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(0, SCREEN_WIDTH // FOOD_SIZE) * FOOD_SIZE, 
                        random.randrange(0, SCREEN_HEIGHT // FOOD_SIZE) * FOOD_SIZE]
            food_spawn = True

        screen.fill(BLACK)

        draw_snake(snake_body)
        draw_food(food_pos)

        if (snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
                snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT):
            game_over(score)

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)

        show_score(score)

        pygame.display.flip()

        clock.tick(FPS)


def game_over(score):
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render(f'Game Over! Score: {score}', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.fill(BLACK)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Change to delay in milliseconds (3000 ms = 3 seconds)
    main_menu()



def show_score(score):
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))


if __name__ == "__main__":
    while True:
        if main_menu():
            main()
