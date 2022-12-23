import re
from dataclasses import dataclass, field

from typing_extensions import Self

VALVE_RE = re.compile(
    r"Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<valves>[\w, ]+)"
)


@dataclass(frozen=True, slots=True)
class Valve:
    name: str = field(hash=True)
    rate: int = field(hash=True)
    linked_to: frozenset[str] = field(hash=True)
    registry: dict[str, Self] = field(hash=False)

    @classmethod
    def from_string(cls, s: str, registry: dict[str, Self]) -> Self:
        match = VALVE_RE.match(s.strip())
        d = match.groupdict()
        instance = cls(
            name=d["name"],
            rate=int(d["rate"]),
            linked_to=frozenset([x.strip() for x in d["valves"].split(", ")]),
            registry=registry,
        )
        registry[d["name"]] = instance

        return instance
