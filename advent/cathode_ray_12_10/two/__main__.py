import pathlib

from advent.cathode_ray_12_10.cpu import Addx, Cpu, Noop
from advent.cathode_ray_12_10.crt import CrtDisplay
from advent.cathode_ray_12_10.reader import read_commands

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        commands = read_commands(f)

        crt = CrtDisplay()
        cpu = Cpu().with_during_cycle_callback(crt)

        cpu.execute(commands)
        print(crt)
