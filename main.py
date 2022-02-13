"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_buffered
"""
import arcade
# Set how many rows and columns we will have
from matplotlib import pyplot as plt

from agent import Agent
from constants import FIELD, SPRITE_SCALING, MARGIN, WIDTH, HEIGHT, TILE_TYPE_SPRITE_DIC, AGENT_SPRITE, \
    ACTION_TYPE_SPRITE_DIC, AGENT_FILENAME, Y, X
from environment import Environment
from tiles.tile import Tile


class FireAgentGame(arcade.Window):
    """
    Main application class.
    """
    agent: Agent

    def __init__(self, max_iterations, is_restore=False, is_manual=False):
        """
        Set up the application.
        """
        self.is_manual = is_manual
        self.max_iterations = max_iterations
        self.env = Environment(FIELD)
        if is_restore:
            self.agent = self.env.create_agent(AGENT_FILENAME)
        else:
            self.agent = self.env.create_agent()
        self.screen_width = (WIDTH + MARGIN) * self.env.columns_count + MARGIN
        self.screen_height = (HEIGHT + MARGIN) * self.env.rows_count + MARGIN
        self.iteration = 0
        super().__init__(self.screen_width, self.screen_height, "Array Backed Grid Buffered Example")
        self.sprite_list = None
        self.update_time_cnt = 0
        arcade.set_background_color(arcade.color.BLACK)
        self.recreate_grid()

    def recreate_grid(self):
        self.sprite_list = arcade.SpriteList()
        for tile in self.env.tiles.values():
            sprite_path = TILE_TYPE_SPRITE_DIC.get(tile.type)
            self.add_tile(tile, sprite_path)
        if self.agent.last_action in ACTION_TYPE_SPRITE_DIC:
            self.add_tile(self.agent.last_state, ACTION_TYPE_SPRITE_DIC.get(self.agent.last_action))
        self.add_tile(self.agent.last_state, AGENT_SPRITE)

    def add_tile(self, tile: Tile, sprite_path: str):
        tile_sprite = arcade.Sprite(sprite_path, SPRITE_SCALING)
        tile_sprite.width = WIDTH
        tile_sprite.height = HEIGHT
        tile_sprite.center_x = (MARGIN + WIDTH) * tile.position[X] + MARGIN + WIDTH // 2
        tile_sprite.center_y = self.screen_height - ((MARGIN + HEIGHT) * tile.position[Y] + MARGIN + HEIGHT // 2)
        self.sprite_list.append(tile_sprite)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()

    def on_update(self, delta_time: float):
        if not self.is_manual:
            self.update_state()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and self.is_manual:
            self.update_state()
            # self.__agent.update_history()
            # self.__agent.reset()
            # self.__iteration += 1

    def update_state(self):
        if self.env.get_burning_trees():
            action = self.agent.best_action()
            self.env.apply(self.agent, action)
            self.recreate_grid()
            self.sprite_list.draw()
            return

        if self.iteration < self.max_iterations:
            self.env.init_state(FIELD)
            self.agent.update_history()
            self.agent.reset(self.env)
            self.iteration += 1

    def run_without_ui(self):
        for i in range(0, self.max_iterations):
            while self.env.get_burning_trees():
                action = self.agent.best_action()
                self.env.apply(self.agent, action)

            # if max(self.agent.history) == self.agent.reward:
            #     print("MAX REWARD !")
            print("Iteration : ", i, ", Score : ", self.agent.reward)

            self.env.init_state(FIELD)
            self.agent.update_history()
            self.agent.reset(self.env)


def main():
    game = FireAgentGame(100, False)
    arcade.run()
    # game.run_without_ui()
    game.agent.save(AGENT_FILENAME)
    plt.plot(game.agent.history)
    plt.show()


if __name__ == "__main__":
    main()
