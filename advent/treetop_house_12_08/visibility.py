from array import array
from functools import partial
from typing import NamedTuple, MutableSequence

from typing_extensions import Self

from advent.treetop_house_12_08.grid import TreeGrid, TreeVisitor


def _fill_visibility_visitor_factory(
    visibility_grid: list[MutableSequence[int]],
) -> TreeVisitor:
    max_observed_height = -1

    def visitor(tree: int, x: int, y: int):
        nonlocal max_observed_height
        if tree > max_observed_height:
            visibility_grid[x][y] = 1
            max_observed_height = tree

    return visitor


class VisibilityMap(NamedTuple):
    visibility: list[MutableSequence[int]]

    def visible_count(self) -> int:
        return sum(x for row in self.visibility for x in row)

    @classmethod
    def make_for_grid(cls, t: TreeGrid) -> Self:
        y_size = len(t.grid[0])
        zero_row = [0] * y_size
        visibility = [array("i", zero_row) for _ in t.grid]

        t.visit_grid_across_all_directions(
            visit_factory=partial(
                _fill_visibility_visitor_factory, visibility_grid=visibility
            )
        )

        return cls(visibility)
