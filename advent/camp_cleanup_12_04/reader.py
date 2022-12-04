from typing import TextIO

from advent.camp_cleanup_12_04.interval import IntervalPair


def read_interval_pairs(f: TextIO):
    return [IntervalPair.from_string(line) for line in f]
