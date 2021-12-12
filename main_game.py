"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_buffered
"""
import arcade

# Set how many rows and columns we will have
from constants import FIELD, SPRITE_SCALING, MARGIN, WIDTH, HEIGHT
from environment import Environment


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def loop(self):
        for i in range(100):
            j = 0
            while self.env.get_burning_trees() != 0:
                j += 1
                action = self.agent.best_action()
                # world change
                self.env.apply(self.agent, action)
            self.env.init_state(FIELD)
            print("Iteration : %d, tours: %d, reward : %d " % (i, j, self.agent.reward))
            self.agent.reset(self.env)

    def __init__(self):
        """
        Set up the application.
        """
        self.env = Environment(FIELD)
        self.agent = self.env.create_agent()
        screen_width = (WIDTH + MARGIN) * self.env.columns_count + MARGIN
        screen_height = (HEIGHT + MARGIN) * self.env.rows_count + MARGIN

        super().__init__(screen_width, screen_height, "Array Backed Grid Buffered Example")

        self.sprite_list = None
        arcade.set_background_color(arcade.color.BLACK)
        self.recreate_grid()

    def recreate_grid(self):
        self.sprite_list = arcade.SpriteList()
        for tile in self.env.tiles.values():
            tile_sprite = arcade.Sprite(":resources:images/topdown_tanks/treeGreen_small.png", SPRITE_SCALING)
            tile_sprite.center_x = (MARGIN + WIDTH) * tile.position[0] + MARGIN + WIDTH // 2
            tile_sprite.center_y = (MARGIN + HEIGHT) * tile.position[1] + MARGIN + HEIGHT // 2

            self.sprite_list.append(tile_sprite)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
