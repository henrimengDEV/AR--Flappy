import sys
import matplotlib.pyplot as plt

from environment import Environment
from ia import ia_basic, ia_advanced_settings, ia_basic_settings
from ia.ia_advanced import ia_advanced
from ia.ia_advanced_settings import *
from ia.ia_basic import *
from player import Player

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))


def ia_training_basic(learning=True):
    player = Player()
    environment = Environment(player)
    ia = ia_basic(player, environment, learning)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if learning:
                    ia.save(ia_basic_settings.FILE_QTABLE)
                plt.plot(ia.history)
                return

        if environment.reset:
            player = Player()
            environment = Environment(player)
            ia.reset(player, environment)

        environment.step()
        environment.draw(screen)

        ia.step()
        ia.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


def ia_training_advanced(learning=True):
    player = Player()
    environment = Environment(player)
    ia = ia_advanced(player, environment)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if learning:
                    ia.save(ia_advanced_settings.FILE_QTABLE)
                plt.plot(ia.history)
                return

        if environment.reset:
            player = Player()
            environment = Environment(player)
            ia.reset(player, environment)

        environment.step()
        environment.draw(screen)

        ia.step()
        ia.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


def classic_game():
    player = Player()
    environment = Environment(player)

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return

        if environment.reset:
            player = Player()
            environment = Environment(player)

        environment.step()
        environment.draw(screen)

        pygame.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    learning = True
    """ Play a classic game """
    # classic_game()

    """ Basic IA training (3 states: X-axis, Y-axis top, Y-axis bottom) (Faster)"""
    #ia_training_basic(learning)

    """ Advanced IA training (4 states: X-axis, Y-axis top, Y-axis bottom, Velocity) (Longer)"""
    ia_training_advanced(learning)

    """ Play a classic game """

    pygame.quit()
    plt.show()
    sys.exit(0)
