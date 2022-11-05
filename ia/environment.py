import pprint

from constant import *


class Environment:
    def __init__(self, str_flappy) -> None:
        super().__init__()
        self.__states, self.__start = self.__parse(str_flappy)
        self.__nb_states = len(self.__states)
        self.__str_flappy = str_flappy

    def __parse(self, str_flappy):
        result = {}
        start = tuple()
        lines = str_flappy.strip().splitlines()

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == FLAPPY_START:
                    start = (col, row)
                result[(col, row)] = char

        self.__rows = row + 1
        self.__cols = col + 1
        return result, start

    def do(self, state: tuple[int, int], action: str):
        move = ACTION_MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        reward = REWARD_DEFAULT

        if self.is_death_state(new_state):
            reward = -1000 * self.__nb_states

        state = new_state
        return reward, state

    def print(self, agent):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (col, row)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[state]
            res += '\n'
        print(res)

    def is_death_state(self, state: tuple[int, int]):
        return state not in self.__states \
               or self.is_tunnel(state) or self.is_out_of_range(state)

    def is_tunnel(self, state: tuple[int, int]):
        return self.__states[state] == FLAPPY_TUNNEL

    def is_start(self, state: tuple[int, int]):
        return self.__states[state] == FLAPPY_START

    def is_out_of_range(self, state: tuple[int, int]):
        return state[1] < 0 or self.__rows < state[1]

    @property
    def start(self):
        return self.__start

    @property
    def width(self):
        return self.__cols - 1

    @property
    def states(self):
        return self.__states
