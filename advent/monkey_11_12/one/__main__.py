import pathlib

from advent.no_space_left_12_07.filesystem import DirectoryNode, Node
from advent.no_space_left_12_07.reader import read_tokens

CURRENT_DIR = pathlib.Path(__file__).parent

MAX_DIR_SIZE = 100000

if __name__ == "__main__":

    total_size = 0

    def add_size(d: DirectoryNode):
        global total_size
        if d.size() <= MAX_DIR_SIZE:
            total_size += d.size()

    with (CURRENT_DIR / "input.txt").open() as f:
        tokens = read_tokens(f)
        root = DirectoryNode.scan_commands(tokens)
        root.visit(predicate=Node.is_directory, callback=add_size)
    print(total_size)
