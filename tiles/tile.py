import random

import constants
from constants import *


class Tile:

    def __init__(self, position: tuple[int, int], tile_type: str):
        self.position = position
        self.type = tile_type
        self.south = None  # type: Tile | None
        self.north = None  # type: Tile | None
        self.east = None  # type: Tile | None
        self.west = None  # type: Tile | None
        self.north_west = None  # type: Tile | None
        self.south_west = None  # type: Tile | None
        self.north_east = None  # type: Tile | None
        self.south_east = None  # type: Tile | None
        self.neighbors = []
        self.next_type = None

    def set_neighbors(self, all_tiles):
        # type: (dict[tuple[int, int], Tile])-> Tile
        self.south = all_tiles.get((self.position[0] + 1, self.position[1]))
        self.north = all_tiles.get((self.position[0] - 1, self.position[1]))
        self.east = all_tiles.get((self.position[0], self.position[1] + 1))
        self.west = all_tiles.get((self.position[0], self.position[1] - 1))
        self.north_west = all_tiles.get((self.position[0] - 1, self.position[1] - 1))
        self.south_west = all_tiles.get((self.position[0] + 1, self.position[1] - 1))
        self.north_east = all_tiles.get((self.position[0] - 1, self.position[1] + 1))
        self.south_east = all_tiles.get((self.position[0] + 1, self.position[1] + 1))
        self.neighbors = [self.south, self.north, self.west, self.east, self.south_east, self.south_west,
                          self.north_east, self.north_west]

    def on_new_turn(self):
        random_value = random.random()
        if self.type not in [BURNING_TREE, TREE]:
            self.next_type = self.type
            return
        if self.type == BURNING_TREE and random_value < constants.EXPIRE_PROBABILITY:
            self.next_type = EMPTY
            return
        if BURNING_TREE in [neighbor.type if neighbor is not None else None for neighbor in self.neighbors]:
            if random_value < constants.BURN_PROBABILITY:
                self.next_type = BURNING_TREE

    def apply_next_type(self):
        self.type = self.next_type

    def on_action(self, action):
        if action == UP:
            return self.north
        if action == DOWN:
            return self.south
        if action == LEFT:
            return self.west
        if action == RIGHT:
            return self.east

        if action == WATER and self.type == BURNING_TREE:
            self.type = TREE
        if action == CUT_TREE and self.type in [TREE, BURNING_TREE]:
            self.type = EMPTY
        return self

    def __hash__(self):
        return hash((self.position, self.type))

    def __eq__(self, other):
        return (self.position, self.type) == (other.position, other.type)
