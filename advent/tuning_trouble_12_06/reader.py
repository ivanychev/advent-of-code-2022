from typing import TextIO

from advent.tuning_trouble_12_06.signal import Signal


def read_signal(f: TextIO):
    return Signal(f.read().strip())
