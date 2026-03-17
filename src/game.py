#! /usr/bin/python
import random
from collections import deque


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
            x = random.randint(0, (self.width-10)//10) * 10
            y = random.randint(0, (self.height-10)//10) * 10
            if [x,y] not in self.snake:
                return [x, y]

    def step(self, action):
        #Human or bot action
        if action in self.DIRECTIONS:
            self.direction = action

        #new head
        curr_head = self.snake[0]
        move = self.DIRECTIONS[self.direction]
        new_head = [curr_head[0]+move[0],curr_head[1]+move[1]]

        
        if new_head in self.snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= self.width or new_head[1] >= self.height:
            self.game_over = True
            return self.game_over, self.score

        # move
        self.snake.appendleft(new_head)

        # food catched?
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()
        
        return self.game_over, self.score