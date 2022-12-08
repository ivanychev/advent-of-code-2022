import pathlib

from advent.treetop_house_12_08.reader import read_grid
from advent.treetop_house_12_08.scenic import ScenicGrid

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        grid = read_grid(f)
        g = ScenicGrid.make_for_grid(grid)
        print(g.highest_scenic_score())
