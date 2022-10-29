from agent import Agent
from constant import FLAPPY
from environment import Environment


class Ia:
    def __init__(self) -> None:
        super().__init__()
        env = Environment(FLAPPY)
        agent = Agent(env)
        agent.learn(2)



if __name__ == '__main__':
    ia = Ia()