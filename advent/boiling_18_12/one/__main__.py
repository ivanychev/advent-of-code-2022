import pathlib
from collections import Counter

from boiling_18_12.reader import read_cubes

CURRENT_DIR = pathlib.Path(__file__).parent

Y = 2000000

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        cubes = read_cubes(f)
        c = Counter()

        for cube in cubes:
            c.update(cube.side_middles())
        space = sum(1 for value in c.values() if value == 1)
        print(space)
