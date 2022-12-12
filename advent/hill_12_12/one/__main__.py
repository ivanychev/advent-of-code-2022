import pathlib

from advent.hill_12_12.graph import ReachabilityMap
from advent.hill_12_12.reader import read_map

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        height_map = read_map(f)
        reachability_map = ReachabilityMap.from_height_map(height_map)
        print(reachability_map.at(*height_map.start_coord))
