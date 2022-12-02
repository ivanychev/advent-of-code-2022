from typing import TextIO, Iterable

from advent.rock_paper_scissors_12_02.game import Game
from advent.rock_paper_scissors_12_02.move import Move
from advent.rock_paper_scissors_12_02.outcome import Outcome


def read_games(f: TextIO) -> Iterable[Game]:
    for line in f:
        first, second = line.rstrip().split(" ", maxsplit=1)
        yield Game(
            first_move=Move.from_symbol(first),
            second_move=Move.from_symbol(second),
        )


def read_games_with_results(f: TextIO) -> Iterable[Game]:
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        first, second = line.rstrip().split(" ", maxsplit=1)
        first_move = Move.from_symbol(first)
        desired_outcome = Outcome.from_symbol(second)
        second_move = first_move.get_response_for_outcome(desired_outcome)
        yield Game(first_move=first_move, second_move=second_move)


if __name__ == "__main__":
    from io import StringIO
    import textwrap

    buf = StringIO()
    buf.write(
        textwrap.dedent(
            """\
    C Z
    """
        )
    )
    buf.seek(0)
    print(list(read_games_with_results(buf))[0].result())
