import pathlib

from advent.volcano_16_12.network import Network, NetworkState, max_cum_pressure
from advent.volcano_16_12.reader import read_valves

CURRENT_DIR = pathlib.Path(__file__).parent

STARTING_VALVE = "AA"
MINUTES = 30

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        valves, registry = read_valves(f)
        network = Network.from_valves(valves, registry, STARTING_VALVE)

        current_state = NetworkState(
            network=network,
            opened_map=0,
            current=network.node_to_idx[STARTING_VALVE],
            minutes_left=MINUTES,
        )
        print(max_cum_pressure(current_state))
