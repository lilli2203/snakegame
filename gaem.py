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

def init_snake(start_pos):
    return [start_pos]

def random_food(snake_positions):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_positions and pos not in obstacles:
            return pos

def game_over(winner):
    pygame.mixer.music.stop()
    game_over_sound.play()
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! {winner} wins!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def welcome_screen():
    screen.fill(BLACK)
    title_text = font.render("Snake Game", True, WHITE)
    instructions_text = font.render("Press Enter to Start", True, WHITE)
    difficulty_text = font.render("Select Difficulty: 1 (Easy) 2 (Medium) 3 (Hard)", True, WHITE)
    mode_text = font.render("Select Mode: 1 (Single) 2 (Multiplayer)", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
    screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, HEIGHT // 2 + 80))
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
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def save_high_score(player_scores):
    try:
        with open("high_scores.txt", "a") as file:
            for player, score in player_scores.items():
                file.write(f"{player}: {score}\n")
    except Exception as e:
        print(f"Failed to save high score: {e}")

def display_high_scores():
    screen.fill(BLACK)
    high_scores_text = font.render("High Scores", True, WHITE)
    screen.blit(high_scores_text, (WIDTH // 2 - high_scores_text.get_width() // 2, HEIGHT // 6))
    try:
        with open("high_scores.txt", "r") as file:
            scores = file.readlines()
        scores = [score.strip() for score in scores]
        scores.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        for i, score in enumerate(scores[:5]):
            score_text = font.render(f"{i+1}. {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + i * 30))
    except Exception as e:
        error_text = font.render(f"Failed to load high scores: {e}", True, WHITE)
        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(3000)

def move_obstacles():
    for i in range(len(obstacles)):
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_pos = (obstacles[i][0] + direction[0], obstacles[i][1] + direction[1])
        if 0 <= new_pos[0] < GRID_WIDTH and 0 <= new_pos[1] < GRID_HEIGHT and new_pos not in obstacles:
            obstacles[i] = new_pos

def apply_power_up(player):
    global directions, speeds
    power_up_type = random.choice(["slow", "fast", "reverse"])
    if power_up_type == "slow":
        speeds[player] = max(5, speeds[player] - 5)
    elif power_up_type == "fast":
        speeds[player] += 5
    elif power_up_type == "reverse":
        directions[player] = (-directions[player][0], -directions[player][1])

def check_collision(player, new_head):
    if new_head in snakes[player] or new_head in obstacles or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
        return True
    for other_player, snake in snakes.items():
        if other_player != player and new_head in snake:
            return True
    return False

player_names = ["Player 1", "Player 2"]
snakes = {
    "Player 1": init_snake((GRID_WIDTH // 4, GRID_HEIGHT // 2)),
    "Player 2": init_snake((3 * GRID_WIDTH // 4, GRID_HEIGHT // 2))
}
directions = {
    "Player 1": (0, 0),
    "Player 2": (0, 0)
}
foods = {
    "Player 1": random_food(list(snakes["Player 1"]) + list(snakes["Player 2"])),
    "Player 2": random_food(list(snakes["Player 1"]) + list(snakes["Player 2"]))
}
scores = {
    "Player 1": 0,
    "Player 2": 0
}
speeds = {
    "Player 1": 10,
    "Player 2": 10
}
levels = {
    "Player 1": 1,
    "Player 2": 1
}
food_timers = {
    "Player 1": 0,
    "Player 2": 0
}
obstacles = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(10)]
food_types = ["normal", "super", "slow", "reverse"]
current_food_types = {
    "Player 1": "normal",
    "Player 2": "normal"
}
game_mode = "single"
game_time = 60000  

welcome_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False
            elif event.key == pygame.K_1:
                speeds["Player 1"] = 5
                speeds["Player 2"] = 5
            elif event.key == pygame.K_2:
                speeds["Player 1"] = 10
                speeds["Player 2"] = 10
            elif event.key == pygame.K_3:
                speeds["Player 1"] = 15
                speeds["Player 2"] = 15
            elif event.key == pygame.K_1:
                game_mode = "single"
            elif event.key == pygame.K_2:
                game_mode = "multiplayer"

if game_mode == "timed":
    pygame.time.set_timer(pygame.USEREVENT, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and directions["Player 1"] != (0, 1):
                directions["Player 1"] = (0, -1)
            elif event.key == pygame.K_DOWN and directions["Player 1"] != (0, -1):
                directions["Player 1"] = (0, 1)
            elif event.key == pygame.K_LEFT and directions["Player 1"] != (1, 0):
                directions["Player 1"] = (-1, 0)
            elif event.key == pygame.K_RIGHT and directions["Player 1"] != (-1, 0):
                directions["Player 1"] = (1, 0)
            elif event.key == pygame.K_w and directions["Player 2"] != (0, 1):
                directions["Player 2"] = (0, -1)
            elif event.key == pygame.K_s and directions["Player 2"] != (0, -1):
                directions["Player 2"] = (0, 1)
            elif event.key == pygame.K_a and directions["Player 2"] != (1, 0):
                directions["Player 2"] = (-1, 0)
            elif event.key == pygame.K_d and directions["Player 2"] != (-1, 0):
                directions["Player 2"] = (1, 0)
            elif event.key == pygame.K_p:
                pause_game()
            elif event.key == pygame.K_h:
                display_high_scores()
        elif event.type == pygame.USEREVENT and game_mode == "timed":
            game_time -= 1000
            if game_time <= 0:
                if scores["Player 1"] > scores["Player 2"]:
                    game_over("Player 1")
                elif scores["Player 2"] > scores["Player 1"]:
                    game_over("Player 2")
                else:
                    game_over("No one, it's a tie!")

    for player in player_names:
        if directions[player] != (0, 0):
            new_head = (snakes[player][0][0] + directions[player][0], snakes[player][0][1] + directions[player][1])
            if check_collision(player, new_head):
                other_player = "Player 2" if player == "Player 1" else "Player 1"
                game_over(other_player)
            snakes[player].insert(0, new_head)
            if new_head == foods[player]:
                eat_sound.play()
                foods[player] = random_food(list(snakes["Player 1"]) + list(snakes["Player 2"]))
                current_food_types[player] = random.choice(food_types)
                food_timers[player] = 5000 if current_food_types[player] != "normal" else 0
                if current_food_types[player] == "normal":
                    scores[player] += 1
                elif current_food_types[player] == "super":
                    scores[player] += 3
                    speeds[player] += 3
                elif current_food_types[player] == "slow":
                    scores[player] += 1
                    speeds[player] = max(5, speeds[player] - 2)
                elif current_food_types[player] == "reverse":
                    scores[player] += 2
                    directions[player] = (-directions[player][0], -directions[player][1])
                if scores[player] % 10 == 0:
                    levels[player] += 1
                    speeds[player] += 2
                    obstacles.append((random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)))
                    move_obstacles()
            else:
                snakes[player].pop()

    if food_timers["Player 1"] > 0:
        food_timers["Player 1"] -= clock.get_time()
        if food_timers["Player 1"] <= 0:
            current_food_types["Player 1"] = "normal"
    if food_timers["Player 2"] > 0:
        food_timers["Player 2"] -= clock.get_time()
        if food_timers["Player 2"] <= 0:
            current_food_types["Player 2"] = "normal"

    screen.fill(BLACK)
    for player in player_names:
        for segment in snakes[player]:
            pygame.draw.rect(screen, GREEN if player == "Player 1" else BLUE, pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for obstacle in obstacles:
        pygame.draw.rect(screen, GREY, pygame.Rect(obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for player in player_names:
        food_color = RED if current_food_types[player] == "normal" else (BLUE if current_food_types[player] == "super" else (YELLOW if current_food_types[player] == "slow" else GREY))
        pygame.draw.rect(screen, food_color, pygame.Rect(foods[player][0] * GRID_SIZE, foods[player][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for player in player_names:
        score_text = font.render(f"{player} Score: {scores[player]}", True, WHITE)
        level_text = font.render(f"{player} Level: {levels[player]}", True, WHITE)
        screen.blit(score_text, (5, 5 if player == "Player 1" else 35))
        screen.blit(level_text, (5, 30 if player == "Player 1" else 60))
    if game_mode == "timed":
        time_text = font.render(f"Time: {game_time // 1000}", True, WHITE)
        screen.blit(time_text, (5, 85))
    pygame.display.flip()

    clock.tick(max(speeds["Player 1"], speeds["Player 2"]))
