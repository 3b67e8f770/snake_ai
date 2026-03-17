#! /usr/bin/python
import random


class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # Stan początkowy
        self.direction = "RIGHT"
        self.head = [100, 50]
        self.snake = [[100, 50], [90, 50], [80, 50]]
        self.food = self._place_food()
        self.score = 0

    def _place_food(self):
        # Losowanie jedzenia (uproszczone do siatki 10x10)
        x = random.randint(0, (self.width-10)//10) * 10
        y = random.randint(0, (self.height-10)//10) * 10
        return [x, y]

    def step(self, action):
        # Tutaj action będzie kierunkiem (strzałka lub decyzja AI)
        # 1. Porusz węża
        # 2. Sprawdź kolizję (koniec gry?)
        # 3. Sprawdź czy zjadł jabłko
        pass