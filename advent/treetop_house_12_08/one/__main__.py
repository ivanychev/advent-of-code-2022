import pathlib
from pprint import pprint

from advent.treetop_house_12_08.reader import read_grid
from advent.treetop_house_12_08.visibility import VisibilityMap

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        grid = read_grid(f)
        visibility_map = VisibilityMap.make_for_grid(grid)
        print(visibility_map.visible_count())
