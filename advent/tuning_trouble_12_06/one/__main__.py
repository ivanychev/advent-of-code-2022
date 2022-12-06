import pathlib

from advent.tuning_trouble_12_06.reader import read_signal

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        s = read_signal(f)
        print(s.find_first_marker())
