ACTION_FLAP = "JUMP"
ACTION_NOTHING = "WAITING"
ACTIONS = [ACTION_FLAP, ACTION_NOTHING]
ACTION_MOVES = {
    ACTION_FLAP: (1, 1),
    ACTION_NOTHING: (1, -1)
}

REWARD_DEFAULT = -1
FLAPPY_START = '.'
FLAPPY_TUNNEL = '#'

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