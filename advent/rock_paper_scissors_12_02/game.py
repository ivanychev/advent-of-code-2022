from typing import NamedTuple

from advent.rock_paper_scissors_12_02.move import Move, Paper, Rock, Scissors


class Game(NamedTuple):
    first_move: Move
    second_move: Move

    def result(self) -> int:

        type_score = None

        match self.second_move:
            case Rock():
                type_score = 1
            case Paper():
                type_score = 2
            case Scissors():
                type_score = 3

        return (self.first_move.against(self.second_move) - 1) * -3 + type_score


if __name__ == "__main__":
    assert Game(first_move=Rock(), second_move=Paper()).result() == 8

    assert Game(first_move=Paper(), second_move=Rock()).result() == 1

    assert Game(first_move=Scissors(), second_move=Scissors()).result() == 6
