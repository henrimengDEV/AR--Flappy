""" IA SETTINGS """

REWARD = 0
PUNISHMENT = -10000

ALPHA = 0.7
ALPHA_MIN = 0.1
ALPHA_DECREASE_START = 55
ALPHA_DECREASE_END = 89

GAMMA = 0.95

EPSILON = 0.0309
EPSILON_DECREASE_START = 0
EPSILON_DECREASE_END = 13

ACTION_FLAP = "FLAP"
ACTION_NOTHING = "NOTHING"
ACTIONS = [ACTION_NOTHING, ACTION_FLAP]

FILE_QTABLE = './qtable_basic.dat'
