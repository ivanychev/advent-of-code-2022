import dataclasses
import enum
from typing import Iterable

from typing_extensions import Self


class Direction(enum.Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


VERTICAL_DIRECTIONS = (Direction.NORTH, Direction.SOUTH)

HORIZONTAL_DIRECTIONS = (Direction.EAST, Direction.WEST)


@dataclasses.dataclass(slots=True, frozen=True)
class Point:
    x: int
    y: int

    def to_north(self) -> Self:
        return dataclasses.replace(self, y=self.y - 1)

    def to_south(self) -> Self:
        return dataclasses.replace(self, y=self.y + 1)

    def to_east(self) -> Self:
        return dataclasses.replace(self, x=self.x + 1)

    def to_west(self) -> Self:
        return dataclasses.replace(self, x=self.x - 1)

    def adjacent_to_direction(self, direction: Direction) -> Iterable[Self]:
        match direction:
            case vertical if vertical in VERTICAL_DIRECTIONS:
                opposite_direction = HORIZONTAL_DIRECTIONS
            case horizontal if horizontal in HORIZONTAL_DIRECTIONS:
                opposite_direction = VERTICAL_DIRECTIONS
            case unknown:
                raise ValueError(f"Unknown direction {unknown}")

        to_direction = self.to_direction(direction)
        yield to_direction
        for d in opposite_direction:
            yield to_direction.to_direction(d)

    def to_direction(self, direction: Direction) -> Self:
        match direction:
            case Direction.NORTH:
                return self.to_north()
            case Direction.SOUTH:
                return self.to_south()
            case Direction.EAST:
                return self.to_east()
            case Direction.WEST:
                return self.to_west()
            case unknown:
                raise ValueError(f"Unknown direction: {unknown}")
