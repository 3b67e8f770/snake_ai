#!/usr/bin/python3
import torch
import random
import numpy as np
from collections import deque
from game import SnakeGame
from model import Linear_QNet, QTrainer
import os
from game import Direction 

MAX_MEMORY = 100_000 # LAst moves
BATCH_SIZE = 1000 # LAst games
LR= 0.001 # LEarning speed

class Agent:

    def __init__(self):
        self.record = 0
        self.n_games = 0
        self.epsilon = 0 # random
        self.gamma = 0.9 # rewards
        self.memory = deque(maxlen=MAX_MEMORY)

        # Neuron 11 in, 3 out
        self.model = Linear_QNet(20,512,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        model_path = './model/model.pth'
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()
            print("previous learning loaded")

    def get_state(self, game):
        head = game.snake[0]

        #input directions
        dir_x, dir_y = 0, 0
        if game.direction == 'LEFT': dir_x = -1
        elif game.direction == 'RIGHT': dir_x = 1
        elif game.direction == 'UP': dir_y = 1
        elif game.direction == 'DOWN': dir_y = -1

        # where is the food?
        food_x = (game.food[0] - head[0]) / game.width
        food_y = (game.food[1] - head[1]) / game.height

        # how far is the wall?
        ray_dirs = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
        rays = [game.get_ray_dist(d) for d in ray_dirs]

        # sectors occupancy
        occupancy = game.get_occupancy_sectors()

        state = [dir_x, dir_y, food_x, food_y, *rays, *occupancy]
        return np.array(state, dtype=float)


    def remember(self, state, action, reward, next_state, done):
        # "I'm still alive" to memory
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        #summarizing at the end
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        #step by step learning
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, game):
        # how random the move is
        if self.n_games > 380:
            self.epsilon = round(self.epsilon * 0.995, 3)
            if self.n_games > 1500:
                self.n_games = 1
        else:
            self.epsilon = 400 - self.n_games
        final_move = [0, 0, 0]

        #random move
        if random.randint(0,400) < self.epsilon:
            target_dir = game.get_simple_ai_move(game)
            move = game.get_relative_move_to(target_dir)
            final_move[move] = 1
        else: # smart move
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # calculate what to do
            move = torch.argmax(prediction).item()  # pick max
            final_move[move] = 1
    
        return final_move # np.array(state, dtype=int)
        


