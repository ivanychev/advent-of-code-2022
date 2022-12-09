from array import array
from functools import partial
from operator import itemgetter
from typing import MutableSequence, NamedTuple

from typing_extensions import Self

from advent.treetop_house_12_08.grid import Tree, TreeGrid


def _fill_scenic_visitor_factory(scenic_grid: list[MutableSequence[int]]):
    pos_sorted_max_trees: list[Tree] = []
    index = 0

    def visitor(tree: int, x: int, y: int):
        nonlocal pos_sorted_max_trees, index

        while pos_sorted_max_trees and pos_sorted_max_trees[-1].height < tree:
            pos_sorted_max_trees.pop()
        if pos_sorted_max_trees:
            delta = abs(x - pos_sorted_max_trees[-1].x) + abs(
                y - pos_sorted_max_trees[-1].y
            )
        else:
            delta = index
        scenic_grid[x][y] *= delta

        while pos_sorted_max_trees and pos_sorted_max_trees[-1].height == tree:
            pos_sorted_max_trees.pop()

        pos_sorted_max_trees.append(Tree(x, y, tree))
        index += 1

    return visitor


class ScenicGrid(NamedTuple):
    visibility: list[MutableSequence[int]]

    @classmethod
    def make_for_grid(cls, t: TreeGrid) -> Self:
        y_size = len(t.grid[0])
        one_row = [1] * y_size
        scenic_grid = [array("i", one_row) for _ in t.grid]
        t.visit_grid_across_all_directions(
            visit_factory=partial(_fill_scenic_visitor_factory, scenic_grid=scenic_grid)
        )
        return cls(scenic_grid)

    def highest_scenic_score(self) -> int:
        return max(
            (
                (x, y, value)
                for x, row in enumerate(self.visibility)
                for y, value in enumerate(row)
            ),
            key=itemgetter(2),
        )[2]
