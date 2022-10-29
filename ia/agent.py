import random
import time

from constant import *
from environment import Environment


class Agent:
    def __init__(self, env: Environment) -> None:
        super().__init__()
        self.__score = None
        self.__state = None
        self.__score = 0
        self.__env = env
        self.reset()

    def reset(self):
        self.__state = self.__env.start
        self.__score = 0

    def learn(self, iterations):
        for i in range(iterations):
            self.reset()
            for y in range(self.__env.width):
                self.step()
                self.__env.print(self)
                time.sleep(1)

    def step(self):
        action = self.best_action()
        reward, self.__state = self.__env.do(self.__state, action)
        print(f"action: {action} state:{self.__state} score:{self.__score}")
        self.__score += reward

    def best_action(self):
        return random.choice(ACTIONS)

    @property
    def state(self):
        return self.__state