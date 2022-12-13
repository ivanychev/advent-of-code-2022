import pathlib

from more_itertools import chunked

from advent.distress_signal_13_12.packet import compare_ordering
from advent.distress_signal_13_12.reader import read_packets

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        packets = read_packets(f)
        sum_idx = 0
        for idx, pair in enumerate(chunked(packets, 2), 1):
            ordering = compare_ordering(left=pair[0].values, right=pair[1].values)
            if not isinstance(ordering, bool):
                raise ValueError(f"Ordering is not bool, {pair}, {ordering=}")
            if ordering:
                sum_idx += idx
        print(sum_idx)
