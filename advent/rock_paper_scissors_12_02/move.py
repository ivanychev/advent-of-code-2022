import abc

from typing_extensions import Self

from advent.rock_paper_scissors_12_02.outcome import Outcome


class Move(abc.ABC):
    @property
    @abc.abstractmethod
    def win_map(self) -> dict[str, int]:
        pass

    def against(self, move: Self) -> int:
        if not isinstance(move, Move):
            raise ValueError("Invalid move class")
        class_name = move.__class__.__name__
        return self.win_map[class_name]

    @classmethod
    def from_symbol(cls, s) -> Self:
        if s in ("A", "X"):
            return Rock()
        if s in ("B", "Y"):
            return Paper()
        if s in ("C", "Z"):
            return Scissors()
        raise ValueError(f"Invalid symbol {s}")

    def get_draw_response(self) -> Self:
        return self

    def get_winning_response(self) -> Self:
        index = LOSING_TO_WINNING_CLASSES.index(self.__class__)
        next_index = (index + 1) % len(LOSING_TO_WINNING_CLASSES)
        return LOSING_TO_WINNING_CLASSES[next_index]()

    def get_losing_response(self) -> Self:
        index = LOSING_TO_WINNING_CLASSES.index(self.__class__)
        next_index = (index - 1) % len(LOSING_TO_WINNING_CLASSES)
        return LOSING_TO_WINNING_CLASSES[next_index]()

    def get_response_for_outcome(self, o: Outcome) -> Self:
        match o:
            case Outcome.WIN:
                return self.get_winning_response()
            case Outcome.DRAW:
                return self.get_draw_response()
            case Outcome.LOSS:
                return self.get_losing_response()
            case _:
                raise ValueError("Invalid outcome")


class Rock(Move):
    @property
    def win_map(self) -> dict[str, int]:
        return {"Rock": 0, "Paper": -1, "Scissors": 1}


class Paper(Move):
    @property
    def win_map(self) -> dict[str, int]:
        return {"Rock": 1, "Paper": 0, "Scissors": -1}


class Scissors(Move):
    @property
    def win_map(self) -> dict[str, int]:
        return {"Rock": -1, "Paper": 1, "Scissors": 0}


LOSING_TO_WINNING_CLASSES = [Rock, Paper, Scissors]
