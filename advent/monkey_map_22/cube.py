from dataclasses import dataclass
from typing import Any, NamedTuple

from monkey_map_22.direction import Direction, Position, turn_clockwise
from monkey_map_22.formation import FORMATIONS, SOLID, Formation

CubeSideRotations = tuple[int, int, int, int, int, int]
Rotations = int
CubeSideIndex = int


def _rotate(map: list[list[Any]]) -> list[list[Any]]:
    return [list(reversed(col)) for col in zip(*map)]


@dataclass(slots=True, frozen=True)
class CubeCell:
    formation: Formation
    orig_row_idx: int
    orig_col_idx: int


class CubeCellBorder(NamedTuple):
    cube_index: int
    rotations: int


@dataclass
class CubeSide:
    index: int
    map: list[list[CubeCell]]
    up_border: CubeCellBorder
    down_border: CubeCellBorder
    left_border: CubeCellBorder
    right_border: CubeCellBorder

    def rotate_point_times(self, point: Position, times: int) -> Position:
        for _ in range(times):
            point = self.side_size - point[1] - 1, point[0]
        return point

    def rotate_direction_times(self, direction: Direction, times: int) -> Direction:
        for _ in range(times):
            direction = turn_clockwise(direction)
        return direction

    @property
    def side_size(self):
        return len(self.map)

    def render_to_buffer(self, buffer: list[list[str]], at_row: int, at_col: int):
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                buffer[at_row + row_idx][at_col + col_idx] = cell.formation

    def move(
        self, position: Position, direction: Direction, cube: "Cube"
    ) -> ("CubeSide", Position, Direction, CubeCell):
        original_state = (self, position, direction, self.map[position[1]][position[0]])
        new_position = [position[0] + direction[0], position[1] + direction[1]]
        new_direction = direction
        new_cube = self
        if new_position[1] == -1:
            # Up
            new_position[1] = self.side_size - 1
            new_cube = cube.sides[self.up_border[0]]
            new_position = self.rotate_point_times(
                tuple(new_position), self.up_border[1]
            )
            new_direction = self.rotate_direction_times(direction, self.up_border[1])
        elif new_position[0] == self.side_size:
            # Right
            new_position[0] = 0
            new_cube = cube.sides[self.right_border[0]]
            new_position = self.rotate_point_times(
                tuple(new_position), self.right_border[1]
            )
            new_direction = self.rotate_direction_times(direction, self.right_border[1])
        elif new_position[1] == self.side_size:
            # Down
            new_position[1] = 0
            new_cube = cube.sides[self.down_border[0]]
            new_position = self.rotate_point_times(
                tuple(new_position), self.down_border[1]
            )
            new_direction = self.rotate_direction_times(direction, self.down_border[1])
        elif new_position[0] == -1:
            # Left
            new_position[0] = self.side_size - 1
            new_cube = cube.sides[self.left_border[0]]
            new_position = self.rotate_point_times(
                tuple(new_position), self.left_border[1]
            )
            new_direction = self.rotate_direction_times(direction, self.left_border[1])

        if new_cube.map[new_position[1]][new_position[0]].formation == SOLID:
            return original_state
        return (
            new_cube,
            tuple(new_position),
            new_direction,
            new_cube.map[new_position[1]][new_position[0]],
        )


