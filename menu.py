import pickle
import pprint

from agent import Player
from environment import Environment
from pipe import *


class MenuManager:
    def __init__(self):
        self.qtable = self.__init_qtable()
        self.menus = {
            'game': Environment(self, self.qtable)
        }
        self.mode = 'game'
        self.menu = self.menus[self.mode]

    def switch_mode(self, mode, reset=False):
        self.mode = mode
        self.menu = self.menus[self.mode]
        if reset:
            self.menu = Environment(self, self.qtable)

    def step(self, events: list[pygame.event.Event], dt):
        self.menu.step(events, dt)

    def draw(self, surf: pygame.Surface):
        self.menu.draw(surf)

    def __init_qtable(self):
        result = {}
        states = {}

        for x in range(-100, 100):
            for y in range(-100, 100):
                states[(x, y)] = 0

        for state in states:
            result[state] = {}
            for action in ACTIONS:
                result[state][action] = 0
        return result

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtable, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.qtable = pickle.load(file)
