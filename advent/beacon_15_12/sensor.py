import dataclasses
import re
from functools import cached_property
from typing import Tuple

from typing_extensions import Self

SENSOR_RE = re.compile(
    r"Sensor at x=(?P<x>[-+]?[0-9]+), y=(?P<y>[-+]?[0-9]+): closest beacon is at x=(?P<beacon_x>[-+]?[0-9]+), y=(?P<beacon_y>[-+]?[0-9]+)"
)


@dataclasses.dataclass
class Sensor:
    x: int
    y: int
    closest_beacon_x: int
    closest_beacon_y: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        m = SENSOR_RE.match(s)
        groups = m.groupdict()
        return cls(
            x=int(groups["x"]),
            y=int(groups["y"]),
            closest_beacon_x=int(groups["beacon_x"]),
            closest_beacon_y=int(groups["beacon_y"]),
        )

    @cached_property
    def distance(self):
        return abs(self.x - self.closest_beacon_x) + abs(self.y - self.closest_beacon_y)

    def no_beacons_at(
        self, y: int, count_existing_beacon: bool = False
    ) -> None | Tuple[int, int]:
        dist_to_y = abs(self.y - y)
        range_radius = self.distance - dist_to_y
        if range_radius < 0:
            return None
        left = self.x - range_radius
        right = self.x + range_radius

        interval = None
        if self.closest_beacon_y != y or count_existing_beacon:
            interval = (left, right + 1)
        elif self.closest_beacon_x == left:
            interval = (left + 1, right + 1)
        elif self.closest_beacon_x == right:
            interval = (left, right)
        if interval[1] > interval[0]:
            return interval
