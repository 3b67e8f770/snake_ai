#!/usr/bin/python3
import torch
import numpy as np
from game import SnakeGame

class Afgent:
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
        

