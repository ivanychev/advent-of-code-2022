import dataclasses
import enum
from typing import Iterable, NamedTuple

from typing_extensions import Self


@dataclasses.dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    def can_step_to(
        self,
        x_range_inclusive: tuple[int, int],
        y_range_inclusive: tuple[int, int],
        start: "Point",
        end: "Point",
    ) -> Iterable[Self]:
        neighbours = (
            Point(self.x, self.y - 1),
            Point(self.x, self.y + 1),
            Point(self.x - 1, self.y),
            Point(self.x + 1, self.y),
        )
        for n in neighbours:
            if (
                n == start
                or n == end
                or (
                    x_range_inclusive[0] <= n.x <= x_range_inclusive[1]
                    and y_range_inclusive[0] <= n.y <= y_range_inclusive[1]
                )
            ):
                yield n


class DirectionEntry(NamedTuple):
    index: int
    delta: int


class Direction(enum.Enum):
    UP = DirectionEntry(0, -1)
    RIGHT = DirectionEntry(1, 1)
    DOWN = DirectionEntry(2, 1)
    LEFT = DirectionEntry(3, -1)

    @staticmethod
    def render(d: "Direction") -> str:
        match d:
            case Direction.UP:
                return "^"
            case Direction.DOWN:
                return "v"
            case Direction.RIGHT:
                return ">"
            case Direction.LEFT:
                return "<"
            case invalid:
                raise ValueError()

    @classmethod
    def from_char(cls, c: str) -> Self:
        match c:
            case ">":
                return cls.RIGHT
            case "<":
                return cls.LEFT
            case "v":
                return cls.DOWN
            case "^":
                return cls.UP
            case unknown:
                raise ValueError(f"Unknown char {c}")


VERTICAL = (Direction.UP, Direction.DOWN)
HORIZONTAL = (Direction.LEFT, Direction.RIGHT)
