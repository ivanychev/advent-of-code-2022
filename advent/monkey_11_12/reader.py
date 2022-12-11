from itertools import islice
from operator import attrgetter
from typing import Callable, TextIO

from advent.monkey_11_12.monkey import Monkey


def read_monkeys(
    f: TextIO, worry_level_change_on_inspection: Callable[[int], int]
) -> list[Monkey]:
    non_empty_lines = (line.strip() for line in f if line != "\n")
    monkeys = []
    monkey_registry = {}
    while monkey_input := list(islice(non_empty_lines, 6)):
        monkeys.append(
            Monkey.read_from_raw_strings(
                monkey_input,
                monkey_registry,
                worry_level_change_on_inspection=worry_level_change_on_inspection,
            )
        )

    for m in monkeys:
        monkey_registry[m.index] = m
    return sorted(monkeys, key=attrgetter("index"))
