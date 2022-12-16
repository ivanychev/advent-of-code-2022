import dataclasses
import functools
from array import array
from collections import deque
from dataclasses import dataclass
from typing import Collection, Iterable, Sequence

from frozendict import frozendict
from typing_extensions import Self

from advent.volcano_16_12.valve import Valve


def _distances(
    from_valve: str, to_valves: Collection[str], registry: dict[str, Valve]
) -> dict[str, int]:
    to_valves = frozenset(to_valves)
    q: deque[tuple[str, int]] = deque([(from_valve, 0)])
    visited = set()
    distances = {}
    while q:
        node, dist = q.popleft()
        if node in visited:
            continue
        visited.add(node)
        distances[node] = dist
        valve = registry[node]
        for linked in valve.linked_to:
            if linked not in visited:
                q.append((linked, dist + 1))
    return {k: v for k, v in distances.items() if k in to_valves}


@dataclass(slots=True, frozen=True)
class Network:
    registry: frozendict[str, Valve]
    idx_to_node: tuple[str, ...]
    node_to_idx: frozendict[str, int]
    valves: tuple[Valve, ...]
    distances_map: tuple[Sequence[int], ...]

    @classmethod
    def from_valves(
        cls, valves: list[Valve], registry: dict[str, Valve], starting_valve: str
    ):
        to_include = set([starting_valve] + [v.name for v in valves if v.rate])
        distances_map = tuple(
            array("i", [0] * len(to_include)) for _ in range(len(to_include))
        )
        idx_to_node = tuple(to_include)
        node_to_idx = {node: idx for idx, node in enumerate(idx_to_node)}
        valves = tuple(registry[node] for node in idx_to_node)

        for v in to_include:
            distances = _distances(v, to_include - {v}, registry)
            for to, value in distances.items():
                distances_map[node_to_idx[v]][node_to_idx[to]] = value

        return cls(
            idx_to_node=idx_to_node,
            node_to_idx=frozendict(node_to_idx),
            registry=frozendict(registry),
            distances_map=distances_map,
            valves=valves,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class NetworkState:
    network: Network = dataclasses.field(hash=False)
    opened_map: int
    current: int
    minutes_left: int

    def __str__(self):
        return f"Left {self.minutes_left}, opened: {sorted(self.opened_valves())}"

    def distance_to(self, idx: int) -> int:
        return self.network.distances_map[self.current][idx]

    def open_current_valve(self) -> Self:
        return NetworkState(
            network=self.network,
            opened_map=self.opened_map | (1 << self.current),
            current=self.current,
            minutes_left=self.minutes_left - 1,
        )

    def go_and_open(self, idx: int):
        return NetworkState(
            network=self.network,
            opened_map=self.opened_map | (1 << idx),
            current=idx,
            minutes_left=self.minutes_left - 1 - self.distance_to(idx),
        )

    def is_valve_opened(self, idx: int):
        return bool(self.opened_map & (1 << idx))

    def is_current_opened(self):
        return self.is_valve_opened(self.current)

    def opened_valves(self) -> Iterable[int]:
        current = 0
        map = self.opened_map
        while map:
            if map & 1:
                yield current
            map >>= 1
            current += 1

    def other_closed_valves(self):
        current_idx = self.current
        count = len(self.network.valves)
        map = self.opened_map
        for idx in range(count):
            if not map & 1 and current_idx != idx:
                yield idx
            map >>= 1

    def pressure_if_wait(self, minutes: int | None = None) -> int:
        valves = self.network.valves
        return (minutes or self.minutes_left) * sum(
            valves[idx].rate for idx in self.opened_valves()
        )


@functools.lru_cache(None)
def max_cum_pressure(state: NetworkState) -> int:
    max_pressure = float("-inf")
    # Do nothing and wait
    max_pressure = max(max_pressure, state.pressure_if_wait())

    if (
        state.network.valves[state.current].rate
        and not state.is_current_opened()
        and state.minutes_left >= 1
    ):
        max_pressure = max(
            max_pressure,
            state.pressure_if_wait(1) + max_cum_pressure(state.open_current_valve()),
        )
    for idx in state.other_closed_valves():
        cost_of_move = 1 + state.distance_to(idx)
        if not state.network.valves[idx].rate or state.minutes_left < cost_of_move:
            continue
        max_pressure = max(
            max_pressure,
            state.pressure_if_wait(cost_of_move)
            + max_cum_pressure(state.go_and_open(idx)),
        )
    return max_pressure
