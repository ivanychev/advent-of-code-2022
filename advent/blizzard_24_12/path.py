import collections
import itertools
from typing import NamedTuple

from blizzard_24_12.blizzard_map import BlizzardMap
from blizzard_24_12.directions import Point
from tqdm import tqdm


class SearchEntry(NamedTuple):
    p: Point
    time: int


def find_shortest_path(start: Point, end: Point, blizzard_map: BlizzardMap) -> int:
    x_range_inclusive = (1, blizzard_map.width)
    y_range_inclusive = (1, blizzard_map.height)
    q = collections.deque([SearchEntry(start, 0)])
    visited = set()
    pbar = tqdm(desc="steps")
    max_time = 0
    while q:
        entry = q.popleft()
        if entry.p == end:
            return entry.time
        if entry.time > max_time:
            max_time = entry.time
            pbar.update(1)
        if entry in visited:
            continue
        visited.add(entry)
        new_time = entry.time + 1
        for neighbour in itertools.chain(
            entry.p.can_step_to(x_range_inclusive, y_range_inclusive, start, end),
            (entry.p,),
        ):
            entry = SearchEntry(neighbour, new_time)
            if (
                not blizzard_map.is_blizzard_at(neighbour, new_time)
                and entry not in visited
            ):
                q.append(entry)
