from typing import TextIO

from advent.beacon_15_12.sensor import Sensor


def read_sensors(f: TextIO) -> list[Sensor]:
    return [Sensor.from_str(row.strip()) for row in f]
