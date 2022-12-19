import re
from typing import TextIO

from minerals_19_12.blueprint import (
    Blueprint,
    ClayRobotBlueprint,
    GeodeRobotBlueprint,
    ObsRobotBlueprint,
    OreRobotBlueprint,
)

BLUEPRINT_RE = re.compile(
    r"Blueprint (?P<index>\d+): Each ore robot costs (?P<ore_costs_ore>\d+) ore. Each clay robot costs (?P<clay_costs_ore>\d+) ore. Each obsidian robot costs (?P<obs_costs_ore>\d+) ore and (?P<obs_costs_clay>\d+) clay. Each geode robot costs (?P<geode_costs_ore>\d+) ore and (?P<geode_costs_obs>\d+) obsidian."
)


def read_blueprints(f: TextIO) -> list[Blueprint]:
    blueprints = []
    for line in f:
        m = BLUEPRINT_RE.match(line).groupdict()
        blueprints.append(
            Blueprint(
                index=int(m["index"]),
                ore_blueprint=OreRobotBlueprint(costs_ore=int(m["ore_costs_ore"])),
                clay_blueprint=ClayRobotBlueprint(costs_ore=int(m["clay_costs_ore"])),
                obs_blueprint=ObsRobotBlueprint(
                    costs_ore=int(m["obs_costs_ore"]),
                    costs_clay=int(m["obs_costs_clay"]),
                ),
                geode_blueprint=GeodeRobotBlueprint(
                    costs_ore=int(m["geode_costs_ore"]),
                    costs_obs=int(m["geode_costs_obs"]),
                ),
            )
        )
    return blueprints
