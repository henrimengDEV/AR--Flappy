import random
import time

import pygame

from IEntity import IEntity
from config import *


class Player(IEntity):
    def __init__(self):
        self.x = 150
        self.y = H // 2
        self.images = [load_image(os.path.join(IMAGES, f'bird{i + 1}.png')) for i in range(3)]
        self.c = 0
        self.timer = time.time()
        self.dy = 0
        self.rot = 45
        self.stopped = False

    @property
    def image(self):
        return pygame.transform.rotate(self.images[self.c], self.rot)

    @property
    def rect(self):
        return self.image.get_rect(center=(self.x, self.y))

    def update(self, events: list[pygame.event.Event], dt):
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
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.dy = -5
        self.rot = clamp(self.rot, -45, 25)
        self.y = clamp(self.y, 0, H - 50)

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, 'red', self.rect, 5)


class Pipe(IEntity):
    """
    This class contains the pipe object which is itself a collection of 2 pipes
    inverted w.r.t each other
    """

    def __init__(self, x=W // 2, y=H - 50 - 320):
        self.x = x
        self.y = y
        self.image = load_image(os.path.join(IMAGES, 'pipe-green.png'))
        self.gap = 150
        self.w, self.h = self.image.get_size()
        self.h1 = random.randint(100, self.h - 50)
        self.h2 = H - self.h1 - 50 - self.gap

        self.surf1 = pygame.transform.rotate(self.image.subsurface((0, 0, self.w, self.h1)), 180)
        self.surf2 = self.image.subsurface((0, 0, self.w, self.h2))

        self.scored = False
        self.visible = True

    @property
    def rectangle_top(self):
        return pygame.Rect(round(self.x), 0, self.w, self.h1)

    @property
    def rectangle_bot(self):
        return pygame.Rect(round(self.x), self.rectangle_top.bottom + self.gap, self.w, self.h2)

    @property
    def rectangle_middle(self):
        return pygame.Rect(round(self.x), self.rectangle_top.bottom, self.w, self.gap)

    def move(self, speed, dt):
        self.x -= speed * dt

    def collision(self, rect: pygame.Rect):
        if self.rectangle_top.inflate(-10, -10).colliderect(rect) or self.rectangle_bot.inflate(-10, -10).colliderect(rect):
            return True
        else:
            return False

    def draw(self, surf: pygame.Surface, is_next=False):
        x = round(self.x)
        surf.blit(self.surf1, (x, 0))
        surf.blit(self.surf2, (x, self.rectangle_top.height + self.gap))
        if not is_next:
            return
        pygame.draw.rect(surf, 'red', self.rectangle_middle)
        # pygame.draw.rect(surf, 'red', self.rect1)
        # pygame.draw.rect(surf, 'red', self.rect2)
