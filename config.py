"""
Entry point for all imports
Here we will need to alias pygame from kengi.pygame
"""

import os
import pickle

import pygame

W, H = 960, 540

FPS = 60
TARGET_FPS = 60
EPSILON = 0.1
ITERATION = 1
ALPHA = 0.7
BEST_SCORE = 0

ASSETS = 'assets'
IMAGES = os.path.join(ASSETS, 'images')
SOUNDS = os.path.join(ASSETS, 'sounds')

SPEED = 3

ACTION_FLAP = "FLAP"
ACTION_NOTHING = "NOTHING"
ACTIONS = [ACTION_NOTHING, ACTION_FLAP]
FILE_QTABLE = 'qtable.dat'

# below are some utility functions

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
