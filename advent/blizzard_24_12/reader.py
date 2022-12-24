from typing import TextIO

from blizzard_24_12.blizzard_map import BlizzardMap, read_blizzards
from blizzard_24_12.directions import Point


def read_blizzard_map(f: TextIO) -> tuple[Point, Point, BlizzardMap]:
    rows = [row.strip() for row in f]
    start_y = 0
    start_x = rows[0].index(".")
    end_y = len(rows) - 1
    end_x = rows[end_y].index(".")

    x_to_vertical_blizzard, y_to_horizontal_blizzard = read_blizzards(rows)

    start = Point(start_x, start_y)
    end = Point(end_x, end_y)
    blizzard_map = BlizzardMap(
        x_to_vertical_blizzard=x_to_vertical_blizzard,
        y_to_horizontal_blizzard=y_to_horizontal_blizzard,
        width=len(rows[0]) - 2,
        height=len(rows) - 2,
        start=start,
        end=end,
    )

    return start, end, blizzard_map
