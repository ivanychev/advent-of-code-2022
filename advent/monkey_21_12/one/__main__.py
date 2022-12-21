import pathlib

from monkey_21_12.reader import read_monkeys

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        monkeys, monkey_registry = read_monkeys(f)
        print(monkey_registry["root"].op.eval(monkey_registry))
