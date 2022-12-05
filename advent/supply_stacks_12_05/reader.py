from typing import Iterable, TextIO, Tuple

from advent.supply_stacks_12_05.crate import CrateStorage
from advent.supply_stacks_12_05.move import Move


def _is_crate_line(line: str) -> bool:
    return line[:2] == " 1"


def get_crate_from_line(crate_index: int, crate_line: str) -> str | None:
    index = 1 + (crate_index - 1) * 4
    if not 0 <= index < len(crate_line):
        return None
    crate = crate_line[index].strip()
    return crate if crate else None


def filter_none(i: Iterable) -> list:
    return [x for x in i if x is not None]


def _read_storage(f: TextIO) -> CrateStorage:
    crate_lines = []
    crate_label_line = None
    for line in f:
        if not _is_crate_line(line):
            crate_lines.append(line)
        else:
            crate_label_line = line
            break

    labels = [int(x) for x in crate_label_line.strip().split()]
    labels_to_crates = {
        l: filter_none(get_crate_from_line(l, line) for line in crate_lines)[::-1]
        for l in labels
    }
    return CrateStorage(label_to_crates=labels_to_crates)


def read_crates(f: TextIO) -> Tuple[CrateStorage, list[Move]]:
    storage = _read_storage(f)
    return storage, [Move.from_string(line) for line in f if line.strip()]
