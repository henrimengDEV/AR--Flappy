import pickle
import pprint

from agent import Player
from environment import Environment
from pipe import *


class MenuManager:
    def __init__(self):
        self.menus = {
            'game': Environment(self)
        }
        self.mode = 'game'
        self.menu = self.menus[self.mode]

    def switch_mode(self, mode, reset=False):
        self.mode = mode
        self.menu = self.menus[self.mode]
        if reset:
            self.menu = Environment(self)

    def step(self, events: list[pygame.event.Event], dt, clock):
        self.menu.step(events, dt, clock)

    def draw(self, surf: pygame.Surface):
        self.menu.draw(surf)
