import pathlib
from collections import Counter, deque
from itertools import product
from operator import attrgetter
from typing import Callable

from boiling_18_12.cube import Cube, Point
from boiling_18_12.reader import read_cubes
from tqdm import tqdm

CURRENT_DIR = pathlib.Path(__file__).parent

Y = 2000000


def find_min_max_coord(surfaces: list[Point], coord: str):
    lowest = min(surfaces, key=attrgetter(coord))
    highest = max(surfaces, key=attrgetter(coord))

    return getattr(lowest, coord), getattr(highest, coord)


def bfs(
    surfaces: frozenset[Point],
    solid_cubes: frozenset[Cube],
    starting_surface: Point,
    visit_predicate: Callable[[Point], bool],
):
    q = deque([starting_surface])
    visited = set()
    external_surfaces = set()
    pbar = tqdm(total=len(surfaces))

    while q:
        surface = q.popleft()
        if surface in visited:
            continue
        visited.add(surface)
        if surface in surfaces and surface not in external_surfaces:
            external_surfaces.add(surface)
            pbar.update(1)
        air_cubes = (c for c in surface.adjacent_cubes() if c not in solid_cubes)
        to_visit = (
            side
            for c in air_cubes
            for side in c.side_middles()
            if side not in visited and visit_predicate(side)
        )
        q.extend(to_visit)
    return external_surfaces


if __name__ == "__main__":
    with (CURRENT_DIR / "test_input.txt").open() as f:
        cubes = frozenset(read_cubes(f))
        c = Counter()
        for cube in cubes:
            c.update(cube.side_middles())
        surfaces = frozenset(p for p, count in c.items() if count == 1)

        x_min, x_max = find_min_max_coord(surfaces, "x")
        y_min, y_max = find_min_max_coord(surfaces, "y")
        z_min, z_max = find_min_max_coord(surfaces, "z")

        def valid_surface(p: Point):
            within_bounds = (
                x_min - 1 <= p.x <= x_max + 1
                and y_min - 1 <= p.y <= y_max + 1
                and z_min - 1 <= p.z <= z_max + 1
            )
            some_cube = p.adjacent_cubes()[0]
            return within_bounds and any(
                Cube(some_cube.x + x, some_cube.y + y, some_cube.z + z) in cubes
                for x, y, z in product(range(-1, 2), range(-1, 2), range(-1, 2))
            )

        start_surface = min(surfaces, key=attrgetter("x"))

        external_surfaces = bfs(surfaces, cubes, start_surface, valid_surface)
        print(len(external_surfaces))
