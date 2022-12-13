from typing import TextIO

from advent.distress_signal_13_12.packet import Packet


def read_packets(f: TextIO) -> list[Packet]:
    non_empty_rows = (row for row in f if row.strip())
    return [Packet.parse_from_strint(s) for s in non_empty_rows]
