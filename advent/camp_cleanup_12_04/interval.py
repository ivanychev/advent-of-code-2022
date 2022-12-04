from operator import attrgetter
from typing import NamedTuple
from typing_extensions import Self


class Interval(NamedTuple):
    start_inclusive: int
    end_exclusive: int

    def __len__(self):
        if not self.end_exclusive >= self.start_inclusive:
            raise ValueError(self.start_inclusive, self.end_exclusive)
        return self.end_exclusive - self.start_inclusive

    @classmethod
    def from_string(cls, s: str) -> Self:
        first, second = s.strip().split("-")
        return cls(start_inclusive=int(first), end_exclusive=int(second) + 1)

    def intersection_with(self, other: Self) -> int:
        first, second = self, other
        first, second = sorted([first, second], key=attrgetter("start_inclusive"))
        if second.start_inclusive >= first.end_exclusive:
            return 0
        return min(first.end_exclusive, second.end_exclusive) - second.start_inclusive


class IntervalPair(NamedTuple):
    first: Interval
    second: Interval

    @classmethod
    def from_string(cls, s: str) -> Self:
        # 20-40,21-58
        first_raw, second_raw = s.strip().split(",")
        return cls(
            first=Interval.from_string(first_raw),
            second=Interval.from_string(second_raw),
        )

    def fully_intersect(self) -> bool:
        return self.first.intersection_with(self.second) == min(
            len(self.first), len(self.second)
        )

    def intersect(self) -> bool:
        return bool(self.first.intersection_with(self.second))


if __name__ == "__main__":
    assert Interval(0, 4).intersection_with(Interval(2, 10)) == 2
    assert Interval(2, 10).intersection_with(Interval(0, 4)) == 2
    assert Interval(0, 4).intersection_with(Interval(4, 6)) == 0
    assert Interval(0, 4).intersection_with(Interval(5, 6)) == 0
    assert Interval(0, 3).intersection_with(Interval(1, 2)) == 1
