import dataclasses

from blizzard_24_12.directions import VERTICAL, Direction, Point


@dataclasses.dataclass(frozen=True, slots=True)
class Blizzard:
    field_size: int
    initial_offset: int
    initial_x: int
    initial_y: int
    direction: Direction

    def compute_changing_coord(self, initial_coord: int, time: int) -> int:
        return (
            ((initial_coord - 1) + self.direction.value[1] * time) % self.field_size
        ) + 1

    def get_coord(self, time: int) -> Point:
        if self.direction in VERTICAL:
            x = self.initial_x
            y = self.compute_changing_coord(self.initial_y, time)
        else:
            y = self.initial_y
            x = self.compute_changing_coord(self.initial_x, time)
        return Point(x, y)
