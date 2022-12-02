import pathlib

from advent.rock_paper_scissors_12_02.reader import read_games

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        games = read_games(f)
        print(sum(g.result() for g in games))
