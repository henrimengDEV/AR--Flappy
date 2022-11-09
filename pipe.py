import random

from config import *


class Pipe:
    """
    This class contains the pipe object which is itself a collection of 2 pipes
    inverted w.r.t each other
    """

    def __init__(self, x=W // 2, y=H - 50 - 320):
        self.x = x
        self.y = y
        self.image = load_image(os.path.join(IMAGES, 'pipe-green.png'))
        self.gap = 200
        self.w, self.h = self.image.get_size()
        self.h1 = self.h - 150
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
        if self.rectangle_top.inflate(-10, -10).colliderect(rect) or self.rectangle_bot.inflate(-10, -10).colliderect(
                rect):
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
