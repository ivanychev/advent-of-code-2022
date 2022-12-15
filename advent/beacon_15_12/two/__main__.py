import pathlib
import sys
from operator import itemgetter
from typing import Tuple

from tqdm import trange

from advent.beacon_15_12.interval import join_intervals
from advent.beacon_15_12.reader import read_sensors
from advent.distress_signal_13_12.packet import compare_ordering
from advent.distress_signal_13_12.reader import read_packets

CURRENT_DIR = pathlib.Path(__file__).parent

MIN_COORD = 0
MAX_COORD = 4000000
TOTAL_CELLS_IN_ROW = MAX_COORD - MIN_COORD + 1

MINUS_LARGE_X = float("-inf")
PlUS_LARGE_X = float("inf")


def median_of_three(a, b, c):
    if a <= b and b <= c:
        return b
    if c <= b and b <= a:
        return b
    if a <= c and c <= b:
        return c
    if b <= c and c <= a:
        return c
    return a


def _adjust_to_min_max(interval: Tuple[int, int]):
    return (
        median_of_three(MIN_COORD, MAX_COORD + 1, interval[0]),
        median_of_three(MIN_COORD, MAX_COORD + 1, interval[1]),
    )


# Answer: 10621647166538

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        sensors = read_sensors(f)

        for y in trange(MIN_COORD, MAX_COORD + 1):
            intervals = (
                s.no_beacons_at(y, count_existing_beacon=True) for s in sensors
            )
            non_empty_intervals = sorted(
                (i for i in intervals if i is not None), key=itemgetter(0)
            )
            non_empty_intervals = join_intervals(non_empty_intervals)
            conditioned_intervals = [
                (_adjust_to_min_max(i)) for i in non_empty_intervals
            ]
            where_can_be_no_beacons = sum(i[1] - i[0] for i in conditioned_intervals)
            if where_can_be_no_beacons != TOTAL_CELLS_IN_ROW:
                if len(conditioned_intervals) == 2:
                    x = conditioned_intervals[0][1]
                elif (
                    len(conditioned_intervals) == 1
                    and conditioned_intervals[0][0] != MIN_COORD
                ):
                    x = MIN_COORD
                elif (
                    len(conditioned_intervals) == 1
                    and conditioned_intervals[0][1] != MAX_COORD
                ):
                    x = MAX_COORD
                print(x * 4000000 + y)
                sys.exit(0)
