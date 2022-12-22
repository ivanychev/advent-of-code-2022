Position = tuple[int, int]
Direction = tuple[int, int]

UP: Direction = (0, -1)
RIGHT: Direction = (1, 0)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)

VERTICAL_MOVES = frozenset((UP, DOWN))

HORIZONTAL_MOVES = frozenset((LEFT, RIGHT))

CLOCKWISE_DIRECTIONS = (
    RIGHT,
    DOWN,
    LEFT,
    UP,
)


def turn_clockwise(direction: Direction) -> Direction:
    idx = CLOCKWISE_DIRECTIONS.index(direction)
    assert idx >= 0
    return CLOCKWISE_DIRECTIONS[(idx + 1) % len(CLOCKWISE_DIRECTIONS)]


def turn_counterclockwise(direction: Direction) -> Direction:
    idx = CLOCKWISE_DIRECTIONS.index(direction)
    assert idx >= 0
    return CLOCKWISE_DIRECTIONS[(idx - 1) % len(CLOCKWISE_DIRECTIONS)]
