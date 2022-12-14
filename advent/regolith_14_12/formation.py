import enum


class Formation(enum.Enum):
    ROCK = "#"
    AIR = "."
    SAND = "o"
    DROP_POINT = "x"


SOLID_FORMATIONS = frozenset([Formation.ROCK, Formation.SAND])
