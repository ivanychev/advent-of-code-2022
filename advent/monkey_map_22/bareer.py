from typing import Callable


class Bareer:
    def __init__(
        self,
        point_from: tuple[int, int],
        point_to: tuple[int, int],
        expects_direction: tuple[int, int],
        new_direction: tuple[int, int],
        coord_transform: Callable[[tuple[int, int]], tuple[int, int]],
    ):
        self.point_from, self.point_to = sorted((point_from, point_to))
        self.new_direction = new_direction
        self.expects_direction = expects_direction
        self.coord_transform = coord_transform

    def handles(self, point: tuple[int, int]) -> bool:
        return (
            self.point_from[0] <= point[0] <= self.point_to[0]
            and self.point_from[1] <= point[1] <= self.point_to[1]
        )

    def transform(
        self, point: tuple[int, int]
    ) -> tuple[[tuple[int, int], tuple[int, int]]]:
        return self.coord_transform(point), self.new_direction
