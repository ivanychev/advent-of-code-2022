import pathlib

from monkey_map_22.reader import read_map_and_path

CURRENT_DIR = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (CURRENT_DIR / "input.txt").open() as f:
        player, actions = read_map_and_path(f)
        for action in actions:
            player.perform(action)
        print(player.get_password())
