import dataclasses
import io
import itertools

from blizzard_24_12.blizzard import Blizzard
from blizzard_24_12.directions import HORIZONTAL, VERTICAL, Direction, Point


@dataclasses.dataclass
class BlizzardMap:
    x_to_vertical_blizzard: tuple[tuple[Blizzard]]
    y_to_horizontal_blizzard: tuple[tuple[Blizzard]]
    width: int
    height: int
    start: Point
    end: Point
    _cache: dict[tuple[Point, int]] = dataclasses.field(default_factory=dict)

    def render(self, time: int) -> str:
        buffer = io.StringIO()
        buffer.write(
            "".join(
                "." if self.start.y == idx else "#" for idx in range(self.width + 2)
            )
        )
        buffer.write("\n")
        for y in range(1, self.height + 1):
            buffer.write("#")
            for x in range(1, self.width + 1):
                buffer.write(self.render_blizzards_at(Point(x, y), time))
            buffer.write("#\n")
        buffer.write(
            "".join("." if self.end.y == idx else "#" for idx in range(self.width + 2))
        )
        buffer.write("\n")
        return buffer.getvalue()

    def is_blizzard_at(self, p: Point, time: int):
        entry = (p, time)
        if entry not in self._cache:
            horizontal = (
                blizzard.get_coord(time).x == p.x
                for blizzard in self.y_to_horizontal_blizzard[p.y]
            )
            vertical = (
                blizzard.get_coord(time).y == p.y
                for blizzard in self.x_to_vertical_blizzard[p.x]
            )
            self._cache[entry] = any(itertools.chain(horizontal, vertical))
        return self._cache[entry]

    def render_blizzards_at(self, p: Point, time: int) -> str:
        horizontal = [
            blizzard
            for blizzard in self.y_to_horizontal_blizzard[p.y]
            if blizzard.get_coord(time).x == p.x
        ]
        vertical = [
            blizzard
            for blizzard in self.x_to_vertical_blizzard[p.x]
            if blizzard.get_coord(time).y == p.y
        ]
        if len(horizontal) + len(vertical) > 1:
            return str(len(horizontal) + len(vertical))[-1]
        elif len(horizontal) + len(vertical) == 1:
            blizzard = (horizontal + vertical)[0]
            return Direction.render(blizzard.direction)
        return "."


def read_blizzards(
    rows: list[str],
) -> tuple[tuple[tuple[Blizzard, ...], ...], tuple[tuple[Blizzard, ...], ...]]:
    field_height = len(rows) - 2
    field_width = len(rows[0]) - 2
    x_to_vertical_blizzard: list[list[Blizzard]] = [[] for _ in range(field_width + 2)]
    y_to_horizontal_blizzard: list[list[Blizzard]] = [
        [] for _ in range(field_height + 2)
    ]

    for y in range(1, field_height + 1):
        for x in range(1, field_width + 1):
            c = rows[y][x]
            if c == ".":
                continue
            direction = Direction.from_char(c)
            if direction in VERTICAL:
                x_to_vertical_blizzard[x].append(
                    Blizzard(
                        field_size=field_height,
                        initial_offset=(y - 1)
                        if direction == Direction.DOWN
                        else (field_width - y),
                        initial_x=x,
                        initial_y=y,
                        direction=direction,
                    )
                )
            elif direction in HORIZONTAL:
                y_to_horizontal_blizzard[y].append(
                    Blizzard(
                        field_size=field_width,
                        initial_offset=(x - 1)
                        if direction == Direction.RIGHT
                        else (field_width - x),
                        initial_x=x,
                        initial_y=y,
                        direction=direction,
                    )
                )
            else:
                raise ValueError(f"Unknown direction {direction}")
    return tuple(tuple(l) for l in x_to_vertical_blizzard), tuple(
        tuple(l) for l in y_to_horizontal_blizzard
    )
