#!/usr/bin/python
import pygame
import numpy as np
from game import SnakeGame
from agent import Agent


def train():

    speed = 75
    #Init
    pygame.init()
    game = SnakeGame()
    agent = Agent() #bot 
    screen = pygame.display.set_mode((640,480)) # size
    clock = pygame.time.Clock()  # game speed
    
    running = True
    ai_mode = True 
    user_direction = None

    print("Let's the lerning begin use 'm' to")

    while running: 
        
        state_old = agent.get_state(game) # curent state
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYDOWN: 
                # Toggle AI
                if event.key == pygame.K_m:
                    ai_mode = not ai_mode
                    print(f'Tryb AI: {ai_mode}')
                # speed +
                if event.key == pygame.K_KP_PLUS:
                    speed  *= 2
                    print(f'Now the speed is {speed}')
                # speed -   
                if event.key == pygame.K_KP_MINUS and speed >= 2:
                    speed = int(speed/2)
                    print(f'Now the speed is {speed}')

                # manual
                if not ai_mode:
                    if event.key == pygame.K_UP: user_direction = 'UP'
                    elif event.key == pygame.K_DOWN: user_direction = 'DOWN'
                    elif event.key == pygame.K_LEFT: user_direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT: user_direction = 'RIGHT'

        if ai_mode:
            final_move = agent.get_action(state_old, game)
        else:
            clock_wise = ['UP', 'RIGHT', 'DOWN', 'LEFT']
            idx = clock_wise.index(game.direction) # curr direction

            if user_direction == clock_wise[(idx + 1) % 4]:
                final_move = [0, 1, 0] # right
            elif user_direction == clock_wise[(idx - 1) % 4]:
                final_move = [0, 0, 1] # left
            else:
                final_move = [1, 0, 0] # forward
        reward, done, score = game.step(final_move) # do
        state_new = agent.get_state(game) # check
        agent.train_short_memory(state_old, final_move, reward, state_new, done) # train
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            #the real learning
            agent.train_long_memory()
            print(f'Attempt #{agent.n_games} reached score: {score}, With EPsilon {agent.epsilon}.')

        if score > agent.record:
            agent.record = score
            agent.model.save()
            print("New record! Model saved")
        

        # screen rendering
        screen.fill((255,255,255)) # white

        # snake rendering
        for seg in game.snake:
            pygame.draw.rect(screen, (128, 128, 128), (seg[0], seg[1], 20, 20))

        #food rendering
        pygame.draw.rect(screen, (0, 0, 0), (game.food[0], game.food[1], 20, 20))

        pygame.display.flip()
        clock.tick(speed) # per second
    pygame.quit()


if __name__ == "__main__":
    train()
