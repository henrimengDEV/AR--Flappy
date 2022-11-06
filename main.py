import sys
import pygame

from menu import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))


def main_game():
    dt = 1  # assuming ratio is 1 initially

    menu_manager = MenuManager()

    while True:
        events = pygame.event.get()
        set_up_windows(events)


        # general display blits
        screen.fill('black')

        menu_manager.update(events, dt)
        menu_manager.draw(screen)

        # display update and dt update
        pygame.display.update()
        dt = TARGET_FPS * clock.tick(FPS) / 1000  # ratio of target to current FPS
        # dt = round(dt, 6)
        # print(clock.get_fps())
        # dt = 1
        if dt == 0:
            dt = 1

        # time.sleep(2)


def set_up_windows(events):
    for e in events:
        if e.type == pygame.QUIT:
            return
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return

if __name__ == '__main__':
    main_game()
    pygame.quit()
    sys.exit(0)
