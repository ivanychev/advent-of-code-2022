from array import array
from typing import TextIO

from advent.treetop_house_12_08.grid import TreeGrid


def read_grid(f: TextIO) -> TreeGrid:
    rows = []
    for line in f:
        line = array("b", [int(x) for x in line.strip()])
        rows.append(line)
    return TreeGrid(rows)
