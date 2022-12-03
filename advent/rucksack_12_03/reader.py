from itertools import islice
from typing import TextIO

from advent.rucksack_12_03.rucksack import Rucksack, RucksackGroup


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


def read_rucksacks(f: TextIO) -> list[Rucksack]:
    return [Rucksack.from_string(line) for line in f]


def read_rucksack_groups(f: TextIO) -> list[RucksackGroup]:
    cleaned_lines = (line for line in f if line)
    return [
        RucksackGroup(
            rucksacks=(
                Rucksack.from_string(raw_group[0]),
                Rucksack.from_string(raw_group[1]),
                Rucksack.from_string(raw_group[2]),
            )
        )
        for raw_group in batched(cleaned_lines, 3)
    ]
