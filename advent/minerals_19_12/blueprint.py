import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class OreRobotBlueprint:
    costs_ore: int


@dataclasses.dataclass(frozen=True, slots=True)
class ClayRobotBlueprint:
    costs_ore: int


@dataclasses.dataclass(frozen=True, slots=True)
class ObsRobotBlueprint:
    costs_ore: int
    costs_clay: int


@dataclasses.dataclass(frozen=True, slots=True)
class GeodeRobotBlueprint:
    costs_ore: int
    costs_obs: int


@dataclasses.dataclass(frozen=True, slots=True)
class Blueprint:
    index: int
    ore_blueprint: OreRobotBlueprint
    clay_blueprint: ClayRobotBlueprint
    obs_blueprint: ObsRobotBlueprint
    geode_blueprint: GeodeRobotBlueprint

    def max_ore_cost(self):
        return max(
            self.geode_blueprint.costs_ore,
            self.obs_blueprint.costs_ore,
            self.ore_blueprint.costs_ore,
            self.clay_blueprint.costs_ore,
        )
