from constants import START, EMPTY
from tiles.tile import Tile


class TileFactory:
    @staticmethod
    def getTile(position: tuple[int, int], type: str) -> Tile:
        return Tile(position, type if type != START else EMPTY)
