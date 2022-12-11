import pathlib
from heapq import nlargest
from math import lcm

from tqdm import tqdm

from advent.monkey_11_12.reader import read_monkeys

CURRENT_DIR = pathlib.Path(__file__).parent
ROUNDS = 10000

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        ordered_monkeys = read_monkeys(
            f, worry_level_change_on_inspection=lambda worry: worry
        )
        worry_mod = lcm(*[m.test_divisible_by for m in ordered_monkeys])
        for m in ordered_monkeys:
            m.set_worry_level_change_on_inspection(lambda worry: worry % worry_mod)

        for _ in tqdm(range(ROUNDS)):
            for monkey in ordered_monkeys:
                monkey.inspect_items()

        registry = ordered_monkeys[0].monkey_registry
        largest_inspections = nlargest(2, (m.insected_count for m in registry.values()))
        print(largest_inspections[0] * largest_inspections[1])
