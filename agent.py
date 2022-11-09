import pprint
import random
import time

import config
import qtbl
from config import *
from qtbl import *


class Player:
    def __init__(self, alpha=0.1, gamma=1):
        self.x = 150
        self.y = H // 2
        self.images = [load_image(os.path.join(IMAGES, f'bird{i + 1}.png')) for i in range(3)]
        self.c = 0
        self.timer = time.time()
        self.dy = 0
        self.rot = 45
        self.stopped = False
        self.last_state = None
        self.last_reward = 0
        self.last_action = None
        self.__score = 0
        self.alpha = alpha
        self.gamma = gamma

    def step(self, events: list[pygame.event.Event], dt, state: tuple[int, int]):
        if not self.stopped:
            if time.time() - self.timer > 0.1:
                self.timer = time.time()
                self.c += 1
                self.c %= len(self.images)
        self.y += self.dy * dt
        self.dy += 0.25 * dt
        self.dy = clamp(self.dy, -5, 10)
        if self.dy > 0:
            self.rot -= 5 * dt
        else:
            self.rot += 5 * dt
        if not self.stopped:
            # if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pressed(num_buttons=3)[0]:
            #     self.dy = -5
            self.last_action = self.best_action(state)
            self.last_state = (round(state[0]), round(state[1]))
            if self.last_action == ACTION_FLAP:
                self.dy = -2
        self.rot = clamp(self.rot, -45, 25)
        self.y = clamp(self.y, 0, H - 50)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, 'red', self.rect, 5)

    def learn(self, reward):

        max_q = max(qtbl.qtable[self.last_state].values())
        qtbl.qtable[self.last_state][self.last_action] = self.alpha * (reward + self.gamma * max_q - qtbl.qtable[self.last_state][self.last_action])
        self.last_reward = reward

    def best_action(self, state: tuple[int, int]):
        actions = qtbl.qtable[(round(state[0]), round(state[1]))]
        config.epsilon = 0.1
        if pygame.key.get_pressed()[pygame.K_UP]:
            config.EPSILON += 0.001
            print(config.EPSILON)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            config.EPSILON -= 0.001
            print(config.EPSILON)
        print(actions)

        if actions["NOTHING"] == actions["FLAP"]:
            """
            Explore: select a random action
            """
            if random.uniform(0, 1) < config.EPSILON:
                return ACTION_FLAP
            else:
                return ACTION_NOTHING
        else:
            """
            Exploit: select the action with max value (future reward)
            """
            return max(actions, key=actions.get)

    @property
    def image(self):
        return pygame.transform.rotate(self.images[self.c], self.rot)

    @property
    def rect(self):
        return self.image.get_rect(center=(self.x, self.y))