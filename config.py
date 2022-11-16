import os

import pygame
""" GAME SETTINGS """

START_SPEED = 3
END_SPEED = 9

W, H = 960, 540

FPS = 180

DT = 1
ASSETS = 'assets'
IMAGES = os.path.join(ASSETS, 'images')
SOUNDS = os.path.join(ASSETS, 'sounds')

BEST_SCORE = 0
NUMBER_OF_ITERATION = 1

def load_image(path, alpha=False, scale=1.0, color_key=None):
    img = pygame.image.load(path)
    if alpha:
        img = img.convert_alpha()
    else:
        img = img.convert()
    if color_key:
        img.set_colorkey(color_key)
    return img


def clamp(value, mini, maxi):
    if value < mini:
        return mini
    if value > maxi:
        return maxi
    return value
