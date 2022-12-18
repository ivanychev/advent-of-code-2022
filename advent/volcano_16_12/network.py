import concurrent.futures
import dataclasses
import enum
import functools
import gc
import itertools
from array import array
from collections import deque
from dataclasses import dataclass
from typing import Collection, Iterable, Sequence

from frozendict import frozendict
from tqdm import tqdm

from advent.volcano_16_12.valve import Valve

TIME_TO_OPEN = 1


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


class TransitionStatus(enum.IntEnum):
    RUNNING = 1
    STANDING = 2
    FINISHED = 3
    OPENING = 4


@dataclasses.dataclass(slots=True, frozen=True)
class TransitionState:
    status: TransitionStatus
    current: int | None
    finish_at_minutes_left: int | None

    def other_closed_valves(self, network_state: "NetworkState"):
        current_idx = self.current
        count = len(network_state.network.valves)
        map = network_state.opened_map_mask
        for idx in range(count):
            if not map & 1 and current_idx != idx:
                yield idx
            map >>= 1


@functools.lru_cache(None)
def _opened_valves_cached(opened_map_mask: int):
    current = 0
    result = []
    while opened_map_mask:
        if opened_map_mask & 1:
            result.append(current)
        opened_map_mask >>= 1
        current += 1
    return result


@dataclasses.dataclass(slots=True, frozen=True)
class NetworkState:
    network: Network = dataclasses.field(hash=False, compare=False)
    opened_map_mask: int
    minutes_left: int
    explorers_states: tuple[TransitionState, ...]

    def __str__(self):
        return f"Left {self.minutes_left}, opened: {sorted(self.opened_valves())}, statuses: {self.explorers_states}"

    def all_explorers_are_standing(self):
        return all(s.status == TransitionStatus.STANDING for s in self.explorers_states)

    def is_valve_opened(self, idx: int):
        return bool(self.opened_map_mask & (1 << idx))

    def opened_valves(self) -> Iterable[int]:
        return _opened_valves_cached(self.opened_map_mask)

    def open_valve(self, idx: int):
        return dataclasses.replace(
            self, opened_map_mask=self.opened_map_mask | (1 << idx)
        )

    def pressure_if_wait(self, minutes: int | None = None) -> int:
        valves = self.network.valves
        return (minutes or self.minutes_left) * sum(
            valves[idx].rate for idx in self.opened_valves()
        )


N = 0
MASK = 2**32 - 1


def do_every_n(callable, n):
    global N
    N = (N + 1) & MASK
    if not N % n:
        callable()


def print_every_n(o, n):
    do_every_n(lambda o=o: print(o), n)


def gc_every_n(n):
    do_every_n(gc.collect, n)


def worker(t):
    return t[0] + max_cum_pressure(t[1])


@functools.lru_cache(maxsize=1000000)
def max_cum_pressure(state: NetworkState, compute_parallel: bool = False) -> int:
    gc_every_n(100000)
    if not state.minutes_left:
        return 0
    max_pressure = float("-inf")

    # Update the network with finishing tasks.
    updated_states = []
    for idx, exp in enumerate(state.explorers_states):
        if exp.finish_at_minutes_left == state.minutes_left:
            if exp.status == TransitionStatus.RUNNING:
                current = exp.current
                state = state.open_valve(current)
            elif exp.status == TransitionStatus.FINISHED:
                continue
            else:
                raise RuntimeError(f"Invalid status {exp.status}")
            updated_states.append(
                TransitionState(
                    status=TransitionStatus.STANDING,
                    current=current,
                    finish_at_minutes_left=None,
                )
            )
        else:
            updated_states.append(exp)

    state = NetworkState(
        network=state.network,
        opened_map_mask=state.opened_map_mask,
        minutes_left=state.minutes_left,
        explorers_states=tuple(updated_states),
    )

    # Do nothing and wait
    if state.all_explorers_are_standing():
        max_pressure = max(max_pressure, state.pressure_if_wait())

    possible_scenarios: list[list[TransitionState]] = [
        [] for _ in state.explorers_states
    ]
    for idx, exp in enumerate(state.explorers_states):
        if exp.status != TransitionStatus.STANDING:
            possible_scenarios[idx].append(exp)
            continue
        theres_closed = False
        for closed_idx in exp.other_closed_valves(state):
            theres_closed = True
            if (
                time_to_reach := state.network.distances_map[exp.current][closed_idx]
                + TIME_TO_OPEN
            ) <= state.minutes_left:
                possible_scenarios[idx].append(
                    TransitionState(
                        status=TransitionStatus.RUNNING,
                        current=closed_idx,
                        finish_at_minutes_left=state.minutes_left - time_to_reach,
                    )
                )
        if not theres_closed:
            # The explorer always can finish here and do nothing forever.
            possible_scenarios[idx].append(
                TransitionState(
                    status=TransitionStatus.FINISHED,
                    current=exp.current,
                    finish_at_minutes_left=0,
                )
            )

    if compute_parallel:
        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as ex:
            tasks = []
            for state_combination in itertools.product(*possible_scenarios):
                next_minutes_left = max(
                    exp.finish_at_minutes_left for exp in state_combination
                )
                tasks.append(
                    (
                        state.pressure_if_wait(state.minutes_left - next_minutes_left),
                        dataclasses.replace(
                            state,
                            minutes_left=next_minutes_left,
                            explorers_states=state_combination,
                        ),
                    )
                )
            max_pressure = max(
                max_pressure, max(tqdm(ex.map(worker, tasks), total=len(tasks)))
            )
    else:
        for state_combination in itertools.product(*possible_scenarios):
            next_minutes_left = max(
                exp.finish_at_minutes_left for exp in state_combination
            )
            if next_minutes_left >= state.minutes_left:
                assert next_minutes_left >= state.minutes_left

            max_pressure = max(
                max_pressure,
                state.pressure_if_wait(state.minutes_left - next_minutes_left)
                + max_cum_pressure(
                    dataclasses.replace(
                        state,
                        minutes_left=next_minutes_left,
                        explorers_states=state_combination,
                    )
                ),
            )
    return max_pressure
