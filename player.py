import time

from config import *

START_POSITION_X = 150
START_POSITION_Y = H // 2
JUMP_VELOCITY = -5
TILT_RATIO = 5
FALL_RATIO = 0.25
DELAY_TOLERANCE = 0.1


class Player:
    def __init__(self):
        self.x = START_POSITION_X
        self.y = START_POSITION_Y
        self.images = [load_image(os.path.join(IMAGES, f'bird{i + 1}.png')) for i in range(3)]
        self.compensation = 0
        self.timer = time.time()
        self.delta_y = 0
        self.rotation = 45
        self.stopped = False

    def step(self, delta_time):
        self.handle_move(delta_time)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.jump()

    def handle_move(self, delta_time):
        if not self.stopped:
            if time.time() - self.timer > DELAY_TOLERANCE:
                self.timer = time.time()
                self.compensation += 1
                self.compensation %= len(self.images)
        self.y += self.delta_y * delta_time
        self.delta_y += FALL_RATIO * delta_time
        self.delta_y = clamp(self.delta_y, -5, 10)
        if self.delta_y > 0:
            self.rotation -= TILT_RATIO * delta_time
        else:
            self.rotation += TILT_RATIO * delta_time
        self.rotation = clamp(self.rotation, -45, 25)
        self.y = clamp(self.y, 0, H - 50)

    def jump(self):
        if not self.stopped:
            self.delta_y = JUMP_VELOCITY

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, 'red', self.rect, 5)

    @property
    def image(self):
        return pygame.transform.rotate(self.images[self.compensation], self.rotation)

    @property
    def rect(self):
        return self.image.get_rect(center=(self.x, self.y))
