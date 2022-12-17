import pathlib

from advent.volcano_16_12.network import (
    Network,
    NetworkState,
    TransitionState,
    TransitionStatus,
    max_cum_pressure,
)
from advent.volcano_16_12.reader import read_valves

CURRENT_DIR = pathlib.Path(__file__).parent

STARTING_VALVE = "AA"
MINUTES = 26

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        valves, registry = read_valves(f)
        network = Network.from_valves(valves, registry, STARTING_VALVE)

        current_state = NetworkState(
            network=network,
            opened_map_mask=0,
            minutes_left=MINUTES,
            explorers_states=tuple(
                TransitionState(
                    status=TransitionStatus.STANDING,
                    from_node=None,
                    to_node=None,
                    current=network.node_to_idx[STARTING_VALVE],
                    finish_at_minutes_left=None,
                )
                for _ in range(2)
            ),
        )
        print(max_cum_pressure(current_state, compute_parallel=True))
