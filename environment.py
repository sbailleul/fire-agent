from copy import copy

from constants import *
from agent import Agent
from tiles.factory import TileFactory
from tiles.tile import Tile


class Environment:
    __start: Tile

    def __init__(self, maze: str):
        self.__tiles = {}
        self.previous_living_trees = 0
        self.__start = None
        self.columns_count = 0
        self.rows_count = 0
        self.init_state(maze)

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

    def create_agent(self) -> Agent:
        return Agent(self)

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
        agent.update(agent.last_state if is_out else new_state, reward, action, LEARNING_RATE,
                     DISCOUNT_FACTOR)

    @staticmethod
    def calculate_state(action, state) -> Tile:
        return state.on_action(action)

    def calculate_reward(self, state: Tile) -> (bool, float):
        reward = 0
        if state is None or state.position not in self.tiles.keys():
            return True, REWARD_OUT + self.calculate_dead_trees_reward()
        tile = self.tiles[state.position]
        if tile.type is EMPTY:
            reward = REWARD_FLOOR

        return False, reward + self.calculate_dead_trees_reward()

    def calculate_dead_trees_reward(self) -> int:
        destroyed_trees_this_turn = self.previous_living_trees - self.get_living_trees()
        return destroyed_trees_this_turn * REWARD_DEAD_TREE
