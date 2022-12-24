import pathlib

from blizzard_24_12.path import find_shortest_path
from blizzard_24_12.reader import read_blizzard_map

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        start, end, blizzard_map = read_blizzard_map(f)
        print(find_shortest_path(start, end, blizzard_map))
        # print(blizzard_map.render(0))
        # print(blizzard_map.render(1))
        # print(blizzard_map.render(2))
