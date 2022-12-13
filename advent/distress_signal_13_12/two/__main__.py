import pathlib

from advent.distress_signal_13_12.packet import Packet
from advent.distress_signal_13_12.reader import read_packets

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        packets = read_packets(f)
        packets.append(Packet([[2]]))
        packets.append(Packet([[6]]))
        packets = sorted(packets)

        res1 = [
            idx
            for idx, packet in enumerate(packets, 1)
            if packet.equals_to_values([[2]])
        ]
        res2 = [
            idx
            for idx, packet in enumerate(packets, 1)
            if packet.equals_to_values([[6]])
        ]
        print(res1[0] * res2[0])
