from advent.cathode_ray_12_10.cpu import Cpu

DISPLAY_WIDTH = 40
DISPLAY_HEIGHT = 6


class CrtDisplay:
    def __init__(self):
        self.pos_y: int | None = None
        self.pos_x: int | None = None
        self.display = [["."] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]

    def _move_pointer(self):
        if self.pos_x is None:
            self.pos_x, self.pos_y = 0, 0
            return
        new_pos_x = (self.pos_x + 1) % DISPLAY_WIDTH
        new_pos_y = self.pos_y + (self.pos_x + 1) // DISPLAY_WIDTH
        self.pos_x, self.pos_y = new_pos_x, new_pos_y

        if not (0 <= self.pos_x < DISPLAY_WIDTH and 0 <= self.pos_y < DISPLAY_HEIGHT):
            raise ValueError(f"Invalid pointer position: {self.pos_x, self.pos_y}")

    def __str__(self):
        return "Display:\n" + "\n".join("".join(row) for row in self.display)

    def _sprite_intersects_pointer(self, cpu: Cpu):
        return abs(cpu.X - self.pos_x) <= 1

    def __call__(self, cpu: Cpu, clock_index: int):
        self._move_pointer()
        if self._sprite_intersects_pointer(cpu):
            self.display[self.pos_y][self.pos_x] = "#"
