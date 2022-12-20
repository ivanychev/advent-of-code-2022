import pathlib

from grove_20_12.reader import read_numbers

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        number_nodes = read_numbers(f)
        zero_node = [n for n in number_nodes if not n.value][0]

        for node in number_nodes:
            # print(node.value)
            node.move(node.value)
            # print(number_nodes[0].print_list())

        result = 0
        node = zero_node
        node = node.walk(1000)
        result += node.value
        node = node.walk(1000)
        result += node.value
        node = node.walk(1000)
        result += node.value

        print(result)
