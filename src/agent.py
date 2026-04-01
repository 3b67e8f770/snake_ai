#!/usr/bin/python3
import torch
import random
import numpy as np
from collections import deque
from game import SnakeGame
from model import Linear_QNet, QTrainer

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
        self.model = Linear_QNet(11,256,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]

        #around the head
        point_le = [head[0] - 20, head[1]]
        point_ri = [head[0] + 20, head[1]]
        point_up = [head[0], head[1] - 20]
        point_do = [head[0], head[1] + 20]

        #forward, right, left
        orientation_map = {
            'UP':    (point_up, point_ri, point_le),
            'DOWN':  (point_do, point_le, point_ri),
            'LEFT':  (point_le, point_up, point_do),
            'RIGHT': (point_ri, point_do, point_up)
        }

        pt_fwd, pt_rig, pt_lef = orientation_map[game.direction]

        state =[
            #Danger
            game._is_collision(pt_fwd),
            game._is_collision(pt_rig),
            game._is_collision(pt_lef),

            # last move direction
            game.direction == "LEFT",
            game.direction == "RIGHT",
            game.direction == "UP",
            game.direction == "DOWN",

            #where is the Food?
            game.food[0] < head[0], #food on the left
            game.food[0] > head[0], #food on the right
            game.food[1] < head[1], #food up
            game.food[1] > head[1]  #food down
        ]
        return np.array(state, dtype=int)

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
        self.epsilon = 160 - self.n_games
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
        


