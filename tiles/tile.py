import random

import constants
from constants import *


class Tile:

    def __copy__(self):
        tile = Tile(self.position, tile_type=self.type)
        tile.north = self.north
        tile.south = self.south
        tile.east = self.east
        tile.west = self.west
        tile.position = self.position
        tile.north_east = self.north_east
        tile.north_west = self.north_west
        tile.south_west = self.south_west
        tile.south_east = self.south_east
        tile.set_existing_neigbors()
        return tile

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
        self.existing_neighbors = []
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
        self.set_existing_neigbors()

    def set_existing_neigbors(self):
        self.existing_neighbors = [neighbor for neighbor in
                                   [self.south, self.north, self.west, self.east, self.south_east, self.south_west,
                                    self.north_east, self.north_west] if neighbor]

    def get_neighbors_types(self) -> list[str]:
        return [neighbor.type for neighbor in self.existing_neighbors]

    def get_neigbors_hashes(self) -> list[int]:
        return [hash((neighbor.position, neighbor.type)) for neighbor in self.existing_neighbors]

    def on_new_turn(self):
        random_value = random.random()
        if self.type not in [BURNING_TREE, TREE]:
            self.next_type = self.type
            return
        if self.type == BURNING_TREE and random_value < constants.EXPIRE_PROBABILITY:
            self.next_type = EMPTY
            return
        if BURNING_TREE in self.get_neighbors_types():
            if random_value < constants.BURN_PROBABILITY:
                self.next_type = BURNING_TREE
            else :
                self.next_type = self.type

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
        return hash((self.position, self.type, *self.get_neigbors_hashes()))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
