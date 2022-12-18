from typing import TextIO

from boiling_18_12.cube import Cube


def read_cubes(f: TextIO):
    cubes = []
    for line in f:
        cubes.append(Cube(*[int(x) for x in line.strip().split(",")]))
    return cubes
