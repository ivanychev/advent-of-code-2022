import collections
import dataclasses
from operator import itemgetter

from cytoolz import curried, merge, pipe
from tqdm import tqdm

from advent.unstable_diffusion_23_12.point import Direction, Point
from advent.unstable_diffusion_23_12.reader import Elf, ElfMap


def _reverse_kv(d: dict) -> dict:
    return {v: k for k, v in d.items()}


def run(elves: list[Elf], elf_map: ElfMap, rounds: int | None = None):
    directions_to_consider = collections.deque(
        [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
    )

    round = 0
    pbar = tqdm(total=rounds)

    while rounds is None or round < rounds:
        proposed = (elf.propose(elf_map, directions_to_consider) for elf in elves)
        proposed_point_to_elves = pipe(
            zip(elves, proposed),
            curried.groupby(itemgetter(1)),
            curried.valmap(lambda elves_and_points: [e for e, _ in elves_and_points]),
            curried.valfilter(lambda elfs: len(elfs) == 1),
            curried.valmap(itemgetter(0)),
        )
        elves_to_proposed_points = _reverse_kv(proposed_point_to_elves)
        any_changed = any(
            elf
            for elf, proposed in elves_to_proposed_points.items()
            if elf.pos != proposed
        )
        if not any_changed:
            round += 1
            break
        new_map = merge(_reverse_kv(elf_map.pos_to_item), elves_to_proposed_points)
        new_elves: list[Elf] = [None] * len(elves)
        for elf, point in new_map.items():
            new_elves[elf.index] = dataclasses.replace(elves[elf.index], pos=point)

        elves: list[Elf] = new_elves
        elf_map = ElfMap(
            pos_to_item={
                point: elves[elf.index] for point, elf in _reverse_kv(new_map).items()
            }
        )
        directions_to_consider.append(directions_to_consider.popleft())
        round += 1
        pbar.update(1)
    return elves, elf_map, round
