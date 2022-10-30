import pprint
import random
import time

from constant import *
from environment import Environment


class Agent:
    def __init__(self, env: Environment, alpha = 1, gamma = 0.2) -> None:
        super().__init__()
        self.__score = None
        self.__state = None
        self.__score = 0
        self.__alpha = alpha
        self.__gamma = gamma
        self.__env = env
        self.reset()
        self.__qtable = self.__init_qtable()

        pprint.pprint(self.__qtable)


    def __init_qtable(self):
        result = {}
        for state in self.__env.states:
            result[state] = {}
            for action in ACTIONS:
                result[state][action] = 0
        return result

    def reset(self):
        self.__state = self.__env.start
        self.__score = 0

    def learn(self, iterations):
        for i in range(iterations):
            self.reset()
            for y in range(self.__env.width):
                self.step()
                self.__env.print(self)
                # time.sleep(1)

    def step(self):
        action = self.best_action()
        reward, self.__state = self.__env.do(self.__state, action)
        print(f"action: {action} state:{self.__state} score:{self.__score}")
        self.__score += reward

        maxQ = max(self.__qtable[self.__state].values())
        self.__qtable[self.state][action] += \
            self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.state][action])

    def best_action(self):
        actions = self.__qtable[self.__state]
        return max(actions, key=actions.get)

    @property
    def state(self):
        return self.__state