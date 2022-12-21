import dataclasses

from monkey_21_12.operation import Operation


@dataclasses.dataclass
class Monkey:
    name: str
    op: Operation
