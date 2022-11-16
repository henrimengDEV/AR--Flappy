import math
import pickle
import random

import config
from config import *
from ia import ia_basic_settings
from ia.ia_basic_settings import *

RADAR_RESOLUTION_X = 100
RADAR_RESOLUTION_Y = 100
Q_TABLE_RANGE = 16


class ia_basic:
    def __init__(self, agent, environment, learning=True):
        self.learning = learning
        self.history = []
        self.agent = agent
        self.environment = environment
        self.last_state = None
        self.last_reward = 0
        self.action = None
        self.alpha = ia_basic_settings.ALPHA
        self.alpha_decrease_rate = (ia_basic_settings.ALPHA - ALPHA_MIN) / (ALPHA_DECREASE_END - ALPHA_DECREASE_START)
        self.gamma = GAMMA
        self.epsilon_decrease_rate = ia_basic_settings.EPSILON / (EPSILON_DECREASE_END - EPSILON_DECREASE_START)
        self.min_qtable = -(Q_TABLE_RANGE // 2)
        self.max_qtable = Q_TABLE_RANGE // 2
        self.q_table = self.init_qtable()

    def init_qtable(self):
        if os.path.exists(FILE_QTABLE):
            ia_basic_settings.EPSILON = 0.0
            qtable, history = self.load(FILE_QTABLE)
            self.history = history
            return qtable

        result = {}
        states = {}

        for x in range(self.min_qtable, self.max_qtable):
            for y in range(self.min_qtable, self.max_qtable):
                for z in range(self.min_qtable, self.max_qtable):
                        states[(x, y, z)] = 0

        for state in states:
            result[state] = {}
            for action in ACTIONS:
                result[state][action] = 0

        return result

    def get_states(self):
        return clamp(self.horizontal_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable), \
               clamp(self.vertical_bot_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable), \
               clamp(self.vertical_top_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable)

    def horizontal_distance_from_next_pipe_clamp(self):
        return math.ceil(self.environment.pipes[0].rectangle_middle.x / RADAR_RESOLUTION_X)

    def vertical_bot_distance_from_next_pipe_clamp(self):
        return math.ceil((self.environment.pipes[0].rectangle_bot.y - self.agent.rect.y) / RADAR_RESOLUTION_Y)

    def vertical_top_distance_from_next_pipe_clamp(self):
        return math.ceil((self.agent.rect.y - self.environment.pipes[0].rectangle_top.bottom) / RADAR_RESOLUTION_Y)

    def vertical_middle_distance_from_next_pipe_clamp(self):
        return math.ceil((self.agent.rect.y - self.environment.pipes[0].rectangle_middle.y) / RADAR_RESOLUTION_Y)

    def step(self):
        self.update_parameters()
        self.handle_reward()

        states = self.get_states()
        self.action = self.best_action(states)

        self.last_state = (states[0], states[1], states[2])

        if self.action == ACTION_FLAP:
            self.agent.jump()

    def update_parameters(self):
        if self.environment.reset:
            config.NUMBER_OF_ITERATION += 1
            if config.NUMBER_OF_ITERATION >= EPSILON_DECREASE_START:
                if ia_basic_settings.EPSILON > self.epsilon_decrease_rate:
                    ia_basic_settings.EPSILON -= self.epsilon_decrease_rate
                else:
                    ia_basic_settings.EPSILON = 0
            if config.NUMBER_OF_ITERATION >= ALPHA_DECREASE_START:
                if ia_basic_settings.ALPHA > self.alpha_decrease_rate * 1.1:
                    ia_basic_settings.ALPHA -= self.alpha_decrease_rate
                else:
                    ia_basic_settings.ALPHA = ALPHA_MIN

        if pygame.key.get_pressed()[pygame.K_UP]:
            ia_basic_settings.EPSILON += self.epsilon_decrease_rate

    def learn(self, reward):
        max_q = max(self.q_table[self.last_state].values())

        self.q_table[self.last_state][self.action] = self.alpha * (
                reward + self.gamma * max_q - self.q_table[self.last_state][self.action])
        self.last_reward = reward

    def best_action(self, state: tuple[int, int, int]):
        actions = self.q_table[state[0], state[1], state[2]]

        if random.uniform(0, 1) < ia_basic_settings.EPSILON:
            return random.choice(ACTIONS)
        else:
            return max(actions, key=actions.get)

    def handle_reward(self):
        if self.environment.has_scored:
            if self.learning:
                self.learn(REWARD)
            self.environment.has_scored = False

        if self.environment.failed:
            if self.learning:
                self.learn(PUNISHMENT)

    def draw(self, surf: pygame.Surface):
        self.display_informations(surf)

    def display_informations(self, surf):
        font = pygame.font.SysFont(None, 24)
        x_distance = font.render(f"x: {self.horizontal_distance_from_next_pipe_clamp()}", True,
                                 pygame.Color('white'))
        y_top_distance = font.render(f"y_top: {self.vertical_top_distance_from_next_pipe_clamp()}", True,
                                     pygame.Color('white'))
        y_bot_distance = font.render(f"y_bot: {self.vertical_bot_distance_from_next_pipe_clamp()}", True,
                                     pygame.Color('white'))
        epsilon = font.render(f"randomness: {round(ia_basic_settings.EPSILON, 2)}", True, pygame.Color('white'))
        alpha = font.render(f"alpha: {round(ia_basic_settings.ALPHA, 2)}", True, pygame.Color('white'))
        iterations = font.render(f"iteration: {config.NUMBER_OF_ITERATION}", True, pygame.Color('white'))
        surf.blit(x_distance, (20, 20))
        surf.blit(y_top_distance, (20, 40))
        surf.blit(y_bot_distance, (20, 60))
        surf.blit(alpha, (20, 90))
        surf.blit(epsilon, (20, 110))
        surf.blit(iterations, ((W / 2) - 55, 10))

    def reset(self, player, environment):
        self.history.append(self.environment.score)
        self.agent = player
        self.environment = environment

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.q_table, self.history), file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
