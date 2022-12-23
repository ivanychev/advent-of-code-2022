import dataclasses
import io
import itertools
from typing import Iterable, TextIO

from advent.unstable_diffusion_23_12.point import Direction, Point

GROUND = "."
ELF = "#"


@dataclasses.dataclass(slots=True, frozen=True)
class Elf:
    index: int
    pos: Point

    def propose(self, map: "ElfMap", directions_to_check: Iterable[Direction]) -> Point:
        all_adjacent_points = itertools.chain(
            self.pos.adjacent_to_direction(Direction.NORTH),
            self.pos.adjacent_to_direction(Direction.SOUTH),
            (self.pos.to_east(), self.pos.to_west()),
        )
        if not map.any_occupied(all_adjacent_points):
            return self.pos
        for direction in directions_to_check:
            if not map.any_occupied(self.pos.adjacent_to_direction(direction)):
                return self.pos.to_direction(direction)
        return self.pos


@dataclasses.dataclass(slots=True)
class ElfMap:
    pos_to_item: dict[Point, Elf | None]

    def any_occupied(self, points: Iterable[Point]) -> bool:
        return any(self.pos_to_item.get(p) for p in points)

    def max_min_x_y(self) -> tuple[int, int, int, int]:
        max_x = max(p.x for p in self.pos_to_item)
        min_x = min(p.x for p in self.pos_to_item)
        max_y = max(p.y for p in self.pos_to_item)
        min_y = min(p.y for p in self.pos_to_item)

        return min_x, max_x, min_y, max_y

    def iterate_rectangular(self) -> Iterable[Point]:
        min_x, max_x, min_y, max_y = self.max_min_x_y()

        for y, x in itertools.product(range(min_y, max_y + 1), range(min_x, max_x + 1)):
            yield Point(x, y)

    def empty_tiles(self) -> int:
        min_x, max_x, min_y, max_y = self.max_min_x_y()
        total = (max_x - min_x + 1) * (max_y - min_y + 1)
        occupied = len(self.pos_to_item)
        return total - occupied

    def render(self) -> str:
        buffer = io.StringIO()
        prev_y = None
        for p in self.iterate_rectangular():
            if prev_y is not None and p.y != prev_y:
                buffer.write("\n")
            prev_y = p.y
            buffer.write("." if not self.pos_to_item.get(p) else "#")
        buffer.write("\n")
        return buffer.getvalue()


def read_ground(f: TextIO) -> tuple[list[Elf], ElfMap]:
    max_y = 0
    max_x = 0
    elfs = []
    pos_to_item = {}
    for y, row in enumerate(f):
        max_y = max(y, max_y)
        row: str = row.strip()

        for x, elem in enumerate(row):
            max_x = max(x, max_x)
            point = Point(x, y)
            if elem == "#":
                elfs.append(Elf(index=len(elfs), pos=point))
                pos_to_item[point] = elfs[-1]

    return elfs, ElfMap(pos_to_item)
