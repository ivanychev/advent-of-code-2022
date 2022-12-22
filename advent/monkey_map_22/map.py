import io

from monkey_map_22.formation import AIR, FORMATIONS
from typing_extensions import Self


def _min_max_horizontal(rows: list[str], y: int) -> tuple[int, int]:
    min_y = min((idx for idx, c in enumerate(rows[y]) if c in FORMATIONS))
    max_y = max((idx for idx, c in enumerate(rows[y]) if c in FORMATIONS))
    return min_y, max_y + 1


def _min_max_vertival(rows: list[str], x: int):
    min_y = min((idx for idx in range(len(rows)) if rows[idx][x] in FORMATIONS))
    max_y = max((idx for idx in range(len(rows)) if rows[idx][x] in FORMATIONS))
    return min_y, max_y + 1


class MonkeyMap:
    def __init__(
        self,
        rows: list[str],
        horizontal_to_range: list[tuple[int, int]],
        vertical_to_range: list[tuple[int, int]],
    ):
        self.rows = rows
        self.horizontal_to_range = horizontal_to_range
        self.vertical_to_range = vertical_to_range

    def render_with_player(self, player_pos: tuple[int, int]) -> str:
        buffer = io.StringIO()
        row = player_pos[1]
        col = player_pos[0]

        for row_idx in range(len(self.rows)):
            for col_idx in range(len(self.rows[0])):
                c = self.rows[row_idx][col_idx]
                if row_idx == row and col_idx == col:
                    c = "$"
                buffer.write(c)
            buffer.write("\n")
        return buffer.getvalue()

    @classmethod
    def from_rows(cls, rows: list[str]) -> Self:
        max_len = max(len(r) for r in rows)
        rows = [r.ljust(max_len) for r in rows]

        horizontal_to_range = [_min_max_horizontal(rows, y) for y in range(len(rows))]
        verical_to_range = [_min_max_vertival(rows, x) for x in range(len(rows[0]))]

        return cls(
            rows=rows,
            horizontal_to_range=horizontal_to_range,
            vertical_to_range=verical_to_range,
        )

    def starting_xy(self) -> tuple[int, int]:
        hrange = self.horizontal_to_range[0]
        for idx in range(hrange[0], hrange[1] + 1):
            if self.rows[0][idx] == AIR:
                return idx, 0  # x, y

    def at_xy(self, point: tuple[int, int]) -> str:
        return self.rows[point[1]][point[0]]
