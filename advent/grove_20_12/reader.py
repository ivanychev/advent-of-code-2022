import dataclasses
from io import StringIO
from typing import List, TextIO

from typing_extensions import Self


@dataclasses.dataclass
class Node:
    index: int
    value: int
    next: Self
    prev: Self
    ring_size: int

    def print_list(self):
        buffer = StringIO()
        buffer.write(f"{self.value}")
        current = self.next
        while current is not self:
            buffer.write(f", {current.value}")
            current = current.next
        return buffer.getvalue()

    def walk(self, delta: int, ignore_node: Self | None = None) -> Self:
        delta = delta % (self.ring_size if not ignore_node else self.ring_size - 1)
        current = self
        while delta > 0:
            current = current.next
            if current is ignore_node:
                current = current.next
            delta -= 1
        while delta < 0:
            current = current.prev
            if current is ignore_node:
                current = current.prev
            delta += 1
        return current

    def move(self, delta: int):
        new_next = self.next.walk(delta, ignore_node=self)
        if new_next is self.next:
            return
        self.prev.next, self.next.prev = self.next, self.prev

        new_prev = new_next.prev
        new_next.prev = self
        self.next = new_next

        new_prev.next = self
        self.prev = new_prev
        return


def read_numbers(f: TextIO, multiply_by: int = 1) -> List[Node]:
    nodes = []
    for idx, row in enumerate(f):
        value = int(row.strip())
        nodes.append(Node(idx, value * multiply_by, None, None, 0))

    for idx, node in enumerate(nodes):
        left_idx = (idx - 1) % len(nodes)
        right_idx = (idx + 1) % len(nodes)
        node.next = nodes[right_idx]
        node.prev = nodes[left_idx]
        node.ring_size = len(nodes)
    return nodes
