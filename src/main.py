#!/usr/bin/python
import pygame
import numpy as np
from game import SnakeGame
from agent import Agent

#Init
pygame.init()
game = SnakeGame()
agent = Agent() #bot 
screen = pygame.display.set_mode((640,480)) # size
clock = pygame.time.Clock()  # game speed
running = True
ai_mode = False # Human is starting

while running:
    action = [1,0,0]
    user_direction = None 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN: 
            # Toggle AI
            if event.key == pygame.K_m:
                ai_mode = not ai_mode
                print(f'Tryb AI: {ai_mode}')

            # manual
            if not ai_mode:
                if event.key == pygame.K_UP: action = 'UP'
                elif event.key == pygame.K_DOWN: action = 'DOWN'
                elif event.key == pygame.K_LEFT: action = 'LEFT'
                elif event.key == pygame.K_RIGHT: action = 'RIGHT'

    if not ai_mode and user_direction:
        clock_wise = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        idx = clock_wise.index(game.direction) # curr direction

        if user_direction == clock_wise[(idx + 1) % 4]:
            action = [0, 1, 0] # right
        elif user_direction == clock_wise[(idx - 1) % 4]:
            action = [0, 0, 1] # left
        else:
            action = [1, 0, 0] # forward

    #  AI
    if ai_mode:
        state = agent.get_state(game)
        action = [1,0,0]
    
    #next iter
    reward, game_over, score = game.step(action)

    if game_over:
        print(f'Game over! Score: {score}')
        game.reset() # restart
        # running = False # Opcjonalnie, jeśli wolisz zamknąć okno

    # screen rendering
    screen.fill((255,255,255)) # white

    # snake rendering
    for seg in game.snake:
        pygame.draw.rect(screen, (128, 128, 128), (seg[0], seg[1], 20, 20))

    #food rendering
    pygame.draw.rect(screen, (0, 0, 0), (game.food[0], game.food[1], 20, 20))

    pygame.display.flip()
    clock.tick(20) # per second
pygame.quit()



