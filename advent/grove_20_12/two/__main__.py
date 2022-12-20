import pathlib

import tqdm
from grove_20_12.reader import read_numbers
from tqdm import trange

CURRENT_DIR = pathlib.Path(__file__).parent
DECRYPTION_KEY = 811589153

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        number_nodes = read_numbers(f, multiply_by=811589153)
        zero_node = [n for n in number_nodes if not n.value][0]

        for _ in trange(10):
            for node in tqdm.tqdm(number_nodes):
                node.move(node.value)

        result = 0
        node = zero_node
        node = node.walk(1000)
        result += node.value
        node = node.walk(1000)
        result += node.value
        node = node.walk(1000)
        result += node.value

        print(result)
