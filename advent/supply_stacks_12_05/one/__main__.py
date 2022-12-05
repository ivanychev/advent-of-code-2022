import pathlib

from advent.supply_stacks_12_05.move import Move
from advent.supply_stacks_12_05.reader import read_crates

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        storage, moves = read_crates(f)
        for m in moves:
            storage.make_move(m)
        print("".join(storage.top(l) for l in storage.get_sorted_labels()))
