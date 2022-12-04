import pathlib

from advent.camp_cleanup_12_04.reader import read_interval_pairs

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        interval_pairs = read_interval_pairs(f)
        print(sum(1 if p.intersect() else 0 for p in interval_pairs))
