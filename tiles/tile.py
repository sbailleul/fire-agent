from __future__ import annotations

import random

import constants
from constants import *


class Tile:
    south: Tile | None
    north: Tile | None
    east: Tile | None
    west: Tile | None
    north_west: Tile | None
    south_west: Tile | None
    north_east: Tile | None
    south_east: Tile | None
    existing_neighbors: list[Tile]
    next_type: str | None
    position: tuple[int, int]
    type: str

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
        self.south = None
        self.north = None
        self.east = None
        self.west = None
        self.north_west = None
        self.south_west = None
        self.north_east = None
        self.south_east = None
        self.existing_neighbors = []
        self.next_type = None

    def set_neighbors(self, all_tiles: dict[tuple[int, int], Tile]):
        self.south = all_tiles.get((self.position[X], self.position[Y] + 1))
        self.north = all_tiles.get((self.position[X], self.position[Y] - 1))
        self.east = all_tiles.get((self.position[X] + 1, self.position[Y]))
        self.west = all_tiles.get((self.position[X] - 1, self.position[Y]))
        self.north_west = all_tiles.get((self.position[X] - 1, self.position[Y] - 1))
        self.south_west = all_tiles.get((self.position[X] - 1, self.position[Y] + 1))
        self.north_east = all_tiles.get((self.position[X] + 1, self.position[Y] - 1))
        self.south_east = all_tiles.get((self.position[X] + 1, self.position[Y] + 1))
        self.set_existing_neigbors()

    @property
    def neighbors(self) -> list[Tile | None]:
        return [self.south, self.north, self.west, self.east, self.south_east, self.south_west,
                self.north_east, self.north_west]

    def set_existing_neigbors(self):
        self.existing_neighbors = [neighbor for neighbor in self.neighbors if neighbor]

    def get_neighbors_types(self) -> list[str]:
        return [neighbor.type for neighbor in self.existing_neighbors]

    @property
    def to_vector(self) -> list[int]:
        resumes = [self.position[X], self.position[Y], STATES.index(self.type)]
        for neighbor in self.neighbors:
            if neighbor is not None:
                resumes.append(STATES.index(neighbor.type))
            else:
                resumes.append(0)
        return resumes

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
                return

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
