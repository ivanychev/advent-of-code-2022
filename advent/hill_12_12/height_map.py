import dataclasses
from array import array
from typing import Iterable, MutableSequence, Sequence

from typing_extensions import Self

START = "S"
END = "E"


def _get_elevation_from_char(c: str) -> int:
    if c == START:
        return 0
    if c == END:
        return ord("z") - ord("a")
    return ord(c) - ord("a")


@dataclasses.dataclass(frozen=True)
class HeightMap:
    start_coord: tuple[int, int]
    end_coord: tuple[int, int]
    map: MutableSequence[MutableSequence[int]]

    @classmethod
    def from_strings(cls, map_rows: Sequence[str]) -> Self:
        start_coord = None
        end_coord = None
        height_map = []
        for x in range(len(map_rows)):
            height_map.append(array("b", [0] * len(map_rows[0])))
            for y in range(len(map_rows[0])):
                c = map_rows[x][y]
                if c == START:
                    start_coord = (x, y)
                elif c == END:
                    end_coord = (x, y)
                height_map[x][y] = _get_elevation_from_char(c)
        if start_coord is None:
            raise ValueError("Start coord is not provided")
        if end_coord is None:
            raise ValueError("End coord is not provided")
        return cls(start_coord=start_coord, end_coord=end_coord, map=height_map)

    def adjacent_cells(self, x: int, y: int) -> Iterable[tuple[int, int]]:
        for delta in (1, -1):
            if self._in_map(x + delta, y):
                yield (x + delta, y)
            if self._in_map(x, y + delta):
                yield (x, y + delta)

    def adjacent_reachable_cells(self, x: int, y: int) -> Iterable[tuple[int, int]]:
        old_height = self.map[x][y]
        for x_new, y_new in self.adjacent_cells(x, y):
            new_height = self.map[x_new][y_new]
            if new_height - old_height >= -1:
                yield x_new, y_new

    def zero_height_cells(self) -> Iterable[tuple[int, int]]:
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if not self.map[x][y]:
                    yield x, y

    def _in_map(self, x: int, y: int) -> bool:
        return 0 <= x < len(self.map) and 0 <= y < len(self.map[0])
