from typing import TextIO

from advent.cathode_ray_12_10.cpu import Addx, Noop
from advent.hill_12_12.height_map import HeightMap


def read_map(f: TextIO) -> HeightMap:
    rows = [row.strip() for row in f]
    return HeightMap.from_strings(rows)
