import dataclasses


class Action:
    pass


@dataclasses.dataclass
class Move(Action):
    value: int


@dataclasses.dataclass
class TurnClockwise(Action):
    pass


@dataclasses.dataclass
class TurnCounterClockwise(Action):
    pass
