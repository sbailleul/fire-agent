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

