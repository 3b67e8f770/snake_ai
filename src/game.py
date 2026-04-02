#! /usr/bin/python
import random
from collections import deque
import numpy as np
import math

class Direction:
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    UP = 'UP'
    DOWN = 'DOWN'


class SnakeGame:
    
    #directions
    DIRECTIONS = {
        'RIGHT': (20, 0),
        'LEFT' : (-20, 0),
        'UP'   : (0, -20),
        'DOWN' : (0, 20)
    }
    CLOCK_WISE = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.reset()
        self.head = self.snake[0]


    def get_ray_dist(self, direction): # => 1/distans to danger
        x , y = self.snake[0]
        distance = 0
        while True:
            distance += 1
            x += direction[0] * 20
            y += direction[1] * 20
            if self._is_collision([x,y]):
                if distance == 0:
                    return 1.0
                return 1.0 /distance
            if distance > 50 or distance > self.width//20 or distance > self.height//20: return 0.0

    def get_occupancy_sectors(self):
        sectors = [0.0] * 8
        if len(self.snake) <= 1: return sectors

        snake_len = len(self.snake)
        for i, segment in enumerate(list(self.snake)[1:]):
            dx = segment[0] - self.snake[0][0]
            dy = segment[1] - self.snake[0][1]

            angle = math.atan2(dy, dx) # in PI
            if angle <0: angle += 2 * math.pi

            sector_idx = int((angle / (2*math.pi)) * 8) % 8
            weight = 1.0 - (i/snake_len) * 0.8
            sectors[sector_idx] += weight

            

        return [min(s / 5.0, 1.0) for s in sectors]

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
    
    def is_path_blocked_by_tail(self, head, food):
        # area between head and food
        min_x, max_x = min(head[0], food[0]), max(head[0], food[0])
        min_y, max_y = min(head[1], food[1]), max(head[1], food[1])

        # counting a risk

    def step(self, action):
        self.game_over = False
        reward = 0

        head_old = self.snake[0]
        dist_old = np.sqrt((head_old[0] - self.food[0])**2 + (head_old[1] - self.food[1])**2)

        # clock wise cirection
        idx = self.CLOCK_WISE.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = self.CLOCK_WISE[idx] # Bez zmian
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = self.CLOCK_WISE[next_idx] # Skręt w prawo (CW)
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = self.CLOCK_WISE[next_idx] # Skręt w lewo (CCW)
        
        self.direction = new_dir

        # cant't turn back
        #opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        #if action in self.DIRECTIONS and action != opposites.get(self.direction):
            #self.direction = action

        # Move
        curr_head = self.snake[0]
        move = self.DIRECTIONS[self.direction]
        new_head = [curr_head[0] + move[0], curr_head[1] + move[1]]

        # collision? 
        if self._is_collision(new_head):
            self.game_over = True
            return -100, self.game_over, self.score
        
        # new head
        self.snake.appendleft(new_head)
        self.head = self.snake[0]

        # food ate?
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
            reward = 50
            
        else:
            self.snake.pop()
            
            # Am I closer?
            dist_new = np.sqrt((new_head[0] - self.food[0])**2 + (new_head[1] - self.food[1])**2)

            if dist_new < dist_old: # closer
                self.occupancy = self.get_square_occupancy(new_head, self.food)
                reward = 0.2 * self.occupancy
            else:
                reward = -0.2 #further

        return reward, self.game_over, self.score
    
    def _is_collision(self, pt):
        if (pt[0] < 0 or pt[0] >= self.width or
            pt[1] < 0 or pt[1] >= self.height or 
            pt in list(self.snake)):
            return True
        return False
    

    
    def get_relative_move_to(self, target_dir):
        #human to computer
        # clock wise cirection

        curr_idx = self.CLOCK_WISE.index(self.direction)
        target_idx = self.CLOCK_WISE.index(target_dir)

        diff = (target_idx - curr_idx) % 4
        if diff == 3 : return 2 # left
        if diff == 1 : return 1 # right
        return 0 # fwd 

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
    
    def get_square_occupancy(self, head, food):
        # 20px is our square by default
        x_range = range(min(head[0], food[0]), max(head[0], food[0]) + 20, 20)
        y_range = range(min(head[1], food[1]), max(head[1], food[1]) + 20, 20)

        area = len(x_range) * len(y_range)
        if area <= 1: return 0.5 # food is next to the head

        total_weight = 0
        snake_len = len(self.snake)

        for i, segment in enumerate(self.snake):
            if segment[0] in x_range and segment[1] in y_range:
                weight = 1.0 - (i/snake_len)*0.9
                total_weight += weight
        
        return ((total_weight / area) *(-1) + 0.5) 
    
    #def checkin_par(self,new_head, direction,):
     #   possibile_move = [new_head + direction, new_head + RIGHT, new_head + LEFT]
     #   denger = []
      #  where_food = []
      #  for single_move in possibile_move:
      #      if single_move in self.snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= self.width or new_head[1] >= self.height:
       #         denger.append(1)
       #     else:
      #          denger.append(0)

        

            
