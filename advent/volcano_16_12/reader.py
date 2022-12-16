from typing import TextIO

from advent.volcano_16_12.valve import Valve


def read_valves(f: TextIO) -> tuple[list[Valve], dict[str, Valve]]:
    registry = {}
    return [Valve.from_string(row, registry) for row in f], registry
