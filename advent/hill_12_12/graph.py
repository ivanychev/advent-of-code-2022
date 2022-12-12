from array import array
from collections import deque
from typing import MutableSequence, NamedTuple

from typing_extensions import Self

from advent.hill_12_12.height_map import HeightMap


class Record(NamedTuple):
    x: int
    y: int
    distance: int

    def point(self):
        return (self.x, self.y)


class ReachabilityMap:
    def __init__(
        self, reachability_map: list[MutableSequence[int]], height_map: HeightMap
    ):
        self.reachability_map = reachability_map
        self.height_map = height_map

    def __str__(self):
        return "\n".join("".join(str(c) for c in row) for row in self.reachability_map)

    @classmethod
    def from_height_map(cls, height_map: HeightMap) -> Self:
        map = [array("l", [-1] * len(height_map.map[0])) for _ in height_map.map]
        visited: set[tuple[int, int]] = set()
        q: deque[Record] = deque(
            [Record(height_map.end_coord[0], height_map.end_coord[1], 0)]
        )
        while q:
            record = q.popleft()
            if (p := record.point()) in visited:
                continue
            else:
                visited.add(p)

            map[record.x][record.y] = record.distance
            for coords in height_map.adjacent_reachable_cells(record.x, record.y):
                if coords in visited:
                    continue
                q.append(Record(coords[0], coords[1], record.distance + 1))
        return cls(reachability_map=map, height_map=height_map)

    def at(self, x: int, y: int) -> int:
        return self.reachability_map[x][y]
