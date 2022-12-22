import pathlib

from monkey_map_22.action import Move, TurnClockwise, TurnCounterClockwise
from monkey_map_22.direction import (
    CLOCKWISE_DIRECTIONS,
    turn_clockwise,
    turn_counterclockwise,
)
from monkey_map_22.reader import read_cube_and_path

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "test_input.txt").open() as f:

        rotations = (0, 0, 0, 2, 1, 2)
        side_map = [
            [None, None, 0, None],
            [3, 4, 1, None],
            [None, None, 2, 5],
        ]

        cube, actions, initial_row_and_column = read_cube_and_path(
            f,
            side_map=side_map,
            rotations=rotations,
        )

        direction = (1, 0)
        position = (0, 0)
        cube_side = cube.sides[0]
        cell = cube_side.map[position[1]][position[0]]

        for action in actions:
            match action:
                case TurnClockwise():
                    direction = turn_clockwise(direction)
                case TurnCounterClockwise():
                    direction = turn_counterclockwise(direction)
                case Move(value=steps):
                    for _ in range(steps):
                        cube_side, position, direction, cell = cube_side.move(
                            position, direction, cube
                        )

        orig_map_direction = direction
        for _ in range(rotations[cube_side.index]):
            # anti clockwise rotation
            orig_map_direction = turn_counterclockwise(orig_map_direction)

        print(
            1000 * (cell.orig_row_idx + 1)
            + 4 * (cell.orig_col_idx + 1)
            + CLOCKWISE_DIRECTIONS.index(orig_map_direction)
        )
