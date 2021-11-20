FIELD = """
    ###########
    # .T      #
    #  T   T  #
    #      T  #
    #  TTTTTM #
    #  T      #
    ###########
    """

# Rewards
# REWARD_TREE_WATERED = 10
REWARD_BOUNCE = -2
REWARD_FLOOR = -1
REWARD_DEAD_TREE = -5
REWARD_OUT = -10


# GOAL = '*'
START = '.'
TREE = 'T'
BURNING_TREE = 'M'
WALL = '#'
EMPTY = ' '


# Actions
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

WATER = 'W'
CUT_TREE = 'C'

ACTIONS = [UP, DOWN, LEFT, RIGHT, WATER, CUT_TREE]

# taux de diminution des renforcements (discount factor)
# • Facteur d’actualisation, coefficient d’actualisation, etc.
DISCOUNT_FACTOR = 0.5

# Dans un environnement déterministe tel que le labyrinthe la valeur vaut 1,
# si environnement stochastique alors la valeur vaut 0 < 1
LEARNING_RATE = 0.5