@dataclass
class Cube:
    sides: tuple[CubeSide, CubeSide, CubeSide, CubeSide, CubeSide, CubeSide]
    side_size: int

    def render(self):
        buffer = [[" "] * (3 * self.side_size) for _ in range(4 * self.side_size)]

        self.sides[4].render_to_buffer(buffer, 0, 0)
        self.sides[0].render_to_buffer(buffer, 0, self.side_size)
        self.sides[5].render_to_buffer(buffer, 0, 2 * self.side_size)
        self.sides[1].render_to_buffer(buffer, self.side_size, self.side_size)
        self.sides[2].render_to_buffer(buffer, 2 * self.side_size, self.side_size)
        self.sides[3].render_to_buffer(buffer, 3 * self.side_size, self.side_size)

        return "\n".join("".join(row) for row in buffer)

    @classmethod
    def read_from_string(
        cls,
        cube_rows: list[str],
        side_map: list[list[int | None]],
        rotations: CubeSideRotations,
    ):
        max_row_length = max(len(s) for s in cube_rows)
        cube_rows = [r.ljust(max_row_length) for r in cube_rows]
        side_size = max(len(cube_rows), len(cube_rows[0])) // 4
        sides: list[list[list[CubeCell]]] = [
            [[None] * side_size for _ in range(side_size)] for _ in range(6)
        ]

        for row_idx in range(len(cube_rows)):
            for col_idx in range(len(cube_rows[0])):
                side_map_row = row_idx // side_size
                side_map_col = col_idx // side_size
                side = side_map[side_map_row][side_map_col]
                if side is None:
                    continue
                if cube_rows[row_idx][col_idx] not in FORMATIONS:
                    raise ValueError(
                        f"Attempting to read {row_idx},{col_idx} with value of '{cube_rows[row_idx][col_idx]}', side size: {side_size}"
                    )
                sides[side][row_idx % side_size][col_idx % side_size] = CubeCell(
                    cube_rows[row_idx][col_idx],
                    orig_row_idx=row_idx,
                    orig_col_idx=col_idx,
                )

        for side in sides:
            for row in side:
                for elem in row:
                    assert elem.formation in FORMATIONS
        for idx, rotation in enumerate(rotations):
            for _ in range(rotation):
                sides[idx] = _rotate(sides[idx])

        return cls(
            sides=(
                CubeSide(
                    index=0,
                    map=sides[0],
                    up_border=CubeCellBorder(cube_index=3, rotations=0),
                    down_border=CubeCellBorder(cube_index=1, rotations=0),
                    left_border=CubeCellBorder(cube_index=4, rotations=0),
                    right_border=CubeCellBorder(cube_index=5, rotations=0),
                ),
                CubeSide(
                    index=1,
                    map=sides[1],
                    up_border=CubeCellBorder(cube_index=0, rotations=0),
                    down_border=CubeCellBorder(cube_index=2, rotations=0),
                    left_border=CubeCellBorder(cube_index=4, rotations=1),
                    right_border=CubeCellBorder(cube_index=5, rotations=3),
                ),
                CubeSide(
                    index=2,
                    map=sides[2],
                    up_border=CubeCellBorder(cube_index=1, rotations=0),
                    down_border=CubeCellBorder(cube_index=3, rotations=0),
                    left_border=CubeCellBorder(cube_index=4, rotations=2),
                    right_border=CubeCellBorder(cube_index=5, rotations=2),
                ),
                CubeSide(
                    index=3,
                    map=sides[3],
                    up_border=CubeCellBorder(cube_index=2, rotations=0),
                    down_border=CubeCellBorder(cube_index=0, rotations=0),
                    left_border=CubeCellBorder(cube_index=4, rotations=3),
                    right_border=CubeCellBorder(cube_index=5, rotations=1),
                ),
                CubeSide(
                    index=4,
                    map=sides[4],
                    up_border=CubeCellBorder(cube_index=3, rotations=1),
                    down_border=CubeCellBorder(cube_index=1, rotations=3),
                    left_border=CubeCellBorder(cube_index=2, rotations=2),
                    right_border=CubeCellBorder(cube_index=0, rotations=0),
                ),
                CubeSide(
                    index=5,
                    map=sides[5],
                    up_border=CubeCellBorder(cube_index=3, rotations=3),
                    down_border=CubeCellBorder(cube_index=1, rotations=1),
                    left_border=CubeCellBorder(cube_index=0, rotations=0),
                    right_border=CubeCellBorder(cube_index=2, rotations=2),
                ),
            ),
            side_size=side_size,
        )
