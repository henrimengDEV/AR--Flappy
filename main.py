import sys

from config import FPS
import Ia

from player import Player
from environment import Environment
from Ia import *
from ia_settings import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.W, config.H))

def main_game():
    player = Player()
    environment = Environment(player)
    ia = Ia(player, environment)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                ia.save(FILE_QTABLE)
                return
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                ia.save(FILE_QTABLE)
                return
        if environment.reset:
            player = Player()
            environment = Environment(player)
            ia.reset(player, environment)

        environment.step()
        ia.step()

        environment.draw(screen)
        ia.draw(screen)

        pygame.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main_game()
    pygame.quit()
    sys.exit(0)
