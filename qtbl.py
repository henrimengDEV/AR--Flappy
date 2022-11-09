import os
import pickle
import random

from config import ACTIONS, FILE_QTABLE



global qtable
global is_init


def init_qtable():
    if os.path.exists(FILE_QTABLE):
        load(FILE_QTABLE)
        return

    result = {}
    states = {}

    for x in range(-64, 64):
        for y in range(-64, 64):
            for z in range(-64, 64):
                states[(x, y, z)] = 0

    for state in states:
        result[state] = {}
        for action in ACTIONS:
            result[state][action] = 0

    global qtable
    global is_init
    is_init = False
    qtable = result


def save(filename):
    with open(filename, 'wb') as file:
        global qtable
        pickle.dump(qtable, file)


def load(filename):
    with open(filename, 'rb') as file:
        global qtable
        qtable = pickle.load(file)
