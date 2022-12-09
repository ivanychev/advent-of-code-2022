from typing import NamedTuple


class Direction(NamedTuple):
    direction: str

    def to_coord_delta(self):
        x, y = 0, 0

        match self.direction:
            case "U":
                y = 1
            case "D":
                y = -1
            case "L":
                x = -1
            case "R":
                x = 1
        return x, y

    def to_opposite_coord_delta(self):
        d = self.to_coord_delta()
        return -d[0], -d[1]


class Motion(NamedTuple):
    direction: Direction
    steps: int
