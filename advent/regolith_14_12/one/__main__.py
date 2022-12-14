import pathlib

from advent.regolith_14_12.reader import read_rocks

CURRENT_DIR = pathlib.Path(__file__).parent

DROP_POINT = (500, 0)

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        rock_field = read_rocks(f)
        dropped = 0
        while True:
            is_dropped = rock_field.drop_sand((500, 0))
            if not is_dropped:
                break
            else:
                dropped += 1
        print(dropped)
