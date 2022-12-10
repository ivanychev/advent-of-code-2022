import pathlib

from advent.cathode_ray_12_10.cpu import Addx, Cpu, Noop
from advent.cathode_ray_12_10.reader import read_commands

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        commands = read_commands(f)

        cycles_to_check_values = frozenset((20, 60, 100, 140, 180, 220))
        signal_strength = 0

        def callback(cpu: Cpu, cycle_index: int):
            global signal_strength
            if cycle_index in cycles_to_check_values:
                signal_strength += cycle_index * cpu.X

        cpu = Cpu().with_during_cycle_callback(callback)

        cpu.execute(commands)
        print(signal_strength)
