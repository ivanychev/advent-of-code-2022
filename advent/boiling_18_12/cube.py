from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from regolith_14_12.field import Point


def is_whole(x: Decimal):
    return x == int(x)


@dataclass(frozen=True, slots=True)
class Point:
    x: Decimal
    y: Decimal
    z: Decimal

    def adjacent_cubes(self) -> tuple["Cube", "Cube"]:
        if is_whole(self.x):
            return (
                Cube(
                    int(self.x),
                    int(self.y - Decimal("0.5")),
                    int(self.z - Decimal("0.5")),
                ),
                Cube(
                    int(self.x) - 1,
                    int(self.y - Decimal("0.5")),
                    int(self.z - Decimal("0.5")),
                ),
            )
        if is_whole(self.y):
            return (
                Cube(
                    int(self.x - Decimal("0.5")),
                    int(self.y),
                    int(self.z - Decimal("0.5")),
                ),
                Cube(
                    int(self.x - Decimal("0.5")),
                    int(self.y) - 1,
                    int(self.z - Decimal("0.5")),
                ),
            )
        if is_whole(self.z):
            return (
                Cube(
                    int(self.x - Decimal("0.5")),
                    int(self.y - Decimal("0.5")),
                    int(self.z),
                ),
                Cube(
                    int(self.x - Decimal("0.5")),
                    int(self.y - Decimal("0.5")),
                    int(self.z) - 1,
                ),
            )
        raise ValueError(f"Invalid side: {self}")


@dataclass(frozen=True, slots=True)
class Cube:
    x: int
    y: int
    z: int

    def side_middles(self) -> Iterable[Point]:
        return (
            Point(
                Decimal(self.x) + Decimal("0.5"),
                Decimal(self.y) + Decimal("0.5"),
                Decimal(self.z) + Decimal("1"),
            ),
            Point(
                Decimal(self.x) + Decimal("0.5"),
                Decimal(self.y) + Decimal("0.5"),
                Decimal(self.z) + Decimal("0"),
            ),
            Point(
                Decimal(self.x) + Decimal("0.5"),
                Decimal(self.y) + Decimal("1"),
                Decimal(self.z) + Decimal("0.5"),
            ),
            Point(
                Decimal(self.x) + Decimal("0.5"),
                Decimal(self.y) + Decimal("0"),
                Decimal(self.z) + Decimal("0.5"),
            ),
            Point(
                Decimal(self.x) + Decimal("1"),
                Decimal(self.y) + Decimal("0.5"),
                Decimal(self.z) + Decimal("0.5"),
            ),
            Point(
                Decimal(self.x) + Decimal("0"),
                Decimal(self.y) + Decimal("0.5"),
                Decimal(self.z) + Decimal("0.5"),
            ),
        )
