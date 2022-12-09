import pathlib

from advent.rope_bridge_12_09.motion import Segment
from advent.rope_bridge_12_09.reader import read_motions

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        motions = read_motions(f)

        rope = Segment.build_rope(2)
        for m in motions:
            rope.move(m)
        print(len(rope.get_tail_set()))
