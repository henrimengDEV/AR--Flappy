import math
import pickle
import random

from config import *
from ia.ia_settings import *

Q_TABLE_RANGE = 32
RADAR_RESOLUTION_X = 100
RADAR_RESOLUTION_Y = 100


class ia_advanced:
    def __init__(self, agent, environment):
        self.velocity_iteration = 0
        self.agent = agent
        self.environment = environment
        self.last_state = None
        self.last_reward = 0
        self.action = None
        self.alpha = ALPHA
        self.alpha_decrease_range = ALPHA_DECREASE_END - ALPHA_DECREASE_START
        self.alpha_decrease_rate = (ALPHA - ALPHA_MIN) / self.alpha_decrease_range
        self.gamma = GAMMA
        self.epsilon_decrease_rate = EPSILON / (EPSILON_DECREASE_END - EPSILON_DECREASE_START)
        self.min_qtable = -(Q_TABLE_RANGE // 2)
        self.max_qtable = Q_TABLE_RANGE // 2
        self.q_table = self.init_qtable()

    def init_qtable(self):
        if os.path.exists(FILE_QTABLE):
            global EPSILON
            global ALPHA
            EPSILON = 0.0
            ALPHA = ALPHA_MIN
            return self.load(FILE_QTABLE)

        result = {}
        states = {}

        for x in range(self.min_qtable, self.max_qtable):
            for y in range(self.min_qtable, self.max_qtable):
                for z in range(self.min_qtable, self.max_qtable):
                    for v in range(self.min_qtable, self.max_qtable):
                        states[(x, y, z, v)] = 0

        for state in states:
            result[state] = {}
            for action in ACTIONS:
                result[state][action] = 0

        return result

    def get_states(self):
        return clamp(self.horizontal_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable), \
               clamp(self.vertical_bot_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable), \
               clamp(self.vertical_top_distance_from_next_pipe_clamp(), self.min_qtable, self.max_qtable), \
               clamp(self.velocity(), self.min_qtable, self.max_qtable)

    def horizontal_distance_from_next_pipe_clamp(self):
        return math.ceil(self.environment.pipes[0].rectangle_middle.x / RADAR_RESOLUTION_X)

    def vertical_bot_distance_from_next_pipe_clamp(self):
        return math.ceil((self.environment.pipes[0].rectangle_bot.y - self.agent.rect.y) / RADAR_RESOLUTION_Y)

    def vertical_top_distance_from_next_pipe_clamp(self):
        return math.ceil((self.agent.rect.y - self.environment.pipes[0].rectangle_top.bottom) / RADAR_RESOLUTION_Y)

    def vertical_middle_distance_from_next_pipe_clamp(self):
        return math.ceil((self.agent.rect.y - self.environment.pipes[0].rectangle_middle.y) / RADAR_RESOLUTION_Y)

    def velocity(self):
        return round(self.environment.speed - START_SPEED)

    def step(self):
        self.update_on_iteration()
        self.handle_reward()

        states = self.get_states()
        self.action = self.optimal_action(states)

        self.last_state = (states[0], states[1], states[2], states[3])

        if self.action == ACTION_FLAP:
            self.agent.jump()

    def update_on_iteration(self):
        global NUMBER_OF_ITERATION
        global EPSILON
        global ALPHA
        if self.environment.reset:
            NUMBER_OF_ITERATION += 1
            if NUMBER_OF_ITERATION >= EPSILON_DECREASE_START:
                if EPSILON > self.epsilon_decrease_rate:
                    EPSILON -= self.epsilon_decrease_rate
                else:
                    EPSILON = 0

            if NUMBER_OF_ITERATION >= ALPHA_DECREASE_START:
                if ALPHA > self.alpha_decrease_rate * 1.1:
                    ALPHA -= self.alpha_decrease_rate
                else:
                    ALPHA = ALPHA_MIN

            if ALPHA < 0.1:
                ALPHA = 0

        if pygame.key.get_pressed()[pygame.K_UP]:
            EPSILON += self.epsilon_decrease_rate

    def learn(self, reward):
        max_q = max(self.q_table[self.last_state].values())

        self.q_table[self.last_state][self.action] = self.alpha * (
                reward + self.gamma * max_q - self.q_table[self.last_state][self.action])
        self.last_reward = reward

    def optimal_action(self, state: tuple[int, int, int, int]):
        actions = self.q_table[state[0], state[1], state[2], state[3]]

        if random.uniform(0, 1) < EPSILON:
            return random.choice(ACTIONS)
        else:
            return max(actions, key=actions.get)

    def handle_reward(self):
        if self.environment.has_scored:
            self.learn(REWARD)
            self.environment.has_scored = False

        if self.environment.failed:
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
        velocity = font.render(f"velocity: {self.velocity()}", True, pygame.Color('white'))
        epsilon = font.render(f"randomness: {round(EPSILON, 2)}", True, pygame.Color('white'))
        alpha = font.render(f"alpha: {round(ALPHA, 2)}", True, pygame.Color('white'))
        iterations = font.render(f"iteration: {NUMBER_OF_ITERATION}", True, pygame.Color('white'))
        surf.blit(iterations, ((W / 2) - 55, 10))
        surf.blit(x_distance, (20, 20))
        surf.blit(y_top_distance, (20, 40))
        surf.blit(y_bot_distance, (20, 60))
        surf.blit(velocity, (20, 80))
        surf.blit(alpha, (20, 110))
        surf.blit(epsilon, (20, 130))

    def reset(self, player, environment):
        self.agent = player
        self.environment = environment

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.q_table, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
