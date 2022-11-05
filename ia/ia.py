import os

from agent import Agent
from constant import FLAPPY, FILE_QTABLE
from environment import Environment


class Ia:
    def __init__(self) -> None:
        super().__init__()
        env = Environment(FLAPPY)
        agent = Agent(env)
        if os.path.exists(FILE_QTABLE):
            agent.load(FILE_QTABLE)
        agent.learn(100)
        agent.save(FILE_QTABLE)




if __name__ == '__main__':
    ia = Ia()