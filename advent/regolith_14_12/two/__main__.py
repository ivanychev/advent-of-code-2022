import pathlib

from advent.regolith_14_12.reader import read_rocks

CURRENT_DIR = pathlib.Path(__file__).parent

DROP_POINT = (500, 0)

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        rock_field = read_rocks(f)

        highest_y = max(y for (_, y) in rock_field.field)
        rock_field.set_floor(highest_y + 2)
        dropped = 0
        while True:
            rock_field.drop_sand(DROP_POINT)
            dropped += 1
            if rock_field._is_solid_point(DROP_POINT):
                break
        print(dropped)
