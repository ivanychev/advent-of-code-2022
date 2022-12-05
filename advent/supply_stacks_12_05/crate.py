from typing import Iterable, NamedTuple

from advent.supply_stacks_12_05.move import Move


class CrateStorage(NamedTuple):
    label_to_crates: dict[int, list[str]]

    def make_move(self, m: Move, batch_move: bool = False):
        from_crates = self.label_to_crates[m.from_label]
        to_crates = self.label_to_crates[m.to_label]
        quantity = min(m.quantity, len(from_crates))

        delta = []
        for _ in range(quantity):
            delta.append(from_crates.pop())

        if batch_move:
            delta.reverse()
        to_crates.extend(delta)

    def get_sorted_labels(self) -> Iterable[int]:
        return sorted(self.label_to_crates)

    def top(self, label: int) -> str:
        return self.label_to_crates[label][-1]
