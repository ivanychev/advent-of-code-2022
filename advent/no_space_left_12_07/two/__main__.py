import pathlib

from advent.no_space_left_12_07.filesystem import DirectoryNode, Node
from advent.no_space_left_12_07.reader import read_tokens

CURRENT_DIR = pathlib.Path(__file__).parent

TOTAL_DISK = 70000000
NEEDED_SPACE = 30000000


if __name__ == "__main__":

    with (CURRENT_DIR / "input.txt").open() as f:
        tokens = read_tokens(f)
    root = DirectoryNode.scan_commands(tokens)
    occupied = root.size()
    need_to_free_up = NEEDED_SPACE - (TOTAL_DISK - occupied)

    best_candidate: DirectoryNode | None = None

    def update_candidate(d: DirectoryNode):
        global best_candidate
        if d.size() < need_to_free_up:
            return
        if not best_candidate or best_candidate.size() > d.size():
            best_candidate = d

    root.visit(predicate=Node.is_directory, callback=update_candidate)
    print(best_candidate.size())
