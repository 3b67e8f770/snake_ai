#! /usr/bin/python
import random
from collections import deque
import numpy as np


class SnakeGame:
    
    #directions
    DIRECTIONS = {
        'RIGHT': (20, 0),
        'LEFT' : (-20, 0),
        'UP'   : (0, -20),
        'DOWN' : (0, 20)
    }
 
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # beginning
        self.direction = "RIGHT"
        self.snake = deque([[100, 60], [80, 60], [60, 60]])
        self.food = self._place_food()
        self.score = 0
        self.game_over = False

    def _place_food(self):
        while True:
            x = random.randint(0, (self.width-20)//20) * 20
            y = random.randint(0, (self.height-20)//20) * 20
            if [x,y] not in self.snake:
                return [x, y]

    def step(self, action):
        self.game_over = False
        reward = 0

        # clock wise cirection
        clock_wise = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # Bez zmian
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # Skręt w prawo (CW)
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Skręt w lewo (CCW)
        
        self.direction = new_dir

        # cant't turn back
        #opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        #if action in self.DIRECTIONS and action != opposites.get(self.direction):
            #self.direction = action

        # MOve
        curr_head = self.snake[0]
        move = self.DIRECTIONS[self.direction]
        new_head = [curr_head[0] + move[0], curr_head[1] + move[1]]

        # collision? 
        if self._is_collision(new_head):
            self.game_over = True
            reward = -20
            return reward, self.game_over, self.score
        
        # new head
        self.snake.appendleft(new_head)

        # food ate?
        if new_head == self.food:
            self.score += 1
            reward = 10 
            self.food = self._place_food()
        else:
            self.snake.pop()
            reward = -0.01
        
        return reward, self.game_over, self.score
    
    def _is_collision(self, pt):
        if (pt[0] < 0 or pt[0] >= self.width or
            pt[1] < 0 or pt[1] >= self.height or 
            pt in list(self.snake)):
            return True
        return False

    @staticmethod
    def get_simple_ai_move(game):
        head = game.snake[0]
        food = game.food
        # easy  AI
        if food[0] > head[0]: return 'RIGHT'
        if food[0] < head[0]: return 'LEFT'
        if food[1] > head[1]: return 'DOWN'
        if food[1] < head[1]: return 'UP'
        return game.direction
    
    #def checkin_par(self,new_head, direction,):
     #   possibile_move = [new_head + direction, new_head + RIGHT, new_head + LEFT]
     #   denger = []
      #  where_food = []
      #  for single_move in possibile_move:
      #      if single_move in self.snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= self.width or new_head[1] >= self.height:
       #         denger.append(1)
       #     else:
      #          denger.append(0)

        

            
