import dataclasses
import re
from typing import Callable

from typing_extensions import Self

MONKEY_INDEX_RE = re.compile(r"^Monkey (?P<index>\d+):$")
STARTING_ITEMS_RE = re.compile(r"^Starting items: (?P<items>.*)$")
OPERATION_RE = re.compile(r"^Operation: (?P<operation>.*)$")
TEST_DIVISIBLE_RE = re.compile(r"^Test: divisible by (?P<value>\d+)$")
IF_TRUE_RE = re.compile(r"^If true: throw to monkey (?P<index>\d+)$")
IF_FALSE_RE = re.compile(r"^If false: throw to monkey (?P<index>\d+)$")


@dataclasses.dataclass
class Item:
    worry_level: int


class Monkey:
    def __init__(
        self,
        index: int,
        items: list[Item],
        true_send_to: int,
        false_send_to: int,
        operation_python: str,
        test_divisible_by: int,
        monkey_registry: dict[int, Self],
        worry_level_change_on_inspection: Callable[[int], int],
    ):
        self.index: int = index
        self.items = items
        self.true_send_to = true_send_to
        self.false_send_to = false_send_to
        self.monkey_registry = monkey_registry
        self.operation_python = operation_python.strip()
        self.test_divisible_by = test_divisible_by
        self.insected_count = 0
        self.worry_level_change_on_inspection = worry_level_change_on_inspection

    def set_worry_level_change_on_inspection(
        self, worry_level_change_on_inspection: Callable[[int], int]
    ):
        self.worry_level_change_on_inspection = worry_level_change_on_inspection

    @classmethod
    def read_from_raw_strings(
        cls,
        descr: list[str],
        monkey_registry: dict[int, Self],
        worry_level_change_on_inspection: Callable[[int], int],
    ) -> Self:
        monkey_index = int(MONKEY_INDEX_RE.match(descr[0]).groupdict()["index"])
        starting_items_worry = [
            int(x)
            for x in STARTING_ITEMS_RE.match(descr[1]).groupdict()["items"].split(", ")
        ]
        operation = OPERATION_RE.match(descr[2]).groupdict()["operation"]
        test_divisible_by = int(TEST_DIVISIBLE_RE.match(descr[3]).groupdict()["value"])
        true_send_to = int(IF_TRUE_RE.match(descr[4]).groupdict()["index"])
        false_send_to = int(IF_FALSE_RE.match(descr[5]).groupdict()["index"])
        return cls(
            index=monkey_index,
            items=[Item(worry) for worry in starting_items_worry],
            monkey_registry=monkey_registry,
            operation_python=operation,
            test_divisible_by=test_divisible_by,
            true_send_to=true_send_to,
            false_send_to=false_send_to,
            worry_level_change_on_inspection=worry_level_change_on_inspection,
        )

    def check_item(self, item: Item):
        self.insected_count += 1
        locals_dict = {"old": item.worry_level}
        exec(self.operation_python, None, locals_dict)
        new = locals_dict["new"]
        if new is None:
            raise ValueError(
                f"Failed to update worry level: op {self.operation_python}"
            )

        # Gets bored, we calm down
        new = self.worry_level_change_on_inspection(new)

        item.worry_level = new
        if new % self.test_divisible_by:
            self.monkey_registry[self.false_send_to].receive_item(item)
        else:
            self.monkey_registry[self.true_send_to].receive_item(item)

    def receive_item(self, item: Item):
        self.items.append(item)

    def inspect_items(self):

        items_count = len(self.items)
        for item in self.items:
            self.check_item(item)
        self.items = self.items[items_count:]
