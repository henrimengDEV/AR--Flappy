import sys

import pygame.display

from menu import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))


def main_game(menu_manager):
    dt = 1
    i = 0
    if os.path.exists(FILE_QTABLE):
        menu_manager.qtable = menu_manager.load(FILE_QTABLE)
        print(menu_manager.qtable)

    while True:
        i += 1
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return

        screen.fill('black')
        menu_manager.step(events, dt)
        menu_manager.draw(screen)

        pygame.display.update()
        dt = TARGET_FPS * clock.tick(FPS) / 1000
        if dt == 0:
            dt = 1

        print(f"Tentative: {i} score: {menu_manager.menu.score}")


if __name__ == '__main__':
    menu_manager = MenuManager()
    main_game(menu_manager)
    menu_manager.save(FILE_QTABLE)
    pygame.quit()
    sys.exit(0)
