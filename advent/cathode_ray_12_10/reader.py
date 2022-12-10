from typing import TextIO

from advent.cathode_ray_12_10.cpu import Addx, Noop


def read_commands(f: TextIO):
    commands = []
    for line in f:
        tokens = line.strip().split()
        match tokens[0]:
            case "addx":
                commands.append(Addx(int(tokens[1])))
            case "noop":
                commands.append(Noop())
            case unknown:
                raise ValueError(f"Unknown command: {unknown}")
    return commands
