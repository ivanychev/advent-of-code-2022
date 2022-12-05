import re
from typing import NamedTuple

from typing_extensions import Self

MOVE_RE = re.compile(
    r"^\s*move (?P<crates>\w+) from (?P<from_label>\w+) to (?P<to_label>\w+)\s*$"
)


class Move(NamedTuple):
    quantity: int
    from_label: int
    to_label: int

    @classmethod
    def from_string(cls, s: str) -> Self:
        m = MOVE_RE.match(s)
        return cls(
            quantity=int(m.groupdict()["crates"]),
            from_label=int(m.groupdict()["from_label"]),
            to_label=int(m.groupdict()["to_label"]),
        )
