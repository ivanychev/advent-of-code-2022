import pathlib

from advent.unstable_diffusion_23_12.game import run
from advent.unstable_diffusion_23_12.reader import read_ground

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        elves, elf_map = read_ground(f)
        print(elf_map.render())

        elves, elf_map, _ = run(elves, elf_map, rounds=10)
        print(elf_map.empty_tiles())
