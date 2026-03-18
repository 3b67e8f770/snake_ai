#!/usr/bin/python
import pygame
from game import SnakeGame

#Init
pygame.init()
game = SnakeGame()
screen = pygame.display.set_mode((640,480)) # size
clock = pygame.time.Clock()  # game speed
running = True

while running:
    action = None # go straight

    # input - controll
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: action = 'UP'
            elif event.key == pygame.K_DOWN: action = 'DOWN'
            elif event.key == pygame.K_LEFT: action = 'LEFT'
            elif event.key == pygame.K_RIGHT: action = 'RIGHT'
    
    # next iter
    game_over, score = game.step(action)

    # Game over
    if game.game_over:
        print(f'Game over! Score: {game.score}')
        running = False

    # rendering
    screen.fill((255,255,255)) # white

    # snake rendering
    for seg in game.snake:
        pygame.draw.rect(screen, (128, 128, 128), (seg[0], seg[1], 20, 20))

    #food rendering
    pygame.draw.rect(screen, (0, 0, 0), (game.food[0], game.food[1], 20, 20))

    pygame.display.flip()
    clock.tick(20) # 10 per second
pygame.quit()



