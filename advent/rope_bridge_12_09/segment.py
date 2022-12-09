from math import dist

from typing_extensions import Self

from advent.rope_bridge_12_09.motion import Motion

EPS = 0.000000001
DIAG_LENGTH = dist((0, 0), (1, 1))
DIRECT_DIAG_2 = dist((0, 0), (1, 2))
DIRECT_DIRECT_2 = dist((0, 0), (2, 0))
DIAG_DIAG_2 = dist((0, 0), (2, 2))


def _approx_eq(x: float, y: float) -> bool:
    return abs(x - y) <= EPS


# 6243
class Segment:
    def __init__(self, child: Self | None = None):
        self.x = 0
        self.y = 0
        self.visited_set: set[tuple[int, int]] = {(self.x, self.y)}
        self.child: Self | None = child

    @classmethod
    def build_rope(cls, length: int) -> Self:
        current = cls()
        for _ in range(length - 1):
            next = cls(child=current)
            current = next
        return current

    def get_tail_set(self) -> set[tuple[int, int]]:
        return self.visited_set if not self.child else self.child.get_tail_set()

    def set_coords(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited_set.add((x, y))

    def move(self, m: Motion):
        delta_x, delta_y = m.direction.to_coord_delta()
        for _ in range(m.steps):
            self.set_coords(
                x=self.x + delta_x,
                y=self.y + delta_y,
            )
            if self.child:
                self.child.follow(self)

    def _transform_diag_2_coord(self, x: int, parent_x: int) -> int:
        if abs(x - parent_x) == 1:
            return parent_x
        return (x + parent_x) // 2

    def _transform_direct_2_coord(self, x: int, parent_x: int) -> int:
        return (x + parent_x) // 2

    def _child_follow_me(self):
        if self.child:
            self.child.follow(self)

    def follow(self, segment: Self):
        distance = dist((self.x, self.y), (segment.x, segment.y))
        if distance <= DIAG_LENGTH:
            return
        if _approx_eq(distance, DIRECT_DIRECT_2) or _approx_eq(distance, DIAG_DIAG_2):
            self.set_coords(
                x=self._transform_direct_2_coord(self.x, segment.x),
                y=self._transform_direct_2_coord(self.y, segment.y),
            )
            return self._child_follow_me()
        if _approx_eq(distance, DIRECT_DIAG_2):
            self.set_coords(
                x=self._transform_diag_2_coord(self.x, segment.x),
                y=self._transform_diag_2_coord(self.y, segment.y),
            )
            return self._child_follow_me()
        raise ValueError(
            f"Unexpected move, me: {(self.x, self.y)}, parent: {(segment.x, segment.y)}"
        )
