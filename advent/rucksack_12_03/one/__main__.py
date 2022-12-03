import pathlib

from advent.rucksack_12_03.reader import read_rucksacks

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        rucksacks = read_rucksacks(f)
        print(sum(r.first_common_element().priority for r in rucksacks))
