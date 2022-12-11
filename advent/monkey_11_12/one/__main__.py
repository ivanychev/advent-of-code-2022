import pathlib
from heapq import nlargest

from advent.monkey_11_12.reader import read_monkeys

CURRENT_DIR = pathlib.Path(__file__).parent
ROUNDS = 20

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        ordered_monkeys = read_monkeys(
            f, worry_level_change_on_inspection=lambda worry: worry // 3
        )

        for _ in range(ROUNDS):
            for monkey in ordered_monkeys:
                monkey.inspect_items()

        registry = ordered_monkeys[0].monkey_registry
        largest_inspections = nlargest(2, (m.insected_count for m in registry.values()))
        print(largest_inspections[0] * largest_inspections[1])
