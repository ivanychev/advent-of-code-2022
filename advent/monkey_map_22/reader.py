import re
from typing import TextIO

from monkey_map_22.action import Action, Move, TurnClockwise, TurnCounterClockwise
from monkey_map_22.bareer import Bareer
from monkey_map_22.cube import Cube
from monkey_map_22.map import MonkeyMap
from monkey_map_22.player import Player

PATH_TOKEN_RE = re.compile(r"(\d+)|[LR]")


def read_map_and_path(
    f: TextIO, bareers: list[Bareer] | None = None
) -> tuple[Player, list[Action]]:
    next_is_password = False
    map_rows = []
    actions = []
    path = None

    for row in f:
        row = row.rstrip("\n")
        if not row:
            next_is_password = True
            continue

        if next_is_password:
            path = row
        else:
            map_rows.append(row)

    for raw_action_match in PATH_TOKEN_RE.finditer(path):
        raw_action = raw_action_match.group(0)
        if raw_action == "R":
            actions.append(TurnClockwise())
        elif raw_action == "L":
            actions.append(TurnCounterClockwise())
        else:
            actions.append(Move(value=int(raw_action)))

    map = MonkeyMap.from_rows(map_rows)
    player = Player.from_map(map, bareers=bareers)

    return player, actions


def read_cube_and_path(
    f: TextIO,
    side_map: list[list[int | None]],
    rotations: tuple[int, int, int, int, int, int],
):
    next_is_password = False
    map_rows = []
    actions = []
    path = None

    for row in f:
        row = row.rstrip("\n")
        if not row:
            next_is_password = True
            continue

        if next_is_password:
            path = row
        else:
            map_rows.append(row)

    for raw_action_match in PATH_TOKEN_RE.finditer(path):
        raw_action = raw_action_match.group(0)
        if raw_action == "R":
            actions.append(TurnClockwise())
        elif raw_action == "L":
            actions.append(TurnCounterClockwise())
        else:
            actions.append(Move(value=int(raw_action)))

    cube = Cube.read_from_string(map_rows, side_map=side_map, rotations=rotations)
    starting_pos = map_rows[0].index(".")

    return cube, actions, (0, starting_pos)
