"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_buffered
"""
import arcade

# Set how many rows and columns we will have
from constants import FIELD, SPRITE_SCALING, MARGIN, WIDTH, HEIGHT, TILE_TYPE_SPRITE_DIC, AGENT_SPRITE
from environment import Environment
from tiles.tile import Tile


class FireAgentGame(arcade.Window):
    """
    Main application class.
    """

    # def loop(self):
    #     for i in range(100):
    #         j = 0
    #         while self.env.get_burning_trees() != 0:
    #             j += 1
    #             action = self.agent.best_action()
    #             # world change
    #             self.env.apply(self.agent, action)
    #         self.env.init_state(FIELD)
    #         print("Iteration : %d, tours: %d, reward : %d " % (i, j, self.agent.reward))
    #         self.agent.reset(self.env)

    def __init__(self):
        """
        Set up the application.
        """
        self.env = Environment(FIELD)
        self.agent = self.env.create_agent()
        self.screen_width = (WIDTH + MARGIN) * self.env.columns_count + MARGIN
        self.screen_height = (HEIGHT + MARGIN) * self.env.rows_count + MARGIN
        self.loop_cnt = 0
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
        self.add_tile(self.agent.last_state, AGENT_SPRITE)

    def add_tile(self, tile: Tile, sprite_path: str):
        tile_sprite = arcade.Sprite(sprite_path, SPRITE_SCALING)
        tile_sprite.center_x = (MARGIN + WIDTH) * tile.position[0] + MARGIN + WIDTH // 2
        tile_sprite.center_y = self.screen_height - ((MARGIN + HEIGHT) * tile.position[1] + MARGIN + HEIGHT // 2)
        self.sprite_list.append(tile_sprite)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()

    def on_update(self, delta_time: float):
        self.update_time_cnt += delta_time
        if self.update_time_cnt < 0.2:
            return
        self.update_time_cnt = 0

        if self.env.get_burning_trees():
            action = self.agent.best_action()
            self.env.apply(self.agent, action)
            self.recreate_grid()
            self.sprite_list.draw()
            return

        if self.loop_cnt < 100:
            self.env.init_state(FIELD)
            self.agent.reset(self.env)
            self.loop_cnt += 1


def main():
    FireAgentGame()
    arcade.run()


if __name__ == "__main__":
    main()
