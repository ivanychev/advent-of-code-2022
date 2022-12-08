from array import array
from functools import partial
from typing import NamedTuple, Tuple, MutableSequence, Callable

from typing_extensions import Self

Height = int


class Tree(NamedTuple):
    x: int
    y: int
    height: int


TreeVisitor = Callable[[int, int, int], None]
TreeVisitorFactory = Callable[[], TreeVisitor]


class TreeGrid(NamedTuple):
    grid: list[MutableSequence[int]]

    def visit_grid_across_direction(
        self, direction: Tuple[int, int], start: Tuple[int, int], visit: TreeVisitor
    ):
        x, y = start
        dx, dy = direction
        while self._within_grid(x, y):
            visit(self.grid[x][y], x, y)
            x += dx
            y += dy

    def visit_grid_across_all_directions(self, visit_factory: TreeVisitorFactory):
        x_size = len(self.grid)
        y_size = len(self.grid[0])
        for x in range(x_size):
            self.visit_grid_across_direction((0, 1), (x, 0), visit=visit_factory())
            self.visit_grid_across_direction(
                (0, -1), (x, y_size - 1), visit=visit_factory()
            )
        for y in range(y_size):
            self.visit_grid_across_direction((1, 0), (0, y), visit=visit_factory())
            self.visit_grid_across_direction(
                (-1, 0), (x_size - 1, y), visit=visit_factory()
            )

    def _within_grid(self, x: int, y: int):
        if not 0 <= x < len(self.grid):
            return False
        if not 0 <= y < len(self.grid[0]):
            return False
        return True
