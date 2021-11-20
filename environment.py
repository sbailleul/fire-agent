from constants import *
from agent import Agent
from tiles.factory import TileFactory
from tiles.tile import Tile


class Environment:
    def __init__(self, maze: str):
        self.__tiles = {}
        lines = maze.strip().split('\n')
        lines = list(map(lambda x: x.strip(), lines))
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                added_tile = TileFactory.getTile((row, col), lines[row][col])
                self.__tiles[(row, col)] = added_tile
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
        state = self.calculate_state(action, agent)
        reward = self.calculate_reward(state)

        # Dans le cas d'une sortie de la grille du labyrinthe le nouvelle état est équivalent à l'ancien état avant sortie
        agent.update(agent.last_state if reward == REWARD_OUT else state, reward, action, LEARNING_RATE,
                     DISCOUNT_FACTOR)

    @staticmethod
    def calculate_state(action, agent) -> Tile:
        state = agent.last_state
        return state.on_action(action)



    def calculate_reward(self, state: Tile) -> float:
        destroyed_trees_this_turn = self.previous_living_trees - self.get_living_trees()
        reward = 0

        if state not in self.tiles:
            reward = REWARD_OUT
        tile = self.tiles[state.position]
        if tile.type is EMPTY:
            reward = REWARD_FLOOR
        if tile.type is WALL:
            reward = REWARD_BOUNCE

        return reward + (destroyed_trees_this_turn * REWARD_DEAD_TREE)
