from dataclasses import dataclass, field, replace
from typing import Iterable

from minerals_19_12.blueprint import Blueprint
from typing_extensions import Self


@dataclass(frozen=True, slots=True)
class FactoryState:
    blueprint: Blueprint = field(hash=False, compare=False)
    previous_state: Self | None = field(
        hash=False, compare=False, default=None, repr=False
    )
    ore: int = 0
    obs: int = 0
    clay: int = 0
    geode: int = 0
    time: int = 0
    obs_robots: int = 0
    ore_robots: int = 0
    clay_robots: int = 0
    geode_robots: int = 0

    def _with_harvest(self) -> Self:
        return replace(
            self,
            ore=self.ore + self.ore_robots,
            clay=self.clay + self.clay_robots,
            obs=self.obs + self.obs_robots,
            geode=self.geode + self.geode_robots,
        )

    def _with_time_tick(self) -> Self:
        return replace(self, time=self.time + 1)

    def can_produce_obs(self):
        return (self.ore - self.blueprint.obs_blueprint.costs_ore) >= 0 and (
            self.clay - self.blueprint.obs_blueprint.costs_clay
        ) >= 0

    def produce_obs(self) -> Self | None:
        if self.can_produce_obs():
            return replace(
                self,
                ore=self.ore + self.ore_robots - self.blueprint.obs_blueprint.costs_ore,
                clay=self.clay
                + self.clay_robots
                - self.blueprint.obs_blueprint.costs_clay,
                obs=self.obs + self.obs_robots,
                geode=self.geode + self.geode_robots,
                time=self.time + 1,
                obs_robots=self.obs_robots + 1,
                previous_state=self,
            )

    def can_build_everything(self):
        return (
            self.can_produce_obs()
            and self.can_produce_geode()
            and self.can_produce_ore()
            and self.can_produce_clay()
        )

    def can_produce_ore(self):
        return self.ore - self.blueprint.ore_blueprint.costs_ore >= 0

    def produce_ore(self) -> Self | None:
        if self.can_produce_ore():
            return replace(
                self,
                ore=self.ore + self.ore_robots - self.blueprint.ore_blueprint.costs_ore,
                clay=self.clay + self.clay_robots,
                obs=self.obs + self.obs_robots,
                geode=self.geode + self.geode_robots,
                time=self.time + 1,
                ore_robots=self.ore_robots + 1,
                previous_state=self,
            )

    def can_produce_clay(self):
        return self.ore - self.blueprint.clay_blueprint.costs_ore >= 0

    def produce_clay(self) -> Self | None:
        if self.can_produce_clay():
            return replace(
                self,
                ore=self.ore
                + self.ore_robots
                - self.blueprint.clay_blueprint.costs_ore,
                clay=self.clay + self.clay_robots,
                obs=self.obs + self.obs_robots,
                geode=self.geode + self.geode_robots,
                time=self.time + 1,
                clay_robots=self.clay_robots + 1,
                previous_state=self,
            )

    def can_produce_geode(self):
        return (self.ore - self.blueprint.geode_blueprint.costs_ore) >= 0 and (
            self.obs - self.blueprint.geode_blueprint.costs_obs
        ) >= 0

    def produce_geode(self) -> Self | None:
        if self.can_produce_geode():
            return replace(
                self,
                ore=self.ore
                + self.ore_robots
                - self.blueprint.geode_blueprint.costs_ore,
                clay=self.clay + self.clay_robots,
                obs=self.obs
                + self.obs_robots
                - self.blueprint.geode_blueprint.costs_obs,
                geode=self.geode + self.geode_robots,
                time=self.time + 1,
                geode_robots=self.geode_robots + 1,
                previous_state=self,
            )

    def do_nothing(self) -> Self:
        return replace(
            self,
            ore=self.ore + self.ore_robots,
            clay=self.clay + self.clay_robots,
            obs=self.obs + self.obs_robots,
            geode=self.geode + self.geode_robots,
            time=self.time + 1,
            previous_state=self,
        )

    def max_ore_cost(self):
        return self.blueprint.max_ore_cost()

    def next_states(self) -> Iterable[Self]:

        if (
            self.can_produce_geode()
            and self.obs_robots >= self.blueprint.geode_blueprint.costs_obs
            and self.ore_robots >= self.blueprint.geode_blueprint.costs_ore
        ):
            yield self.produce_geode()
            return

        could_built_geode = None
        could_built_clay = None
        could_built_obs = None
        could_built_ore = None

        if s := self.produce_geode():
            could_built_geode = s
            yield s
        if (
            self.clay_robots < self.blueprint.obs_blueprint.costs_clay
            and self.obs_robots < self.blueprint.geode_blueprint.costs_obs
            and (s := self.produce_clay())
        ):
            could_built_clay = s
            yield s
        if self.obs_robots < self.blueprint.geode_blueprint.costs_obs and (
            s := self.produce_obs()
        ):
            could_built_obs = s
            yield s
        if self.ore_robots < self.max_ore_cost() and (s := self.produce_ore()):
            could_built_ore = s
            yield s
        if (
            not self.can_build_everything()
            and not (could_built_geode and self.max_ore_cost() <= could_built_geode.ore)
            and not (could_built_ore and self.max_ore_cost() <= could_built_ore.ore)
            and not (could_built_clay and self.max_ore_cost() <= could_built_clay.ore)
            and not (could_built_obs and self.max_ore_cost() <= could_built_obs.ore)
        ):
            yield self.do_nothing()
