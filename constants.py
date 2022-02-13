FIELD = """
    ###########
    #  T      #
    #  T   T  #
    # .    T  #
    #  TTTTTM #
    #  T      #
    ###########
    """

X = 0
Y = 1

STATE_TILLS_COUNT = 9
STATE_X_Y_POSITION = 2
STATE_RADAR_FIRE_TILL = 2

# Rewards
REWARD_BOUNCE = -2
REWARD_FLOOR = -9
REWARD_TREE = 6
REWARD_DEAD_TREE = -14
REWARD_BURNING_TREE = -4
REWARD_OUT = -8
REWARD_BURNING_TREE_DIST = 100

START = '.'
TREE = 'T'
BURNING_TREE = 'M'
WALL = '#'
EMPTY = ' '

STATES = [TREE, BURNING_TREE, EMPTY]

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

ACTION_TYPE_SPRITE_DIC = {
    CUT_TREE: ":resources:images/tiles/sandCenter.png",
    WATER: ":resources:images/tiles/water.png"
}

ACTIONS = [UP, DOWN, LEFT, RIGHT, WATER, CUT_TREE]

# taux de diminution des renforcements (discount factor)
# • Facteur d’actualisation, coefficient d’actualisation, etc.
DISCOUNT_FACTOR = 0.5

# Dans un environnement déterministe tel que le labyrinthe la valeur vaut 1,
# si environnement stochastique alors la valeur vaut 0 < 1
LEARNING_RATE = 0.5
EXPLORATION = 1.0
BURN_PROBABILITY = 0.005
EXPIRE_PROBABILITY = 0.002

SPRITE_SCALING = 0.5
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5
# Do the math to figure out our screen dimensions


AGENT_FILENAME = 'agent.dat'
