import enum

from typing_extensions import Self


class Outcome(enum.IntEnum):
    WIN = 1
    DRAW = 2
    LOSS = 3

    @classmethod
    def from_symbol(cls, s: str) -> Self:
        match s:
            case "X":
                return Outcome.LOSS
            case "Y":
                return Outcome.DRAW
            case "Z":
                return Outcome.WIN
            case unknown_symbol:
                raise ValueError(f"Invalid symbol: {unknown_symbol}")
