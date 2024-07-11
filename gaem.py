import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')

def init_snake():
    return [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]

def random_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake and pos not in obstacles:
            return pos

def game_over():
    pygame.mixer.music.stop()
    game_over_sound.play()
    screen.fill(BLACK)
    game_over_text = font.render("Game Over! Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    save_high_score(score)
    pygame.quit()
    sys.exit()

def welcome_screen():
    screen.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    instructions_text = font.render("Press Enter to Start", True, WHITE)
    difficulty_text = font.render("Select Difficulty: 1 (Easy) 2 (Medium) 3 (Hard)", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
    screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.flip()

def pause_game():
    paused = True
    screen.fill(BLACK)
    pause_text = font.render("Game Paused. Press 'P' to Resume", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def save_high_score(score):
    try:
        with open("high_scores.txt", "a") as file:
            file.write(str(score) + "\n")
    except Exception as e:
        print(f"Failed to save high score: {e}")

def display_high_scores():
    screen.fill(BLACK)
    high_scores_text = font.render("High Scores", True, WHITE)
    screen.blit(high_scores_text, (WIDTH // 2 - high_scores_text.get_width() // 2, HEIGHT // 6))
    try:
        with open("high_scores.txt", "r") as file:
            scores = file.readlines()
        scores = [int(score.strip()) for score in scores]
        scores.sort(reverse=True)
        for i, score in enumerate(scores[:5]):
            score_text = font.render(f"{i+1}. {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + i * 30))
    except Exception as e:
        error_text = font.render(f"Failed to load high scores: {e}", True, WHITE)
        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(3000)

snake = init_snake()
direction = (0, 0)
food = random_food()
score = 0
speed = 10
level = 1
food_timer = 0
obstacles = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(10)]
food_types = ["normal", "super", "slow", "reverse"]
current_food_type = "normal"

welcome_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False
            elif event.key == pygame.K_1:
                speed = 5
            elif event.key == pygame.K_2:
                speed = 10
            elif event.key == pygame.K_3:
                speed = 15

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_p:
                pause_game()
            elif event.key == pygame.K_h:
                display_high_scores()

    if direction != (0, 0):
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake or new_head in obstacles or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            game_over()
        snake.insert(0, new_head)
        if new_head == food:
            eat_sound.play()
            food = random_food()
            current_food_type = random.choice(food_types)
            food_timer = 5000 if current_food_type != "normal" else 0
            if current_food_type == "normal":
                score += 1
            elif current_food_type == "super":
                score += 3
                speed += 3
            elif current_food_type == "slow":
                score += 1
                speed -= 2
            elif current_food_type == "reverse":
                score += 2
                direction = (-direction[0], -direction[1])
            if score % 10 == 0:
                level += 1
                speed += 2
                obstacles.append((random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)))
        else:
            snake.pop()

    if food_timer > 0:
        food_timer -= clock.get_time()
        if food_timer <= 0:
            current_food_type = "normal"

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREY, pygame.Rect(obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    if current_food_type == "normal":
        pygame.draw.rect(screen, RED, pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    elif current_food_type == "super":
        pygame.draw.rect(screen, BLUE, pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    elif current_food_type == "slow":
        pygame.draw.rect(screen, YELLOW, pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    elif current_food_type == "reverse":
        pygame.draw.rect(screen, GREY, pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    score_text = font.render("Score: " + str(score), True, WHITE)
    level_text = font.render("Level: " + str(level), True, WHITE)
    screen.blit(score_text, (5, 5))
    screen.blit(level_text, (5, 30))
    pygame.display.flip()

    clock.tick(speed)
