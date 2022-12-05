from functools import reduce
from itertools import chain
from typing import FrozenSet, NamedTuple, Tuple

from typing_extensions import Self


class Item(NamedTuple):
    value: str

    @property
    def priority(self) -> int:
        if "a" <= self.value <= "z":
            return ord(self.value) - ord("a") + 1
        if "A" <= self.value <= "Z":
            return ord(self.value) - ord("A") + 27
        raise ValueError(f"Invalid item {self.value}")


class Rucksack(NamedTuple):
    first_compartment: Tuple[Item, ...]
    second_compartment: Tuple[Item, ...]

    def itemset(self) -> FrozenSet:
        return frozenset(
            x for x in chain(self.first_compartment, self.second_compartment)
        )

    def first_common_element(self) -> Item:
        diff = set(self.first_compartment).intersection(set(self.second_compartment))
        return next(iter(diff))

    @classmethod
    def from_string(cls, s: str) -> Self:
        s = s.strip()
        first, second = s[: len(s) // 2], s[len(s) // 2 :]
        return cls(
            first_compartment=tuple(Item(x) for x in first),
            second_compartment=tuple(Item(x) for x in second),
        )


class RucksackGroup(NamedTuple):
    rucksacks: Tuple[Rucksack, ...]

    def find_common_item(self) -> Item:
        common_items = reduce(
            lambda x, y: x.intersection(y), (x.itemset() for x in self.rucksacks)
        )

        return next(iter(common_items))


if __name__ == "__main__":
    g1 = RucksackGroup(
        rucksacks=(
            Rucksack.from_string("vJrwpWtwJgWrhcsFMMfFFhFp"),
            Rucksack.from_string("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
            Rucksack.from_string("PmmdzqPrVvPwwTWBwg"),
        )
    )
    g2 = RucksackGroup(
        rucksacks=(
            Rucksack.from_string("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
            Rucksack.from_string("ttgJtRGJQctTZtZT"),
            Rucksack.from_string("CrZsJsPPZsGzwwsLwLmpwMDw"),
        )
    )
    print(g1.find_common_item().priority + g2.find_common_item().priority)
