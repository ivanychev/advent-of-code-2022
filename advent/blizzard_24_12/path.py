import collections
import enum
import itertools
from typing import NamedTuple

from blizzard_24_12.blizzard_map import BlizzardMap
from blizzard_24_12.directions import Point
from tqdm import tqdm


class State(enum.IntEnum):
    STARTED = 1
    VISITED_END = 2
    VISITED_END_AND_START = 3
    VISITED_END_AND_START_AND_END = 4

    @staticmethod
    def transform_state(state: "State", point: Point, start: Point, end: Point):
        if state == State.STARTED and point == end:
            return State.VISITED_END
        if state == State.VISITED_END and point == start:
            return State.VISITED_END_AND_START
        if state == State.VISITED_END_AND_START and point == end:
            return State.VISITED_END_AND_START_AND_END
        return state


class SearchEntry(NamedTuple):
    p: Point
    time: int
    state: State


def find_shortest_path(
    start: Point,
    end: Point,
    blizzard_map: BlizzardMap,
    stop_state: State = State.VISITED_END,
) -> int:
    x_range_inclusive = (1, blizzard_map.width)
    y_range_inclusive = (1, blizzard_map.height)
    q = collections.deque([SearchEntry(start, 0, State.STARTED)])
    visited = set()
    debug_encountered_states = set()
    pbar = tqdm(desc="steps")
    max_time = 0
    while q:
        entry = q.popleft()
        if entry.time > max_time:
            max_time = entry.time
            pbar.update(1)
        if entry in visited:
            continue
        new_state = State.transform_state(entry.state, entry.p, start, end)
        if new_state not in debug_encountered_states:
            debug_encountered_states.add(new_state)
            print(f"Saw new state: {new_state}")
        if new_state == stop_state:
            return entry.time
        visited.add(entry)
        new_time = entry.time + 1
        for neighbour in itertools.chain(
            entry.p.can_step_to(x_range_inclusive, y_range_inclusive, start, end),
            (entry.p,),
        ):
            entry = SearchEntry(neighbour, new_time, new_state)
            if (
                not blizzard_map.is_blizzard_at(neighbour, new_time)
                and entry not in visited
            ):
                q.append(entry)
