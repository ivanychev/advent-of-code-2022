from typing import TextIO

from advent.rope_bridge_12_09.motion import Direction, Motion


def read_motions(f: TextIO) -> list[Motion]:
    motions = []
    for line in f:
        line = line.strip()
        direction, steps = line.split(" ", maxsplit=1)

        motions.append(Motion(direction=Direction(direction), steps=int(steps)))
    return motions
