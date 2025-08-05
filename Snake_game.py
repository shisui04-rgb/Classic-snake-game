import pygame
import random

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)  # Define gray color

# Game settings
width, height = 600, 400
grid_size = 10  # Define grid size
snake_speed = 10

# Initialize display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Classic Snake Game')

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, width, grid_size):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (width, y))

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, green, (segment[0], segment[1], grid_size, grid_size))
        pygame.draw.rect(screen, dark_green, (segment[0], segment[1], grid_size, grid_size), 1)

def draw_food(food_pos):
    pygame.draw.rect(screen, red, (food_pos[0], food_pos[1], grid_size, grid_size))

def show_score(score):
    font = pygame.font.SysFont('Arial', 20)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, [10, 10])

def game_over_screen(score):
    screen.fill(black)
    font_large = pygame.font.SysFont('Arial', 40)
    font_small = pygame.font.SysFont('Arial', 25)

    game_over_text = font_large.render("GAME OVER!", True, red)
    score_text = font_small.render(f"Final score: {score}", True, white)
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, gray)
        
    screen.blit(game_over_text, [width//2 - 120, height//2 - 60])
    screen.blit(score_text, [width//2 - 80, height//2 - 10])
    screen.blit(restart_text, [width//2 - 150, height//2 + 40])

    pygame.display.update()

def game():
    running = True
    game_active = True

    # Initial snake position
    snake = [[width // 2, height // 2]]
    snake_direction = [0, 0]

    # Initial food position
    food = [
        random.randint(0, (width - grid_size) // grid_size) * grid_size,
        random.randint(0, (height - grid_size) // grid_size) * grid_size
    ]
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake_direction[1] == 0:
                        snake_direction = [0, -grid_size]
                    elif event.key == pygame.K_DOWN and snake_direction[1] == 0:
                        snake_direction = [0, grid_size]
                    elif event.key == pygame.K_LEFT and snake_direction[0] == 0:
                        snake_direction = [-grid_size, 0]
                    elif event.key == pygame.K_RIGHT and snake_direction[0] == 0:
                        snake_direction = [grid_size, 0]
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()  # Restart game
                        return
                    elif event.key == pygame.K_q:
                        running = False

        if game_active:
            # Move snake
            new_head = [snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1]]
            snake.insert(0, new_head)

            # Check for food collision
            if snake[0] == food:
                score += 1
                food = [
                    random.randint(0, (width - grid_size) // grid_size) * grid_size,
                    random.randint(0, (height - grid_size) // grid_size) * grid_size
                ]
                # Make sure food doesn't spawn on snake
                while food in snake:
                    food = [
                        random.randint(0, (width - grid_size) // grid_size) * grid_size,
                        random.randint(0, (height - grid_size) // grid_size) * grid_size
                    ]
            else:
                snake.pop()

            # Check for collisions
            if (snake[0][0] < 0 or snake[0][0] >= width or
                snake[0][1] < 0 or snake[0][1] >= height or
                snake[0] in snake[1:]):
                game_active = False

            # Draw everything
            screen.fill(black)
            draw_grid()  # Draw the grid
            draw_snake(snake)
            draw_food(food)
            show_score(score)
        else:
            game_over_screen(score)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game()
