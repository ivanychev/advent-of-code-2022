import pathlib
from operator import itemgetter

from more_itertools import chunked

from advent.beacon_15_12.interval import join_intervals
from advent.beacon_15_12.reader import read_sensors
from advent.distress_signal_13_12.packet import compare_ordering
from advent.distress_signal_13_12.reader import read_packets

CURRENT_DIR = pathlib.Path(__file__).parent

Y = 2000000

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        sensors = read_sensors(f)
        intervals = (s.no_beacons_at(Y) for s in sensors)
        non_empty_intervals = [i for i in intervals if i is not None]
        non_empty_intervals.sort(key=itemgetter(0))
        non_empty_intervals = join_intervals(non_empty_intervals)
        print(sum(i[1] - i[0] for i in non_empty_intervals))
