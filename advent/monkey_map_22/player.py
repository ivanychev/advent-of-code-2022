from dataclasses import dataclass
from typing import Sequence

from monkey_map_22.action import Action, Move, TurnClockwise, TurnCounterClockwise
from monkey_map_22.bareer import Bareer
from monkey_map_22.direction import (
    CLOCKWISE_DIRECTIONS,
    HORIZONTAL_MOVES,
    VERTICAL_MOVES,
    turn_clockwise,
    turn_counterclockwise,
)
from monkey_map_22.formation import SOLID
from monkey_map_22.map import MonkeyMap


@dataclass
class Player:
    x: int
    y: int
    direction: tuple[int, int]
    map: MonkeyMap
    bareers: list[Bareer] | None

    @classmethod
    def from_map(cls, map: MonkeyMap, bareers: list[Bareer] | None = None):
        initial_xy = map.starting_xy()
        direction = (1, 0)
        return cls(
            x=initial_xy[0],
            y=initial_xy[1],
            direction=direction,
            map=map,
            bareers=bareers,
        )

    def coord(self) -> tuple[int, int]:
        return self.x, self.y

    def set_coord(self, coord: Sequence[int]):
        self.x = coord[0]
        self.y = coord[1]

    def move_to_next_position(self):
        if self.direction in VERTICAL_MOVES:
            coord_index = 1
            keep_coord_index = 0
            coord_range = self.map.vertical_to_range[self.coord()[keep_coord_index]]
        elif self.direction in HORIZONTAL_MOVES:
            coord_index = 0
            keep_coord_index = 1
            coord_range = self.map.horizontal_to_range[self.coord()[keep_coord_index]]
        else:
            raise ValueError(f"Invalid direction: {self.direction}")

        current_coord = self.coord()[coord_index]
        updated_coord = current_coord + self.direction[coord_index]

        point = [0, 0]
        point[keep_coord_index] = self.coord()[keep_coord_index]
        point[coord_index] = updated_coord
        new_direction = None

        if self.bareers is None:
            if updated_coord == coord_range[1]:
                point[coord_index] = coord_range[0]
            elif updated_coord == coord_range[0] - 1:
                point[coord_index] = coord_range[1] - 1
        elif updated_coord in (coord_range[1], coord_range[0] - 1):
            for b in self.bareers:
                if b.handles(point):
                    point, new_direction = b.transform(tuple(point))
                    break
            else:
                raise ValueError(f"Didn't find a barreer for point {point}")

        if self.map.at_xy(point) == SOLID:
            return
        self.set_coord(point)
        if new_direction:
            self.direction = new_direction

    def perform(self, action: Action):
        match action:
            case TurnClockwise():
                self.direction = turn_clockwise(self.direction)
            case TurnCounterClockwise():
                self.direction = turn_counterclockwise(self.direction)
            case Move(value=steps):
                for _ in range(steps):
                    self.move_to_next_position()
            case unknown:
                raise ValueError(f"unknown action: {unknown}")

    def get_password(self):
        return (
            1000 * (self.y + 1)
            + 4 * (self.x + 1)
            + CLOCKWISE_DIRECTIONS.index(self.direction)
        )

    def render(self) -> str:
        return self.map.render_with_player((self.x, self.y))
