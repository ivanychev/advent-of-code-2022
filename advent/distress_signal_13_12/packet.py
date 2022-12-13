import dataclasses
import json
from itertools import zip_longest
from typing import TypeVar

PacketListItem = TypeVar("PacketListItem")


def compare_ordering(left: list, right: list) -> bool | None:
    for left_x, right_x in zip_longest(left, right):
        if left_x is None:
            return True
        if right_x is None:
            return False
        if isinstance(left_x, int) and isinstance(right_x, int):
            if left_x < right_x:
                return True
            if left_x > right_x:
                return False
        if (
            isinstance(left_x, int)
            and isinstance(right_x, list)
            or isinstance(left_x, list)
            and isinstance(right_x, int)
        ):
            left_x = [left_x] if isinstance(left_x, int) else left_x
            right_x = [right_x] if isinstance(right_x, int) else right_x
        if isinstance(left_x, list) and isinstance(right_x, list):
            ordering = compare_ordering(left_x, right_x)
            if isinstance(ordering, bool):
                return ordering


def _cast_int_recursive(l: list) -> list:
    return [
        round(x) if isinstance(x, (int, float)) else _cast_int_recursive(x) for x in l
    ]


@dataclasses.dataclass
class Packet:
    values: list

    @classmethod
    def parse_from_strint(cls, s: str):
        return cls(_cast_int_recursive(json.loads(s)))

    def equals_to_values(self, values: list):
        return self.values == values

    def __lt__(self, other):
        return compare_ordering(self.values, other.values) == True

    def __le__(self, other):
        return compare_ordering(self.values, other.values) in (True, None)

    def __eq__(self, other):
        return compare_ordering(self.values, other.values) is None

    def __gt__(self, other):
        return compare_ordering(self.values, other.values) == False

    def __ge__(self, other):
        return compare_ordering(self.values, other.values) in (False, None)
