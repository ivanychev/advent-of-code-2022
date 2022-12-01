from functools import cached_property
from typing import NamedTuple, TextIO, Iterable
from typing_extensions import Self


class ElfInventory(NamedTuple):
    items: tuple[int, ...]

    @classmethod
    def from_inventory_string(cls, s: str) -> Self:
        calories = tuple(int(x) for x in s.split("\n"))
        return cls(calories)

    @property
    def sum_calories(self) -> int:
        return sum(self.items)


def _read_elves_gen(f: TextIO) -> Iterable[ElfInventory]:
    current_inventory = []
    for line in f:
        line = line.rstrip("\n")
        if line:
            current_inventory.append(int(line.strip()))
        else:
            yield ElfInventory(tuple(current_inventory))
            current_inventory.clear()
    if current_inventory:
        yield ElfInventory(tuple(current_inventory))


def read_elves(f: TextIO) -> list[ElfInventory]:
    return list(_read_elves_gen(f))
