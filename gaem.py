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
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def init_snake():
    return [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]

def random_food():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

snake = init_snake()
direction = (0, 0)
food = random_food()

def game_over():
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (1, 0)

    if direction != (0, 0):
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if new_head in snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            game_over()
        snake.insert(0, new_head)
        if new_head == food:
            food = random_food()
        else:
            snake.pop()

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()

    clock.tick(10)

