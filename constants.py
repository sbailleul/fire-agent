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

START = '.'
TREE = 'T'
BURNING_TREE = 'M'
WALL = '#'
EMPTY = ' '


TILE_TYPE_SPRITE_DIC = {TREE: ":resources:images/topdown_tanks/treeGreen_small.png",
                        BURNING_TREE: ":resources:images/topdown_tanks/treeBrown_small.png",
                        EMPTY: ":resources:images/topdown_tanks/tileGrass2.png"
                        }
AGENT_SPRITE = ":resources:images/animated_characters/robot/robot_idle.png"
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

BURN_PROBABILITY = 0.1
EXPIRE_PROBABILITY = 0.1

SPRITE_SCALING = 0.5
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5
# Do the math to figure out our screen dimensions
