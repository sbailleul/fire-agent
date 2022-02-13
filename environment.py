from copy import copy

from agent import Agent
from constants import *
from tiles.factory import TileFactory
from tiles.tile import Tile


class Environment:
    __start: Tile
    columns_count: int
    rows_count: int

    def __init__(self, maze: str):
        self.__tiles = {}
        self.previous_living_trees = 0
        self.__start = None
        self.columns_count = 0
        self.rows_count = 0
        self.init_state(maze)
        self.learning_rate = LEARNING_RATE
        self.discount_factor = DISCOUNT_FACTOR

    def init_state(self, maze):
        lines = maze.strip().split('\n')
        lines = list(map(lambda x: x.strip(), lines))
        self.columns_count = len(lines[0]) - 2
        self.rows_count = len(lines) - 2
        for row in range(1, len(lines) - 1):
            for col in range(1, len(lines[row]) - 1):
                added_tile = TileFactory.getTile((col - 1, row - 1), lines[row][col])
                self.__tiles[(col - 1, row - 1)] = added_tile
                if lines[row][col] == START:
                    self.__start = added_tile
        for tile in self.__tiles.values():
            tile.set_neighbors(self.__tiles)
        self.previous_living_trees = self.get_living_trees()

    @property
    def start(self) -> Tile:
        return self.__start

    @property
    def tiles(self) -> dict[tuple[int, int], Tile]:
        return self.__tiles

    def create_agent(self, previous_state_file=None) -> Agent:
        return Agent(self, previous_state_file)

    def get_living_trees(self):
        counter = 0
        for tile in self.__tiles.values():
            if tile.type == TREE:
                counter += 1

        return counter

    def get_burning_trees(self):
        counter = 0
        for tile in self.__tiles.values():
            if tile.type == BURNING_TREE:
                counter += 1

        return counter

    def get_fire_direction_from_tile(self, check_tile: Tile) -> list[int]:
        min_dist_tile = self.get_min_fire_tile_dist(check_tile)
        min_dist_tile = check_tile if min_dist_tile is None else min_dist_tile
        return [min_dist_tile.position[X] - check_tile.position[X], min_dist_tile.position[Y] - check_tile.position[Y]]

    def get_min_fire_tile_dist(self, check_tile):
        min_dist_tile = None
        min_dist = self.columns_count + self.rows_count
        for tile in self.tiles.values():
            if tile.type == BURNING_TREE:
                dist = self.get_tile_dist(check_tile, tile)
                if dist < min_dist:
                    min_dist_tile = tile
                    min_dist = dist
        return min_dist_tile

    @staticmethod
    def get_tile_dist(check_tile: Tile, tile: Tile):
        return abs(tile.position[X] - check_tile.position[X]) + abs(tile.position[Y] - check_tile.position[Y])

    def apply(self, agent: Agent, action: str):
        new_state = agent.last_state
        agent.last_state = copy(agent.last_state)
        new_state = self.calculate_state(action, new_state)
        (is_out, reward) = self.calculate_reward(new_state)

        for tile in self.tiles.values():
            tile.on_new_turn()
        for tile in self.tiles.values():
            tile.apply_next_type()
        # Dans le cas d'une sortie de la grille du labyrinthe le nouvelle état est équivalent à l'ancien état avant sortie
        agent.update(agent.last_state if is_out else new_state, reward, action)

    @staticmethod
    def calculate_state(action, state) -> Tile:
        return state.on_action(action)

    def calculate_reward(self, new_state: Tile) -> (bool, float):
        reward = 0
        if new_state is None or new_state.position not in self.tiles.keys():
            return True, REWARD_OUT + self.calculate_dead_trees_reward()
        tile = self.tiles[new_state.position]
        if tile.type is EMPTY:
            reward = REWARD_FLOOR
        return False, reward + self.calculate_dead_trees_reward() + self.calculate_fire_dist_reward(new_state)

    def calculate_fire_dist_reward(self, new_state: Tile) -> float:
        # nearest_burning_tile = self.get_min_fire_tile_dist(new_state)
        # if nearest_burning_tile:
        #     dist = self.get_tile_dist(nearest_burning_tile, new_state)
        #     reward = REWARD_BURNING_TREE_DIST if dist == 0 else REWARD_BURNING_TREE_DIST / dist
        #     return reward
        return 0

    def calculate_dead_trees_reward(self) -> int:
        destroyed_trees_this_turn = self.previous_living_trees - self.get_living_trees()
        if destroyed_trees_this_turn > 0:
            print("Diff destroyed trees", destroyed_trees_this_turn, "new turn", self.get_living_trees(), "old turn",
                  self.previous_living_trees)
        self.previous_living_trees = self.get_living_trees()

        return destroyed_trees_this_turn * REWARD_DEAD_TREE
