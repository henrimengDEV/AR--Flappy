ACTION_FLAP = "FLAP"
ACTION_NOTHING = "NOTHING"
ACTIONS = [ACTION_FLAP, ACTION_NOTHING]
ACTION_MOVES = {
    ACTION_FLAP: (1, -1),
    ACTION_NOTHING: (1, 1)
}

REWARD_DEFAULT = 0
FLAPPY_START = '.'
FLAPPY_TUNNEL = '#'
FILE_QTABLE = 'qtable.dat'


FLAPPY = """
######################
     #   #   #   #   #
     #   #   #       #
     #   #   #       #
.        #   #   #   #
         #       #    
     #           #    
     #       #   #   #
     #   #   #   #   #
######################
"""