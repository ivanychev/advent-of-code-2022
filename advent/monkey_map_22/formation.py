from typing import Final, Literal

SOLID: Final[str] = "#"
AIR: Final[str] = "."

Formation = Literal["#"] | Literal["."]

FORMATIONS = frozenset((SOLID, AIR))
