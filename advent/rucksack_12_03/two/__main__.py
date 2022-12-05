import pathlib

from advent.rucksack_12_03.reader import read_rucksack_groups, read_rucksacks

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        groups = read_rucksack_groups(f)
        print(sum(g.find_common_item().priority for g in groups))
