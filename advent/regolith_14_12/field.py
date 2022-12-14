import dataclasses
import io
from collections import defaultdict

from more_itertools import sliding_window
from sortedcontainers import SortedSet

from advent.regolith_14_12.formation import SOLID_FORMATIONS, Formation

Point = tuple[int, int]


@dataclasses.dataclass
class RockField:
    field: dict[Point, Formation] = dataclasses.field(default_factory=dict)
    x_to_formations: defaultdict[int, SortedSet[Point]] = dataclasses.field(
        default_factory=lambda: defaultdict(SortedSet)
    )
    floor: int | None = None

    def _set_formation(self, x: int, y: int, formation: Formation):
        point = (x, y)
        self.field[point] = formation
        self.x_to_formations[x].add(point)

    def _set_formation_interval(
        self, from_point: Point, to_point: Point, formation: Formation
    ):
        x_min, x_max = sorted([from_point[0], to_point[0]])
        y_min, y_max = sorted([from_point[1], to_point[1]])
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                self._set_formation(x, y, formation)

    def fill_rock_from_traces(self, traces: list[str]):
        for trace in traces:
            points = (
                tuple(int(x) for x in raw_point.split(",", maxsplit=1))
                for raw_point in trace.split(" -> ")
            )
            for from_point, to_point in sliding_window(points, 2):
                self._set_formation_interval(from_point, to_point, Formation.ROCK)

    def drop_sand(self, point: Point) -> bool:
        next_point = self._next_point_for_sand(point)
        if next_point is None:
            return False
        self._set_formation(next_point[0], next_point[1], Formation.SAND)
        return True

    def _next_point_for_sand(self, point: Point):
        current = point
        while True:
            next_solid_point = self._get_next_solid_point(current)
            if next_solid_point is None:
                return None
            just_above_next_solid_point = (next_solid_point[0], next_solid_point[1] - 1)
            left_down = (
                just_above_next_solid_point[0] - 1,
                just_above_next_solid_point[1] + 1,
            )
            right_down = (
                just_above_next_solid_point[0] + 1,
                just_above_next_solid_point[1] + 1,
            )
            if not self._is_solid_point(left_down):
                current = left_down
                continue
            elif not self._is_solid_point(right_down):
                current = right_down
                continue
            else:
                return just_above_next_solid_point

    def _get_next_solid_point(self, point: Point):
        x_sorted_formations = self.x_to_formations[point[0]]
        next_solid_point_idx = x_sorted_formations.bisect_left(point)
        if next_solid_point_idx == len(x_sorted_formations) and self.floor is None:
            # Nothing below.
            return None
        elif next_solid_point_idx == len(x_sorted_formations):
            return (point[0], self.floor)
        else:
            next_solid_point = list(
                x_sorted_formations.islice(
                    next_solid_point_idx, next_solid_point_idx + 1
                )
            )[0]
            return next_solid_point

    def _is_solid_point(self, point: Point):
        if self.floor and point[1] >= self.floor:
            return True
        formation = self.field.get(point, Formation.AIR)
        return formation in SOLID_FORMATIONS

    def draw(self, from_point: Point, to_point: Point, with_drop_point: Point):
        string_buf = io.StringIO()
        for y in range(from_point[1], to_point[1] + 1):
            for x in range(from_point[0], to_point[0] + 1):
                formation = self.field.get((x, y), Formation.AIR)
                if (x, y) == with_drop_point:
                    formation = Formation.DROP_POINT
                elif self.floor is not None and y >= self.floor:
                    formation = Formation.ROCK
                string_buf.write(formation.value)
            string_buf.write("\n")
        return string_buf.getvalue()

    def set_floor(self, y: int):
        self.floor = y
